import mysql.connector

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": " ", # Update with your MySQL root password
}

def run_schema():
    try:
        print("🔌 Connecting to MySQL...")
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        print("📦 Creating database...")
        cursor.execute("CREATE DATABASE IF NOT EXISTS cqms_db")
        cursor.execute("USE cqms_db")

        print("👤 Creating users table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            mobile_number VARCHAR(15) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            role ENUM('Client','Support') NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        print("🧑‍💼 Creating support_agents table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_agents (
            support_id VARCHAR(20) PRIMARY KEY,
            support_name VARCHAR(100) NOT NULL,
            email VARCHAR(150),
            active_status BOOLEAN DEFAULT TRUE
        )
        """)

        print("📨 Creating client_queries table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS client_queries (
            query_id VARCHAR(20) PRIMARY KEY,
            client_email VARCHAR(150) NOT NULL,
            client_mobile VARCHAR(15) NOT NULL,
            normalized_mobile VARCHAR(10),
            is_valid_mobile BOOLEAN DEFAULT 1,
            is_valid_email BOOLEAN DEFAULT 1,
            category VARCHAR(50) NOT NULL,
            query_heading VARCHAR(150) NOT NULL,
            query_description TEXT NOT NULL,
            status ENUM('Open','In Progress','Closed') DEFAULT 'Open',
            assigned_support_id VARCHAR(20),
            query_created_time DATETIME NOT NULL,
            query_closed_time DATETIME NULL,
            issue_image_path VARCHAR(255),
            FOREIGN KEY (assigned_support_id)
                REFERENCES support_agents(support_id)
                ON DELETE SET NULL
        )
        """)

        print("⭐ Creating client_reviews table...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS client_reviews (
            review_id INT AUTO_INCREMENT PRIMARY KEY,
            query_id VARCHAR(20) NOT NULL,
            rating INT CHECK (rating BETWEEN 1 AND 5),
            review_text TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (query_id)
                REFERENCES client_queries(query_id)
                ON DELETE CASCADE
        )
        """)

        conn.commit()
        print("✅ Database schema created successfully!")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        cursor.close()
        conn.close()
        print("🔒 MySQL connection closed.")

if __name__ == "__main__":
    run_schema()
