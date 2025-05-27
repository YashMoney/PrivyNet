privyNet 🔒 Secure File Sharing System

privyNet is a secure, client-server file sharing system with role-based access control (RBAC), two-factor authentication (2FA), and real-time file locking. It offers distinct functionalities for admin and user roles, ensuring secure file management through a Flask backend and a responsive web frontend.
📋 Table of Contents

Overview
Features
Architecture
Backend Components
Frontend Components


Roles and Permissions
Technology Stack
Getting Started
Prerequisites
Installation
Configuration
Running the Application


Usage
Logging In
Performing Actions


Project Structure
Contributing
License

🌟 Overview
privyNet enables secure file storage, sharing, and management. Admins have full control over files and user requests, while users can list/read files and submit requests for admin approval. The system emphasizes security with 2FA, RBAC, and file locking to prevent concurrent access issues.
✨ Features

Authentication:
Username/password login with TOTP-based 2FA 🔐
Role-Based Access Control (RBAC) for admins and users


File Operations:
Admins: Create, read, edit, delete, lock/unlock files, manage requests
Users: List/read files, request create/edit/delete operations


File Locking:
Read/write locks to prevent data corruption
Real-time lock status updates via WebSocket


Request System:
Users submit file operation requests for admin approval
Admins can approve/reject requests


Security:
Secure 2FA, RBAC, input validation, and session management



🏛 Architecture
Backend Components

Web Server (web_server.py): Flask app handling HTTP requests, file locking (threading.Lock/RLock), sessions, and REST APIs.
WebSocket Server (backend.py): Real-time communication for lock status and concurrent access.
2FA (two_fa.py): TOTP-based 2FA using pyotp.
Storage:
users.json: User credentials, roles, 2FA secrets
requests.json: User request tracking
files/ directory: File storage



Frontend Components

HTML (templates/index.html, templates/home.html): Responsive interface with Tailwind CSS.
JavaScript (static/app.js): Handles user interactions, API requests, and real-time UI updates.
Styling (static/styles.css, static/home.css): Dark theme, responsive design.

👥 Roles and Permissions



Role
Permissions



Admin
Create, read, edit, delete, lock/unlock files; manage user requests.


User
List/read files; request create/edit/delete operations.


🛠 Technology Stack

Backend: Python 3, Flask, PyOTP, WebSockets
Frontend: HTML5, CSS3 (Tailwind CSS), Vanilla JavaScript
Storage: JSON files (users.json, requests.json), local filesystem (files/)

🚀 Getting Started
Prerequisites

🐍 Python 3.8+
📦 pip (Python package installer)
📱 TOTP authenticator app (e.g., Google Authenticator, Authy, FreeOTP)

Installation

Clone the Repository:git clone https://github.com/your-username/privyNet.git
cd privyNet


Set Up Virtual Environment:python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


Install Dependencies:Create requirements.txt:Flask
pyotp
qrcode
websockets

Install:pip install -r requirements.txt



Configuration

User Accounts (users.json):
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


Set Up 2FA:
Open your TOTP app and add a new account.
Enter the 2fa_secret from users.json (e.g., "your-secret-key").
Select "Time-based (TOTP)" and name it (e.g., "privyNet Admin").
Codes refresh every 30 seconds.




Create Storage:

files/ directory (auto-created if missing)
requests.json: Initialize with [] (auto-created if missing)



Running the Application

Start the Flask server:python web_server.py


Open http://localhost:8000 in your browser to access the home page.

📖 Usage
Logging In

Go to the login page (index.html).
Enter username/password (e.g., admin/admin123).
Input the 6-digit 2FA code from your authenticator app.
Click "Login".

Performing Actions

Interface: Role-specific dashboard with action dropdown (LIST, CREATE, READ, EDIT, DELETE, MAKE_REQUEST, LIST_REQUESTS, HANDLE_REQUEST).
Steps:
Select an action.
Provide filename/content if needed.
Click "Execute".
View results in the output area.


Admin Actions:
Lock/unlock files for editing.
Approve/reject requests using request IDs.


User Actions:
Submit requests for file operations.



📂 Project Structure
privyNet/
├── files/               # Stored files
├── static/              # Frontend assets
│   ├── app.js           # Client-side logic
│   ├── styles.css      # Custom styles
│   └── home.css        # Home page styles
├── templates/           # HTML templates
│   ├── index.html      # File system interface
│   └── home.html       # Landing page
├── two_fa.py           # 2FA functions
├── users.json          # User data
├── requests.json       # User requests
├── web_server.py       # Flask server
├── backend.py          # WebSocket server
└── README.md           # Documentation

🤝 Contributing

Fork the repository.
Create a feature branch: git checkout -b feature/your-feature
Commit changes: git commit -m "Add your feature"
Push: git push origin feature/your-feature
Open a pull request.

📜 License
This project is licensed under the MIT License.
