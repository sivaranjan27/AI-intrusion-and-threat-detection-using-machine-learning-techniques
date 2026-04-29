# Streamlit Security Attack Detection System - Setup Guide

## Overview
This is a complete rewrite of the application from Next.js to pure Python Streamlit. It includes all 5 attack detection features with a modern dark-mode UI.

## Features
- **Tab 1: Login & Attack Detection** - Test login with Excel credentials, detect brute force/dictionary/rainbow attacks
- **Tab 2: Phishing Detection** - Analyze URLs for phishing characteristics with risk scoring
- **Tab 3: DOS Information** - Educational content about DOS/DDoS attacks with prevention strategies
- **Chatbot (Sidebar)** - AI-powered assistant using Google Gemini API
- **Email Alerts** - Automatic alerts when attacks are detected (Gmail)

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Gmail account with app password
- Google Gemini API key (for chatbot)

## Installation

### 1. Clone/Setup the Project
```bash
cd /path/to/project
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
The application has hardcoded credentials (as per your request):
- GMAIL_USER = "vishwa.003@gmail.com"
- GMAIL_APP_PASSWORD = "hvpycoaqgo"
- ADMIN_EMAIL = "norepnect@gmail.com"
- Gemini API Key = "AIzaSJkgrBnDdeU93OEjUDtLtwE"

If you want to change these, edit the respective utility files:
- Email: `/utils/email_service.py`
- Chatbot: `/utils/chatbot.py`

### 5. Run the Application
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## Project Structure
```
project/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── utils/
│   ├── attack_detection.py        # Brute force/dictionary/rainbow detection
│   ├── phishing_detector.py       # Phishing analysis logic
│   ├── email_service.py           # Gmail email alerts
│   └── chatbot.py                 # Gemini AI chatbot integration
└── STREAMLIT_SETUP.md             # This file
```

## How to Use

### Tab 1: Login & Attack Detection

1. **Upload Excel File (Optional)**
   - Prepare an Excel file with columns: `username` and `password`
   - Click "Upload Excel file" to load credentials
   - Format: Two columns named exactly "username" and "password"

2. **Test Login**
   - Enter a username and password
   - Click "Login" button
   - System tracks failed attempts:
     - 1-5 attempts: Warning
     - 6+ attempts: ATTACK DETECTED

3. **Attack Detection**
   - System automatically identifies attack type:
     - **Brute Force**: Multiple failed attempts with varied passwords
     - **Dictionary Attack**: Failed attempts using common passwords (admin, password123, etc.)
     - **Rainbow Attack**: 8+ failed attempts (indicating precomputed hash tables)

4. **Email Alerts**
   - When attack is detected (6+ failed attempts), email is automatically sent to admin
   - Email includes: User ID, attack type, attempt count, timestamp, recommendations

### Tab 2: Phishing Detection

1. **Enter URL to Analyze**
   - Copy a suspicious URL
   - Paste into the input field
   - Click Enter or wait for automatic analysis

2. **Review Analysis Results**
   - **Verdict**: Legitimate, Suspicious, or Likely Phishing
   - **Risk Score**: 0-100% (higher = more risky)
   - **Confidence**: How confident the analysis is (70-90%)
   - **Risk Indicators**: Specific warnings (if any)

3. **Features Analyzed**
   - URL length (75+ chars is suspicious)
   - HTTPS encryption (missing = risky)
   - Domain structure (legitimate vs spoofing)
   - Special characters in domain
   - Phishing keywords in URL
   - Known vs unknown domains
   - Number of subdomains

4. **Safety Tips**
   - Review the 8 safety tips provided at the bottom
   - Use these to identify phishing manually

### Tab 3: DOS Information

1. **Learn About DOS/DDoS**
   - Expandable sections for 5 types of attacks
   - Information about each attack method

2. **Prevention Strategies**
   - Rate Limiting
   - Traffic Filtering
   - Infrastructure improvements
   - Detection methods
   - Response procedures

3. **Incident Response**
   - Immediate actions to take
   - Who to contact (FBI, ISP, DDoS services, CERT)

### Chatbot (Sidebar)

1. **Ask Questions**
   - Type in the text box: "What is a brute force attack?"
   - System responds with AI-powered answers
   - Also supports rule-based responses if API fails

2. **Supported Topics**
   - Brute Force Attacks
   - Dictionary Attacks
   - Rainbow Attacks
   - Phishing Attacks
   - DOS/DDoS Attacks

3. **Clear History**
   - Click "Clear Chat" button to reset conversation

## Default Test Credentials
If no Excel file is uploaded, use these for testing:
- Username: `admin`, Password: `admin123`
- Username: `user`, Password: `password123`

Try logging in with wrong password 6 times to trigger attack detection.

## Gmail Setup (For Email Alerts)

If you want to use a different Gmail account:

1. Enable 2-Factor Authentication on Gmail
2. Create an App Password:
   - Go to myaccount.google.com
   - Select "Security" (left menu)
   - Enable 2-Step Verification
   - Generate App Password (select "Mail" and "Windows Computer")
   - Copy the 16-character password

3. Update `/utils/email_service.py`:
   ```python
   ADMIN_EMAIL = "your-email@gmail.com"
   GMAIL_USER = "your-email@gmail.com"
   GMAIL_APP_PASSWORD = "your-16-char-password"
   ```

4. Restart the application

## Gemini API Setup (For Chatbot)

If you want to use a different Gemini API key:

1. Go to https://makersuite.google.com/app/apikeys
2. Create a new API key
3. Update `/utils/chatbot.py`:
   ```python
   API_KEY = "your-new-api-key"
   ```
4. Restart the application

## Deployment

### Deploy to Streamlit Cloud (Recommended)
1. Push code to GitHub repository
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your GitHub repo and `app.py`
5. Add secrets in Settings:
   - GMAIL_USER
   - GMAIL_APP_PASSWORD
   - ADMIN_EMAIL
   - GOOGLE_GENERATIVE_AI_API_KEY

### Deploy with Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t security-system .
docker run -p 8501:8501 security-system
```

### Deploy to AWS/GCP/Azure
- Use Docker image method above
- Deploy to: AWS ECS, Google Cloud Run, Azure Container Instances

## Troubleshooting

### Email not sending
- Check Gmail credentials in `utils/email_service.py`
- Ensure "Less secure app access" is enabled (if not using App Password)
- Check spam folder for test emails

### Chatbot not responding
- Verify Gemini API key is correct
- Check internet connection
- System falls back to rule-based responses if API fails

### Excel file not loading
- Ensure file has exactly columns: "username" and "password"
- File must be in .xlsx or .xls format
- Check for special characters in column names

### Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

## Features Comparison

| Feature | Next.js Version | Streamlit Version |
|---------|-----------------|-------------------|
| Login Detection | ✓ | ✓ |
| Attack Detection | ✓ | ✓ |
| Email Alerts | ✓ | ✓ |
| Phishing Detection | ✓ | ✓ |
| DOS Info | ✓ | ✓ |
| Chatbot | ✓ | ✓ |
| Dark Mode UI | ✓ | ✓ |
| Excel Integration | ✓ | ✓ |
| No Node.js Required | ✗ | ✓ |

## Performance Notes
- Streamlit version is faster to deploy (Python only)
- Runs on single port (8501)
- No database required
- Session state resets on page refresh (expected Streamlit behavior)

## Security Notes
- Credentials are stored in session state (cleared on page refresh)
- Email credentials are in code (use env vars in production)
- Never commit credentials to version control
- Use Streamlit Cloud secrets for sensitive data

## Support
For issues, check:
1. Streamlit documentation: https://docs.streamlit.io
2. Google Generative AI docs: https://ai.google.dev
3. Gmail app password guide: https://support.google.com/accounts/answer/185833

## License
This project is for educational purposes.
