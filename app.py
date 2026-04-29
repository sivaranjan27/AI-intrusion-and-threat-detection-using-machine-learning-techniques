import streamlit as st
import pandas as pd
from io import StringIO
import sys
import os
from datetime import datetime
from pathlib import Path
# ================= LOGIN LOG FILE =================
LOG_FILE = os.path.join(Path(__file__).parent, "login_logs.xlsx")

def save_login_log(username, status):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log_data = {
        "Username": username,
        "Time": current_time,
        "Status": status
    }

    if os.path.exists(LOG_FILE):
        df = pd.read_excel(LOG_FILE)
        df = pd.concat([df, pd.DataFrame([log_data])], ignore_index=True)
    else:
        df = pd.DataFrame([log_data])

    df.to_excel(LOG_FILE, index=False)
# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.attack_detection import (
    is_common_password, detect_attack_type, get_attack_description,
    validate_credentials, check_attack_threshold, get_attempt_summary
)
from utils.phishing_detector import analyze_url, get_safety_tips, validate_url
from utils.email_service import send_attack_alert, send_test_email
from utils.chatbot import get_chatbot_response, get_rule_based_response

# Page config
st.set_page_config(
    page_title="Security Attack Detection System",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Add theme toggle in sidebar
with st.sidebar:
    st.markdown("### Settings")
    theme_mode = st.radio("Theme Mode", ["Dark", "Light"], 
                          index=0 if st.session_state.theme == 'dark' else 1,
                          horizontal=True)
    
    if theme_mode == "Light":
        st.session_state.theme = 'light'
    else:
        st.session_state.theme = 'dark'

# Custom CSS with Theme Support
theme_colors = {
    'dark': {
        'primary': '#7c5dff',
        'primary_dark': '#6b4ee8',
        'accent': '#00d4ff',
        'accent_dark': '#00a8cc',
        'danger': '#ff4757',
        'success': '#2ed573',
        'warning': '#ffa502',
        'bg': '#0f1419',
        'card_bg': '#1a1f29',
        'border': '#2a3141',
        'text_primary': '#e0e0e0',
        'text_secondary': '#a0a0a0',
    },
    'light': {
        'primary': '#6b4ee8',
        'primary_dark': '#5a3fd7',
        'accent': '#0095cc',
        'accent_dark': '#0078a8',
        'danger': '#e63946',
        'success': '#06a77d',
        'warning': '#f77f00',
        'bg': '#ffffff',
        'card_bg': '#f8f9fa',
        'border': '#e0e0e0',
        'text_primary': '#1a1a1a',
        'text_secondary': '#666666',
    }
}

colors = theme_colors[st.session_state.theme]

css = f"""
<style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    :root {{
        --primary: {colors['primary']};
        --primary-dark: {colors['primary_dark']};
        --accent: {colors['accent']};
        --accent-dark: {colors['accent_dark']};
        --danger: {colors['danger']};
        --success: {colors['success']};
        --warning: {colors['warning']};
        --bg: {colors['bg']};
        --card-bg: {colors['card_bg']};
        --border-color: {colors['border']};
        --text-primary: {colors['text_primary']};
        --text-secondary: {colors['text_secondary']};
    }}
    
    body {{
        background-color: var(--bg);
        color: var(--text-primary);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    }}
    
    .main {{
        background-color: var(--bg);
        color: var(--text-primary);
    }}
    
    .stApp {{
        background-color: var(--bg);
    }}
    
    [data-testid="stAppViewContainer"] {{
        background-color: var(--bg);
        color: var(--text-primary);
    }}
    
    [data-testid="stSidebar"] {{
        background-color: var(--card-bg);
    }}
    
    .stMarkdown {{
        color: var(--text-primary);
    }}
    
    p {{
        color: var(--text-primary) !important;
    }}
    
    label {{
        color: var(--text-primary) !important;
    }}
    
    /* Streamlit-specific text fixes */
    .stMarkdown > div {{
        color: var(--text-primary) !important;
    }}
    
    .stMarkdown * {{
        color: var(--text-primary) !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary) !important;
    }}
    
    [data-testid="stMarkdownContainer"] {{
        color: var(--text-primary) !important;
    }}
    
    [data-testid="stMarkdownContainer"] * {{
        color: var(--text-primary) !important;
    }}
    
    .stSuccess {{
        background-color: rgba(6, 168, 125, 0.1) !important;
        color: var(--success) !important;
    }}
    
    .stError {{
        background-color: rgba(230, 57, 70, 0.1) !important;
        color: var(--danger) !important;
    }}
    
    .stWarning {{
        background-color: rgba(247, 127, 0, 0.1) !important;
        color: var(--warning) !important;
    }}
    
    .stInfo {{
        background-color: rgba(0, 149, 204, 0.1) !important;
        color: var(--accent) !important;
    }}
    
    div[data-testid="stMetricValue"] {{
        color: var(--text-primary) !important;
    }}
    
    div[data-testid="stMetricLabel"] {{
        color: var(--text-secondary) !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] button {{
        background-color: transparent !important;
        border-bottom: 2px solid transparent !important;
        color: var(--text-secondary) !important;
        padding: 15px 20px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: var(--accent) !important;
        border-bottom-color: var(--accent) !important;
        background-color: transparent !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] button:hover {{
        color: var(--accent) !important;
    }}
    
    .stTextInput > div > div > input {{
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }}
    
    .stTextArea > div > div > textarea {{
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }}
    
    .stNumberInput > div > div > input {{
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }}
    
    .stSelectbox > div > div > select {{
        background-color: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white !important;
    }}
    
    /* Table styling */
    table {{
        color: var(--text-primary) !important;
    }}
    
    td {{
        color: var(--text-primary) !important;
    }}
    
    th {{
        color: white !important;
        background-color: var(--primary) !important;
    }}
    
    [data-testid="dataFrameContainer"] {{
        color: var(--text-primary) !important;
    }}
    
    [data-testid="dataFrameContainer"] * {{
        color: var(--text-primary) !important;
    }}
    
    /* Text input labels */
    .stTextInput > label {{
        color: var(--text-primary) !important;
    }}
    
    .stTextArea > label {{
        color: var(--text-primary) !important;
    }}
    
    .stNumberInput > label {{
        color: var(--text-primary) !important;
    }}
    
    .stSelectbox > label {{
        color: var(--text-primary) !important;
    }}
    
    .stFileUploader > label {{
        color: var(--text-primary) !important;
    }}
    
    .stCheckbox {{
        color: var(--text-primary) !important;
    }}
    
    .stRadio {{
        color: var(--text-primary) !important;
    }}
    
    .card {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }}
    
    .card:hover {{
        border-color: var(--primary);
        box-shadow: 0 8px 12px rgba(107, 78, 232, 0.2);
    }}
    
    .alert {{
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid;
    }}
    
    .alert-danger {{
        background-color: rgba(230, 57, 70, 0.1);
        border-color: var(--danger);
        color: var(--danger);
    }}
    
    .alert-success {{
        background-color: rgba(6, 168, 125, 0.1);
        border-color: var(--success);
        color: var(--success);
    }}
    
    .alert-warning {{
        background-color: rgba(247, 127, 0, 0.1);
        border-color: var(--warning);
        color: var(--warning);
    }}
    
    .alert-info {{
        background-color: rgba(0, 149, 204, 0.1);
        border-color: var(--accent);
        color: var(--accent);
    }}
    
    .btn-primary {{
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .btn-primary:hover {{
        transform: translateY(-2px);
    }}
    
    .stat-box {{
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 10px;
    }}
    
    .stat-label {{
        font-size: 14px;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 5px;
    }}
    
    .stat-value {{
        font-size: 32px;
        font-weight: bold;
    }}
    
    .badge {{
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 5px 5px 5px 0;
    }}
    
    .badge-danger {{
        background-color: rgba(230, 57, 70, 0.2);
        color: var(--danger);
    }}
    
    .badge-success {{
        background-color: rgba(6, 168, 125, 0.2);
        color: var(--success);
    }}
    
    .badge-warning {{
        background-color: rgba(247, 127, 0, 0.2);
        color: var(--warning);
    }}
    
    .badge-info {{
        background-color: rgba(0, 149, 204, 0.2);
        color: var(--accent);
    }}
    
    .header-title {{
        color: var(--accent);
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .header-subtitle {{
        color: var(--text-secondary);
        font-size: 14px;
        margin-bottom: 20px;
    }}
    
    .form-group {{
        margin: 15px 0;
    }}
    
    .form-label {{
        display: block;
        color: var(--text-primary);
        font-weight: 600;
        margin-bottom: 8px;
        font-size: 14px;
    }}
    
    .risk-bar {{
        background-color: var(--border-color);
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        margin: 10px 0;
    }}
    
    .risk-fill {{
        height: 100%;
        border-radius: 4px;
        transition: width 0.3s ease;
    }}
    
    .risk-low {{
        background: linear-gradient(90deg, var(--success), #06a87d);
    }}
    
    .risk-medium {{
        background: linear-gradient(90deg, var(--warning), #f7a01e);
    }}
    
    .risk-high {{
        background: linear-gradient(90deg, var(--danger), #e85d6e);
    }}
    
    .sidebar .sidebar-content {{
        background-color: var(--card-bg);
    }}
    
    .stButton > button {{
        border: none !important;
        font-weight: 600 !important;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
    }}
    
    .stFileUploadDropzone {{
        background-color: var(--card-bg) !important;
        border: 2px dashed var(--primary) !important;
    }}
    
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }}
    
    th {{
        background-color: var(--primary);
        color: white;
        padding: 12px;
        text-align: left;
        font-weight: 600;
    }}
    
    td {{
        padding: 12px;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-primary);
    }}
    
    tr:hover {{
        background-color: var(--card-bg);
    }}
    
    .divider {{
        border-top: 1px solid var(--border-color);
        margin: 20px 0;
    }}
    
    .feature-list {{
        list-style: none;
        padding: 0;
    }}
    
    .feature-list li {{
        padding: 10px 0;
        padding-left: 30px;
        position: relative;
        color: var(--text-primary);
    }}
    
    .feature-list li:before {{
        content: "✓";
        position: absolute;
        left: 0;
        color: var(--success);
        font-weight: bold;
    }}
    
    .expander {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin: 10px 0;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: var(--text-primary);
    }}
    
    hr {{
        border: none;
        border-top: 1px solid var(--border-color);
    }}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# Initialize session state
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = {}

if 'excel_data' not in st.session_state:
    st.session_state.excel_data = {}

if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'admin' not in st.session_state:
    st.session_state.admin = False
    
# Sidebar - Chatbot
st.sidebar.markdown('<div class="header-title">🤖 Security Assistant</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="header-subtitle">Ask questions about security attacks</div>', unsafe_allow_html=True)

# Chat input
user_input = st.sidebar.text_input(
    "Your question:",
    placeholder="Ask about attacks, prevention, etc."
)

if st.sidebar.button("Ask", key="ask_btn"):
    if user_input.strip():
        with st.spinner("Analyzing..."):
            response = get_chatbot_response(user_input)

        st.sidebar.markdown("### Assistant Response")
        st.sidebar.write(response)
    else:
        st.sidebar.warning("Please enter a question first.")

# Main content
st.markdown('<div class="header-title">🔒 Security Attack Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="header-subtitle">Detect, analyze, and learn about cybersecurity threats</div>', unsafe_allow_html=True)

# Create tabs
if st.session_state.logged_in:
    
    if st.session_state.admin:
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Dashboard", "Phishing Detection", "DOS Information", "Admin Dashboard"]
        )
    else:
        tab1, tab2, tab3 = st.tabs(
            ["Dashboard", "Phishing Detection", "DOS Information"]
        )
        tab4 = None
else:
    tab1 = st.tabs(["Login"])[0]
    tab2 = tab3 = None

# ===== TAB 1: LOGIN & ATTACK DETECTION =====
with tab1:

    # ------------------ LOGIN VIEW ------------------
    if not st.session_state.logged_in:

        st.markdown("### Login with Excel Credentials")

        col1, col2 = st.columns(2)

        with col1:
            uploaded_file = st.file_uploader(
                "Upload Excel file with credentials", 
                type=['xlsx', 'xls']
            )

            if uploaded_file:
                try:
                    df = pd.read_excel(uploaded_file)
                    if 'username' in df.columns and 'password' in df.columns:
                        st.session_state.excel_data = dict(
                            zip(df['username'], df['password'])
                        )
                        st.success(f"Loaded {len(st.session_state.excel_data)} credentials")
                    else:
                        st.error("Excel must have 'username' and 'password' columns")
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")

        with col2:
            st.markdown("### Login")
            test_username = st.text_input("Username:", key="login_user")
            test_password = st.text_input("Password:", type="password", key="login_pass")

            if st.button("Login", key="login_btn"):

                if not test_username or not test_password:
                    st.warning("Please enter both username and password")
                else:

                    if not st.session_state.excel_data:
                        st.session_state.excel_data = {
                            'admin': 'admin123',
                            'user': 'password123'
                        }

                    if test_username == "admin" and test_password == "admin123":
                        is_valid = True
                        message = "Admin Login Successful"
                    else:
                        is_valid, message = validate_credentials(
                        test_username,
                        test_password,
                        st.session_state.excel_data
                    )

                    if is_valid:
                        save_login_log(test_username, "Success")
                        if test_username == "admin" and test_password == "admin123":
                            st.session_state.admin = True
                        else:
                            st.session_state.admin = False
                        st.session_state.logged_in = True
                        st.session_state.current_user = test_username
                        st.rerun()
                        
                    else:
                        save_login_log(test_username, "Failed")
                        st.error(message)
                        # ---------------- TRACK FAILED ATTEMPTS ----------------
                        if test_username not in st.session_state.login_attempts:
                            st.session_state.login_attempts[test_username] = []
                        st.session_state.login_attempts[test_username].append(test_password)
                        password_list = st.session_state.login_attempts[test_username]
                        attempts = len(password_list)
                        attack_type = detect_attack_type(password_list)
                        is_attack, threshold_msg = check_attack_threshold(attempts)
                        st.warning(f"Failed Attempts: {attempts}")
                        if is_attack and attack_type != "normal":
                            st.markdown(
                                 f'<div class="alert alert-danger"><strong>ATTACK DETECTED:</strong> {attack_type.upper()}</div>',
                                 unsafe_allow_html=True
                            )
                            success, email_msg = send_attack_alert(
                                test_username,
                                attack_type,
                                attempts,
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            )
                            if success:
                                st.success("Admin has been notified via email.")
                            else:
                                st.warning(f"Email Error: {email_msg}")
                            attack_info = get_attack_description(attack_type)
                            with st.expander(f"📊 {attack_info['name']} Details"):
                                st.write(f"**Description:** {attack_info['description']}")
                                st.write("**Characteristics:**")
                                for char in attack_info['characteristics']:
                                    st.write(f"• {char}")
                                st.write("**Prevention:**")
                                for prev in attack_info['prevention']:
                                    st.write(f"• {prev}")

    # ------------------ DASHBOARD VIEW ------------------
    else:

        st.markdown("## 🛡️ Attack Detection Dashboard")
        st.markdown(f"Welcome, **{st.session_state.current_user}**")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.admin = False
            st.rerun()

        st.markdown("### Security Threats Overview")

        with st.expander("📘 Dictionary Attack"):
            st.markdown("""
A **Dictionary Attack** is a type of password attack where the attacker attempts to gain unauthorized 
access by systematically trying a list of commonly used passwords.

Instead of trying every possible combination (like brute force), the attacker uses a predefined 
"dictionary" of passwords that are frequently used by users such as:

- 123456
- password
- admin123
- qwerty
- welcome

These password lists are often compiled from:
- Previously leaked data breaches
- Common password databases
- Predictable user behavior patterns

### 🔎 How It Works:
1. The attacker selects a target username.
2. The system automatically tests passwords from the dictionary list.
3. If the entered password matches, access is granted.

### ⚠️ Why It Is Dangerous:
- Many users reuse simple or common passwords.
- It is faster than brute-force attacks.
- It requires less computational power.

### 🛡️ Prevention Methods:
- Use strong and unique passwords.
- Enforce minimum password complexity rules.
- Implement account lockout after multiple failed attempts.
- Use Multi-Factor Authentication (MFA).

Dictionary attacks are especially effective when password policies are weak or when users rely on 
simple, predictable passwords.
""")

        with st.expander("⚡ Brute Force Attack"):
            st.markdown("""
A **Brute Force Attack** is a trial-and-error method used by attackers to gain unauthorized 
access to accounts by trying every possible password combination until the correct one is found.

Unlike dictionary attacks (which use common passwords), brute force attacks attempt:
- All possible letter combinations
- Numbers
- Symbols
- Mixed character patterns

### 🔎 How It Works:
1. The attacker selects a target account.
2. An automated tool generates password combinations.
3. Each combination is tested one by one.
4. The attack continues until the correct password is discovered.

For example, if the password is 4 digits long:
- 0000
- 0001
- 0002
- ...
- 9999

Eventually, the correct password will be found if there are no security restrictions.

### ⚠️ Why It Is Dangerous:
- Guaranteed to succeed if given enough time.
- Automated tools can test thousands of passwords per second.
- Weak or short passwords are cracked very quickly.

### 🛡️ Prevention Methods:
- Use long and complex passwords.
- Limit login attempts.
- Implement account lockout after multiple failures.
- Add CAPTCHA verification.
- Enable Multi-Factor Authentication (MFA).
- Monitor login attempts and trigger alerts.

Brute force attacks are highly effective against systems that do not enforce 
strong password policies or rate-limiting mechanisms.
""")

        with st.expander("🌈 Rainbow Table Attack"):
            st.markdown("""
A **Rainbow Table Attack** is a password cracking technique that uses precomputed tables 
of hash values to reverse cryptographic hash functions and recover original passwords.

When passwords are stored in a database, they are usually saved as **hashes**, not plain text.  
For example:

- Password: admin123  
- Hash: 240be518fabd2724ddb6f04eebc6e1c4  

A rainbow table contains millions of precomputed hash–password pairs.  
Instead of guessing passwords one by one, the attacker simply:

1. Obtains the hashed password from a breached database.
2. Searches the rainbow table for a matching hash.
3. If found, retrieves the original password instantly.

### 🔎 How It Works:
- Step 1: The attacker generates a massive list of possible passwords.
- Step 2: Each password is hashed.
- Step 3: The hash and password pairs are stored in a structured table.
- Step 4: When a database is compromised, the attacker compares stored hashes against the table.

This method is much faster than brute force because the heavy computation is done in advance.

### ⚠️ Why It Is Dangerous:
- Extremely fast lookup once the table is built.
- Effective against unsalted password hashes.
- Can crack weak or common passwords almost instantly.

### 🛡️ Prevention Methods:
- Use **salted hashing** (add random value before hashing).
- Use strong hashing algorithms (bcrypt, Argon2, PBKDF2).
- Avoid storing plain or unsalted MD5/SHA1 hashes.
- Enforce strong password policies.

Modern systems prevent rainbow table attacks by adding a unique random "salt" 
to each password before hashing, making precomputed tables useless.
""")

        with st.expander("🎣 Phishing Attack"):
            st.markdown("""
A **Phishing Attack** is a social engineering attack where attackers impersonate a trusted 
organization or individual to trick users into revealing sensitive information such as:

- Usernames
- Passwords
- Credit card details
- OTP codes
- Banking information

Instead of attacking the system directly, phishing targets the **human user**.

### 🔎 How It Works:
1. The attacker creates a fake website that looks identical to a legitimate site.
2. A phishing email or message is sent to victims.
3. The message contains a malicious link (e.g., fake banking login page).
4. The user enters credentials on the fake site.
5. The attacker captures and stores the entered data.

Example:
- Real site: https://bank.com  
- Fake site: https://bank-login-security.com  

The difference is small, but dangerous.

### 🎯 Common Phishing Methods:
- Email phishing
- SMS phishing (Smishing)
- Voice phishing (Vishing)
- Fake login pages
- Fake job or prize offers

### ⚠️ Why It Is Dangerous:
- Targets human psychology.
- Can bypass strong password systems.
- Often difficult to detect visually.
- Used in large-scale financial fraud.

### 🛡️ Prevention Methods:
- Check URLs carefully.
- Verify HTTPS certificates.
- Avoid clicking suspicious email links.
- Enable Multi-Factor Authentication (MFA).
- Use anti-phishing detection systems (like this module).

Phishing attacks are among the most common and successful cyber threats 
because they exploit human trust rather than technical vulnerabilities.
""")

        with st.expander("💣 DOS Attack"):
            st.markdown("""
A **Denial of Service (DoS) Attack** is a cyber attack that aims to make a system, 
website, or network unavailable to legitimate users by overwhelming it with excessive traffic.

Instead of stealing data, the goal is to **disrupt availability**.

### 🔎 How It Works:
1. The attacker sends a massive number of requests to a target server.
2. The server becomes overloaded.
3. System resources (CPU, memory, bandwidth) get exhausted.
4. Legitimate users can no longer access the service.

Example:
If a website can handle 1,000 requests per second, 
an attacker may send 100,000 requests per second to crash it.

### 🌍 DDoS (Distributed Denial of Service):
When the attack traffic comes from multiple compromised systems 
(often called a botnet), it becomes a **DDoS attack**.

This makes the attack:
- Harder to block
- Harder to trace
- More powerful

### 🎯 Common Types of DoS Attacks:
- Volumetric attacks (traffic flooding)
- SYN Flood attacks
- HTTP Flood attacks
- DNS Amplification attacks

### ⚠️ Why It Is Dangerous:
- Causes website downtime
- Leads to financial loss
- Damages brand reputation
- Disrupts business operations

### 🛡️ Prevention Methods:
- Rate limiting
- Firewalls and Intrusion Detection Systems (IDS)
- Load balancing
- CDN services (Cloudflare, Akamai)
- DDoS mitigation tools
- Continuous traffic monitoring

DoS attacks target system availability and are one of the most common 
threats against online services and enterprise infrastructure.
""")

        st.markdown("---")
        st.markdown("### Attack Summary")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">Total Failed Attempts</div>
                <div class="stat-value">{sum(len(v) for v in st.session_state.login_attempts.values())}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">Targeted Users</div>
                <div class="stat-value">{len(st.session_state.login_attempts)}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            max_attempts = max(len(v) for v in st.session_state.login_attempts.values()) if st.session_state.login_attempts else 0
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-label">Max Attempts</div>
                <div class="stat-value">{max_attempts}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.login_attempts:
            st.markdown("**Attempt Details:**")

            for user, pwd_list in st.session_state.login_attempts.items():
                count = len(pwd_list)

                colA, colB = st.columns([3, 1])
                with colA:
                    st.write(f"User: **{user}**")

                with colB:
                    if count >= 5:
                        st.markdown(
                            f'<span class="badge badge-danger">{count} attempts</span>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<span class="badge badge-warning">{count} attempts</span>',
                            unsafe_allow_html=True
                        )

# ===== TAB 2: PHISHING DETECTION =====
# ===== TAB 2: PHISHING DETECTION =====
if tab2:
    with tab2:

        st.markdown("### Analyze URLs for Phishing")
        
        url_input = st.text_input(
            "Enter URL to analyze:",
            placeholder="https://example.com",
            key="phishing_url"
        )
        
        if url_input:
            # Validate URL
            is_valid, validation_msg = validate_url(url_input)
            
            if not is_valid:
                st.error(validation_msg)
            else:
                # Analyze URL
                analysis = analyze_url(url_input)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### Analysis Results")
                    
                    # Verdict
                    verdict = analysis['verdict']
                    if 'Phishing' in verdict:
                        st.markdown(
                            f'<div class="alert alert-danger"><strong>Verdict:</strong> {verdict}</div>',
                            unsafe_allow_html=True
                        )
                    elif 'Suspicious' in verdict:
                        st.markdown(
                            f'<div class="alert alert-warning"><strong>Verdict:</strong> {verdict}</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="alert alert-success"><strong>Verdict:</strong> {verdict}</div>',
                            unsafe_allow_html=True
                        )
                    
                    # Risk score visualization
                    risk_score = analysis['risk_score']
                    confidence = analysis['confidence']
                    
                    st.markdown("**Risk Score:**")
                    
                    if risk_score < 30:
                        risk_class = "risk-low"
                    elif risk_score < 70:
                        risk_class = "risk-medium"
                    else:
                        risk_class = "risk-high"
                    
                    st.markdown(f"""
                    <div class="risk-bar">
                        <div class="risk-fill {risk_class}" style="width: {risk_score}%"></div>
                    </div>
                    <p>{risk_score}% Risk | {confidence}% Confidence</p>
                    """, unsafe_allow_html=True)
                    
                    # Indicators
                    if analysis['indicators']:
                        st.markdown("**Risk Indicators:**")
                        for indicator in analysis['indicators']:
                            st.markdown(
                                f'<div class="alert alert-warning">⚠️ {indicator}</div>',
                                unsafe_allow_html=True
                            )
                
                with col2:
                    st.markdown("### Features Analyzed")
                    
                    features = analysis['features']
                    st.write(f"**URL Length:** {features.get('url_length', 'N/A')} chars")
                    st.write(f"**HTTPS:** {'✓' if features.get('has_https') else '✗'}")
                    st.write(f"**Domain:** {features.get('domain', 'N/A')}")
                    st.write(f"**Known Domain:** {'✓' if features.get('is_known_domain') else '✗'}")
        
        # Safety tips
        st.markdown("---")
        st.markdown("### Safety Tips")
        
        tips = get_safety_tips()
        for i, tip in enumerate(tips, 1):
            st.markdown(f"**{i}.** {tip}")

# ===== TAB 3: DOS INFORMATION =====
# ===== TAB 3: DOS INFORMATION =====
if tab3:
    with tab3:

        st.markdown("### Denial of Service (DOS) Attacks")
        
        st.markdown("""
        A Denial of Service (DOS) attack is a malicious attempt to disrupt the normal functioning of 
        a network, website, or online service by overwhelming it with a flood of traffic or requests. 
        When the attack comes from multiple sources, it's called a Distributed Denial of Service (DDoS).
        """)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Types of DOS Attacks")
            
            dos_types = {
                "Volumetric Attacks": "Overwhelm the target with massive amounts of traffic (e.g., UDP floods, ICMP floods)",
                "Protocol Attacks": "Exploit weaknesses in network protocols (e.g., SYN floods, fragmented packet attacks)",
                "Application Layer": "Target specific web applications (e.g., HTTP floods, Slowloris attacks)",
                "Botnet Attacks": "Use infected computers to send attack traffic",
                "DNS Amplification": "Use DNS servers to amplify and redirect traffic to the target"
            }
            
            for attack_type, description in dos_types.items():
                with st.expander(f"🎯 {attack_type}"):
                    st.write(description)
        
        with col2:
            st.markdown("### Prevention Strategies")
            
            prevention = {
                "Rate Limiting": [
                    "Limit requests per IP address",
                    "Implement throttling mechanisms",
                    "Use token bucket algorithms"
                ],
                "Traffic Filtering": [
                    "Filter malicious traffic patterns",
                    "Use firewalls and IDS systems",
                    "Implement geo-blocking if needed"
                ],
                "Infrastructure": [
                    "Use CDN services (Cloudflare, Akamai)",
                    "Distribute load across multiple servers",
                    "Use DDoS mitigation services"
                ],
                "Detection": [
                    "Monitor bandwidth usage",
                    "Set up alerts for traffic spikes",
                    "Analyze traffic patterns"
                ],
                "Response": [
                    "Have incident response plan",
                    "Contact ISP for upstream filtering",
                    "Work with DDoS mitigation providers"
                ]
            }
            
            for strategy, points in prevention.items():
                with st.expander(f"🛡️ {strategy}"):
                    for point in points:
                        st.write(f"• {point}")
        
        st.markdown("---")
        st.markdown("### Impact of DOS Attacks")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="stat-box" style="background: linear-gradient(135deg, #ff4757, #ff8a9b);">
                <div class="stat-label">Financial Loss</div>
                <div class="stat-value">$$$</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("Lost revenue, recovery costs, ransom demands")
        
        with col2:
            st.markdown("""
            <div class="stat-box" style="background: linear-gradient(135deg, #ffa502, #ffc244);">
                <div class="stat-label">Reputation Damage</div>
                <div class="stat-value">📉</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("Customer trust erosion, brand damage")
        
        with col3:
            st.markdown("""
            <div class="stat-box" style="background: linear-gradient(135deg, #ff4757, #ff8a9b);">
                <div class="stat-label">Service Downtime</div>
                <div class="stat-value">⏱️</div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("Unavailable services, productivity loss")
        
        st.markdown("---")
        st.markdown("### Incident Response")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Immediate Actions:**")
            st.markdown("""
            1. Activate incident response team
            2. Notify relevant stakeholders
            3. Contact DDoS mitigation service
            4. Engage ISP/network provider
            5. Activate backup infrastructure
            6. Begin traffic analysis
            7. Document all actions taken
            """)
        
        with col2:
            st.markdown("**Who to Contact:**")
            st.markdown("""
            - **Law Enforcement:** FBI, local cybercrime units
            - **ISP Support:** Contact your internet service provider
            - **DDoS Services:** Cloudflare, AWS Shield, Akamai
            - **CERT/CC:** cert@cert.org (US-CERT)
            - **Cybersecurity Firms:** For professional mitigation
            """)
# ===== TAB 4: ADMIN DASHBOARD =====
if st.session_state.get("admin") and 'tab4' in locals() and tab4:
    with tab4:

        st.markdown("## 🛠️ Admin Dashboard")
        st.markdown("### 📂 Login Logs (Excel Data)")

        if os.path.exists(LOG_FILE):

            df = pd.read_excel(LOG_FILE)

            st.dataframe(df, use_container_width=True)

            st.markdown("---")

            # Total logins
            st.markdown("### 📊 Login Count Per User")
            user_counts = df["Username"].value_counts()
            st.bar_chart(user_counts)

            # Success vs Failed
            st.markdown("### 📈 Success vs Failed Attempts")
            status_counts = df["Status"].value_counts()
            st.bar_chart(status_counts)

            # Logins over time
            st.markdown("### 📅 Login Activity Over Time")
            df["Time"] = pd.to_datetime(df["Time"])
            time_counts = df.groupby(df["Time"].dt.date).size()
            st.line_chart(time_counts)

        else:
            st.warning("No login logs available yet.")
if st.session_state.logged_in:
    st.markdown("---")
    st.markdown("### System Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Current Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col2:
        st.markdown("**AI Mode:** Active")
    with col3:
        st.markdown(f"**System Status:** Operational ✓")
