-- Run this in MySQL Workbench first

CREATE DATABASE IF NOT EXISTS portfolio_db;
USE portfolio_db;

-- Hero / About section
CREATE TABLE IF NOT EXISTS hero (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    tagline VARCHAR(255),
    bio TEXT,
    email VARCHAR(100),
    phone VARCHAR(20),
    location VARCHAR(100),
    github_url VARCHAR(255),
    linkedin_url VARCHAR(255),
    leetcode_url VARCHAR(255),
    resume_url VARCHAR(255)
);

-- Education
CREATE TABLE IF NOT EXISTS education (
    id INT PRIMARY KEY AUTO_INCREMENT,
    degree VARCHAR(150) NOT NULL,
    institution VARCHAR(200) NOT NULL,
    year_range VARCHAR(50),
    score VARCHAR(50),
    score_label VARCHAR(20) DEFAULT 'CGPA',
    display_order INT DEFAULT 0
);

-- Skills
CREATE TABLE IF NOT EXISTS skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category VARCHAR(100) NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    display_order INT DEFAULT 0
);

-- Projects
CREATE TABLE IF NOT EXISTS projects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    tech_stack VARCHAR(500),
    github_url VARCHAR(255),
    live_url VARCHAR(255),
    highlight BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0
);

-- Achievements
CREATE TABLE IF NOT EXISTS achievements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    icon VARCHAR(10) DEFAULT '🏆',
    display_order INT DEFAULT 0
);

-- Certifications
CREATE TABLE IF NOT EXISTS certifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    issuer VARCHAR(200),
    year VARCHAR(10),
    url VARCHAR(255)
);

-- Admin credentials
CREATE TABLE IF NOT EXISTS admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- ─── Seed Data ────────────────────────────────────────────────────────────────

INSERT INTO hero (name, tagline, bio, email, phone, location, github_url, linkedin_url, leetcode_url)
VALUES (
    'Patan Jamsheer',
    'AI/ML Engineer · Competitive Programmer · Full-Stack Builder',
    'B.Tech CSE (AI & ML) student at MITS with a passion for building real-world solutions. NPTEL IIT Ropar intern, 250+ LeetCode problems, and multiple coding competition winner. I love turning ideas into scalable products.',
    'jamsheerkhan118@gmail.com',
    '+91 9652403534',
    'Kadiri, Andhra Pradesh',
    'https://github.com/jamsheer',
    'https://linkedin.com/in/jamsheer',
    'https://leetcode.com/jamsheer'
);

INSERT INTO education (degree, institution, year_range, score, score_label, display_order) VALUES
('B.Tech — CSE (AI & ML)', 'Madanapalle Institute of Technology & Science', '2024 – 2028', '8.96', 'CGPA', 1),
('Intermediate (MPC)', 'Sri Chaitanya Junior College, Vijayawada', '2022 – 2024', '96%', 'Score', 2),
('SSC', 'ZPHS Obuladevaracheruvu', '2022', '90%', 'Score', 3);

INSERT INTO skills (category, skill_name, display_order) VALUES
('Languages', 'Python', 1), ('Languages', 'C', 2), ('Languages', 'JavaScript', 3),
('Web', 'Flask', 4), ('Web', 'HTML/CSS', 5), ('Web', 'MERN Stack', 6),
('Database', 'MySQL', 7), ('Database', 'MongoDB', 8),
('AI/ML', 'TensorFlow', 9), ('AI/ML', 'Scikit-learn', 10),
('Tools', 'Git & GitHub', 11), ('Tools', 'VS Code', 12), ('Tools', 'LeetCode 250+', 13);

INSERT INTO projects (title, description, tech_stack, highlight, display_order) VALUES
('Vi-SlideS', 'AI-powered adaptive classroom platform with real-time question submission, Groq AI auto-responses, mood/sentiment analysis, and teacher override. Built for IIT Ropar Vinternship.', 'MERN, TypeScript, Socket.io, Groq API, JWT', TRUE, 1),
('Campus Lost & Found', 'Full-stack platform for MITS 3000+ students with Groq AI smart matching, CampusBot, Cloudinary images, claim/handover system, OTP auth, and admin dashboard.', 'Flask, MySQL, Groq AI, Cloudinary, Brevo', TRUE, 2),
('Cancer Detection System', 'Early cancer detection using ResNet model from HuggingFace. Features image upload, AI prediction with confidence scores, PDF reports, and patient history dashboard.', 'React, Express, Flask, ResNet, MongoDB', FALSE, 3),
('City Transit Planner', 'Hyderabad-inspired transit planner with Bronze→Gold tiers, route search, fare comparison, peak-hour logic, and route history.', 'HTML/CSS/JS, Flask, MySQL', FALSE, 4);

INSERT INTO achievements (title, description, icon, display_order) VALUES
('NPTEL IIT Ropar Internship', 'Selected for competitive NPTEL Winter Internship under Prof. Sudarshan Iyengar with ₹10,000 stipend. Hands-on AI, Python & app development.', '🎓', 1),
('250+ LeetCode Problems', 'Solved 250+ problems across Data Structures, Algorithms, and competitive programming challenges.', '⚡', 2),
('Coding Competition Winner', '1st Prize twice in college-level coding competitions at Technophilia-2K26.', '🥇', 3),
('Top 5% NPTEL', 'Ranked in Top 5% nationally in NPTEL – Joy of Computing using Python.', '📊', 4),
("Engineer's Got Talent Runner-up", 'Runner-up in Engineer''s Got Talent organized by ASCE Student Chapter, MITS.', '🎯', 5);

INSERT INTO certifications (name, issuer, year) VALUES
('Joy of Computing using Python', 'NPTEL – IIT Madras', '2024');

-- Default admin: username=admin, password=admin123 (change after setup!)
-- Using SHA2 hash: SELECT SHA2('admin123', 256);
INSERT INTO admin (username, password_hash) VALUES
('admin', SHA2('admin123', 256));




USE portfolio_db;

INSERT INTO admin (username, password_hash) 
VALUES ('admin', SHA2('admin123', 256))
ON DUPLICATE KEY UPDATE password_hash = SHA2('admin123', 256);