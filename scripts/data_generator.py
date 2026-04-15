import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Configuration
NUM_ASSETS = 500
NUM_VULNS = 3000
NUM_INCIDENTS = 1000
NUM_REMEDIATIONS = 1500

# Directory Setup
RAW_DATA_PATH = "data/raw"
os.makedirs(RAW_DATA_PATH, exist_ok=True)

def generate_assets():
    print("Generating Assets...")
    departments = ["Finance", "IT", "HR", "Sales", "Marketing", "Operations", "Legal", "R&D"]
    asset_types = ["Server", "Workstation", "Database", "Cloud Instance", "Mobile Device", "IoT Device", "Network Switch"]
    locations = ["New York", "London", "Tokyo", "Singapore", "Dublin", "On-Prem"]
    criticality_levels = ["Critical", "High", "Medium", "Low"]
    
    assets = []
    for i in range(1, NUM_ASSETS + 1):
        dept = random.choice(departments)
        asset_type = random.choice(asset_types)
        
        # Business Logic: Finance and IT have higher criticality and business value
        if dept in ["Finance", "IT"]:
            criticality = random.choice(["Critical", "High"])
            business_value = random.randint(70, 100)
        else:
            criticality = random.choice(criticality_levels)
            business_value = random.randint(10, 80)
            
        is_exposed = random.choice([True, False]) if asset_type in ["Server", "Database", "Cloud Instance"] else False
        
        assets.append({
            "asset_id": f"AST-{i:04d}",
            "asset_name": f"{asset_type}_{i}",
            "department": dept,
            "asset_type": asset_type,
            "owner_role": f"{dept} Admin",
            "location": random.choice(locations),
            "criticality": criticality,
            "internet_exposed": "Yes" if is_exposed else "No",
            "cloud_or_onprem": "Cloud" if "Cloud" in asset_type else "On-Prem",
            "business_value": business_value
        })
    df = pd.DataFrame(assets)
    df.to_csv(f"{RAW_DATA_PATH}/assets.csv", index=False)
    return df

def generate_vulnerabilities(assets_df):
    print("Generating Vulnerabilities...")
    vulns = []
    cve_ids = [f"CVE-2023-{random.randint(1000, 9999)}" for _ in range(500)]
    severities = ["Critical", "High", "Medium", "Low"]
    statuses = ["Open", "In Progress", "Closed", "Risk Accepted"]
    cwe_types = ["CWE-79", "CWE-89", "CWE-20", "CWE-119", "CWE-200", "CWE-287"]

    for i in range(1, NUM_VULNS + 1):
        asset = assets_df.sample(1).iloc[0]
        severity = random.choice(severities)
        
        # Business logic: Critical vulns have higher CVSS scores
        if severity == "Critical":
            cvss = round(random.uniform(9.0, 10.0), 1)
        elif severity == "High":
            cvss = round(random.uniform(7.0, 8.9), 1)
        elif severity == "Medium":
            cvss = round(random.uniform(4.0, 6.9), 1)
        else:
            cvss = round(random.uniform(0.1, 3.9), 1)
            
        discovery_date = fake.date_between(start_date="-1y", end_date="today")
        
        vulns.append({
            "vuln_id": f"VULN-{i:05d}",
            "asset_id": asset["asset_id"],
            "cve_id": random.choice(cve_ids),
            "severity": severity,
            "cvss_score": cvss,
            "cwe_type": random.choice(cwe_types),
            "discovery_date": discovery_date,
            "status": random.choice(statuses),
            "patch_due_days": random.choice([7, 14, 30, 60, 90]),
            "exploit_available": random.choice(["Yes", "No"])
        })
    df = pd.DataFrame(vulns)
    # Add some missing values for cleaning script
    df.loc[df.sample(int(NUM_VULNS * 0.05)).index, 'cvss_score'] = np.nan
    df.to_csv(f"{RAW_DATA_PATH}/vulnerabilities.csv", index=False)
    return df

def generate_incidents(assets_df):
    print("Generating Incidents...")
    incidents = []
    incident_types = ["Malware", "Phishing", "DDoS", "Unauthorized Access", "Data Leak", "Ransomware"]
    teams = ["SOC Tier 1", "SOC Tier 2", "Incident Response Team", "Forensics"]

    for i in range(1, NUM_INCIDENTS + 1):
        asset = assets_df.sample(1).iloc[0]
        
        # Business logic: High value assets might have higher impact incidents
        if asset["business_value"] > 80:
            impact = random.randint(7, 10)
        else:
            impact = random.randint(1, 6)
            
        incidents.append({
            "incident_id": f"INC-{i:05d}",
            "asset_id": asset["asset_id"],
            "incident_type": random.choice(incident_types),
            "incident_date": fake.date_between(start_date="-1y", end_date="today"),
            "impact_score": impact,
            "downtime_hours": random.randint(0, 48),
            "resolved": random.choice(["Yes", "No"]),
            "response_team": random.choice(teams)
        })
    df = pd.DataFrame(incidents)
    df.to_csv(f"{RAW_DATA_PATH}/incidents.csv", index=False)
    return df

def generate_remediation(vulns_df):
    print("Generating Remediation Actions...")
    actions = []
    action_types = ["Patching", "Config Change", "User Training", "Network Segregation", "Software Update"]
    priorities = ["Immediate", "High", "Medium", "Low"]
    
    # We only remediate a subset of vulnerabilities
    remediated_vulns = vulns_df.sample(NUM_REMEDIATIONS)
    
    for i, (_, vuln) in enumerate(remediated_vulns.iterrows(), 1):
        start_date = vuln["discovery_date"] + timedelta(days=random.randint(1, 5))
        closed_date = start_date + timedelta(days=random.randint(1, 20))
        
        actions.append({
            "action_id": f"ACT-{i:05d}",
            "vuln_id": vuln["vuln_id"],
            "action_type": random.choice(action_types),
            "assigned_to": fake.name(),
            "priority": random.choice(priorities),
            "start_date": start_date,
            "due_date": start_date + timedelta(days=30),
            "closed_date": closed_date if random.random() > 0.2 else None, # Some are still open
            "action_status": "Completed" if random.random() > 0.2 else "In Progress"
        })
    df = pd.DataFrame(actions)
    df.to_csv(f"{RAW_DATA_PATH}/remediation_actions.csv", index=False)
    return df

if __name__ == "__main__":
    assets_df = generate_assets()
    vulns_df = generate_vulnerabilities(assets_df)
    generate_incidents(assets_df)
    generate_remediation(vulns_df)
    print("Synthetic Data Generation Complete!")
