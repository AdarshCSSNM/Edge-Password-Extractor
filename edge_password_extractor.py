import os
import shutil
import sqlite3
import json
import base64
import win32crypt
from Crypto.Cipher import AES
import getpass

ascii_art = r"""                          
Developed by Adarsh Poojary
Email: adarshmsg11@gmail.com
LinkedIn: https://www.linkedin.com/in/adarsh-poojary-8a2526275/
"""

def get_edge_profile_path():
    """Get the path to Edge's user data directory"""
    app_data = os.getenv('LOCALAPPDATA')
    edge_path = os.path.join(app_data, 'Microsoft', 'Edge', 'User  Data')
    return edge_path

def get_encryption_key():
    """Retrieve the encryption key from Edge's Local State file"""
    local_state_path = os.path.join(get_edge_profile_path(), 'Local State')
    try:
        with open(local_state_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
        
        # Extract the encrypted key
        encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        # Remove 'DPAPI' prefix
        encrypted_key = encrypted_key[5:]
        # Decrypt using Windows DPAPI
        key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return key
    except Exception as e:
        print(f"Error retrieving encryption key: {e}")
        return None

def decrypt_password(password, key):
    """Decrypt the password using the provided key"""
    try:
        # Check if password is DPAPI encrypted (older Edge versions) or AES encrypted
        if password.startswith(b'v10') or password.startswith(b'v11'):
            # AES encryption (Chromium-based Edge)
            iv = password[3:15]  # Initialization vector
            encrypted_password = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt(encrypted_password)[:-16].decode('utf-8')
            return decrypted
        else:
            # DPAPI encryption (legacy Edge)
            decrypted = win32crypt.CryptUnprotectData(password, None, None, None, 0)[1].decode('utf-8')
            return decrypted
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return ""

def extract_passwords(output_file="edge_passwords.txt"):
    """Extract all stored passwords from Microsoft Edge"""
    edge_path = get_edge_profile_path()
    db_path = os.path.join(edge_path, 'Default', 'Login Data')
    temp_db = 'temp_login_data.db'

    if not os.path.exists(db_path):
        print("Edge password database not found. Ensure Edge is installed and has saved passwords.")
        return

    # Copy the database to avoid locking issues
    shutil.copyfile(db_path, temp_db)

    try:
        # Connect to the database
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Query the logins table
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        rows = cursor.fetchall()

        if not rows:
            print("No passwords found in Edge.")
            return

        # Get the decryption key
        key = get_encryption_key()
        if not key:
            print("Failed to retrieve decryption key.")
            return

        # Extract and decrypt passwords
        passwords = []
        for row in rows:
            url, username, encrypted_password = row
            if username and encrypted_password:
                password = decrypt_password(encrypted_password, key)
                if password:
                    passwords.append((url, username, password))

        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("URL | Username | Password\n")
            f.write("-" * 50 + "\n")
            for url, username, password in passwords:
                f.write(f"{url} | {username} | {password}\n")
        
        print(f"Extracted {len(passwords)} passwords and saved to {output_file}")
        
        # Print to console
        for url, username, password in passwords:
            print(f"URL: {url}\nUsername: {username}\nPassword: {password}\n{'-'*50}")

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Clean up
        conn.close()
        if os.path.exists(temp_db):
            os.remove(temp_db)

def main():
    print(ascii_art)  # Display the ASCII art
    print("Microsoft Edge Password Extractor")
    print("This script will extract all passwords stored in Edge.")
    print("Note: You must run this on the same Windows account where passwords are saved.")
    
    # Verify user is ready
    if input("Continue? (y/n): ").lower() != 'y':
        print("Aborted.")
        return
    
    output_file = "edge_passwords.txt"
    extract_passwords(output_file)

if __name__ == "__main__":
    main()