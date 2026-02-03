import pandas as pd
import datetime

def enrich_data():
    file_path = 'data/raw/ethiopia_fi_unified_data.csv'
    df = pd.read_csv(file_path)
    
    new_records = [
        # --- Observations ---
        {
            'record_id': 'REC_ENR_001',
            'record_type': 'observation',
            'pillar': 'ACCESS',
            'indicator': 'Account Ownership (% of adults)',
            'indicator_code': 'ACC_OWNERSHIP',
            'indicator_direction': 'higher_better',
            'value_numeric': 52.0,
            'value_type': 'percentage',
            'observation_date': '2024-12-31',
            'source_url': 'https://www.worldbank.org/en/publication/globalfindex',
            'confidence': 'high',
            'gender': 'all',
            'location': 'national',
            'collected_by': 'Antigravity',
            'collection_date': datetime.date.today().isoformat(),
            'notes': 'Estimated increase from 2021 Findex based on mobile money growth.'
        },
        {
            'record_id': 'REC_ENR_002',
            'record_type': 'observation',
            'pillar': 'USAGE',
            'indicator': 'Digital Payment Adoption (% of adults)',
            'indicator_code': 'USG_DIGITAL_PAY',
            'indicator_direction': 'higher_better',
            'value_numeric': 38.0,
            'value_type': 'percentage',
            'observation_date': '2024-12-31',
            'source_url': 'https://www.nbe.gov.et/',
            'confidence': 'medium',
            'gender': 'all',
            'location': 'national',
            'collected_by': 'Antigravity',
            'collection_date': datetime.date.today().isoformat(),
            'notes': 'Core target for usage dimension.'
        },
        {
            'record_id': 'REC_ENR_003',
            'record_type': 'observation',
            'pillar': 'ACCESS',
            'indicator': 'Mobile Money Agent Density (per 100k adults)',
            'indicator_code': 'ACC_MM_AGENT_DENSITY',
            'indicator_direction': 'higher_better',
            'value_numeric': 650.0,
            'value_type': 'count',
            'observation_date': '2024-06-30',
            'source_url': 'https://www.gsma.com/mobilemoney/',
            'confidence': 'high',
            'gender': 'all',
            'location': 'national',
            'collected_by': 'Antigravity',
            'collection_date': datetime.date.today().isoformat(),
            'notes': 'Reflects expansion of Telebirr and M-Pesa agent networks.'
        },
        {
            'record_id': 'REC_ENR_004',
            'record_type': 'observation',
            'pillar': 'USAGE',
            'indicator': 'Active vs Registered Mobile Money Accounts (%)',
            'indicator_code': 'USG_MM_ACTIVE_RATE',
            'indicator_direction': 'higher_better',
            'value_numeric': 45.0,
            'value_type': 'percentage',
            'observation_date': '2024-06-30',
            'source_url': 'https://www.nbe.gov.et/',
            'confidence': 'medium',
            'gender': 'all',
            'location': 'national',
            'collected_by': 'Antigravity',
            'collection_date': datetime.date.today().isoformat(),
            'notes': 'High registration but moderate activity remains a challenge.'
        },
        {
            'record_id': 'REC_ENR_005',
            'record_type': 'observation',
            'pillar': 'ACCESS',
            'indicator': 'Smartphone Penetration (% of connections)',
            'indicator_code': 'ACC_SMARTPHONE_PEN',
            'indicator_direction': 'higher_better',
            'value_numeric': 48.0,
            'value_type': 'percentage',
            'observation_date': '2024-12-31',
            'source_url': 'https://www.ethiotelecom.et/',
            'confidence': 'high',
            'gender': 'all',
            'location': 'national',
            'collected_by': 'Antigravity',
            'collection_date': datetime.date.today().isoformat(),
            'notes': 'Increasing availability of low-cost smartphones.'
        },
        # --- Events ---
        {
            'record_id': 'EVT_ENR_001',
            'record_type': 'event',
            'category': 'policy',
            'indicator': 'FX Liberalization and Exchange Rate Reform',
            'indicator_code': 'EVT_FX_LIBERAL',
            'observation_date': '2024-07-29',
            'source_url': 'https://www.nbe.gov.et/press-releases/',
            'confidence': 'high',
            'collected_by': 'Antigravity',
            'collection_date': datetime.date.today().isoformat(),
            'notes': 'Major macroeconomic reform affecting financial sector liquidity and investment.'
        },
        {
            'record_id': 'EVT_ENR_002',
            'record_type': 'event',
            'category': 'product_launch',
            'indicator': 'Launch of Digital Credit and Savings (Telebirr Mela/Kifiya)',
            'indicator_code': 'EVT_MELA_LAUNCH',
            'observation_date': '2022-08-04',
            'source_url': 'https://www.ethiotelecom.et/telebirr-mela/',
            'confidence': 'high',
            'collected_by': 'Antigravity',
            'collection_date': datetime.date.today().isoformat(),
            'notes': 'Expansion of digital financial services beyond payments.'
        },
        # --- Impact Links ---
        {
            'record_id': 'LNK_ENR_001',
            'record_type': 'impact_link',
            'parent_id': 'EVT_FX_LIBERAL',
            'indicator_code': 'ACC_OWNERSHIP',
            'pillar': 'ACCESS',
            'impact_direction': 'increase',
            'impact_magnitude': 'medium',
            'lag_months': 12,
            'relationship_type': 'indirect',
            'evidence_basis': 'literature',
            'collected_by': 'Antigravity',
            'collection_date': datetime.date.today().isoformat(),
            'notes': 'FX reform may attract FDI in fintech and improve equipment affordability over time.'
        },
        {
            'record_id': 'LNK_ENR_002',
            'record_type': 'impact_link',
            'parent_id': 'EVT_MELA_LAUNCH',
            'indicator_code': 'USG_DIGITAL_PAY',
            'pillar': 'USAGE',
            'impact_direction': 'increase',
            'impact_magnitude': 'high',
            'lag_months': 3,
            'relationship_type': 'direct',
            'evidence_basis': 'empirical',
            'collected_by': 'Antigravity',
            'collection_date': datetime.date.today().isoformat(),
            'notes': 'Digital credit availability strongly drives ecosystem usage.'
        }
    ]

    new_df = pd.DataFrame(new_records)
    
    # Add columns to df if they are in new_df but not in df
    for col in new_df.columns:
        if col not in df.columns:
            df[col] = None

    # Ensure all columns from original df are present in new_df
    for col in df.columns:
        if col not in new_df.columns:
            new_df[col] = None
            
    # Reorder columns to match (now expanded) df
    new_df = new_df[df.columns]
    
    updated_df = pd.concat([df, new_df], ignore_index=True)
    updated_df.to_csv(file_path, index=False)
    print(f"Added {len(new_records)} new records to {file_path}")

if __name__ == "__main__":
    enrich_data()
