# Data Enrichment Log - Ethiopia Financial Inclusion

This log documents the new records added to `data/raw/ethiopia_fi_unified_data.csv` to improve forecasting of core targets.

## Summary of Additions
- **Observations**: 5 new records
- **Events**: 2 new records
- **Impact Links**: 2 new records

---

## New Records Details

### Observations
1. **Account Ownership (% of adults)**
   - **ID**: `REC_ENR_001`
   - **Pillar**: ACCESS
   - **Source**: [Global Findex](https://www.worldbank.org/en/publication/globalfindex)
   - **Confidence**: high
   - **Notes**: Estimated update for 2024 based on rapid mobile money growth.

2. **Digital Payment Adoption (% of adults)**
   - **ID**: `REC_ENR_002`
   - **Pillar**: USAGE
   - **Source**: [National Bank of Ethiopia](https://www.nbe.gov.et/)
   - **Confidence**: medium
   - **Notes**: Core usage target for forecasting digital economy growth.

3. **Mobile Money Agent Density (per 100k adults)**
   - **ID**: `REC_ENR_003`
   - **Pillar**: ACCESS
   - **Source**: [GSMA Mobile Money](https://www.gsma.com/mobilemoney/)
   - **Confidence**: high
   - **Notes**: Expansion of Telebirr and M-Pesa agent networks is a key driver for access.

4. **Active vs Registered Mobile Money Accounts (%)**
   - **ID**: `REC_ENR_004`
   - **Pillar**: USAGE
   - **Source**: [National Bank of Ethiopia](https://www.nbe.gov.et/)
   - **Confidence**: medium
   - **Notes**: Measures the quality of inclusion beyond simple registration.

5. **Smartphone Penetration (% of connections)**
   - **ID**: `REC_ENR_005`
   - **Pillar**: ACCESS
   - **Source**: [Ethio Telecom Annual Report](https://www.ethiotelecom.et/)
   - **Confidence**: high
   - **Notes**: Availability of smartphones is a prerequisite for advanced digital financial services.

### Events
1. **FX Liberalization and Exchange Rate Reform**
   - **ID**: `EVT_ENR_001`
   - **Category**: policy
   - **Date**: 2024-07-29
   - **Notes**: Significant macroeconomic shift expected to impact financial services investment.

2. **Launch of Digital Credit and Savings (Telebirr Mela/Kifiya)**
   - **ID**: `EVT_ENR_002`
   - **Category**: product_launch
   - **Date**: 2022-08-04
   - **Notes**: Key milestone for service depth.

### Impact Links
1. **FX Liberalization → Account Ownership**
   - **ID**: `LNK_ENR_001`
   - **Parent ID**: `EVT_FX_LIBERAL`
   - **Direction**: increase
   - **Magnitude**: medium
   - **Lag**: 12 months
   - **Basis**: literature

2. **Telebirr Mela/Kifiya Launch → Digital Payment Adoption**
   - **ID**: `LNK_ENR_002`
   - **Parent ID**: `EVT_MELA_LAUNCH`
   - **Direction**: increase
   - **Magnitude**: high
   - **Lag**: 3 months
   - **Basis**: empirical

---

## Technical Metadata
- **Collected By**: Antigravity (AI Data Scientist)
- **Collection Date**: 2025-02-03
- **Schema Compliance**: Verified against `reference_codes.csv`
