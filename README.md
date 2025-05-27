# privyNet - Secure File Sharing System

privyNet is a secure, client-server based file sharing system featuring role-based access control, two-factor authentication (2FA), and real-time file locking mechanisms. It provides distinct functionalities for 'admin' and 'user' roles, ensuring controlled access and management of files.

## Table of Contents
1.  [Overview](#overview)
2.  [Features](#features)
3.  [Architecture](#architecture)
    *   [Backend Components](#backend-components)
    *   [Frontend Components](#frontend-components)
4.  [Roles and Permissions](#roles-and-permissions)
5.  [Technology Stack](#technology-stack)
6.  [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
    *   [Configuration](#configuration)
    *   [Running the Application](#running-the-application)
7.  [How to Use](#how-to-use)
    *   [Logging In](#logging-in)
    *   [Performing Actions](#performing-actions)
8.  [Project Structure](#project-structure)

## Overview

privyNet allows users to securely store, share, and manage files. Administrators have full control over files and user requests, while regular users can list and read files, and request further operations. The system is built with a Flask backend and a responsive web frontend.

## Features

*   **Authentication:**
    *   Username/password authentication.
    *   **Two-Factor Authentication (2FA)** using TOTP (Time-based One-Time Password) for enhanced security.
    *   **Role-Based Access Control (RBAC):** Distinct 'admin' and 'user' roles.
*   **File Operations:**
    *   **Admin Capabilities:**
        *   Create, Read, Edit, Delete files.
        *   Lock/Unlock files for exclusive access.
        *   List all files with their lock status.
        *   Handle user requests (approve/reject).
        *   View pending requests.
    *   **User Capabilities:**
        *   List available files.
        *   Read files (if not locked for writing).
        *   Make requests for file operations (e.g., create, edit, delete).
*   **File Locking Mechanism:**
    *   Read/Write locks to manage concurrent access.
    *   Prevents data corruption during simultaneous edits.
    *   Lock ownership tracking and display.
*   **Request System:**
    *   Users can request file operations that require admin privileges.
    *   Admins can review, approve, or reject these requests.
    *   Request tracking.
*   **Security:**
    *   Secure 2FA.
    *   RBAC for granular permissions.
    *   File locking.
    *   (Assumed: Secure password handling - not explicitly detailed but implied by 'secure system').
    *   Input validation and session management.

## Architecture

### Backend Components
*   **Web Server (`web_server.py`):**
    *   Main Flask application serving the web interface.
    *   Handles HTTP requests for authentication and file operations.
    *   Implements the file locking mechanism using `threading.Lock` and `threading.RLock`.
    *   Manages user sessions and role-based access.
    *   Provides REST API endpoints.
*   **WebSocket Server (`backend.py` - *as per documentation*):**
    *   Handles real-time communication with clients (e.g., for instant lock status updates).
    *   Manages concurrent access control.
*   **Two-Factor Authentication (`two_fa.py`):**
    *   Implements 2FA using `pyotp` for TOTP.
    *   Provides functions for generating 2FA secrets and verifying OTP codes.
*   **User Configuration (`users.json`):**
    *   Stores user credentials (username, password), roles, and 2FA secrets.
*   **Requests Data (`requests.json`):**
    *   Stores user-submitted file operation requests.
*   **File Storage (`files/` directory):**
    *   Directory where actual files are stored.

### Frontend Components
*   **HTML Interface (`templates/index.html`, `templates/home.html`):**
    *   Responsive web interface built with Tailwind CSS.
    *   Login form with 2FA input.
    *   Role-specific action menus and file operation controls.
    *   Real-time output display area.
*   **Client-side Logic (`static/app.js`):**
    *   Handles user interactions and authentication flow.
    *   Manages file operation commands and requests to the backend.
    *   Provides real-time UI updates (e.g., based on server responses).
*   **Styling (`static/styles.css`, `static/home.css`):**
    *   Custom styling, including a dark theme and responsive design.

## Roles and Permissions

*   **Admin:**
    *   Can perform all file operations: Create, Read, Edit, Delete.
    *   Can Lock and Unlock files.
    *   Can List all files.
    *   Can view and Handle (Approve/Reject) user requests.
*   **User:**
    *   Can List available files.
    *   Can Read files.
    *   Can Make Requests for file operations (Create, Edit, Delete) which admins then review.

## Technology Stack

*   **Backend:**
    *   Python 3
    *   Flask (Web Framework)
    *   PyOTP (For 2FA TOTP generation and verification)
    *   WebSockets (For real-time communication, as per documentation)
*   **Frontend:**
    *   HTML5
    *   CSS3 (Tailwind CSS for utility-first styling)
    *   JavaScript (Vanilla JS for client-side logic)
*   **Data Storage:**
    *   JSON files (`users.json`, `requests.json`) for user data and requests.
    *   Local filesystem for file storage (`files/` directory).

## Getting Started

### Prerequisites
*   Python 3.x
*   pip (Python package installer)
*   A TOTP Authenticator App (e.g., Google Authenticator, Authy, FreeOTP) for 2FA.

### Installation
1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd privyNet
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    Create a `requirements.txt` file with the following content:
    ```txt
    Flask
    pyotp
    qrcode # For generating QR codes if you extend 2FA setup
    # Add 'websockets' if you implement the backend.py functionality
    ```
    Then run:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **User Accounts (`users.json`):**
    The `users.json` file contains predefined user accounts, their passwords, roles, and 2FA secrets.
    ```json
    {
      "admin": {
        "password": "admin123",
        "role": "admin",
        "2fa_secret": "your-secret-key"
      },
      "admin1": {
        "password": "admin1234",
        "role": "admin",
        "2fa_secret": "your-secret-key"
      },
      "user": {
        "password": "user123",
        "role": "user",
        "2fa_secret": "your-secret-key"
      }
    }
    ```
    *   **Setting up 2FA:** To log in with these users, you need to add their `2fa_secret` to your TOTP authenticator app.
        *   Open your authenticator app.
        *   Choose to add a new account.
        *   Select "manual entry" or "enter setup key".
        *   Provide an account name (e.g., "privyNet Admin") and enter the corresponding `2fa_secret` from `users.json`.
        *   Ensure the type is "Time-based (TOTP)".
        *   The app will then generate 6-digit codes that change every 30 seconds.

2.  **Create Directories:**
    Ensure the following directory and file exist in the root of your project:
    *   `files/` (directory for storing uploaded files)
    *   `requests.json` (empty JSON array `[]` if it doesn't exist, for storing user requests)

    You can create them manually or the `web_server.py` script will create them on first run if they don't exist (for `files/` and `requests.json`).

### Running the Application
1.  Start the Flask web server:
    ```bash
    python web_server.py
    ```
2.  Open your web browser and navigate to: `http://127.0.0.1:8000` or `http://localhost:8000`.
    You should see the home page, from which you can navigate to the file system login page (`index.html`).

## How to Use

### Logging In
1.  Navigate to the login page (`index.html`).
2.  Enter the username and password for one of the users defined in `users.json` (e.g., `admin` / `admin123`).
3.  Open your TOTP authenticator app and get the current 6-digit code for the user you are logging in as.
4.  Enter this 2FA code into the "2FA Code" field.
5.  Click "Login".

### Performing Actions
Once logged in, the interface will adapt based on your role:

*   **Select Action:** Choose an action from the dropdown menu (e.g., LIST, CREATE, READ, EDIT, DELETE, MAKE_REQUEST, LIST_REQUESTS, HANDLE_REQUEST).
*   **Filename:** Enter the filename if required by the action.
*   **Content:** Enter file content if creating or editing a file.
*   **Execute:** Click the "Execute" button to perform the action.
*   **Lock/Unlock (Admin only for EDIT):** Admins can lock files before editing to prevent conflicts and unlock them afterward.
*   **Output:** Results of operations, file contents, or error messages will be displayed in the output area.

**Admin Specifics:**
*   **HANDLE_REQUEST:** When selected, you'll be prompted for the Request ID and whether to 'approve' or 'reject'.

**User Specifics:**
*   **MAKE_REQUEST:** When selected, you'll be prompted for the type of request (CREATE, EDIT, DELETE), filename, and content (if applicable).

## Project Structure
privyNet/
├── files/ # Directory where shared files are stored
├── static/
│ ├── app.js # Frontend JavaScript logic
│ ├── styles.css # Custom CSS styles
│ └── home.css # CSS for home page
├── templates/
│ ├── index.html # Main file system interface
│ └── home.html # Home/Landing page
├── two_fa.py # 2FA helper functions
├── users.json # User credentials, roles, and 2FA secrets
├── requests.json # Stores user file operation requests
├── web_server.py # Flask backend application
├── backend.py # WebSocket server (as per documentation)
└── README.md # This file
