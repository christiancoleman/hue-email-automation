# Hue Email Automation

A Python script that monitors for specific emails and triggers Philips Hue lights to flicker.

## Setup

1. Install required packages:
```
pip install requests
```

2. Configure your settings in `config.py`:
	- Hue Bridge IP and API key
	- Gmail credentials (see `gmail_setup.md`)
	- Email trigger settings
	- Light group settings

3. Run the script:
```
python main.py
```

## First Run & API Key

If you don't have a Hue API key:
1. Edit `config.py` with your Hue Bridge IP address
2. Run `python hue_controller.py`
3. When prompted, press the link button on your Hue Bridge
4. Copy the API key that's generated and update `config.py`

## Project Structure

- `config.py` - Configuration settings
- `hue_controller.py` - Philips Hue API interface
- `gmail_monitor.py` - Gmail monitoring module
- `main.py` - Main script that ties everything together
- `gmail_setup.md` - Instructions for Gmail app password

## Customizing Triggers

Edit `config.py` to change:
- Which email senders trigger the lights
- Which keywords in email subjects trigger the lights
- How the lights flicker (times and interval)
- Which light group to control

## Running as a Service

To run continuously in the background:
1. Windows: Use Task Scheduler to run on startup
2. Linux: Create a systemd service
3. Mac: Create a launchd service

## Troubleshooting

- If lights don't flicker, check your Hue Bridge IP and API key
- If emails aren't detected, verify your Gmail app password
- Run individual modules directly for testing:
	- `python hue_controller.py` - Test Hue connection
	- `python gmail_monitor.py` - Test Gmail monitoring

## FYI FUTURE ME

- Documentation on how to use Hue as a dev: https://developers.meethue.com/develop/get-started-2/
- Can use https://discovery.meethue.com/ to find your IP address
- Go to https://<bridge ip address>/debug/clip.html
	- Ex: https://192.168.68.63/debug/clip.html

## CONFIG.PY NEEDED - EXAMPLE BELOW:

```python
# Hue Email Automation - Configuration
# Fill in your personal configuration details here

# Hue Bridge Configuration
HUE_BRIDGE_IP = ""  # Replace with your Hue Bridge IP
HUE_API_KEY = ""   # Replace with the API key/username from registration

# Email Configuration (Gmail)
EMAIL_ADDRESS = ""
EMAIL_APP_PASSWORD = ""  # Gmail app-specific password
EMAIL_CHECK_INTERVAL = 15  # Seconds between email checks

# Triggers
# The script will trigger if an email meets EITHER of these criteria:
# 1. The email is from ANY sender in the EMAIL_SENDERS list
# 2. The email subject contains ANY keyword in the EMAIL_SUBJECTS list
#
# For example, with the settings below, the script will trigger for:
# - Any email from nintendo-noreply@nintendo.net OR
# - Any email from no-reply@noa.nintendo.com OR
# - Any email with "potato" in the subject OR
# - Any email with "new" in the subject
EMAIL_SENDERS = [""]
EMAIL_SUBJECTS = [""]  

# To only trigger on specific senders (no subject matching), leave EMAIL_SUBJECTS as an empty list:
# EMAIL_SUBJECTS = []

# To only trigger on specific subjects (any sender), leave EMAIL_SENDERS as an empty list:
# EMAIL_SENDERS = []

# Light Configuration
LIGHT_GROUP = ""  # Group name or ID to flicker
FLICKER_TIMES = 5    # Number of flicker cycles
FLICKER_INTERVAL = 0.2  # Seconds between state changes
```
