import pandas as pd
import numpy as np
import os

def explore_data():
    raw_path = 'data/raw/ethiopia_fi_unified_data.csv'
    ref_path = 'data/raw/reference_codes.csv'
    
    if not os.path.exists(raw_path) or not os.path.exists(ref_path):
        print("Data files not found.")
        return

    df = pd.read_csv(raw_path)
    ref = pd.read_csv(ref_path)

    print("--- Step 1: Understand the Schema ---")
    print(f"Total records: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")

    """
    SCHEMA EXPLANATION:
    - observation: Actual measured values of indicators (e.g., % of adults with accounts). Contains 'pillar'.
    - event: Macro events, policy launches, or milestones. Do NOT have 'pillar' because they affect multiple pillars or create environment.
    - impact_link: Defines relationships between an 'event' (via parent_id) and an 'indicator' (via indicator_code).
    - target: Official policy goals or benchmarks.
    - parent_id: Used in impact_link records to reference the record_id of an event.
    """
    
    # Confirm all records share the same columns
    # (By definition of CSV, they do, but we check for non-null counts)
    print("\nNon-null counts per column:")
    print(df.info())

    print("\nRecord types distribution:")
    print(df['record_type'].value_counts())

    print("\n--- Step 2: Explore the Existing Data ---")
    
    # Summary of record counts
    print("\nSummary Counts (record_type, pillar, source_type, confidence):")
    summary = df.groupby(['record_type', 'pillar', 'source_type', 'confidence'], dropna=False).size().reset_index(name='count')
    print(summary.to_string(index=False))

    # Temporal coverage
    obs_df = df[df['record_type'] == 'observation'].copy()
    if not obs_df.empty:
        obs_df['observation_date'] = pd.to_datetime(obs_df['observation_date'])
        print(f"\nObservation range: {obs_df['observation_date'].min().date()} to {obs_df['observation_date'].max().date()}")
        
        # Missing years/gaps
        obs_df['year'] = obs_df['observation_date'].dt.year
        unique_years = sorted(obs_df['year'].unique())
        print(f"Unique years covered: {unique_years}")
        full_range = list(range(int(min(unique_years)), int(max(unique_years)) + 1))
        gaps = [y for y in full_range if y not in unique_years]
        print(f"Gaps in time series: {gaps}")

    # Indicator coverage
    print("\nIndicator coverage (Observations):")
    indicator_counts = df[df['record_type'] == 'observation'].groupby('indicator_code').size().reset_index(name='count')
    print(indicator_counts.to_string(index=False))

    # Events
    print("\nEvents:")
    events_df = df[df['record_type'] == 'event']
    if not events_df.empty:
        print(events_df[['record_id', 'category', 'observation_date', 'indicator_code']].to_string(index=False))

    # Impact links
    print("\nImpact Links:")
    links_df = df[df['record_type'] == 'impact_link']
    if not links_df.empty:
        print(links_df[['record_id', 'parent_id', 'indicator_code', 'impact_direction', 'impact_magnitude', 'lag_months']].to_string(index=False))

    # Validation against reference codes
    print("\n--- Validation ---")
    valid_record_types = ref[ref['field'] == 'record_type']['code'].tolist()
    invalid_record_types = df[~df['record_type'].isin(valid_record_types)]['record_type'].unique()
    print(f"Invalid record types: {invalid_record_types}")

    valid_pillars = ref[ref['field'] == 'pillar']['code'].tolist()
    # Events should NOT have pillars
    events_with_pillar = df[(df['record_type'] == 'event') & (df['pillar'].notnull())]
    print(f"Events with pillars (should be 0): {len(events_with_pillar)}")
    
    # Observations should have pillars
    obs_without_pillar = df[(df['record_type'] == 'observation') & (df['pillar'].isnull())]
    print(f"Observations without pillars (should be 0): {len(obs_without_pillar)}")

if __name__ == "__main__":
    explore_data()
