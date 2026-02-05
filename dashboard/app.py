
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------------
# Configuration & Setup
# -----------------------------------------------------------------------------------
st.set_page_config(
    page_title="Ethiopia Financial Inclusion Dashboard",
    page_icon="charts",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------------
# Data Loading (Cached)
# -----------------------------------------------------------------------------------
@st.cache_data
def load_data():
    """Load historical and forecast data."""
    # Historical Data
    try:
        df_hist = pd.read_csv("data/raw/ethiopia_fi_unified_data.csv")
        # Ensure observation_date is datetime
        df_hist['observation_date'] = pd.to_datetime(df_hist['observation_date'], errors='coerce')
        df_hist['Year'] = df_hist['observation_date'].dt.year
    except FileNotFoundError:
        st.error("Historical data file not found: data/raw/ethiopia_fi_unified_data.csv")
        df_hist = pd.DataFrame()

    # Forecast Data
    try:
        df_forecast = pd.read_csv("data/forecasts_2025_2027.csv")
    except FileNotFoundError:
        st.error("Forecast data file not found: data/forecasts_2025_2027.csv")
        df_forecast = pd.DataFrame()
        
    return df_hist, df_forecast

try:
    df_hist, df_forecast = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# -----------------------------------------------------------------------------------
# Sidebar Navigation
# -----------------------------------------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Trends", "Forecasts", "Inclusion Projections"])

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "Ethiopia Financial Inclusion Forecasting Project.\n\n"
    "Visualizing historical trends and future scenarios (2025-2027)."
)

# -----------------------------------------------------------------------------------
# Page: Overview
# -----------------------------------------------------------------------------------
if page == "Overview":
    st.title("📊 Financial Inclusion Overview")
    st.markdown("Key metrics and current status of financial inclusion in Ethiopia.")

    # -- Calculate Key Metrics --
    # Account Ownership (ACC_OWNERSHIP)
    acc_data = df_hist[df_hist['indicator_code'] == 'ACC_OWNERSHIP'].sort_values('observation_date')
    latest_acc_val = acc_data['value_numeric'].iloc[-1] if not acc_data.empty else 0
    latest_acc_year = acc_data['Year'].iloc[-1] if not acc_data.empty else "N/A"
    
    # Digital Payment Adoption (Using USG_DIGITAL_PAY or proxy)
    dig_data = df_hist[df_hist['indicator_code'] == 'USG_DIGITAL_PAY'].sort_values('observation_date')
    latest_dig_val = dig_data['value_numeric'].iloc[-1] if not dig_data.empty else 0
    
    # P2P / ATM Crossover
    cross_data = df_hist[df_hist['indicator_code'] == 'USG_CROSSOVER'].sort_values('observation_date')
    latest_cross_val = cross_data['value_numeric'].iloc[-1] if not cross_data.empty else 0

    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Account Ownership Ratio", f"{latest_acc_val}%", f"Latest ({latest_acc_year})")
    col2.metric("Digital Payment Adoption", f"{latest_dig_val}%", "Latest Estimate")
    col3.metric("P2P/ATM Crossover Ratio", f"{latest_cross_val:.2f}", "Ratio > 1 indicates Digital Dominance")

    st.markdown("---")
    
    # Quick Summary Visualization
    st.subheader("Historical Trajectory")
    
    # Filter for key indicators
    key_indicators = ['ACC_OWNERSHIP', 'ACC_MOBILE_PEN', 'USG_DIGITAL_PAY']
    summary_df = df_hist[df_hist['indicator_code'].isin(key_indicators)].copy()
    
    if not summary_df.empty:
        fig = px.line(summary_df, x='observation_date', y='value_numeric', color='indicator',
                      title="Key Indicators Over Time",
                      labels={'value_numeric': 'Value (%)', 'observation_date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------------
# Page: Trends
# -----------------------------------------------------------------------------------
elif page == "Trends":
    st.title("📈 Historical Trends")
    st.markdown("Deep dive into Access and Usage metrics.")
    
    # Filters
    pillars = df_hist['pillar'].unique() if 'pillar' in df_hist.columns else []
    selected_pillar = st.selectbox("Select Pillar", pillars, index=0 if len(pillars) > 0 else 0)
    
    # Date Range
    min_date = df_hist['observation_date'].min().date()
    max_date = df_hist['observation_date'].max().date()
    date_range = st.slider("Select Date Range", min_date, max_date, (min_date, max_date))
    
    # Filter Data
    mask = (df_hist['pillar'] == selected_pillar) & \
           (df_hist['observation_date'].dt.date >= date_range[0]) & \
           (df_hist['observation_date'].dt.date <= date_range[1])
    filtered_df = df_hist[mask]
    
    if not filtered_df.empty:
        # P2P vs ATM Special View
        if selected_pillar == 'USAGE':
            st.subheader("Comparison: P2P vs ATM Transactions")
            p2p_atm_codes = ['USG_P2P_COUNT', 'USG_ATM_COUNT']
            p2p_atm_df = filtered_df[filtered_df['indicator_code'].isin(p2p_atm_codes)]
            
            if not p2p_atm_df.empty:
                fig_comp = px.bar(p2p_atm_df, x='Year', y='value_numeric', color='indicator', barmode='group',
                                  title="Transaction Counts: P2P vs ATM",
                                  labels={'value_numeric': 'Count'})
                st.plotly_chart(fig_comp, use_container_width=True)
        
        # General Time Series
        st.subheader(f"{selected_pillar} Indicators Time Series")
        fig_trend = px.line(filtered_df, x='observation_date', y='value_numeric', color='indicator',
                            markers=True,
                            title=f"{selected_pillar} Metrics over Time")
        st.plotly_chart(fig_trend, use_container_width=True)
        
        with st.expander("View Raw Data"):
            st.dataframe(filtered_df[['observation_date', 'indicator', 'value_numeric', 'source_name']])
            
    else:
        st.write("No data available for selected filters.")

# -----------------------------------------------------------------------------------
# Page: Forecasts
# -----------------------------------------------------------------------------------
elif page == "Forecasts":
    st.title("🔮 Strategies & Forecasts (2025-2027)")
    
    if df_forecast.empty:
        st.warning("No forecast data available.")
    else:
        indicators = df_forecast['Indicator'].unique()
        selected_indicator = st.selectbox("Select Indicator to Forecast", indicators)
        
        # Filter Logic
        # Note: Mapping Indicator codes if necessary. Forecast file uses ACC_OWNERSHIP, USG_DIGITAL_PAYMENT
        subset = df_forecast[df_forecast['Indicator'] == selected_indicator]
        
        st.markdown(f"### Forecast for: {selected_indicator}")
        
        # Visualization
        # Use plot to show Scenarios
        fig_cast = px.line(subset, x='Year', y='Value', color='Scenario',
                           markers=True,
                           line_shape='spline',
                           color_discrete_map={'Base': 'blue', 'Optimistic': 'green', 'Pessimistic': 'red'},
                           title=f"Projected {selected_indicator} (2025-2027)")
        
        # Emphasize confidence implicitly via scenarios
        st.plotly_chart(fig_cast, use_container_width=True)
        
        st.markdown("""
        **Scenarios:**
        - **Base**: Assumes current growth trends and implemented policies continue.
        - **Optimistic**: Assumes accelerated policy reforms (e.g. telecom liberalization) and higher adoption.
        - **Pessimistic**: Assumes economic headwinds or slower infrastructure rollout.
        """)

# -----------------------------------------------------------------------------------
# Page: Inclusion Projections
# -----------------------------------------------------------------------------------
elif page == "Inclusion Projections":
    st.title("🎯 Progress to Targets")
    st.markdown("Tracking progress towards the **60% Financial Inclusion** target.")
    
    target_val = 60.0
    
    # Filter for Account Ownership Forecasts
    acc_forecasts = df_forecast[df_forecast['Indicator'] == 'ACC_OWNERSHIP']
    
    if acc_forecasts.empty:
        st.warning("Account Ownership forecasts missing.")
    else:
        # Scenario Selector
        scenarios = acc_forecasts['Scenario'].unique()
        selected_scenario = st.radio("Select Scenario", scenarios, horizontal=True)
        
        scenario_data = acc_forecasts[acc_forecasts['Scenario'] == selected_scenario].sort_values('Year')
        
        # Combine with historical if available
        # Find latest historical
        acc_hist = df_hist[df_hist['indicator_code'] == 'ACC_OWNERSHIP'].sort_values('Year')
        
        # Plot
        fig_proj = go.Figure()
        
        # Historical Trace
        if not acc_hist.empty:
            fig_proj.add_trace(go.Scatter(x=acc_hist['Year'], y=acc_hist['value_numeric'],
                                          mode='lines+markers', name='Historical',
                                          line=dict(color='gray', dash='dot')))
            
        # Forecast Trace
        fig_proj.add_trace(go.Scatter(x=scenario_data['Year'], y=scenario_data['Value'],
                                      mode='lines+markers', name=f'Forecast ({selected_scenario})',
                                      line=dict(width=3)))
        
        # Target Line
        last_year = scenario_data['Year'].max() if not scenario_data.empty else 2027
        first_year = acc_hist['Year'].min() if not acc_hist.empty else 2014
        
        fig_proj.add_shape(type="line",
                           x0=first_year, y0=target_val, x1=last_year, y1=target_val,
                           line=dict(color="gold", width=2, dash="dash"),
                           name="60% Target")
        
        fig_proj.add_annotation(x=last_year, y=target_val, text="60% Target", showarrow=False, yshift=10)
        
        fig_proj.update_layout(title="Financial Inclusion Trajectory vs Target",
                               xaxis_title="Year", yaxis_title="Account Ownership (%)")
        
        st.plotly_chart(fig_proj, use_container_width=True)
        
        # Analysis Text
        # Simple logic to find crossing point
        crossing_year = None
        for _, row in scenario_data.iterrows():
            if row['Value'] >= target_val:
                crossing_year = row['Year']
                break
        
        result_box = st.container()
        if crossing_year:
            result_box.success(f"✅ Under the **{selected_scenario}** scenario, the 60% target is projected to be reached in **{int(crossing_year)}**.")
        else:
            result_box.warning(f"⚠️ Under the **{selected_scenario}** scenario, the 60% target may NOT be reached by 2027.")

# -----------------------------------------------------------------------------------
# Footer & Download
# -----------------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### Data Download")
# Convert df_forecast to csv
csv = df_forecast.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download Forecasts CSV",
    data=csv,
    file_name='ethiopia_fi_forecasts.csv',
    mime='text/csv',
)
