-- ==========================================
-- Cyber Risk & Compliance Analytics Project
-- Analytical Queries
-- Created by: Ayush Kumar
-- ==========================================

USE cyber_risk_db;

-- 1. Top 10 High-Risk Assets
SELECT 
    a.asset_id, 
    a.asset_name, 
    a.department, 
    r.asset_risk_score, 
    r.risk_band, 
    r.top_risk_driver
FROM assets a
JOIN risk_scores r ON a.asset_id = r.asset_id
ORDER BY r.asset_risk_score DESC
LIMIT 10;

-- 2. Vulnerability Distribution by Severity
SELECT 
    severity, 
    COUNT(*) as count, 
    ROUND(AVG(cvss_score), 2) as avg_cvss
FROM vulnerabilities
GROUP BY severity
ORDER BY avg_cvss DESC;

-- 3. Incident Count and Total Downtime by Department
SELECT 
    a.department, 
    COUNT(i.incident_id) as total_incidents, 
    SUM(i.downtime_hours) as total_downtime_hours,
    AVG(i.impact_score) as avg_impact
FROM assets a
JOIN incidents i ON a.asset_id = i.asset_id
GROUP BY a.department
ORDER BY total_incidents DESC;

-- 4. Overdue Remediation Actions (Compliance Check)
SELECT 
    ra.action_id, 
    ra.vuln_id, 
    ra.assigned_to, 
    ra.due_date, 
    v.severity,
    ra.action_status
FROM remediation_actions ra
JOIN vulnerabilities v ON ra.vuln_id = v.vuln_id
WHERE ra.action_status != 'Completed' AND ra.due_date < CURDATE()
ORDER BY v.severity ASC;

-- 5. Risk Posture Summary by Department
SELECT 
    a.department, 
    COUNT(a.asset_id) as asset_count,
    ROUND(AVG(r.asset_risk_score), 2) as avg_risk_score,
    SUM(CASE WHEN r.risk_band = 'Critical' THEN 1 ELSE 0 END) as critical_assets
FROM assets a
JOIN risk_scores r ON a.asset_id = r.asset_id
GROUP BY a.department
ORDER BY avg_risk_score DESC;
