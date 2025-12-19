# 📊 Client Query Management System (CQMS)

A **data-driven, role-based support management system** that enables clients to submit queries in real time, support teams to manage and resolve them efficiently, and stakeholders to analyze service performance using analytics.

---

## 🧩 Project Overview

Organizations receive a large number of client support queries daily. Manual handling leads to delays, poor tracking, and low customer satisfaction.

The **Client Query Management System (CQMS)** solves this by providing:
- Secure authentication for clients and support teams
- Real-time query submission and lifecycle tracking
- Support workload management
- Analytics-driven service efficiency insights
- Clean, validated, and analytics-ready data pipeline

---

## 🎯 Project Objectives

- Organize incoming client queries
- Track query lifecycle (Open → Closed)
- Improve query resolution efficiency
- Monitor support workload and trends
- Maintain high-quality, validated data for analytics

---

## 🏗️ System Architecture

### High-Level Flow

Client / Support User
↓
Streamlit UI
↓
Authentication Layer
↓
Validation & Cleaning
↓
MySQL Database
↓
Analytics Engine


📸 *(Attach Architecture Diagram Screenshot Here)*

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| Programming Language | Python |
| Frontend | Streamlit |
| Database | MySQL |
| Data Processing | Pandas |
| Security | hashlib (SHA-256) |
| Validation | Regular Expressions |
| Visualization | Streamlit Charts |
| Version Control | Git |

---

## 🔐 Login System

### Roles Supported
- **Client**
- **Support**

### Authentication Design
- Database-level authentication only
- No OTP / Email / SMS verification
- Passwords stored using **SHA-256 hashing**

### Login Options
Users can authenticate using:
- Username + Password  
- Email + Password  
- Mobile Number + Password  

### Security Techniques
- `hashlib.sha256()` for password hashing
- SQL-based credential verification
- Role-based routing using Streamlit session state

📸 *(Attach Login Page Screenshot Here)*

---

## 👤 Client Dashboard

The Client Dashboard provides a unified interface for clients to view analytics, manage their queries, and raise new issues.

### Tabs Included
1. **Client Analytics**
2. **My Queries**
3. **New Query**

---

### 1️⃣ Client Analytics
Displays:
- Total number of queries
- Open vs Closed queries
- Average & median resolution time
- Queries by category
- Queries raised over time

📸 *(Attach Client Analytics Screenshot Here)*

---

### 2️⃣ My Queries
Features:
- View all submitted queries
- Filter by status, category, and date
- Status-based highlighting (Open / Closed)
- Invalid mobile number highlighting
- CSV export functionality

📸 *(Attach My Queries Table Screenshot Here)*

---

### 3️⃣ New Query
Clients can:
- Select query category
- Enter query heading and description
- Upload issue screenshot (image)
- Submit query in real time

#### Validations Applied
- Mobile number regex validation
- Mandatory field validation
- Image upload support

📸 *(Attach New Query Form Screenshot Here)*

---

## 🧑‍💼 Support Dashboard

The Support Dashboard is designed for operational workflow management and analytics.

### Tabs Included
1. **Open Queue**
2. **My In-Progress**
3. **Closed Queries**
4. **Team Analytics**

---

### Query Lifecycle
 
Open → In Progress → Closed
 
Support workflow:
- Pick queries from Open Queue
- Work on assigned queries
- Close queries after resolution

📸 *(Attach Support Dashboard Screenshot Here)*

---

### Team Analytics
Displays:
- Queries handled per support agent
- Average resolution time per agent
- Support load by category
- SLA breach identification

📸 *(Attach Support Analytics Screenshot Here)*

---

## 📈 Analytics Engine

### Key Metrics
- Average resolution time
- Median resolution time
- Query volume by category
- Agent workload analytics
- SLA breach counts

### Example Formula
Resolution Time = query_closed_time − query_created_time

Analytics are computed using **Pandas groupby operations and datetime calculations**.

---

## 🧹 Data Cleaning & Validation

All data cleaning is performed before database insertion and documented in `data_cleaning.ipynb`.

### Techniques Used

#### 1️⃣ Email Validation
- Regex-based format validation
- Invalid emails flagged (not deleted)

Valid Email Rate = 5200 / 5200 = 100%


#### 2️⃣ Mobile Number Cleaning
- Normalized to last 10 digits
- Indian mobile regex validation
- Invalid mobile numbers flagged

#### 3️⃣ Status Normalization
- Standardized to `Open` and `Closed`

#### 4️⃣ Date Handling
- Converted to datetime
- Resolution time derived

#### 5️⃣ Output
- Cleaned dataset saved as:
cleaned_client_queries.csv


📸 *(Attach Data Cleaning Notebook Screenshot Here)*

---

## 🗄️ Database Schema

### Tables
- `users`
- `support_agents`
- `client_queries`
- `client_reviews`

### Relationships
- Clients submit queries
- Queries are assigned to support agents
- Clients provide reviews after query closure

📸 *(Attach ER Diagram Screenshot Here)*

---

## 📂 Project Structure
```bash
client-query-management-system/
│
├── README.md
├── requirements.txt
├── schema.sql
├── schema.py
│
├── data/
│   ├── raw/
│   │   └── synthetic_client_queries.csv
│   ├── cleaned/
│   │   └── cleaned_client_queries.csv
│   └── sample_images/
│       └── issue_screenshot_example.png
│
├── notebooks/
│   └── data_cleaning.ipynb
│
├── src/
│   ├── app.py
│   │
│   ├── services/
│   │   ├── db_connection.py
│   │   ├── csv_loader.py
│   │   └── __init__.py
│   │
│   ├── auth/
│   │   ├── login.py
│   │   ├── auth_utils.py
│   │   └── __init__.py
│   │
│   ├── client/
│   │   ├── client_dashboard.py
│   │   ├── query_form.py
│   │   └── __init__.py
│   │
│   ├── support/
│   │   ├── support_dashboard.py
│   │   └── __init__.py
│   │
│   ├── analytics/
│   │   ├── analytics.py
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── regex_utils.py
│       ├── date_utils.py
│       └── __init__.py
│
└── assets/
    ├── architecture_diagram.png
    ├── er_diagram.png
    └── miro_exports/
        ├── cqms_architecture_miro.png
        └── cqms_mindmap_miro.png

```

---

## ▶️ How to Run the Project

### 1️⃣ Create Database Schema
```bash
python schema.py
```
2️⃣ Load Cleaned CSV Data
```bash
python -m src.services.csv_loader
```
3️⃣ Run Streamlit Application
```bash
streamlit run src/app.py
```

## 🚀 Future Enhancements
```bash
- Email / OTP verification

- SLA automation

- Advanced analytics dashboards

- Notification system
```
## 👤 Author
```bash
- Bhuvana PS
- Website Developer / SEO Specialist / Digital Marketing advisor
- Domain: Data Engineering / Data Analytics / Python
```


