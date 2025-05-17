# Configuration loader for Hue Email Automation
import os
import json
import sys

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

def get_config_path():
	"""Get the path to the config file based on the application's location"""
	if getattr(sys, 'frozen', False):
		# Running as a bundled exe
		app_dir = os.path.dirname(sys.executable)
	else:
		# Running as a script
		app_dir = os.path.dirname(os.path.abspath(__file__))
		
	return os.path.join(app_dir, 'hue_config.json')

def create_default_config(config_path):
	"""Create a default configuration file"""
	with open(config_path, 'w') as config_file:
		json.dump(DEFAULT_CONFIG, config_file, indent=4)
	print(f"Created default configuration file at: {config_path}")

def load_config():
	"""Load configuration from file or create default if it doesn't exist"""
	config_path = get_config_path()
	
	# Create default config if file doesn't exist
	if not os.path.exists(config_path):
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
	print("Current configuration:")
	for key, value in CONFIG.items():
		# Don't print password
		if "password" in key:
			print(f"{key}: ****")
		else:
			print(f"{key}: {value}")
