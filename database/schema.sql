-- =====================================================
-- Client Query Management System (CQMS)
-- Database Schema created by Bhuvaneswari G
-- =====================================================

CREATE DATABASE IF NOT EXISTS client_query_db;
USE client_query_db;

-- =====================================================
-- USERS TABLE (Client & Support Login)
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    mobile_number VARCHAR(15) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('Client','Support') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- SUPPORT AGENTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS support_agents (
    support_id VARCHAR(20) PRIMARY KEY,
    support_name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    active_status BOOLEAN DEFAULT TRUE
);

-- =====================================================
-- CLIENT QUERIES TABLE
-- =====================================================
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

    CONSTRAINT fk_support
        FOREIGN KEY (assigned_support_id)
        REFERENCES support_agents(support_id)
        ON DELETE SET NULL
);

-- =====================================================
-- CLIENT REVIEWS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS client_reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    query_id VARCHAR(20) NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_review_query
        FOREIGN KEY (query_id)
        REFERENCES client_queries(query_id)
        ON DELETE CASCADE
);

-- =====================================================
-- INDEXES (Performance)
-- =====================================================
CREATE INDEX idx_query_status ON client_queries(status);
CREATE INDEX idx_query_category ON client_queries(category);
CREATE INDEX idx_support_agent ON client_queries(assigned_support_id);
