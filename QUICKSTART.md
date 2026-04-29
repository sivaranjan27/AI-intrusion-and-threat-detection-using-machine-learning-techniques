# Quick Start Guide - Security Attack Detection System

Get up and running in 5 minutes!

## Step 1: Install & Run (2 minutes)

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Navigate to `http://localhost:3000` - you should see the application!

## Step 2: Prepare Test Data (1 minute)

Create a simple Excel file (`test-credentials.xlsx`) with:

| username | password |
|----------|----------|
| john     | pass123  |
| admin    | admin456 |
| user1    | test789  |

## Step 3: Test Login Tab (1 minute)

1. Go to **Login & Attacks** tab
2. Click **Choose File** and select your Excel file
3. Login attempts:
   - **Correct credentials**: Use `john` / `pass123` → Success!
   - **Wrong password**: Try `john` / `wrongpass` 6 times → See attack alert!

## Step 4: Test Phishing Detection (1 minute)

1. Go to **Phishing Detection** tab
2. Try these URLs:
   - `https://www.google.com` → Shows "Legitimate"
   - `https://paypal-verify.com` → Shows "Phishing Detected"
   - `http://192.168.1.1/login` → Shows "Suspicious"

## Optional: Setup Email Alerts

To receive actual email alerts when attacks are detected:

### For Gmail:
1. Go to [Google Account Security](https://myaccount.google.com/apppasswords)
2. Enable 2-Step Verification
3. Generate an App Password
4. Create `.env.local`:
   ```
   GMAIL_USER=your-email@gmail.com
   GMAIL_APP_PASSWORD=your-app-password
   ADMIN_EMAIL=your-admin-email@gmail.com
   ```
5. Restart the server: `npm run dev`

### For Other Email Services:
Update `.env.local` with your SMTP details:
```
SMTP_HOST=smtp.provider.com
SMTP_PORT=587
SMTP_SECURE=false
SMTP_USER=your-email@provider.com
SMTP_PASS=your-password
ADMIN_EMAIL=admin@yourcompany.com
```

## Features Overview

### Tab 1: Login & Attack Detection
- Upload Excel credentials
- Test login attempts
- View attack detection
- See alert details

### Tab 2: Phishing Detection
- Enter any URL
- Get phishing risk score
- View feature analysis
- Safe/phishing recommendation

### Tab 3: DOS Attack Info
- Learn about DOS/DDoS attacks
- Review prevention strategies
- Read incident response guide
- Find contact resources

### Chatbot (Floating Widget)
- Ask about any attack type
- Get security recommendations
- Click message icon to open

## Testing Attack Detection

### To Trigger Attack Alert:
1. Upload Excel file with credentials
2. Enter a username (e.g., "john")
3. Try wrong passwords 6+ times
4. Check the alert that appears
5. If email configured, check inbox

### Attack Types Shown:
- **Brute Force**: Rapid failed attempts
- **Dictionary**: Using common passwords
- **Rainbow**: Excessive attempts (8+)

## Troubleshooting

### Can't find http://localhost:3000?
- Make sure `npm run dev` is running
- Check port 3000 isn't in use
- Try `http://127.0.0.1:3000`

### Excel file won't load?
- Make sure columns are named "username" and "password"
- Save as .xlsx format
- No empty rows between data

### Email not sending?
- Check `.env.local` configuration
- Verify Gmail App Password (not regular password)
- Check admin email is correct
- Look for error in terminal

### Chatbot not responding?
- Refresh the page
- Check browser console for errors
- Verify `/api/chat` route is accessible

## Project Structure

```
security-detection/
├── app/
│   ├── page.tsx          ← Main dashboard
│   ├── api/
│   │   ├── chat/         ← Chatbot API
│   │   └── send-alert/   ← Email alerts
│   └── globals.css       ← Design system
├── components/
│   ├── tabs/             ← Attack tabs
│   └── Chatbot.tsx       ← Chat widget
├── package.json          ← Dependencies
├── .env.local           ← Your config
└── README.md            ← Full docs
```

## Key Files to Know

| File | Purpose |
|------|---------|
| `app/page.tsx` | Main dashboard layout |
| `components/tabs/LoginTab.tsx` | Login & brute force detection |
| `components/tabs/PhishingTab.tsx` | URL phishing analysis |
| `components/tabs/DOSTab.tsx` | DOS attack education |
| `components/Chatbot.tsx` | Chat widget UI |
| `app/api/chat/route.ts` | Chat responses |
| `app/api/send-alert/route.ts` | Email alerts |
| `app/globals.css` | Colors & design tokens |

## Common Customizations

### Change Colors
Edit colors in `app/globals.css`:
```css
:root {
  --primary: oklch(...);  /* Change this */
  --accent: oklch(...);   /* And this */
}
```

### Update Email Template
Edit HTML in `app/api/send-alert/route.ts` - look for `emailHtml` variable

### Add More Attack Types
1. Update `SECURITY_RESPONSES` in `app/api/chat/route.ts`
2. Add detection logic in `components/tabs/LoginTab.tsx`
3. Update email template in `app/api/send-alert/route.ts`

### Customize Phishing Detection
Edit `analyzePhishingRisk()` function in `components/tabs/PhishingTab.tsx` to:
- Add new features
- Adjust scoring weights
- Change risk thresholds

## Deployment

### Deploy to Vercel (1 click!)
```bash
npm install -g vercel
vercel
```

### Deploy Elsewhere
```bash
npm run build
npm start
```

## Next Steps

1. ✅ Run locally: `npm run dev`
2. ✅ Test all features
3. ✅ Setup email (optional)
4. ✅ Customize as needed
5. ✅ Deploy to production

## Getting Help

- Read `README.md` for detailed documentation
- Check `FEATURES.md` for feature list
- Review code comments in components
- Check browser console for errors

## Tips & Tricks

- Use the example URLs in Phishing tab for testing
- Try different password combinations to see different attack types
- Refresh page to reset failed attempts counter
- Minimize chatbot to save screen space
- Test on mobile to check responsive design
- Check dark mode by toggling system theme

---

**Congratulations! You now have a fully functional Security Attack Detection System!**

For more advanced setup and customization, see the full `README.md` file.
