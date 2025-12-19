📊 Client Query Management System (CQMS)

A data-driven, role-based support management system that enables clients to submit queries in real time, support teams to manage and resolve them efficiently, and stakeholders to analyze service performance using analytics.

🧩 Project Overview

Organizations receive a large number of support queries daily. Manual handling leads to delays, poor tracking, and low customer satisfaction.

CQMS solves this problem by providing:

Secure login for clients and support teams

Real-time query submission and tracking

Clear query lifecycle management

Analytics to measure service efficiency and support load

Clean, validated, and analytics-ready data pipeline

🎯 Objectives

Organize incoming client queries

Track query lifecycle from Open → Closed

Improve support response efficiency

Monitor support workload and trends

Maintain clean and reliable data for analytics

🏗️ System Architecture

High-Level Flow

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


📸 Screenshot: Architecture Diagram (attach here)

🛠️ Tech Stack
Layer	Technology
Language	Python
Frontend	Streamlit
Database	MySQL
Data Handling	Pandas
Security	hashlib (SHA-256)
Validation	Regular Expressions
Visualization	Streamlit Charts
Version Control	Git
🔐 Login System
Roles Supported

Client

Support

Authentication Logic

Database-level authentication only

No OTP / Email / External services

Passwords stored using SHA-256 hashing

Login Options

Users can log in using:

Username + Password

Email + Password

Mobile Number + Password

Security Techniques Used

hashlib.sha256()

SQL credential verification

Role-based routing using Streamlit session state

📸 Screenshot: Login Page

👤 Client Dashboard
Tabs Included

Client Analytics

My Queries

New Query

1️⃣ Client Analytics

Displays:

Total queries

Open vs Closed queries

Average & median resolution time

Query distribution by category

Query trend over time

📸 Screenshot: Client Analytics Tab

2️⃣ My Queries

Features:

View all submitted queries

Filter by status, category, date

Status highlighting (Open / Closed)

Invalid mobile highlighting

CSV export option

📸 Screenshot: My Queries Table

3️⃣ New Query

Clients can:

Select query category

Enter heading & description

Upload issue screenshot (image)

Submit query in real time

Validations Applied

Mobile number regex validation

Mandatory field checks

Image attachment support

📸 Screenshot: New Query Form

🧑‍💼 Support Dashboard
Tabs Included

Open Queue

My In-Progress

Closed Queries

Team Analytics

Query Lifecycle
Open → In Progress → Closed


Support workflow:

Pick query from Open Queue

Work on assigned queries

Close queries after resolution

📸 Screenshot: Support Dashboard – Open Queue

Team Analytics

Displays:

Queries handled per support agent

Average resolution time per agent

Support load by category

SLA breach identification

📸 Screenshot: Support Analytics

📈 Analytics Engine
Key Metrics

Average resolution time

Median resolution time

Query volume by category

Agent workload

SLA breach count

Formula Example
Resolution Time = query_closed_time − query_created_time


Analytics are computed using Pandas groupby and datetime operations.

🧹 Data Cleaning & Validation

All cleaning is performed before database insertion and documented in data_cleaning.ipynb.

Techniques Used
1️⃣ Email Validation

Regex-based format validation

Invalid emails flagged (not removed)

Valid Email Rate = 5200 / 5200 = 100%

2️⃣ Mobile Number Cleaning

Normalized to last 10 digits

Indian mobile regex validation

Invalid mobiles flagged

3️⃣ Status Normalization

Standardized to Open / Closed

4️⃣ Date Handling

Converted to datetime

Resolution time derived

5️⃣ Output

Cleaned dataset saved as:

cleaned_client_queries.csv


📸 Screenshot: Data Cleaning Notebook

🗄️ Database Schema
Tables

users

support_agents

client_queries

client_reviews

Relationships

Clients submit queries

Queries assigned to support agents

Clients submit reviews after closure

📸 Screenshot: ER Diagram

📂 Project Structure
client-query-management-system/
│
├── src/
│   ├── app.py
│   ├── client/
│   ├── support/
│   ├── analytics/
│   ├── services/
│   └── utils/
│
├── notebooks/
│   └── data_cleaning.ipynb
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── assets/
│   ├── architecture_diagram.png
│   ├── er_diagram.png
│   └── miro_exports/
│
├── schema.sql
├── schema.py
├── requirements.txt
└── README.md

▶️ How to Run the Project
1️⃣ Create Database
python schema.py

2️⃣ Load Cleaned CSV
python -m src.services.csv_loader

3️⃣ Run Application
streamlit run src/app.py

🧠 Key Learnings

Role-based system design

Secure authentication handling

Data validation using regex

End-to-end data pipeline

Analytics-driven decision making

Streamlit dashboard design

🎤 Interview-Ready Summary

“This project implements a complete client support management system using Python, MySQL, and Streamlit, with secure authentication, real-time query tracking, and analytics to measure service efficiency and support workload.”

🚀 Future Enhancements

Email / OTP verification

SLA automation

Advanced analytics

Notification system

👤 Author

Bhuvana PS
Domain: Data Engineering / Analytics / Python
