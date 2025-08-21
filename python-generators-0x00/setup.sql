-- Sql Set up

-- Create the database
CREATE DATABASE IF NOT EXISTS ALX_prodev;


-- Create the user_data Table
CREATE TABLE IF NOT EXISTS user_data (
    user_id CHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    age DECIMAL NOT NULL
);