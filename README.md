privyNet - Secure File Sharing System
privyNet is a secure, client-server-based file sharing system designed for controlled file management with role-based access control (RBAC), two-factor authentication (2FA), and real-time file locking. It provides distinct functionalities for admin and user roles, ensuring secure and efficient file operations.
Table of Contents

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

Overview
privyNet enables secure file storage, sharing, and management through a Flask-based backend and a responsive web frontend. Administrators have full control over files and user requests, while users can perform limited operations and submit requests for admin approval. The system ensures security with 2FA, role-based permissions, and file locking to prevent concurrent access issues.
Features

Authentication:
Username/password-based login.
Two-Factor Authentication (2FA) using Time-based One-Time Password (TOTP).
Role-Based Access Control (RBAC) with distinct admin and user roles.


File Operations:
Admins: Create, read, edit, delete, lock/unlock files, and manage user requests.
Users: List and read files, submit requests for create/edit/delete operations.


File Locking:
Read/write locks to prevent data corruption during concurrent access.
Lock ownership tracking and real-time status updates.


Request System:
Users can submit file operation requests for admin approval.
Admins can view, approve, or reject requests.


Security:
Secure 2FA with TOTP.
RBAC for granular permissions.
Input validation and secure session management.



Architecture
Backend Components

Web Server (web_server.py):
Flask application handling HTTP requests for authentication and file operations.
Implements file locking using threading.Lock and threading.RLock.
Manages user sessions and provides REST API endpoints.


WebSocket Server (backend.py):
Facilitates real-time communication for lock status updates and concurrent access control.


Two-Factor Authentication (two_fa.py):
Uses pyotp for TOTP-based 2FA secret generation and verification.


Data Storage:
users.json: Stores user credentials, roles, and 2FA secrets.
requests.json: Tracks user-submitted file operation requests.
files/ directory: Stores uploaded files.



Frontend Components

HTML Interface (templates/index.html, templates/home.html):
Responsive web interface styled with Tailwind CSS.
Includes login forms with 2FA and role-specific dashboards.


Client-Side Logic (static/app.js):
Manages user interactions, authentication flows, and API requests.
Updates UI in real-time based on server responses.


Styling (static/styles.css, static/home.css):
Custom CSS with a dark theme and responsive design.



Roles and Permissions



Role
Permissions



Admin
Create, read, edit, delete files; lock/unlock files; manage user requests.


User
List and read files; submit requests for create/edit/delete operations.


Technology Stack

Backend:
Python 3
Flask (Web Framework)
PyOTP (2FA with TOTP)
WebSockets (Real-time communication)


Frontend:
HTML5
CSS3 (Tailwind CSS)
JavaScript (Vanilla JS)


Storage:
JSON files (users.json, requests.json)
Local filesystem (files/ directory)



Getting Started
Prerequisites

Python 3.8+
pip (Python package installer)
A TOTP authenticator app (e.g., Google Authenticator, Authy, FreeOTP)

Installation

Clone the Repository:git clone https://github.com/your-username/privyNet.git
cd privyNet


Set Up a Virtual Environment (recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:Create a requirements.txt file:Flask
pyotp
qrcode
websockets

Then run:pip install -r requirements.txt



Configuration

User Accounts (users.json):Configure user credentials, roles, and 2FA secrets in users.json:
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
Open your TOTP authenticator app.
Add a new account using the 2fa_secret from users.json.
Select "Time-based (TOTP)" and name the account (e.g., "privyNet Admin").
The app will generate 6-digit codes every 30 seconds.




Create Directories and Files:Ensure the following exist:

files/ directory (for file storage)
requests.json (initialize with [] if not present)These will be created automatically on first run if missing.



Running the Application

Start the Flask server:python web_server.py


Open a browser and navigate to http://localhost:8000.
You’ll see the home page (home.html) with a link to the file system interface (index.html).



Usage
Logging In

Navigate to the login page (index.html).
Enter a username and password from users.json (e.g., admin/admin123).
Retrieve the current 6-digit 2FA code from your authenticator app.
Enter the 2FA code and click "Login".

Performing Actions

Interface: After login, a role-specific dashboard appears with a dropdown menu for actions (e.g., LIST, CREATE, READ, EDIT, DELETE, MAKE_REQUEST, LIST_REQUESTS, HANDLE_REQUEST).
Steps:
Select an action.
Enter the filename and/or content (if required).
Click "Execute" to perform the action.
View results or error messages in the output area.


Admin Actions:
Lock/unlock files before editing.
Approve/reject user requests using the request ID.


User Actions:
Submit requests for file operations (CREATE, EDIT, DELETE).



Project Structure
privyNet/
├── files/               # Directory for stored files
├── static/              # Frontend static assets
│   ├── app.js           # Client-side JavaScript logic
│   ├── styles.css      # Custom CSS styles
│   └── home.css        # Home page styles
├── templates/           # HTML templates
│   ├── index.html      # File system interface
│   └── home.html       # Landing page
├── two_fa.py           # 2FA helper functions
├── users.json          # User credentials and 2FA secrets
├── requests.json       # User file operation requests
├── web_server.py       # Flask backend server
├── backend.py          # WebSocket server
└── README.md           # Project documentation

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
