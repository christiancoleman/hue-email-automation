# Main script for Hue Email Automation
import time
from datetime import datetime
from hue_controller import HueController
from gmail_monitor import GmailMonitor
from config import LIGHT_GROUP, FLICKER_TIMES, FLICKER_INTERVAL

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

def main():
	"""Main function to run the automation"""
	print("=" * 50)
	print("HUE EMAIL AUTOMATION".center(50))
	print("=" * 50)
	
	# Test Hue connection first
	try:
		hue = HueController()
		groups = hue.get_all_groups()
		print(f"Connected to Hue Bridge successfully!")
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
			print("Please check your LIGHT_GROUP setting in config.py")
			return
	
	except Exception as e:
		print(f"Failed to connect to Hue Bridge: {e}")
		print("Please check your HUE_BRIDGE_IP and HUE_API_KEY in config.py")
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
		print("Please check your email configuration in config.py")
		return

if __name__ == "__main__":
	main()
