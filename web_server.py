# web_server.py
from flask import Flask, send_from_directory, request, jsonify
import json
import os
from threading import Lock, RLock
from collections import defaultdict
from two_fa import verify_otp

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load users with roles from JSON
with open('users.json', 'r') as f:
    USERS = json.load(f)

# Ensure files directory exists
FILES_DIR = 'files'
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

# File locking mechanism
file_locks = {}  # Dictionary to store file locks
readers_count = defaultdict(int)  # Count of readers per file
lock_manager = RLock()  # Global lock for managing reader/writer access

def acquire_read_lock(filename, username):
    with lock_manager:
        if filename in file_locks and file_locks[filename]['type'] == 'write':
            return False, f"File is being edited by {file_locks[filename]['user']}"
        readers_count[filename] += 1
        return True, None

def release_read_lock(filename):
    with lock_manager:
        if readers_count[filename] > 0:
            readers_count[filename] -= 1
        if readers_count[filename] == 0:
            readers_count.pop(filename, None)

def acquire_write_lock(filename, username):
    with lock_manager:
        if filename in file_locks:
            return False, f"File is locked by {file_locks[filename]['user']}"
        if readers_count.get(filename, 0) > 0:
            return False, f"File is currently being read by {readers_count[filename]} users"
        file_locks[filename] = {'type': 'write', 'user': username}
        return True, None

def release_write_lock(filename, username):
    with lock_manager:
        if filename in file_locks and file_locks[filename]['user'] == username:
            del file_locks[filename]
            return True
        return False

@app.route('/')
def home():
    return send_from_directory('templates', 'home.html')

@app.route('/home.html')
def index():
    return send_from_directory('templates', 'home.html')

@app.route('/index.html')
def file():
    return send_from_directory('templates', 'index.html')

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    otp_input = data.get('otp') # <-- FIX: Get OTP, might be None or empty

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password required"}), 400

    user_data = USERS.get(username)

    if user_data and user_data["password"] == password:
        # Since all users in users.json have a 2fa_secret, 2FA is effectively mandatory.
        if "2fa_secret" in user_data and user_data["2fa_secret"]: # Check if secret exists
            if not otp_input: # OTP must be provided if 2FA is configured
                return jsonify({
                    "status": "error",
                    "message": "OTP required"
                }), 401 

            if not verify_otp(user_data["2fa_secret"], otp_input):
                return jsonify({
                    "status": "error",
                    "message": "Invalid OTP"
                }), 401
            
            # If OTP is valid, or if 2FA wasn't configured (though it is for all current users)
            return jsonify({
                "status": "success",
                "role": user_data["role"]
            })
        else:
            # Fallback for users without 2FA (not applicable with current users.json but good practice)
            return jsonify({
                "status": "success",
                "role": user_data["role"]
            })
    
    return jsonify({
        "status": "error",
        "message": "Invalid credentials"
    }), 401

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    command = data.get('command', '')
    username = data.get('username', '')
    role = data.get('role', '')
    
    if not command:
        return jsonify({"status": "error", "message": "No command provided"})
        
    parts = command.split("::")
    action = parts[0]
    
    try:
        if action == "LOCK" and role == "admin":
            if len(parts) < 2:
                return jsonify({"status": "error", "message": "Filename required"})
            filename = parts[1]
            
            success, message = acquire_write_lock(filename, username)
            if success:
                return jsonify({"status": "success", "message": f"File {filename} locked"})
            return jsonify({"status": "error", "message": message})
            
        elif action == "UNLOCK" and role == "admin":
            if len(parts) < 2:
                return jsonify({"status": "error", "message": "Filename required"})
            filename = parts[1]
            
            if release_write_lock(filename, username):
                return jsonify({"status": "success", "message": f"File {filename} unlocked"})
            return jsonify({"status": "error", "message": "You don't have the lock for this file"})
            
        elif action == "LIST":
            files = [f for f in os.listdir(FILES_DIR) 
                    if os.path.isfile(os.path.join(FILES_DIR, f))]
            # Include lock information in response
            lock_info = {
                'files': files,
                'locked_files': {
                    filename: {
                        'type': info['type'],
                        'user': info['user']
                    } for filename, info in file_locks.items()
                },
                'readers': {
                    filename: count for filename, count in readers_count.items() if count > 0
                }
            }
            return jsonify({"status": "success", **lock_info})
            
        elif action == "READ":
            if len(parts) < 2:
                return jsonify({"status": "error", "message": "Filename required"})
            filename = parts[1]
            file_path = os.path.join(FILES_DIR, filename)
            
            if not os.path.exists(file_path):
                return jsonify({"status": "error", "message": "File not found"})
            
            if filename in file_locks:
                return jsonify({"status": "error", "message": f"File is locked by {file_locks[filename]['user']}"})
                
            success, message = acquire_read_lock(filename, username)
            if not success:
                return jsonify({"status": "error", "message": message})
                
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                return jsonify({"status": "success", "content": content})
            finally:
                release_read_lock(filename)
            
        elif action == "CREATE" and role == "admin":
            if len(parts) < 3:
                return jsonify({"status": "error", "message": "Filename and content required"})
            filename = parts[1]
            content = parts[2]
            file_path = os.path.join(FILES_DIR, filename)
            
            if os.path.exists(file_path):
                return jsonify({"status": "error", "message": "File already exists"})
            
            if filename in file_locks:
                return jsonify({"status": "error", "message": f"File is locked by {file_locks[filename]['user']}"})
                
            success, message = acquire_write_lock(filename, username)
            if not success:
                return jsonify({"status": "error", "message": message})
                
            try:
                with open(file_path, 'w') as f:
                    f.write(content)
                return jsonify({"status": "success", "message": f"File {filename} created"})
            finally:
                release_write_lock(filename, username)
            
        elif action == "EDIT" and role == "admin":
            if len(parts) < 3:
                return jsonify({"status": "error", "message": "Filename and content required"})
            filename = parts[1]
            content = parts[2]
            file_path = os.path.join(FILES_DIR, filename)
            
            if not os.path.exists(file_path):
                return jsonify({"status": "error", "message": "File not found"})
            
            if filename in file_locks and file_locks[filename]['user'] != username:
                return jsonify({"status": "error", "message": f"File is locked by {file_locks[filename]['user']}"})
            
            if filename not in file_locks:
                success, message = acquire_write_lock(filename, username)
                if not success:
                    return jsonify({"status": "error", "message": message})
                
            try:
                with open(file_path, 'w') as f:
                    f.write(content)
                return jsonify({"status": "success", "message": f"File {filename} updated"})
            finally:
                if filename not in file_locks: # Only release if newly acquired in this block
                    release_write_lock(filename, username)
            
        elif action == "DELETE" and role == "admin":
            if len(parts) < 2:
                return jsonify({"status": "error", "message": "Filename required"})
            filename = parts[1]
            file_path = os.path.join(FILES_DIR, filename)
            
            if not os.path.exists(file_path):
                return jsonify({"status": "error", "message": "File not found"})
            
            if filename in file_locks:
                return jsonify({"status": "error", "message": f"File is locked by {file_locks[filename]['user']}"})
                
            success, message = acquire_write_lock(filename, username)
            if not success:
                return jsonify({"status": "error", "message": message})
                
            try:
                os.remove(file_path)
                return jsonify({"status": "success", "message": f"File {filename} deleted"})
            finally:
                release_write_lock(filename, username)
            
        elif action == "MAKE_REQUEST" and role == "user":
            if len(parts) < 4: # MAKE_REQUEST::TYPE::FILENAME::CONTENT (content optional for delete)
                if len(parts) == 3 and parts[1] == "DELETE": # MAKE_REQUEST::DELETE::FILENAME
                     pass # Allow this format for delete
                else:
                    return jsonify({"status": "error", "message": "Invalid request format"})

            request_type = parts[1]
            filename = parts[2]
            content = parts[3] if len(parts) > 3 else "" # Content is empty if not provided
            
            requests_file = 'requests.json'
            requests_data = []
            if os.path.exists(requests_file):
                with open(requests_file, 'r') as f:
                    try:
                        requests_data = json.load(f)
                    except json.JSONDecodeError:
                        requests_data = [] # Handle empty or corrupted file
            
            new_request = {
                "id": len(requests_data) + 1,
                "username": username,
                "type": request_type,
                "filename": filename,
                "content": content,
                "status": "pending"
            }
            requests_data.append(new_request)
            
            with open(requests_file, 'w') as f:
                json.dump(requests_data, f, indent=2)
            
            return jsonify({"status": "success", "message": f"Request #{new_request['id']} submitted"})
            
        elif action == "LIST_REQUESTS" and role == "admin":
            if not os.path.exists('requests.json'):
                return jsonify({"status": "success", "requests": []})
            with open('requests.json', 'r') as f:
                try:
                    requests_data = json.load(f)
                except json.JSONDecodeError:
                    requests_data = [] # Handle empty or corrupted file
            return jsonify({"status": "success", "requests": requests_data})
            
        elif action == "HANDLE_REQUEST" and role == "admin":
            if len(parts) < 3:
                return jsonify({"status": "error", "message": "Request ID and decision required"})
            try:
                request_id = int(parts[1])
            except ValueError:
                 return jsonify({"status": "error", "message": "Invalid Request ID format"})
            decision = parts[2].lower() # 'approve' or 'reject'
            
            if decision not in ['approve', 'reject']:
                return jsonify({"status": "error", "message": "Decision must be 'approve' or 'reject'"})

            if not os.path.exists('requests.json'):
                return jsonify({"status": "error", "message": "No requests found"})
                
            with open('requests.json', 'r') as f:
                try:
                    requests_data = json.load(f)
                except json.JSONDecodeError:
                    return jsonify({"status": "error", "message": "Requests file is corrupted"})

            request_found = False
            for req in requests_data:
                if req['id'] == request_id:
                    request_found = True
                    if req['status'] != 'pending':
                        return jsonify({"status": "error", "message": f"Request #{request_id} has already been processed."})
                    
                    req['status'] = 'approved' if decision == 'approve' else 'rejected'
                    
                    if decision == 'approve':
                        file_path = os.path.join(FILES_DIR, req['filename'])
                        # Admin should ideally lock the file before operations
                        # For simplicity, direct operation is shown as per original logic
                        if req['type'] == 'CREATE':
                            with open(file_path, 'w') as f:
                                f.write(req['content'])
                        elif req['type'] == 'EDIT':
                             if not os.path.exists(file_path):
                                return jsonify({"status": "error", "message": f"File {req['filename']} not found for editing."})
                             with open(file_path, 'w') as f:
                                f.write(req['content'])
                        elif req['type'] == 'DELETE':
                            if os.path.exists(file_path):
                                os.remove(file_path)
                            else:
                                # If file doesn't exist, request is still "approved" as action is done
                                pass 
                    break
            
            if not request_found:
                return jsonify({"status": "error", "message": f"Request ID #{request_id} not found."})

            with open('requests.json', 'w') as f:
                json.dump(requests_data, f, indent=2)
            
            return jsonify({
                "status": "success", 
                "message": f"Request #{request_id} {req['status']}" # Use the updated status
            })
            
        return jsonify({"status": "error", "message": "Invalid command or insufficient permissions"})
        
    except Exception as e:
        app.logger.error(f"Error processing command: {e}", exc_info=True) # Log error for debugging
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    if not os.path.exists('requests.json'):
        with open('requests.json', 'w') as f:
            json.dump([], f)
    app.run(host='192.168.16.147', port=8000, debug=True)