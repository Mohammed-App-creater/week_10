import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def get_magnitude_numeric(magnitude_str):
    mapping = {
        'high': 0.2,
        'medium': 0.1,
        'low': 0.05,
        'negligible': 0.01
    }
    return mapping.get(str(magnitude_str).lower(), 0.0)

def train_baseline_model(history_df):
    if len(history_df) < 2:
        return None, None
    X = history_df['observation_date'].map(datetime.toordinal).values.reshape(-1, 1)
    y = history_df['value_numeric'].values
    slope, intercept = np.polyfit(X.flatten(), y, 1)
    return slope, intercept

def calculate_event_add_ons(unified_df, start_date, end_date, target_indicator):
    timeline = pd.date_range(start=start_date, end=end_date, freq='ME')
    total_impact = np.zeros(len(timeline))
    
    impact_links = unified_df[unified_df['record_type'] == 'impact_link']
    
    for idx, row in impact_links.iterrows():
        # Check target
        target = row.get('indicator_code')
        if pd.isna(target): target = row.get('indicator')
        
        # Handle alias
        if target == 'USG_DIGITAL_PAY': target = 'USG_DIGITAL_PAYMENT'
        if target_indicator == 'USG_DIGITAL_PAY': target_indicator = 'USG_DIGITAL_PAYMENT'
        
        if target != target_indicator: continue
            
        # Get magnitude
        mag = row.get('impact_estimate')
        if pd.isna(mag):
            mag = get_magnitude_numeric(row.get('impact_magnitude'))
        else:
            mag = float(mag)
            
        direction = 1 if row.get('impact_direction', 'increase') == 'increase' else -1
        final_impact = mag * direction
        
        # Get event date
        parent = row['parent_id']
        event_row = unified_df[(unified_df['record_type'] == 'event') & 
                               ((unified_df['record_id'] == parent) | (unified_df['indicator_code'] == parent))]
        
        if event_row.empty: continue
        
        evt_date = pd.to_datetime(event_row.iloc[0]['observation_date'])
        if pd.isna(evt_date): continue

        lag = float(row.get('lag_months', 0))
        if pd.isna(lag): lag = 0
        
        impact_start = evt_date + timedelta(days=int(lag*30))
        ramp_days = 180 # 6 month ramp
        
        for i, t in enumerate(timeline):
            if t < impact_start:
                continue
            
            days_since = (t - impact_start).days
            factor = min(1.0, days_since / ramp_days)
            # Simple additive accumulation
            total_impact[i] += final_impact * factor
            
    return pd.Series(total_impact, index=timeline)

def generate_forecast(slope, intercept, impact_series, scenario='Base'):
    forecast_dates = impact_series.index
    X_future = forecast_dates.map(datetime.toordinal).values
    
    baseline = slope * X_future + intercept
    impacts = impact_series.values
    
    if scenario == 'Optimistic':
        adjusted_baseline = baseline * 1.05
        adjusted_impacts = impacts * 1.2
    elif scenario == 'Pessimistic':
        adjusted_baseline = baseline * 0.95 
        adjusted_impacts = impacts * 0.8
    else:
        adjusted_baseline = baseline
        adjusted_impacts = impacts
        
    final_forecast = np.clip(adjusted_baseline + adjusted_impacts, 0, 100)
    
    return pd.DataFrame({'Date': forecast_dates, 'Value': final_forecast, 'Scenario': scenario})

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'raw', 'ethiopia_fi_unified_data.csv')
    
    print(f"Loading {data_path}...")
    unified_df = pd.read_csv(data_path)
    unified_df['observation_date'] = pd.to_datetime(unified_df['observation_date'], errors='coerce')
    
    obs_df = unified_df[unified_df['record_type'] == 'observation'].copy()
    
    indicators = ['ACC_OWNERSHIP', 'USG_DIGITAL_PAYMENT']
    scenarios = ['Base', 'Optimistic', 'Pessimistic']
    
    all_results = []
    
    for ind in indicators:
        print(f"Processing {ind}...")
        # Get history
        # Handle alias in observation data
        lookup_ind = ind
        if ind == 'USG_DIGITAL_PAYMENT':
            # Check if it exists as USG_DIGITAL_PAYMENT or USG_DIGITAL_PAY
            if 'USG_DIGITAL_PAYMENT' not in obs_df['indicator_code'].unique():
                lookup_ind = 'USG_DIGITAL_PAY'
        
        history = obs_df[obs_df['indicator_code'] == lookup_ind].sort_values('observation_date')
        history = history.drop_duplicates(subset=['observation_date'], keep='last')
        
        if len(history) < 2:
            print(f"  Not enough history for {ind} (Found {len(history)} records).")
            if ind in ['USG_DIGITAL_PAYMENT', 'USG_DIGITAL_PAY']:
                print("  Using ACC_OWNERSHIP slope as proxy baseline.")
                # Find ACC history to derive slope
                acc_hist = obs_df[obs_df['indicator_code'] == 'ACC_OWNERSHIP'].sort_values('observation_date')
                if len(acc_hist) >= 2:
                    slope, _ = train_baseline_model(acc_hist)
                    # Calculate synthetic intercept to match the ONE usage point we might have
                    # or if we have 0 points, we can't do anything. We likely have 1 point (2024).
                    if len(history) == 1:
                        # y = mx + b -> b = y - mx
                        latest_pt = history.iloc[-1]
                        x_val = datetime.toordinal(latest_pt['observation_date'])
                        y_val = latest_pt['value_numeric']
                        intercept = y_val - slope * x_val
                        print(f"  Proxy Baseline: Slope={slope:.6f}, Intercept={intercept:.2f} (Anchored to {y_val} at {latest_pt['observation_date'].date()})")
                    else:
                        print("  No history at all for USG. Skipping.")
                        continue
                else:
                    print("  ACC_OWNERSHIP also lacks history. Skipping.")
                    continue
            else:
                print("  Skipping.")
                continue
            
        else:
            slope, intercept = train_baseline_model(history)
            print(f"  Baseline: Slope={slope:.6f}, Intercept={intercept:.2f}")
        
        impacts = calculate_event_add_ons(unified_df, '2020-01-01', '2027-12-31', ind)
        
        for s in scenarios:
            res = generate_forecast(slope, intercept, impacts, s)
            res['Indicator'] = ind
            all_results.append(res)
            
    if not all_results:
        print("No forecasts generated.")
        return

    final_df = pd.concat(all_results)
    
    # Save CSV
    out_path = os.path.join(base_dir, 'data', 'forecasts_2025_2027.csv')
    
    # Format for export
    export_df = final_df[final_df['Date'].dt.year >= 2025].copy()
    export_df['Year'] = export_df['Date'].dt.year
    summary = export_df.groupby(['Indicator', 'Scenario', 'Year'])['Value'].last().reset_index()
    summary['Value'] = summary['Value'].round(2)
    
    summary.to_csv(out_path, index=False)
    print(f"Saved forecasts to {out_path}")
    print(summary)
    
    # Plotting
    try:
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(18, 6))
        
        for i, ind in enumerate(indicators):
            if i >= len(axes): break
            
            ax = axes[i]
            subset = final_df[final_df['Indicator'] == ind]
            
            if subset.empty: continue
            
            # Plot forecast
            for s in scenarios:
                data = subset[subset['Scenario'] == s]
                color = {'Base': 'blue', 'Optimistic': 'green', 'Pessimistic': 'red'}.get(s, 'black')
                ax.plot(data['Date'], data['Value'], label=s, color=color, linestyle='--' if s != 'Base' else '-')
                
            # Plot history
            lookup_ind = ind
            if ind == 'USG_DIGITAL_PAYMENT' and 'USG_DIGITAL_PAYMENT' not in obs_df['indicator_code'].unique():
                lookup_ind = 'USG_DIGITAL_PAY'
            
            hist_data = obs_df[obs_df['indicator_code'] == lookup_ind]
            ax.scatter(hist_data['observation_date'], hist_data['value_numeric'], color='black', label='Historical', zorder=5)
            
            ax.set_title(f"Forecast: {ind}")
            ax.set_ylim(0, 100)
            ax.legend()
            
        plt.tight_layout()
        plot_path = os.path.join(base_dir, 'reports', 'forecast_plot_2025_2027.png')
        plt.savefig(plot_path)
        print(f"Saved plot to {plot_path}")
        
    except Exception as e:
        print(f"Plotting failed: {e}")

if __name__ == "__main__":
    main()
