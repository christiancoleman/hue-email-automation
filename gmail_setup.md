# Gmail App Password Setup

To monitor Gmail using this script, you'll need to create an App Password:

1. Go to your Google Account → Security → 2-Step Verification
	https://myaccount.google.com/security

2. Make sure 2-Step Verification is enabled

3. Scroll down and click on "App passwords"

4. Select "Mail" as the app and "Other" as the device
	- Name it something like "Hue Email Automation"

5. Click "Generate"

6. Copy the 16-character password provided

7. Paste it in the config.py file for EMAIL_APP_PASSWORD

Note: Google doesn't show app passwords again after generation, so save it securely.
