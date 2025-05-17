# Main script for Hue Email Automation
import time
import os
import sys
from datetime import datetime
from hue_controller import HueController
from gmail_monitor import GmailMonitor
# Import from config_loader instead of config
from config_loader import (
	LIGHT_GROUP,
	FLICKER_TIMES,
	FLICKER_INTERVAL,
	CONFIG
)

def handle_trigger_email(email_message):
	"""Handle a triggering email by flickering lights"""
	sender = email_message.get('From', 'Unknown Sender')
	subject = email_message.get('Subject', 'No Subject')

	print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Trigger received!")
	print(f"From: {sender}")
	print(f"Subject: {subject}")

	# Initialize Hue controller
	hue = HueController()

	try:
		# Find group ID if needed
		if LIGHT_GROUP.isdigit():
			group_id = LIGHT_GROUP
		else:
			group_id = hue.find_group_id(LIGHT_GROUP)

		print(f"Flickering {LIGHT_GROUP} (ID: {group_id})...")
		result = hue.flicker_group(
			group_id=group_id,
			times=FLICKER_TIMES,
			interval=FLICKER_INTERVAL
		)

		if result:
			print("Lights flickered successfully!")
		else:
			print("Failed to flicker lights")

	except Exception as e:
		print(f"Error during light control: {e}")

def print_config_path():
	"""Print the path to the configuration file"""
	if getattr(sys, 'frozen', False):
		# Running as a bundled exe
		app_dir = os.path.dirname(sys.executable)
	else:
		# Running as a script
		app_dir = os.path.dirname(os.path.abspath(__file__))

	config_path = os.path.join(app_dir, 'hue_config.json')
	print(f"Configuration file: {config_path}")
	return config_path

def main():
	"""Main function to run the automation"""
	print("=" * 50)
	print("HUE EMAIL AUTOMATION".center(50))
	print("=" * 50)

	# Print configuration info
	print_config_path()
	print("\nCurrent configuration:")
	for key, value in CONFIG.items():
		# Don't print password
		if "password" in key:
			print(f"  {key}: ****")
		else:
			print(f"  {key}: {value}")

	# Test Hue connection first
	try:
		hue = HueController()
		groups = hue.get_all_groups()
		print(f"\nConnected to Hue Bridge successfully!")
		print(f"Found {len(groups)} light groups")

		# Validate configured group
		try:
			if LIGHT_GROUP.isdigit():
				group_id = LIGHT_GROUP
			else:
				group_id = hue.find_group_id(LIGHT_GROUP)
			group_info = hue.get_group_state(group_id)
			print(f"Target group '{LIGHT_GROUP}' (ID: {group_id}) is valid")
			print(f"Group has {len(group_info.get('lights', []))} lights")
		except Exception as e:
			print(f"Error with configured light group: {e}")
			print("Please check your 'light_group' setting in the configuration file")
			return

	except Exception as e:
		print(f"Failed to connect to Hue Bridge: {e}")
		print("Please check your 'hue_bridge_ip' and 'hue_api_key' in the configuration file")
		return

	# Start email monitoring
	monitor = GmailMonitor()

	try:
		# Do initial check without callbacks to avoid triggering on existing emails
		print("\nDoing initial email check...")
		monitor.check_for_triggers()
		print("Initial check complete. Starting continuous monitoring...\n")

		# Start continuous monitoring
		monitor.monitor_continuously(handle_trigger_email)

	except Exception as e:
		print(f"Error in email monitoring: {e}")
		print("Please check your email configuration in the configuration file")
		return

if __name__ == "__main__":
	main()
