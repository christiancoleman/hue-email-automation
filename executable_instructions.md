# Creating an Executable with External Configuration

This document explains how to build and use the Hue Email Automation executable with external configuration.

## Building the Executable

1. Make sure PyInstaller is installed:
	```
	pip install pyinstaller
	```

2. Build using the provided spec file:
	```
	pyinstaller hue.spec
	```

	This will create a `dist` folder containing `hue-email-automation.exe`.

3. Alternatively, build with command line options:
	```
	pyinstaller --onefile --add-data "hue_config.json;." main.py
	```

## Configuration

The executable will look for a file named `hue_config.json` in the same directory as the executable. This allows you to:

1. Change settings without rebuilding the executable
2. Share the executable with others who can adjust their own settings

If no config file is found, a default one will be created automatically.

## What to Configure

Edit the `hue_config.json` file to customize:

```json
{
	"hue_bridge_ip": "192.168.1.x",
	"hue_api_key": "your_api_key",
	"email_address": "your.email@gmail.com",
	"email_app_password": "your_app_password",
	"email_check_interval": 60,
	"email_senders": ["important.sender@example.com"],
	"email_subjects": ["urgent", "alert"],
	"light_group": "All",
	"flicker_times": 5,
	"flicker_interval": 0.2
}
```

## Using the Executable

1. Place `hue-email-automation.exe` and `hue_config.json` in the same folder
2. Edit `hue_config.json` with your settings
3. Run the executable

## Running as a Background Service

For a Windows system:

1. Create a scheduled task:
	- Open Task Scheduler
	- Create a new task
	- Set to run at startup
	- Action: Start a program
	- Program/script: path to your exe
	- Start in: folder containing your exe

For hiding the console window, change `console=True` to `console=False` in the spec file and rebuild.
