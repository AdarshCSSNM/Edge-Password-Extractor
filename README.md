# Edge Password Extractor

A Python script to extract and decrypt passwords from Microsoft Edge on Windows systems.

## 📦 Requirements
- Python 3.6+
- Windows OS
- Microsoft Edge installed
- Administrator privileges

## ⚙️ Installation
1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install required packages:
```bash
pip install pycryptodome pywin32
```

3. Download the script:
```bash
git clone https://github.com/yourusername/edge-password-extractor.git
cd edge-password-extractor
```

## 🚀 Usage
Run with administrator privileges:
```bash
python edge_password_extractor.py
```

Sample output:
```
Decrypted Passwords:

1. URL: https://example.com
   Username: user@example.com
   Password: mySecurePassword123

[+] Results saved to C:\path\to\edge_passwords_20231025_143022.json
```

## 📝 Features
- Extracts passwords from Edge's encrypted database
- Automatically retrieves decryption key
- Generates timestamped JSON output
- Copies database to avoid locking issues
- Clean console presentation

## ⚠️ Important Notes
- Requires Windows and Microsoft Edge
- Must run as Administrator
- Only works for the current user account
- Output file contains sensitive data - handle carefully
- Tested on Edge versions 115+

## 🔒 Security Notice
This tool:
- Does not transmit data over networks
- Deletes temporary files immediately
- Stores output only if passwords are found
- Shows passwords in clear text only during execution

## 🛑 Disclaimer
Use this tool only:
- For legitimate password recovery on systems you own
- For educational purposes
- With proper authorization

The author is not responsible for misuse of this software.

---

**Legal Warning:** Unauthorized access to computer systems is illegal in most jurisdictions. Use responsibly.
