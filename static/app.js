// static/app.js

let currentRole = null;
let currentUsername = null;

// Function to format lock information
function formatLockInfo(files, lockedFiles, readers) {
    let output = [];
    
    output.push('Files:');
    files.forEach(file => {
        let status = [];
        if (lockedFiles[file]) {
            status.push(`[Locked for ${lockedFiles[file].type} by ${lockedFiles[file].user}]`);
        }
        if (readers[file]) {
            status.push(`[Being read by ${readers[file]} users]`);
        }
        output.push(`- ${file} ${status.length ? status.join(' ') : ''}`);
    });
    
    return output.join('\n');
}

// Function to toggle input fields based on selected action
function toggleInputFields(action) {
    const filenameInput = document.getElementById('filename');
    const contentInput = document.getElementById('content');
    const lockButtons = document.getElementById('lockButtons');
    
    filenameInput.style.display = (action === 'LIST' || action === 'LIST_REQUESTS') ? 'none' : 'block';
    contentInput.style.display = (action === 'CREATE' || action === 'EDIT') ? 'block' : 'none';
    lockButtons.style.display = (action === 'EDIT' && currentRole === 'admin') ? 'block' : 'none';
}

// Function to send command to server
async function sendCommand() {
    const action = document.getElementById('action').value;
    const filename = document.getElementById('filename').value;
    const content = document.getElementById('content').value;
    
    let command = action;
    if (filename) command += `::${filename}`;
    if (content) command += `::${content}`;
    
    try {
        const response = await fetch('/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                command: command,
                username: currentUsername,
                role: currentRole
            })
        });
        
        const data = await response.json();
        const output = document.getElementById('output');
        
        if (data.status === 'success') {
            if (data.files) {
                output.value = formatLockInfo(data.files, data.locked_files || {}, data.readers || {});
            } else {
                output.value = data.message || 'Command executed successfully';
            }
        } else {
            output.value = `Error: ${data.message}`;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('output').value = `Error: ${error.message}`;
    }
}

// Function to lock/unlock file
async function toggleLock(action) {
    const filename = document.getElementById('filename').value;
    if (!filename) {
        document.getElementById('output').value = 'Error: Please enter a filename';
        return;
    }

    const command = `${action}::${filename}`;
    try {
        const response = await fetch('/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                command: command,
                username: currentUsername,
                role: currentRole
            })
        });
        
        const data = await response.json();
        const output = document.getElementById('output');
        output.value = data.message || (data.status === 'success' ? 'Command executed successfully' : 'Operation failed');
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('output').value = `Error: ${error.message}`;
    }
}



// Event listeners
document.getElementById('action').addEventListener('change', function() {
    toggleInputFields(this.value);
});

document.getElementById('login-btn').addEventListener('click', async () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const otp = document.getElementById('otp').value; // <-- FIX: Get OTP value

    if (!username || !password) {
        alert('Username and password are required.');
        document.getElementById('output').textContent = 'Username and password are required.';
        return;
    }
    // OTP field can be empty if user hasn't entered it yet, server will validate if it's required.

    try {
        const response = await fetch('/auth', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password, otp }) // <-- FIX: Send OTP
        });
        const result = await response.json();
        if (result.status === 'success') {
            currentRole = result.role;
            currentUsername = username;
            document.getElementById('txt').textContent = 'File Management System';
            document.getElementById('nb').style.display = 'block';
            document.getElementById('login-section').classList.add('hidden');
            document.getElementById('main-section').classList.remove('hidden');
            document.getElementById(result.role === 'admin' ? 'admin-controls' : 'user-controls').classList.remove('hidden');
            if(result.role === 'user') {
                document.getElementById('lockButtons').classList.add('hidden');
            }
            else if(result.role === 'admin') {
                document.getElementById('lockButtons').classList.remove('hidden');
            }
            document.getElementById('output').textContent = `Logged in as ${result.role}`;
            executeCommand('LIST');
        } else {
            // Use server message for more specific feedback
            alert(result.message || 'Authentication failed'); 
            document.getElementById('output').textContent = result.message || 'Authentication failed';
        }
    } catch (error) {
        alert('Login request failed: ' + error.message);
        document.getElementById('output').textContent = 'Error: ' + error.message;
    }
});

async function executeCommand(action, filename = '', content = '') {
    try {
        let command = action;
        
        if (action === 'CREATE' || action === 'EDIT') {
            command = `${action}::${filename}::${content}`;
        } else if (action === 'READ' || action === 'DELETE') {
            command = `${action}::${filename}`;
        } else if (action === 'MAKE_REQUEST') {
            const requestAction = prompt('Enter request action (CREATE/EDIT/DELETE):');
            if (!requestAction) return;
            
            if (requestAction === 'CREATE' || requestAction === 'EDIT') {
                command = `${action}::${requestAction}::${filename}::${content}`;
            } else if (requestAction === 'DELETE') {
                command = `${action}::${requestAction}::${filename}`;
            } else {
                document.getElementById('output').textContent = 'Invalid request action';
                return;
            }
        } else if (action === 'HANDLE_REQUEST') {
            const requestId = prompt('Enter request ID:');
            if (!requestId) return;
            
            const approve = confirm('Approve request?');
            command = `${action}::${requestId}::${approve ? 'approve' : 'reject'}`;
        }

        const response = await fetch('/command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                command,
                username: currentUsername,
                role: currentRole
            })
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            if (action === 'LIST') {
                document.getElementById('output').textContent = formatLockInfo(
                    result.files,
                    result.locked_files || {},
                    result.readers || {}
                );
            } else if (action === 'READ') {
                document.getElementById('output').textContent = result.content;
            } else if (action === 'LIST_REQUESTS') {
                document.getElementById('output').textContent = JSON.stringify(result.requests, null, 2);
            } else {
                document.getElementById('output').textContent = result.message;
                if (['CREATE', 'EDIT', 'DELETE'].includes(action)) {
                    executeCommand('LIST');
                }
            }
        } else {
            document.getElementById('output').textContent = result.message || 'Operation failed';
        }
    } catch (error) {
        document.getElementById('output').textContent = 'Error: ' + error.message;
    }
}

document.getElementById('execute-btn').addEventListener('click', async () => {
    const action = currentRole === 'admin' ? 
        document.getElementById('action').value : 
        document.getElementById('user-action').value;
    const filename = document.getElementById('filename').value;
    const content = document.getElementById('content').value;
    
    if (!action) {
        document.getElementById('output').textContent = 'Please select an action';
        return;
    }
    
    if ((action === 'CREATE' || action === 'EDIT' || action === 'READ' || action === 'DELETE') && !filename) {
        document.getElementById('output').textContent = 'Please enter a filename';
        return;
    }
    
    if ((action === 'CREATE' || action === 'EDIT') && !content) {
        document.getElementById('output').textContent = 'Please enter content';
        return;
    }
    
    await executeCommand(action, filename, content);
});

document.getElementById('logout-btn').addEventListener('click', () => {
    currentRole = null;
    currentUsername = null;
    document.getElementById('txt').textContent = 'Sign in your account';
    document.getElementById('nb').style.display = 'none';
    document.getElementById('output').textContent = 'Logged out successfully';
    document.getElementById('main-section').classList.add('hidden');
    document.getElementById('admin-controls').classList.add('hidden');
    document.getElementById('user-controls').classList.add('hidden');
    document.getElementById('login-section').classList.remove('hidden');
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('otp').value = ''; // Clear OTP field on logout
});