# Hue Email Automation

A Python application that monitors Gmail for specific messages and triggers Philips Hue lights to flicker - perfect for important notifications or alerts.

## Features

- **Email Monitoring**: Detect emails from specific senders or with specific keywords in the subject
- **Light Control**: Flicker any Hue light group (rooms, zones, etc.)
- **External Configuration**: Use a JSON config file that can be modified without rebuilding
- **Modular Design**: Each component can be tested separately
- **Executable Support**: Can be packaged as a standalone Windows executable

## Project Structure

- `config_loader.py` - Loads configuration from external JSON file
- `hue_config.json` - External configuration file (created automatically if missing)
- `hue_controller.py` - Philips Hue API interface
- `gmail_monitor.py` - Gmail monitoring module
- `main.py` - Main script that ties everything together
- `gmail_setup.md` - Instructions for Gmail app password setup
- `hue.spec` - PyInstaller specification for building the executable
- `executable_instructions.md` - Detailed guide for building and using the executable

## Setup & Installation

### 1. Install Dependencies
```
pip install requests
```

### 2. Configure the Application
Edit `hue_config.json` with your settings:
```json
{
	"hue_bridge_ip": "192.168.1.x",
	"hue_api_key": "your_api_key",
	"email_address": "your.email@gmail.com",
	"email_app_password": "your_app_password",
	"email_check_interval": 15,
	"email_senders": ["important@example.com"],
	"email_subjects": ["urgent", "alert"],
	"light_group": "All",
	"flicker_times": 5,
	"flicker_interval": 0.2
}
```

### 3. Get Your Hue API Key
If you don't have a Hue API key:
1. Edit `hue_config.json` with your Hue Bridge IP address
2. Run `python hue_controller.py`
3. When prompted, press the link button on your Hue Bridge
4. Copy the API key that's generated and update `hue_config.json`

### 4. Configure Gmail Access
Follow the instructions in `gmail_setup.md` to create a Gmail app password:
1. Go to your Google Account → Security → 2-Step Verification
2. Enable 2-Step Verification if not already enabled
3. Scroll down to "App passwords" and create a new one
4. Copy the 16-character password to `hue_config.json`

## Running the Application

### As Python Script
```
python main.py
```

### As Executable
1. Install PyInstaller: `pip install pyinstaller`
2. Build using spec file: `pyinstaller hue.spec`
3. Run the generated executable in `dist/hue-email-automation.exe`

## Email Trigger Logic

The application will monitor for emails that match EITHER:
- From ANY sender in the `email_senders` list OR
- Containing ANY keyword in the `email_subjects` list

This provides flexibility to monitor for multiple conditions simultaneously.

## Customizing Behavior

All settings can be adjusted in `hue_config.json`:

```json
{
	"hue_bridge_ip": "192.168.x.x",
	"hue_api_key": "your_api_key",
	"email_address": "youremail@gmail.com",
	"email_app_password": "your_app_password",
	"email_check_interval": 15,
	"email_senders": [
		"no-reply@noa.nintendo.com", 
		"nintendo-noreply@nintendo.net"
	],
	"email_subjects": [
		"potato", 
		"new"
	],
	"light_group": "All",
	"flicker_times": 5,
	"flicker_interval": 0.2
}
```

## Running as a Background Service

### Windows
1. Use Task Scheduler to run the executable at startup:
   - Action: Start a program
   - Program: Path to your exe
   - "Start in": Folder containing your exe

### Adding to Startup
Create a shortcut to the executable in:
`C:\Users\[Username]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

## Troubleshooting

### Diagnostics
Run individual modules directly for testing:
- `python hue_controller.py` - Test Hue connection
- `python gmail_monitor.py` - Test Gmail monitoring
- `python gmail_monitor.py --all` - Test with all emails (including read ones)
- `python gmail_monitor.py --monitor` - Run continuous monitoring

### Common Issues
- **No API key**: Run `python hue_controller.py` to generate one
- **Email connectivity**: Verify app password and account settings
- **Unicode errors**: The application handles special characters, but check email subjects/addresses for unusual characters
- **Lights not found**: Verify group names match exactly as shown in the Hue app

### Useful Resources
- Hue Developer Documentation: https://developers.meethue.com/develop/get-started-2/
- Find your Hue Bridge IP: https://discovery.meethue.com/
- Hue Debug Tool: https://[bridge-ip]/debug/clip.html

## Development Notes

### External Configuration
The application uses `config_loader.py` to manage external configuration. When packaged as an executable:
1. It looks for `hue_config.json` in the same directory as the executable
2. If not found, it creates a default configuration file
3. All settings can be modified without rebuilding

### PyInstaller
- The `hue.spec` file contains the build specification for PyInstaller
- It includes `hue_config.json` in the build automatically
- Build the executable with: `pyinstaller hue.spec`

### Console vs. Hidden Mode
- The current spec file builds with a console window (`console=True`)
- For a hidden background application, change to `console=False` in the spec file and rebuild
