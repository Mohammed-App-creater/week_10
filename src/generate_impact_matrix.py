import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import os

def calculate_ramp_factor(current_date, start_date, ramp_months=6):
    """Calculates a linear ramp factor (0.0 to 1.0)."""
    if current_date < start_date:
        return 0.0
    days_elapsed = (current_date - start_date).days
    ramp_days = ramp_months * 30
    if days_elapsed >= ramp_days:
        return 1.0
    return max(0.0, days_elapsed / ramp_days)

def get_magnitude_numeric(magnitude_str, default_high=0.2, default_med=0.1, default_low=0.05):
    mapping = {
        'high': default_high,
        'medium': default_med,
        'low': default_low,
        'negligible': 0.01
    }
    return mapping.get(str(magnitude_str).lower(), 0.0)

def main():
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'raw', 'ethiopia_fi_unified_data.csv')
    output_path = os.path.join(base_dir, 'data', 'processed', 'event_indicator_matrix.csv')

    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)

    # Parse dates
    for col in ['observation_date']:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # Clean strings
    str_cols = ['record_type', 'parent_id', 'record_id', 'indicator_code']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    events = df[df['record_type'] == 'event'].copy()
    impact_links = df[df['record_type'] == 'impact_link'].copy()

    impact_effects = []
    
    print(f"Processing {len(impact_links)} impact links...", flush=True)

    for idx, link in impact_links.iterrows():
        # Get Event
        event_id = link['parent_id'] # In this dataset, parent_id often points to indicator_code if record_id match fails
        
        # Debug
        print(f"Link {link.get('record_id', 'Unknown')}: Looking for parent '{event_id}'...", end='', flush=True)

        # Try finding event
        event_row = events[events['record_id'] == event_id]
        if event_row.empty:
            event_row = events[events['indicator_code'] == event_id]
        
        if event_row.empty:
            print(f" NOT FOUND.", flush=True)
            print(f"   Available Codes: {events['indicator_code'].unique()[:5]}...", flush=True)
            continue
            
        print(f" FOUND ({event_row['record_id'].values[0]}).", flush=True)
        
        event = event_row.iloc[0]
        event_date = event['observation_date']
        
        if pd.isna(event_date):
            print("   WARN: Event has no date. Skipping.", flush=True)
            continue

        # Parameters
        # Impact links target an indicator. In the CSV, this target ID is in 'indicator_code'.
        indicator_target = link['indicator_code']
        if pd.isna(indicator_target) or indicator_target == '':
             indicator_target = link['indicator']
        
        # Direction
        direction_map = {'increase': 1, 'decrease': -1, 'stabilize': 0, 'mixed': 0}
        direction = direction_map.get(link.get('impact_direction', 'increase'), 1)

        # Magnitude
        if pd.notna(link.get('impact_estimate')):
            magnitude = float(link['impact_estimate'])
        else:
            magnitude = get_magnitude_numeric(link.get('impact_magnitude'))

        impact_effects.append({
            'event_name': event.get('indicator', 'Unknown'),
            'target_indicator': indicator_target,
            'net_impact': direction * magnitude
        })

    # Pivot and Save Matrix
    if impact_effects:
        df_effects = pd.DataFrame(impact_effects)
        matrix = df_effects.pivot_table(
            index='event_name',
            columns='target_indicator',
            values='net_impact',
            aggfunc='sum'
        ).fillna(0)
        
        print("\nGenerated Matrix:", flush=True)
        print(matrix, flush=True)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        matrix.to_csv(output_path)
        print(f"\nSaved matrix to {output_path}", flush=True)
        
        # --- Visualization ---
        try:
            import matplotlib.pyplot as plt
            
            # Generate timeline for a key indicator
            target_ind = 'ACC_OWNERSHIP' 
            # Check if this indicator is affected
            relevant_links = [l for i, l in impact_links.iterrows() if l.get('indicator_code') == target_ind or l.get('indicator') == target_ind]
            
            if relevant_links:
                print(f"\nGenerating visualization for {target_ind}...", flush=True)
                timeline = pd.date_range(start='2020-01-01', end='2030-12-31', freq='ME')
                series_data = np.zeros(len(timeline))
                
                for idx, link in impact_links.iterrows():
                    code = link.get('indicator_code')
                    if pd.isna(code) or code == '': code = link.get('indicator')
                    if code != target_ind: continue
                    
                    # Get event date again (inefficient lookup but fine for script)
                    event_id = link['parent_id']
                    event_row = events[events['record_id'] == event_id]
                    if event_row.empty: event_row = events[events['indicator_code'] == event_id]
                    if event_row.empty: continue
                    e_date = event_row.iloc[0]['observation_date']
                    if pd.isna(e_date): continue
                    
                    mdir = direction_map.get(link.get('impact_direction', 'increase'), 1)
                    mmag = float(link['impact_estimate']) if pd.notna(link.get('impact_estimate')) else get_magnitude_numeric(link.get('impact_magnitude'))
                    mlag = float(link.get('lag_months', 0))
                    
                    start_date = e_date + timedelta(days=mlag*30)
                    
                    # Add to series
                    for i, t in enumerate(timeline):
                        factor = calculate_ramp_factor(t, start_date)
                        series_data[i] += mdir * mmag * factor
                
                # Plot
                plt.figure(figsize=(10, 6))
                plt.plot(timeline, series_data, label=f'Model Impact: {target_ind}', color='blue', linewidth=2)
                plt.title(f'Modeled Cumulative Impact on {target_ind}')
                plt.ylabel('Impact Magnitude (Additive)')
                plt.grid(True)
                plt.legend()
                
                vis_path = os.path.join(base_dir, 'reports', 'impact_visualization.png')
                os.makedirs(os.path.dirname(vis_path), exist_ok=True)
                plt.savefig(vis_path)
                print(f"Saved visualization to {vis_path}", flush=True)
                
        except Exception as e:
            print(f"Visualization failed: {e}", flush=True)

    else:
        print("No effects generated.", flush=True)

if __name__ == "__main__":
    main()
