# Configuration loader for Hue Email Automation
import os
import json
import sys
import tempfile

# Default configuration
DEFAULT_CONFIG = {
	# Hue Bridge Configuration
	"hue_bridge_ip": "192.168.1.x",
	"hue_api_key": "your_api_key",

	# Email Configuration (Gmail)
	"email_address": "your.email@gmail.com",
	"email_app_password": "your_app_password",
	"email_check_interval": 60,

	# Triggers
	"email_senders": ["important.sender@example.com"],
	"email_subjects": ["urgent", "alert"],

	# Light Configuration
	"light_group": "All",
	"flicker_times": 5,
	"flicker_interval": 0.2
}

def get_application_path():
	"""Get the real application path, even when running as a PyInstaller bundle"""
	if getattr(sys, 'frozen', False):
		# If the application is run as a PyInstaller bundle
		if hasattr(sys, '_MEIPASS'):
			# PyInstaller creates a temp folder and stores its path in _MEIPASS
			# BUT we don't want the temp path, we want the actual EXE location
			return os.path.dirname(sys.executable)
		else:
			return os.path.dirname(sys.executable)
	else:
		# Running as a normal Python script
		return os.path.dirname(os.path.abspath(__file__))

def get_config_path():
	"""Get the path to the config file based on the application's actual location"""
	app_dir = get_application_path()
	config_path = os.path.join(app_dir, 'hue_config.json')
	return config_path

def create_default_config(config_path):
	"""Create a default configuration file"""
	try:
		with open(config_path, 'w') as config_file:
			json.dump(DEFAULT_CONFIG, config_file, indent=4)
		print(f"Created default configuration file at: {config_path}")
	except Exception as e:
		print(f"Warning: Could not create default config file: {e}")
		print("Will use default configuration in memory instead")

def load_config():
	"""Load configuration from file or create default if it doesn't exist"""
	config_path = get_config_path()
	print(f"Looking for configuration at: {config_path}")
	
	# Create default config if file doesn't exist
	if not os.path.exists(config_path):
		print(f"Config file not found: {config_path}")
		create_default_config(config_path)
	
	# Load config
	try:
		with open(config_path, 'r') as config_file:
			config = json.load(config_file)
		print(f"Loaded configuration from: {config_path}")
		return config
	except Exception as e:
		print(f"Error loading configuration: {e}")
		print("Using default configuration")
		return DEFAULT_CONFIG

# Global configuration that will be used by other modules
CONFIG = load_config()

# For backwards compatibility with existing code - these variables 
# match the names used in the original config.py
HUE_BRIDGE_IP = CONFIG["hue_bridge_ip"]
HUE_API_KEY = CONFIG["hue_api_key"]
EMAIL_ADDRESS = CONFIG["email_address"]
EMAIL_APP_PASSWORD = CONFIG["email_app_password"]
EMAIL_CHECK_INTERVAL = CONFIG["email_check_interval"]
EMAIL_SENDERS = CONFIG["email_senders"]
EMAIL_SUBJECTS = CONFIG["email_subjects"]
LIGHT_GROUP = CONFIG["light_group"]
FLICKER_TIMES = CONFIG["flicker_times"]
FLICKER_INTERVAL = CONFIG["flicker_interval"]

# For testing
if __name__ == "__main__":
	print("Application path:", get_application_path())
	print("Config path:", get_config_path())
	print("Current configuration:")
	for key, value in CONFIG.items():
		# Don't print password
		if "password" in key:
			print(f"{key}: ****")
		else:
			print(f"{key}: {value}")
