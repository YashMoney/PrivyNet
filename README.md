# PrivyNet - Secure File Sharing System

**PrivyNet** is a secure, client-server based file sharing system featuring role-based access control, two-factor authentication (2FA), and real-time file locking. It ensures secure, controlled access to files for both administrators and users.

---

## 🧭 Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
   - [Backend Components](#backend-components)
   - [Frontend Components](#frontend-components)
4. [Roles and Permissions](#roles-and-permissions)
5. [Technology Stack](#technology-stack)
6. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Configuration](#configuration)
   - [Running the Application](#running-the-application)
7. [How to Use](#how-to-use)
   - [Logging In](#logging-in)
   - [Performing Actions](#performing-actions)
8. [Project Structure](#project-structure)

---

## 📌 Overview

**PrivyNet** enables secure file storage, access, and management using a Flask-based backend and a responsive frontend. It supports multiple users with different roles and privileges, implementing 2FA and file locking for high security.

---

## ✨ Features

### 🔐 Authentication
- Username/password login.
- **Two-Factor Authentication (2FA)** using TOTP via `pyotp`.
- Role-Based Access Control (**RBAC**).

### 📁 File Operations

#### Admin
- Create, Read, Edit, Delete files.
- Lock/Unlock files.
- View all files and their lock status.
- Handle user requests (Approve/Reject).
- View pending requests.

#### User
- List and read files.
- Request file operations (Create, Edit, Delete).

### 🔒 File Locking Mechanism
- Read/Write locks to manage concurrent access.
- Prevents conflicts and data corruption.
- Lock ownership and status displayed.

### 📥 Request System
- Users submit file operation requests.
- Admins review and handle requests.
- Tracks request history.

### 🔐 Security
- 2FA login with TOTP.
- RBAC for permission control.
- Secure session handling and input validation.

---

## 🏗️ Architecture

### Backend Components
- **`web_server.py`**: Main Flask app, handles API requests, authentication, RBAC, file operations, and locking.
- **`backend.py`**: (Optional) WebSocket server for real-time file status updates.
- **`two_fa.py`**: Generates and verifies 2FA TOTP codes using `pyotp`.
- **`users.json`**: Stores usernames, passwords, roles, and 2FA secrets.
- **`requests.json`**: Stores user requests for file operations.
- **`files/`**: Directory containing all shared files.

### Frontend Components
- **HTML Templates**: `index.html`, `home.html` — UI pages for login and operations.
- **JavaScript**: `app.js` — Handles form submissions, action selection, real-time feedback.
- **CSS**: `styles.css`, `home.css` — Custom styling with Tailwind CSS.

---

## 👥 Roles and Permissions

| Role  | Permissions |
|-------|-------------|
| Admin | Full file access, lock/unlock, request handling |
| User  | View and request file operations |

---

## 🧰 Technology Stack

- **Backend**: Python 3, Flask, pyotp, threading, JSON
- **Frontend**: HTML5, Tailwind CSS, JavaScript (Vanilla)
- **Data Storage**: Local filesystem (`files/`), JSON (`users.json`, `requests.json`)

---

## 🚀 Getting Started

### 📋 Prerequisites
- Python 3.x
- pip
- A TOTP authenticator app (e.g., Google Authenticator, Authy)

### 🔧 Installation

```bash
git clone <your-repository-url>
cd privyNet
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Create requirements.txt:

txt
Copy
Edit
Flask
pyotp
qrcode
# Add websockets if using backend.py
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
⚙️ Configuration
users.json
Define users with passwords, roles, and 2FA secrets:

json
Copy
Edit
{
  "admin": {
    "password": "admin123",
    "role": "admin",
    "2fa_secret": "your-secret-key"
  },
  "user": {
    "password": "user123",
    "role": "user",
    "2fa_secret": "your-secret-key"
  }
}
Set up TOTP:

Open your authenticator app.

Add a new account → Enter 2fa_secret manually.

Choose "Time-based (TOTP)".

Directory Setup
Ensure:

files/ directory exists

requests.json exists (initialize with [] if empty)

🏃 Running the Application
bash
Copy
Edit
python web_server.py
Open your browser:

cpp
Copy
Edit
http://127.0.0.1:8000
📘 How to Use
🔑 Logging In
Go to the login page.

Enter username and password from users.json.

Open your authenticator app and enter the current 6-digit TOTP.

Click “Login”.

🧭 Performing Actions
Depending on your role, you can:

Select action (LIST, CREATE, READ, EDIT, DELETE, MAKE_REQUEST, etc.)

Enter filename and content as required.

Click "Execute" to perform the action.

View results/output area.

Admin Only:
Lock/Unlock files before editing.

Handle user requests (approve/reject by request ID).

User Only:
Submit file operation requests via MAKE_REQUEST.

📁 Project Structure
graphql
Copy
Edit
privyNet/
├── files/              # Directory for stored files
├── static/
│   ├── app.js          # JavaScript logic
│   ├── styles.css      # CSS styles
│   └── home.css        # CSS for home page
├── templates/
│   ├── index.html      # Main interface
│   └── home.html       # Landing page
├── two_fa.py           # TOTP-based 2FA handling
├── users.json          # User credentials and 2FA keys
├── requests.json       # Request log
├── web_server.py       # Main Flask backend
├── backend.py          # WebSocket server (optional)
└── README.md           # Project documentation
