# 🛡️ Cyber Risk & Compliance Analytics Dashboard

## 📊 Project Overview
This project presents an end-to-end **Cyber Risk Analytics** solution built using **Python, MySQL, and Power BI**. It analyzes vulnerabilities, incidents, and remediation data to identify high-risk assets and support data-driven decision-making in an enterprise environment.

---

## 🚀 Key Features
* **Risk Analysis**: Quantifying risk across various departments (Finance, IT, HR, etc.).
* **Vulnerability Management**: Identifying and prioritizing critical CVEs.
* **Incident Intelligence**: Tracking trends and downtime impact over time.
* **Risk Prioritization**: Focus on the Top 10 Risky Assets using a custom scoring algorithm.
* **Interactive Visualization**: Comprehensive Power BI dashboard for executive reporting.

---

## 🛠️ Tech Stack
* **Python**: `pandas`, `numpy`, `faker` (Data Generation & Processing)
* **MySQL**: Relational Database Management & Analytical Querying
* **Power BI**: ETL, Data Modeling, and Interactive Dashboarding

---

## 📁 Project Structure
* `data/` → Synthetic raw and processed datasets (CSV)
* `scripts/` → Python scripts for data pipeline automation
* `sql/` → Database schema and advanced analytical queries
* `screenshots/` → Dashboard visuals and previews
* `Cyber-Risk-Analytics-Dashboard.pbix` → Interactive Power BI Dashboard file

---

## 📈 Key Insights
* **Departmental Risk**: IT and Finance departments consistently show the highest risk exposure due to high business value.
* **Critical Vulnerabilities**: A subset of vulnerabilities accounts for 80% of the total risk (Pareto Principle).
* **Incident Trends**: Correlation between unpatched critical vulnerabilities and security incidents.
* **Resource Optimization**: Top 10 assets contribute significantly to overall organizational risk.

---

## 🖼️ Dashboard Preview
Here are some previews of the interactive Power BI dashboard:

![Dashboard Overview](screenshots/Screenshot%202026-04-16%20040848.png)
![Risk Analysis](screenshots/Screenshot%202026-04-16%20040935.png)
![Vulnerability Distribution](screenshots/Screenshot%202026-04-16%20040949.png)
![Incident Tracking](screenshots/Screenshot%202026-04-16%20040957.png)
![Remediation Performance](screenshots/Screenshot%202026-04-16%20041006.png)
![Top Risky Assets](screenshots/Screenshot%202026-04-16%20041014.png)
![Departmental Risk](screenshots/Screenshot%202026-04-16%20041022.png)

---

## 💡 Outcome
Developed a complete, production-quality analytics pipeline that transforms raw security data into actionable insights, enabling a proactive approach to cyber risk management.

---

## 📋 How to Run
1.  **Environment**: Install Python and run `pip install pandas numpy faker`.
2.  **Generate Data**: Execute `python scripts/data_generator.py` and `python scripts/data_processor.py`.
3.  **Database**: Load `sql/schema.sql` into MySQL and import the processed CSVs.
4.  **Visualize**: Connect Power BI to the MySQL database or the processed CSV files.

---

## 🎯 Resume Bullets
- *Developed an end-to-end Cyber Risk Analytics pipeline using Python and MySQL to quantify enterprise risk across 500+ assets.*
- *Engineered a custom risk-scoring algorithm incorporating CVSS v3.1 scores, business criticality, and incident impact.*
- *Designed a 4-page Power BI executive dashboard providing visibility into compliance posture and security SLAs.*

---

## 👤 Author
**Ayush Kumar**
📧 [ayushkumarwork2554@gmail.com](mailto:ayushkumarwork2554@gmail.com)
