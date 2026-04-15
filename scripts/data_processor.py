import pandas as pd
import numpy as np
import os

# Configuration
RAW_DATA_PATH = "data/raw"
PROCESSED_DATA_PATH = "data/processed"
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

def clean_data():
    print("Cleaning data...")
    assets = pd.read_csv(f"{RAW_DATA_PATH}/assets.csv")
    vulns = pd.read_csv(f"{RAW_DATA_PATH}/vulnerabilities.csv")
    incidents = pd.read_csv(f"{RAW_DATA_PATH}/incidents.csv")
    remediation = pd.read_csv(f"{RAW_DATA_PATH}/remediation_actions.csv")

    # Handle missing CVSS scores (Fill with median for that severity)
    vulns['cvss_score'] = vulns.groupby('severity')['cvss_score'].transform(lambda x: x.fillna(x.median()))
    
    # Ensure dates are in datetime format
    # Using errors='coerce' turns invalid/empty strings into NaT (Not a Time)
    # which pandas handles as NULL when exporting to CSV
    date_cols = {
        'vulns': ['discovery_date'],
        'incidents': ['incident_date'],
        'remediation': ['start_date', 'due_date', 'closed_date']
    }

    # Clean remediation dates specifically
    for col in date_cols['remediation']:
        # Replace empty strings with None before conversion as requested
        remediation[col] = remediation[col].replace('', None)
        remediation[col] = pd.to_datetime(remediation[col], errors='coerce')

    vulns['discovery_date'] = pd.to_datetime(vulns['discovery_date'], errors='coerce')
    incidents['incident_date'] = pd.to_datetime(incidents['incident_date'], errors='coerce')

    return assets, vulns, incidents, remediation

def calculate_risk_scores(assets, vulns, incidents):
    print("Calculating Risk Scores...")
    
    # Mapping for weights
    criticality_map = {"Critical": 1.0, "High": 0.8, "Medium": 0.5, "Low": 0.2}
    severity_map = {"Critical": 10, "High": 7, "Medium": 4, "Low": 2}

    # 1. Base Score from Criticality and Business Value
    assets['base_score'] = assets['criticality'].map(criticality_map) * assets['business_value']

    # 2. Vulnerability Score Impact
    vuln_scores = vulns.groupby('asset_id')['cvss_score'].sum().reset_index()
    vuln_scores.columns = ['asset_id', 'vuln_impact']

    # 3. Incident Score Impact
    incident_scores = incidents.groupby('asset_id')['impact_score'].sum().reset_index()
    incident_scores.columns = ['asset_id', 'incident_impact']

    # Merge everything
    risk_df = assets.merge(vuln_scores, on='asset_id', how='left').merge(incident_scores, on='asset_id', how='left')
    risk_df[['vuln_impact', 'incident_impact']] = risk_df[['vuln_impact', 'incident_impact']].fillna(0)

    # 4. Exposure Penalty
    risk_df['exposure_penalty'] = risk_df['internet_exposed'].apply(lambda x: 15 if x == "Yes" else 0)

    # Final Composite Score
    risk_df['raw_risk_score'] = (
        risk_df['base_score'] + 
        (risk_df['vuln_impact'] * 0.5) + # Weighting down sums to prevent outliers
        (risk_df['incident_impact'] * 2) + 
        risk_df['exposure_penalty']
    )

    # Normalize to 0-100
    min_score = risk_df['raw_risk_score'].min()
    max_score = risk_df['raw_risk_score'].max()
    risk_df['asset_risk_score'] = ((risk_df['raw_risk_score'] - min_score) / (max_score - min_score)) * 100
    risk_df['asset_risk_score'] = risk_df['asset_risk_score'].round(2)

    # Risk Banding
    def get_risk_band(score):
        if score > 80: return "Critical"
        if score > 60: return "High"
        if score > 30: return "Medium"
        return "Low"

    risk_df['risk_band'] = risk_df['asset_risk_score'].apply(get_risk_band)

    # Top Risk Driver
    def get_top_driver(row):
        scores = {
            "Vulnerabilities": row['vuln_impact'],
            "Incidents": row['incident_impact'],
            "Exposure": row['exposure_penalty']
        }
        return max(scores, key=scores.get)

    risk_df['top_risk_driver'] = risk_df.apply(get_top_driver, axis=1)

    # Final Risk Scores Table
    scores_final = risk_df[['asset_id', 'asset_risk_score', 'risk_band', 'top_risk_driver']]
    
    return assets, vulns, incidents, scores_final

def export_final_data(assets, vulns, incidents, remediation, risk_scores):
    print("Exporting dashboard-ready CSVs...")
    
    # Final Validation
    print(f"Validation: Remediation row count = {len(remediation)} (Expected: 1500)")
    if len(remediation) != 1500:
        print("WARNING: Data loss detected in remediation table!")

    # Optional: Format dates to YYYY-MM-DD strings to be safe
    # This will keep NaT as empty fields, which is correct for CSV
    for col in ['start_date', 'due_date', 'closed_date']:
        remediation[col] = remediation[col].dt.strftime('%Y-%m-%d')

    assets.to_csv(f"{PROCESSED_DATA_PATH}/assets_clean.csv", index=False, na_rep='\\N')
    vulns.to_csv(f"{PROCESSED_DATA_PATH}/vulnerabilities_clean.csv", index=False, na_rep='\\N')
    incidents.to_csv(f"{PROCESSED_DATA_PATH}/incidents_clean.csv", index=False, na_rep='\\N')
    remediation.to_csv(f"{PROCESSED_DATA_PATH}/remediation_clean.csv", index=False, na_rep='\\N')
    risk_scores.to_csv(f"{PROCESSED_DATA_PATH}/risk_scores_final.csv", index=False, na_rep='\\N')

if __name__ == "__main__":
    assets, vulns, incidents, remediation = clean_data()
    assets, vulns, incidents, risk_scores = calculate_risk_scores(assets, vulns, incidents)
    export_final_data(assets, vulns, incidents, remediation, risk_scores)
    
    # Show preview
    print("\n--- Cleaned Remediation Data Preview ---")
    print(remediation[['action_id', 'vuln_id', 'start_date', 'closed_date', 'action_status']].head())
    
    print("\nData Processing and Risk Scoring Complete!")
