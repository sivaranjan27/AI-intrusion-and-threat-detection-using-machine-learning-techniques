# Security Attack Detection & Prevention System

A comprehensive web application that detects, analyzes, and educates users about five different types of cybersecurity attacks: Brute Force, Dictionary, Rainbow, Phishing, and DOS/DDoS attacks.

## Features

### 1. Login Page with Attack Detection (Tab 1)
- **Excel Credentials Upload**: Load credentials from an Excel file with username and password columns
- **Real-time Attack Detection**: Monitors login attempts and automatically detects:
  - **Brute Force Attack**: Multiple rapid failed attempts
  - **Dictionary Attack**: Attempts using common passwords
  - **Rainbow Attack**: Excessive attempts (8+ failed tries)
- **Automatic Email Alerts**: Sends detailed alert emails to admin when attacks are detected
- **Failed Attempt Tracking**: Visual display of failed login attempts per user

### 2. Phishing Link Detection (Tab 2)
- **URL Analysis**: Enter any URL to analyze for phishing characteristics
- **Feature-Based Detection**: Analyzes:
  - URL length and structure
  - HTTPS/SSL certificate status
  - Suspicious keywords in pathname
  - IP address in domain
  - Special character frequency
  - Domain reputation
- **Risk Score**: Displays confidence percentage (0-100%)
- **Detailed Insights**: Feature-by-feature risk assessment
- **Real-time Feedback**: Visual indicators for safe vs. phishing URLs

### 3. DOS Attack Information (Tab 3)
- **Educational Content**: Comprehensive guide to Denial of Service attacks
- **Attack Types**: Detailed explanations of:
  - Ping Floods
  - SYN Floods
  - UDP Floods
  - HTTP Floods
  - Distributed DoS (DDoS)
- **Prevention Strategies**: 
  - Firewall configuration
  - CDN and load balancing
  - Real-time monitoring
  - System patching
  - Backup and redundancy
- **Incident Response Guide**: Step-by-step actions during an attack
- **Contact Information**: Resources for reporting and getting help

### 4. AI-Powered Security Chatbot
- **24/7 Availability**: Floating chatbot widget for instant answers
- **Intelligent Responses**: Rule-based responses covering all 5 attack types
- **Gemini AI Integration** (Optional): Enhanced responses using Google's Gemini API
- **Conversation Memory**: Maintains context across multiple messages
- **Minimizable Interface**: Can be minimized or closed as needed

## Tech Stack

- **Frontend**: Next.js 14, React 19, TypeScript
- **Styling**: Tailwind CSS, Shadcn/ui
- **Backend**: Next.js API Routes
- **File Processing**: XLSX for Excel parsing
- **Email Service**: Nodemailer (Gmail/SMTP)
- **AI Integration**: Google Gemini API (optional)
- **Icons**: Lucide React

## Installation

1. **Clone or download the project**

2. **Install dependencies**
   ```bash
   npm install
   # or
   pnpm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```

4. **Configure environment variables** (see Configuration section below)

5. **Run the development server**
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

6. **Open your browser**
   Navigate to `http://localhost:3000`

## Configuration

### Email Service Setup

#### Option 1: Gmail (Recommended)
1. Go to [Google Account Security](https://myaccount.google.com/apppasswords)
2. Enable 2-Step Verification if not already enabled
3. Generate an App Password for "Mail" and "Windows Computer"
4. Copy the 16-character password
5. Add to `.env.local`:
   ```
   GMAIL_USER=your-email@gmail.com
   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
   ADMIN_EMAIL=admin@yourcompany.com
   ```

#### Option 2: Custom SMTP
Add to `.env.local`:
```
SMTP_HOST=smtp.yourprovider.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@provider.com
SMTP_PASS=your-password
ADMIN_EMAIL=admin@yourcompany.com
```

### Gemini AI Setup (Optional)
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Click "Create API Key" in your Google Cloud project
3. Copy the API key
4. Add to `.env.local`:
   ```
   GOOGLE_GENERATIVE_AI_API_KEY=your-api-key
   ```

## Usage Guide

### Testing Login Security (Tab 1)

1. **Prepare Excel File**:
   - Create a spreadsheet with columns: `username`, `password`
   - Example:
     ```
     username    password
     john        secure123
     admin       password456
     user1       test789
     ```

2. **Upload File**: Click "Choose File" and select your Excel file

3. **Test Logins**:
   - Enter correct credentials to trigger successful login
   - Enter wrong passwords repeatedly to trigger attack detection
   - After 5 failed attempts, the system will trigger a security alert

4. **Review Alerts**:
   - Check the alert panel for detected attack types
   - Admin will receive email notification

### Testing Phishing Detection (Tab 2)

1. **Enter URLs** to test (examples provided):
   - `https://www.google.com` (legitimate)
   - `https://paypal-verify.com` (phishing attempt)
   - `http://192.168.1.1/login` (suspicious)

2. **Review Results**:
   - Check risk score and classification
   - Review individual feature analysis
   - Read recommendations

### Learning about DOS (Tab 3)

1. **Read Overview**: Understand what DOS attacks are
2. **Explore Types**: Learn different attack methods
3. **Study Prevention**: Review defense strategies
4. **Check Resources**: Find contacts and help resources

### Chatting with Security Assistant

1. **Open Chatbot**: Click the message icon in bottom-right
2. **Ask Questions**: 
   - "What is a brute force attack?"
   - "How do I prevent phishing?"
   - "Tell me about DOS attacks"
3. **Minimize/Close**: Use the minimize or close buttons

## Excel File Format

Create an Excel file with these columns:

| username | password |
|----------|----------|
| john_doe | SecurePass123! |
| admin    | AdminPass456! |
| user1    | TestPass789 |

- Column names are case-insensitive
- At least 2 columns (username, password) are required
- All rows with both username and password will be loaded

## Attack Detection Rules

### Brute Force Attack
- **Trigger**: > 5 failed attempts in a row
- **Indicator**: Rapid failed attempts with different passwords
- **Response**: Automatic email alert to admin

### Dictionary Attack
- **Trigger**: Failed attempts using common passwords (5+ attempts)
- **Common Passwords**: password, 123456, admin, etc.
- **Indicator**: Common words from password dictionary
- **Response**: Email alert specifying dictionary attack

### Rainbow Attack
- **Trigger**: Excessive attempts (8+ failed logins)
- **Indicator**: Suggests use of pre-computed hash tables
- **Response**: Email alert with attack classification

## Email Alert Example

When an attack is detected, the admin receives:
- **Subject**: Attack type and user ID
- **Content Includes**:
  - Attack type classification
  - User ID attempting login
  - Number of failed attempts
  - Timestamp of detection
  - Recommended actions
  - Attack description and prevention tips

## API Routes

### `POST /api/chat`
Handles chatbot messages
- **Request**: `{ messages: Array<{ role: string, content: string }> }`
- **Response**: `{ message: string }`

### `POST /api/send-alert`
Sends email alerts for detected attacks
- **Request**: `{ userId, attackType, attempts, timestamp }`
- **Response**: `{ success: boolean, message: string }`

## Customization

### Adding New Attack Types
1. Update `SECURITY_RESPONSES` in `/app/api/chat/route.ts`
2. Add detection logic in `/components/tabs/LoginTab.tsx`
3. Update email templates in `/app/api/send-alert/route.ts`

### Changing Color Scheme
1. Edit design tokens in `/app/globals.css`
2. Update dark mode colors in the `.dark` selector
3. Modify `tailwind.config.ts` if needed

### Modifying Phishing Detection Features
1. Edit `analyzePhishingRisk()` function in `/components/tabs/PhishingTab.tsx`
2. Add new feature extraction logic
3. Adjust risk scoring weights

## Deployment

### Vercel Deployment (Recommended)
```bash
npm install -g vercel
vercel
```

### Self-Hosted
```bash
npm run build
npm start
```

## Important Notes

1. **Excel Parsing**: Uses in-memory storage. Large files (1000+ rows) may impact performance.
2. **Email Service**: Requires proper SMTP configuration for production use.
3. **Security**: 
   - Never commit `.env.local` to version control
   - Use strong, unique admin email account
   - Keep API keys secure
4. **Development**: Phishing detection uses feature-based analysis, not ML models. For production ML models, integrate with TensorFlow or scikit-learn.

## Troubleshooting

### Email not sending
- Check GMAIL_USER and GMAIL_APP_PASSWORD are correct
- Verify 2-Step Verification is enabled on Gmail account
- Check that App Password (not regular password) is used
- Look for error logs in console

### Excel file not loading
- Ensure file has "username" and "password" column headers
- Check that columns contain text data (not formulas)
- Try saving file in Excel 2007 format (.xlsx)

### Chatbot not responding
- Check browser console for errors
- Verify API route is accessible
- Check that chat endpoint is properly configured

## Browser Compatibility
- Chrome/Edge: Full support
- Firefox: Full support  
- Safari: Full support
- IE11: Not supported

## Performance Optimization
- Lazy load tabs for faster initial page load
- Cache phishing analysis results
- Optimize image assets
- Use CSS minification in production

## License
MIT License - feel free to use and modify as needed

## Support
For issues or questions, create an issue in the repository or contact the development team.

---

**Made with Security in Mind** - Educating users about cyber threats and defenses.
