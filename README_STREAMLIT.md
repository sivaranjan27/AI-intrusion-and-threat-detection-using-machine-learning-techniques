# Security Attack Detection System - Streamlit Version

A comprehensive cybersecurity educational and testing platform built with Python Streamlit for detecting and analyzing 5 types of security attacks: Brute Force, Dictionary, Rainbow, Phishing, and DOS/DDoS.

## Quick Start (60 seconds)

### Windows
1. Double-click `run.bat`
2. Open browser to `http://localhost:8501`

### macOS/Linux
```bash
chmod +x run.sh
./run.sh
```

Or manually:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features

### 1. Login & Attack Detection (Tab 1)
- Upload Excel file with credentials (username, password)
- Test login attempts with real-time attack detection
- Identifies 3 attack types:
  - **Brute Force**: Multiple failed attempts with varied passwords
  - **Dictionary Attack**: Failed attempts using common passwords
  - **Rainbow Attack**: 8+ failed attempts (precomputed hash tables)
- Automatic email alerts to admin when attacks detected
- Real-time tracking of failed attempts per user
- Attack summary dashboard with statistics

**Default Test Credentials:**
- Username: `admin` | Password: `admin123`
- Try logging in with wrong password 6+ times to trigger detection

### 2. Phishing Detection (Tab 2)
- Advanced URL analysis with 6 feature analysis:
  - URL length detection
  - HTTPS encryption check
  - Domain reputation analysis
  - Special characters detection
  - Phishing keyword identification
  - Subdomain anomaly detection
- Risk scoring (0-100%)
- Confidence percentage (70-90%)
- Detailed risk indicators
- 8 practical safety tips

**Example URLs to test:**
- Suspicious: `http://g00gle.com` (no HTTPS, misspelled domain)
- Moderate: `https://secure-verify-account-now.example.com` (long URL, keywords)
- Legitimate: `https://www.google.com`

### 3. DOS Information (Tab 3)
- 5 types of DOS/DDoS attacks explained:
  - Volumetric Attacks
  - Protocol Attacks
  - Application Layer Attacks
  - Botnet Attacks
  - DNS Amplification
- 5 prevention strategy categories:
  - Rate Limiting
  - Traffic Filtering
  - Infrastructure Hardening
  - Detection Methods
  - Incident Response
- Impact analysis
- Incident response guide
- Emergency contacts and procedures

### 4. AI Chatbot (Sidebar)
- Google Gemini-powered security assistant
- Answers questions about all 5 attack types
- Fallback rule-based responses if API unavailable
- Chat history with clear functionality
- Real-time responses

**Example Questions:**
- "What is a brute force attack?"
- "How do I prevent phishing?"
- "Tell me about DOS attacks"
- "What are dictionary attacks?"

## System Architecture

```
app.py (769 lines)
├── Custom CSS Styling (Dark mode, purple/cyan theme)
├── Streamlit UI Layout (Tabs, sidebar, components)
│
└── utils/
    ├── attack_detection.py (118 lines)
    │   └── Brute force, dictionary, rainbow detection logic
    │
    ├── phishing_detector.py (131 lines)
    │   └── URL analysis, risk scoring, feature extraction
    │
    ├── email_service.py (107 lines)
    │   └── Gmail SMTP integration, HTML email templates
    │
    └── chatbot.py (112 lines)
        └── Google Gemini API integration, rule-based fallback
```

## Requirements

- Python 3.8+
- `pip` package manager
- Internet connection (for Gemini API, Gmail, phishing analysis)
- Gmail account (for email alerts)
- Gemini API key (for chatbot)

## Installation

### Option 1: Automatic (Recommended)

**Windows:**
```bash
run.bat
```

**macOS/Linux:**
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual

```bash
# 1. Clone/Navigate to project
cd /path/to/project

# 2. Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
streamlit run app.py
```

The application opens automatically at `http://localhost:8501`

## Configuration

### Email Configuration
Edit `/utils/email_service.py`:
```python
ADMIN_EMAIL = "norepnect@gmail.com"        # Admin email for alerts
GMAIL_USER = "vishwa.003@gmail.com"        # Gmail sender
GMAIL_APP_PASSWORD = "hvpycoaqgo"          # App password
```

**To generate Gmail App Password:**
1. Enable 2-Factor Authentication on Gmail account
2. Visit: https://myaccount.google.com/apppasswords
3. Select Mail and Windows Computer
4. Copy 16-character password

### Chatbot Configuration
Edit `/utils/chatbot.py`:
```python
API_KEY = "AIzaSJkgrBnDdeU93OEjUDtLtwE"
MODEL_NAME = "models/gemini-flash-latest"
```

## File Structure

```
project/
├── app.py                      # Main Streamlit application (769 lines)
├── requirements.txt            # Python dependencies
├── run.sh                      # Linux/macOS launcher
├── run.bat                     # Windows launcher
├── README_STREAMLIT.md         # This file
├── STREAMLIT_SETUP.md          # Detailed setup guide
│
└── utils/
    ├── __init__.py
    ├── attack_detection.py     # Attack type identification
    ├── phishing_detector.py    # URL analysis engine
    ├── email_service.py        # Gmail alert system
    └── chatbot.py              # Gemini chatbot integration
```

## Usage Examples

### Example 1: Test Brute Force Attack
1. Go to Tab 1: "Login & Attack Detection"
2. In username field enter: `testuser`
3. In password field enter: `wrong123`
4. Click "Login" 6 times with wrong password
5. After 6th attempt, you'll see:
   - "ATTACK DETECTED: BRUTE-FORCE"
   - Email alert confirmation
   - Attack details and prevention measures

### Example 2: Analyze Phishing URL
1. Go to Tab 2: "Phishing Detection"
2. Enter: `http://secure-paypal-login.verify-account.com`
3. View results:
   - Risk Score: ~75% (High risk)
   - Verdict: Likely Phishing
   - Indicators: Long URL, no HTTPS, phishing keywords

### Example 3: Learn about DOS
1. Go to Tab 3: "DOS Information"
2. Click on "Volumetric Attacks" expander
3. Click on "Rate Limiting" prevention strategy
4. Review incident response procedures

### Example 4: Chat with Security Assistant
1. Look at sidebar on the left
2. Type: "How do I prevent dictionary attacks?"
3. Get AI-powered response from Gemini
4. Follow up with more questions
5. Click "Clear Chat" to reset history

## Attack Detection Logic

### Brute Force
- **Definition**: Systematic trying of many password combinations
- **Detection**: Any failed attempt pattern with threshold > 5
- **Risk**: Account compromise, resource exhaustion

### Dictionary Attack
- **Definition**: Trying common passwords from a list
- **Detection**: Failed attempts with common passwords (admin, password123, etc.) + threshold > 5
- **Risk**: Weak password accounts compromised

### Rainbow Attack
- **Definition**: Using precomputed hash tables for password cracking
- **Detection**: Very high number of failed attempts (> 8)
- **Risk**: Immediate account compromise if successful

## Phishing Detection Algorithm

Analyzes 6 features and calculates risk score:

| Feature | Weight | Low Risk | High Risk |
|---------|--------|----------|-----------|
| URL Length | 15% | <75 chars | >75 chars |
| HTTPS | 25% | Present | Missing |
| Domain | 20% | Known domain | Unknown/IP |
| Special Chars | 20% | None in domain | Has special chars |
| Keywords | 15% | No phishing words | Multiple keywords |
| Subdomains | 5% | ≤2 | >2 |

**Risk Score Interpretation:**
- 0-30%: Likely Legitimate
- 30-70%: Suspicious (Review carefully)
- 70-100%: Likely Phishing (Avoid clicking)

## Email Alert Example

When attack is detected, admin receives email with:
- Attack type (Brute Force, Dictionary, Rainbow)
- User ID targeted
- Number of failed attempts
- Timestamp of detection
- Recommended actions:
  - Review account activity
  - Consider account lockout
  - Notify user
  - Update security policies

## Common Passwords Detected

The system checks against 30+ common passwords including:
- password, 123456, 12345678, qwerty, abc123
- monkey, letmein, trustno1, dragon, baseball
- admin, root, pass123, and many more

Add more to `/utils/attack_detection.py` COMMON_PASSWORDS list.

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Install requirements
```bash
pip install -r requirements.txt
```

### Issue: Email not sending
**Solution:** 
1. Verify Gmail credentials in `/utils/email_service.py`
2. Ensure App Password is used (not regular password)
3. Check spam folder
4. Enable "Less secure apps" if not using 2FA

### Issue: Chatbot not responding
**Solution:**
1. Check internet connection
2. Verify Gemini API key is valid
3. System falls back to rule-based if API fails

### Issue: Port 8501 in use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Issue: Excel file not loading
**Solution:**
1. Ensure exactly 2 columns: `username` and `password`
2. Use .xlsx or .xls format
3. No special characters in column names

## Performance Metrics

- **Response Time**: <1 second for most operations
- **Memory Usage**: ~100-150 MB
- **Concurrent Users**: 1 (Streamlit single-session design)
- **Email Send Time**: 1-3 seconds
- **Phishing Analysis**: <500ms per URL
- **Chatbot Response**: 1-5 seconds (API dependent)

## Security Considerations

### Production Deployment
1. Use environment variables for credentials (Streamlit Secrets)
2. Enable HTTPS
3. Implement rate limiting
4. Add authentication layer
5. Use environment-specific configs
6. Never commit credentials to version control

### Streamlit Cloud Deployment
In Settings > Secrets, add:
```
GMAIL_USER = "your-email@gmail.com"
GMAIL_APP_PASSWORD = "your-app-password"
ADMIN_EMAIL = "admin@company.com"
GOOGLE_GENERATIVE_AI_API_KEY = "your-api-key"
```

## Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud (Recommended)
1. Push to GitHub
2. Deploy at: https://streamlit.io/cloud
3. Add secrets in Settings

### Docker
```bash
docker build -t security-system .
docker run -p 8501:8501 security-system
```

### AWS/GCP/Azure
Use Docker image deployment

## Advanced Features

### Custom Excel Upload
- Prepare Excel with columns: `username`, `password`
- Upload via file uploader
- Auto-loads credentials for testing

### Session State Management
- Tracks login attempts per user
- Maintains chat history
- Persists attempt counts during session

### Real-time Alerts
- Instant email on attack detection
- HTML-formatted email templates
- Timestamp and user tracking

## Customization

### Change Theme Colors
Edit CSS variables in `app.py` (around line 50):
```python
--primary: #7c5dff;        # Purple
--accent: #00d4ff;         # Cyan
--danger: #ff4757;         # Red
--success: #2ed573;        # Green
```

### Add More Common Passwords
Edit `/utils/attack_detection.py`:
```python
COMMON_PASSWORDS = [
    'password', '123456', ...
    'your-custom-password'  # Add here
]
```

### Customize Detection Thresholds
Edit `/utils/attack_detection.py`:
```python
def detect_attack_type(...):
    if is_common_password and attempts > 5:  # Change 5
        return 'dictionary'
    elif attempts > 8:  # Change 8
        return 'rainbow'
```

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Known Limitations

1. Session state resets on page refresh (Streamlit design)
2. Single-user at a time (Streamlit default)
3. No persistent database (in-memory storage)
4. Requires internet for Gemini API and email
5. Local IP addresses can't receive emails

## Support & Documentation

- Streamlit Docs: https://docs.streamlit.io
- Google Generative AI: https://ai.google.dev
- Gmail App Passwords: https://support.google.com/accounts/answer/185833
- Issue Tracking: Check error messages in console

## License

Educational project. Use responsibly.

## Credits

Built with:
- Streamlit (UI Framework)
- Google Generative AI (Chatbot)
- Python 3.9+
- pandas (Data handling)
- openpyxl (Excel parsing)

## Version

Streamlit Edition v1.0
- 4 main tabs
- Chatbot in sidebar
- Email alerts
- Dark mode UI
- No Node.js required
- Full Python-based architecture

---

**Happy Testing! Stay Secure!**
