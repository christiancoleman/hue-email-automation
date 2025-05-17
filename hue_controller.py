# Hue API Connection Module
import requests
import json
import time
from config import HUE_BRIDGE_IP, HUE_API_KEY

class HueController:
	def __init__(self, bridge_ip=None, api_key=None):
		self.bridge_ip = bridge_ip or HUE_BRIDGE_IP
		self.api_key = api_key or HUE_API_KEY
		self.base_url = f"http://{self.bridge_ip}/api/{self.api_key}"
		
	def get_all_lights(self):
		"""Returns information about all lights connected to the bridge"""
		response = requests.get(f"{self.base_url}/lights")
		return response.json()
	
	def get_all_groups(self):
		"""Returns information about all light groups"""
		response = requests.get(f"{self.base_url}/groups")
		return response.json()
	
	def find_group_id(self, group_name):
		"""Find a group ID by name"""
		groups = self.get_all_groups()
		for group_id, group_data in groups.items():
			if group_data.get('name', '').lower() == group_name.lower():
				return group_id
		raise ValueError(f"Group '{group_name}' not found")
	
	def get_group_state(self, group_id):
		"""Gets the current state of a light group"""
		response = requests.get(f"{self.base_url}/groups/{group_id}")
		return response.json()
	
	def set_group_state(self, group_id, state):
		"""Sets the state of a light group"""
		response = requests.put(f"{self.base_url}/groups/{group_id}/action", json=state)
		return response.json()
	
	def flicker_group(self, group_name=None, group_id=None, times=5, interval=0.2):
		"""Make a group of lights flicker
		
		Args:
			group_name: Name of the group to flicker (optional if group_id provided)
			group_id: ID of the group to flicker (optional if group_name provided)
			times: Number of flicker cycles
			interval: Seconds between state changes
		"""
		# Resolve group ID if only name provided
		if group_id is None and group_name is not None:
			group_id = self.find_group_id(group_name)
		elif group_id is None and group_name is None:
			raise ValueError("Either group_name or group_id must be provided")
			
		# Get original state to restore later
		original_state = self.get_group_state(group_id)
		original_on = original_state.get('state', {}).get('all_on', True)
		original_bri = original_state.get('action', {}).get('bri', 254)
		
		try:
			# Ensure lights are on
			self.set_group_state(group_id, {"on": True})
			
			# Flicker sequence
			for _ in range(times):
				# Low brightness
				self.set_group_state(group_id, {"bri": 10, "transitiontime": 0})
				time.sleep(interval)
				# High brightness
				self.set_group_state(group_id, {"bri": 254, "transitiontime": 0})
				time.sleep(interval)
				
			# Restore original state
			restore_state = {"bri": original_bri}
			if not original_on:
				# Wait a moment before turning off to ensure the last state change was seen
				time.sleep(interval * 2)
				restore_state["on"] = False
				
			self.set_group_state(group_id, restore_state)
			
			return True
		except Exception as e:
			print(f"Error during light flickering: {e}")
			return False

# Function to help generate API key
def generate_api_key(bridge_ip):
	"""Helper function to generate a Hue API key
	
	Make sure to press the link button on your bridge before calling this function
	
	Returns:
		API key string or None if request failed
	"""
	try:
		response = requests.post(f"http://{bridge_ip}/api", 
							   json={"devicetype":"hue_email_automation"})
		result = response.json()
		
		if 'success' in result[0]:
			return result[0]['success']['username']
		elif 'error' in result[0]:
			print(f"Error: {result[0]['error']['description']}")
			return None
	except Exception as e:
		print(f"Failed to generate API key: {e}")
		return None

# For testing this module
if __name__ == "__main__":
	# Test connection to bridge
	from config import HUE_BRIDGE_IP, HUE_API_KEY, LIGHT_GROUP, FLICKER_TIMES, FLICKER_INTERVAL
	
	# If API key is not configured, try to generate one
	if HUE_API_KEY == "your_api_key":
		print("No API key configured. Press the link button on your Hue bridge, then press Enter...")
		input()
		api_key = generate_api_key(HUE_BRIDGE_IP)
		if api_key:
			print(f"Generated API key: {api_key}")
			print("Update this key in config.py")
		else:
			print("Failed to generate API key")
	else:
		# Test light control
		hue = HueController()
		print("Testing connection to Hue bridge...")
		groups = hue.get_all_groups()
		print(f"Found {len(groups)} groups: {', '.join([g.get('name', f'ID: {id}') for id, g in groups.items()])}")
		
		try:
			if LIGHT_GROUP.isdigit():
				group_id = LIGHT_GROUP
			else:
				group_id = hue.find_group_id(LIGHT_GROUP)
				
			print(f"Flickering {LIGHT_GROUP} (ID: {group_id})...")
			hue.flicker_group(group_id=group_id, times=FLICKER_TIMES, interval=FLICKER_INTERVAL)
			print("Flickering complete")
		except Exception as e:
			print(f"Error: {e}")
