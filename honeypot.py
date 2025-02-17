import socket
import threading
import sqlite3
import paramiko
paramiko.util.log_to_file("paramiko_debug.log")  

# Database file
DB_FILE = "honeypot_logs.db"

# SSH Server Configuration
HOST = "0.0.0.0"
PORT = 2222

# Generate SSH Host Key (for authentication)
HOST_KEY = paramiko.RSAKey.generate(2048)

# Initialize Database
def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS attack_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            username TEXT,
            password TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Log Failed Login Attempt
def log_attempt(ip, username, password):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO attack_logs (ip_address, username, password) VALUES (?, ?, ?)", 
                (ip, username, password))
    conn.commit()
    conn.close()
    print(f"📌 Logged: {ip} | {username} | {password}")

# SSH Server Handler
class FakeSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        log_attempt(self.client_ip, username, password)
        return paramiko.AUTH_FAILED

# Handle SSH Connection
def handle_client(client, addr):
    print(f"🔗 Connection from: {addr[0]}")
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(HOST_KEY)
        server = FakeSSHServer(addr[0])

        transport.start_server(server=server)

        # Wait for client to authenticate
        channel = transport.accept(20)
        if channel is None:
            print(f"⚠ SSH handshake failed or client {addr[0]} disconnected early.")
            transport.close()  # Ensure transport closes
            return
        
        print(f"✅ SSH session established with {addr[0]}")
        channel.send("Welcome to the SSH Honeypot!\n")
        channel.close()

    except paramiko.SSHException as e:
        print(f"❌ SSH error from {addr[0]}: {e}")
    except EOFError:
        print(f"⚠ Client {addr[0]} closed connection unexpectedly.")
    except OSError as e:
        print(f"⚠ Socket error from {addr[0]}: {e}")
    except Exception as e:
        print(f"❌ Unexpected error from {addr[0]}: {e}")
    finally:
        transport.close()  # Ensure transport closes cleanly
        client.close()

# Start Honeypot
def start_honeypot():
    initialize_database()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(100)

    print(f"🚀 Honeypot running on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()

if __name__ == "__main__":
    start_honeypot()
