# 📦 Client Query Management System (CQMS)

A complete end-to-end **Client Query Management System** built using:

- **Python**
- **Streamlit**
- **MySQL**
- **Pandas**
- **bcrypt Authentication**
- **CSV Data Import**
- **Dark/Light Theme Support**

This project helps organizations track client issues, assign them to support teams, update status, and analyze support performance.

---

## 🚀 Features

### 👤 Client
- Submit new queries  
- Track open/closed issues  
- Search by query ID / mobile  
- Download history as CSV  
- See personal insights  

### 🎧 Support Team
- Login per category  
- View only assigned category queries  
- Close / update query status  
- View client history  
- Support performance insights  

### 🛠 Admin
- Create support team users  
- Manage categories  
- Set SLA hours  
- Upload CSV (clients, queries, support users)  
- Access dashboards & analytics  

---

## 🗂 Project Structure

client-query-management-system/
│
├── app.py
├── README.md
├── requirements.txt
├── schema.sql
│
├── services/
│ ├── db.py
│ ├── client_service.py
│ ├── support_service.py
│ ├── query_service.py
│ └── admin_service.py
│
├── auth/
│ ├── auth_utils.py
│ └── reset_utils.py
│
├── ui/
│ ├── theme.py
│ └── cards.py
│
├── pages/
│ ├── 1_Client_Dashboard.py
│ ├── 2_Support_Dashboard.py
│ ├── 3_Admin_Dashboard.py
│ ├── 3_Admin_Create_Support.py
│ ├── 3_Admin_Settings.py
│ ├── 3_Analytics_Admin.py
│ ├── 3_Analytics_Support.py
│ ├── 3_Analytics_Client.py
│ └── 4_CSV_Upload.py
│
├── static/
│ └── css/
│ ├── dark.css
│ └── light.css
│
└── data/
├── clients.csv
├── queries.csv
└── support_users.csv

   

---

## 🛢 Database Setup

1. Create database:

```sql
CREATE DATABASE client_query_statusdb;
Run schema:

```sql

SOURCE schema.sql;
Insert default admin:

pgsql

Email: admin@cqms.com  
Password: Admin@123
🧪 Running the Project
1️⃣ Create virtual environment
nginx

python -m venv venv
2️⃣ Activate venv
Windows:


venv\Scripts\activate
3️⃣ Install dependencies
nginx

pip install -r requirements.txt
4️⃣ Start the app
arduino

streamlit run app.py
📈 Capstone Outcomes
Complete data engineering pipeline

User authentication

Real-world support workflow

CSV ingestion

MySQL integration

Full EDA & analytics

👨‍💻 Author
Bhuvana P S

