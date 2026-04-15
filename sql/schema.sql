-- ==========================================
-- Cyber Risk & Compliance Analytics Project
-- Database Schema (MySQL Compatible)
-- Created by: Ayush Kumar
-- ==========================================

CREATE DATABASE IF NOT EXISTS cyber_risk_db;
USE cyber_risk_db;

-- 1. Assets Table
CREATE TABLE IF NOT EXISTS assets (
    asset_id VARCHAR(20) PRIMARY KEY,
    asset_name VARCHAR(100),
    department VARCHAR(50),
    asset_type VARCHAR(50),
    owner_role VARCHAR(50),
    location VARCHAR(50),
    criticality ENUM('Critical', 'High', 'Medium', 'Low'),
    internet_exposed ENUM('Yes', 'No'),
    cloud_or_onprem ENUM('Cloud', 'On-Prem'),
    business_value INT
);

-- 2. Vulnerabilities Table
CREATE TABLE IF NOT EXISTS vulnerabilities (
    vuln_id VARCHAR(20) PRIMARY KEY,
    asset_id VARCHAR(20),
    cve_id VARCHAR(20),
    severity ENUM('Critical', 'High', 'Medium', 'Low'),
    cvss_score DECIMAL(3, 1),
    cwe_type VARCHAR(50),
    discovery_date DATE,
    status ENUM('Open', 'In Progress', 'Closed', 'Risk Accepted'),
    patch_due_days INT,
    exploit_available ENUM('Yes', 'No'),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

-- 3. Incidents Table
CREATE TABLE IF NOT EXISTS incidents (
    incident_id VARCHAR(20) PRIMARY KEY,
    asset_id VARCHAR(20),
    incident_type VARCHAR(50),
    incident_date DATE,
    impact_score INT,
    downtime_hours INT,
    resolved ENUM('Yes', 'No'),
    response_team VARCHAR(50),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

-- 4. Remediation Actions Table
CREATE TABLE IF NOT EXISTS remediation_actions (
    action_id VARCHAR(20) PRIMARY KEY,
    vuln_id VARCHAR(20),
    action_type VARCHAR(50),
    assigned_to VARCHAR(100),
    priority ENUM('Immediate', 'High', 'Medium', 'Low'),
    start_date DATE,
    due_date DATE,
    closed_date DATE,
    action_status ENUM('Completed', 'In Progress', 'Failed', 'Pending'),
    FOREIGN KEY (vuln_id) REFERENCES vulnerabilities(vuln_id)
);

-- 5. Risk Scores Table
CREATE TABLE IF NOT EXISTS risk_scores (
    asset_id VARCHAR(20) PRIMARY KEY,
    asset_risk_score DECIMAL(5, 2),
    risk_band ENUM('Critical', 'High', 'Medium', 'Low'),
    top_risk_driver VARCHAR(50),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);
