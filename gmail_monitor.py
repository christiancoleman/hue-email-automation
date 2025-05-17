# Gmail Monitoring Module
import imaplib
import email
import time
import re
from datetime import datetime
# Import from config_loader instead of config
from config_loader import (
	EMAIL_ADDRESS, 
	EMAIL_APP_PASSWORD, 
	EMAIL_CHECK_INTERVAL,
	EMAIL_SENDERS,
	EMAIL_SUBJECTS
)

class GmailMonitor:
	def __init__(self, email_address=None, password=None):
		self.email_address = email_address or EMAIL_ADDRESS
		self.password = password or EMAIL_APP_PASSWORD
		self.server = "imap.gmail.com"
		self.last_check_time = None
		self.first_run = True  # Flag to track first run
		
	def _connect(self):
		"""Connect to Gmail IMAP server"""
		mail = imaplib.IMAP4_SSL(self.server)
		mail.login(self.email_address, self.password)
		return mail
	
	def _sanitize_for_imap(self, text):
		"""Sanitize text for IMAP search by removing or replacing non-ASCII characters"""
		# Replace smart/curly quotes and apostrophes with straight ones
		text = text.replace('\u2018', "'").replace('\u2019', "'")
		text = text.replace('\u201c', '"').replace('\u201d', '"')
		
		# Remove any remaining non-ASCII characters
		return ''.join(c for c in text if ord(c) < 128)
	
	def _build_search_criteria(self):
		"""
		Build IMAP search criteria that works as an OR between sender and subject
		"""
		search_parts = []
		
		# Only check for unread emails after the first run
		if not self.first_run:
			search_parts.append("UNSEEN")
		
		# Create combined OR search for senders and subjects
		or_conditions = []
		
		# Add sender criteria
		for sender in EMAIL_SENDERS:
			# Sanitize the email for IMAP search
			safe_sender = self._sanitize_for_imap(sender.replace('"', '\\"'))
			or_conditions.append(f'FROM "{safe_sender}"')
		
		# Add subject criteria 
		for subject in EMAIL_SUBJECTS:
			# Sanitize the subject for IMAP search
			safe_subject = self._sanitize_for_imap(subject.replace('"', '\\"'))
			or_conditions.append(f'SUBJECT "{safe_subject}"')
		
		# Only add the OR part if we have conditions
		if or_conditions:
			# For a single condition, no need for OR
			if len(or_conditions) == 1:
				search_parts.append(or_conditions[0])
			else:
				# IMAP OR syntax: (OR criteria1 criteria2)
				# Build nested OR conditions for multiple terms
				search_expr = self._build_or_expression(or_conditions)
				search_parts.append(search_expr)
		
		return " ".join(search_parts) if search_parts else "ALL"
	
	def _build_or_expression(self, conditions):
		"""Build a properly formatted IMAP OR expression"""
		if len(conditions) == 1:
			return conditions[0]
		elif len(conditions) == 2:
			return f'(OR {conditions[0]} {conditions[1]})'
		else:
			# For more than 2 conditions, we need to nest OR expressions
			# (OR condition1 (OR condition2 condition3))
			result = conditions[-2:]
			result = f'(OR {result[0]} {result[1]})'
			
			for i in range(len(conditions)-3, -1, -1):
				result = f'(OR {conditions[i]} {result})'
			
			return result
		
	def check_for_triggers(self, callback=None):
		"""
		Check for emails matching trigger criteria - emails match if they are from
		any sender in EMAIL_SENDERS OR contain any subject keyword in EMAIL_SUBJECTS
		
		Args:
			callback: Function to call when matching email found.
					 Will receive the email message object as an argument.
		
		Returns:
			List of matching email messages
		"""
		try:
			mail = self._connect()
			mail.select("inbox")
			
			# Build search criteria as OR between senders and subjects
			search_str = self._build_search_criteria()
			
			print(f"Using search criteria: {search_str}")
			print(f"First run: {self.first_run} ({'checking all emails' if self.first_run else 'only checking unread emails'})")
			
			# Search for emails
			status, message_ids = mail.search(None, search_str)
			
			if status != 'OK':
				print(f"Search failed with status: {status}")
				print(f"Response: {message_ids}")
				return []
				
			if not message_ids[0]:
				# No matching emails
				mail.logout()
				self.last_check_time = datetime.now()
				self.first_run = False  # Mark that we've completed a run
				return []
				
			matching_emails = []
			
			for num in message_ids[0].split():
				try:
					# Fetch email data
					status, data = mail.fetch(num, "(RFC822)")
					if status != 'OK':
						print(f"Failed to fetch email {num}: {status}")
						continue
						
					raw_email = data[0][1]
					msg = email.message_from_bytes(raw_email)
					
					matching_emails.append(msg)
					
					# Debug info
					from_addr = msg.get("From", "Unknown sender")
					subject = msg.get("Subject", "No subject")
					print(f"Found matching email - From: {from_addr}, Subject: {subject}")
					
					# Call the callback if provided
					if callback and callable(callback):
						callback(msg)
						
					# Mark as read 
					mail.store(num, '+FLAGS', '\\Seen')
				except Exception as e:
					print(f"Error processing email {num}: {e}")
			
			mail.logout()
			self.last_check_time = datetime.now()
			self.first_run = False  # Mark that we've completed a run
			return matching_emails
			
		except Exception as e:
			print(f"Error checking email: {e}")
			self.last_check_time = datetime.now()
			self.first_run = False  # Mark that we've completed a run
			return []
	
	def monitor_continuously(self, callback=None, interval=None, initial_unread_only=True):
		"""
		Continuously monitor for new emails
		
		Args:
			callback: Function to call when matching email found
			interval: Seconds between checks (defaults to config value)
			initial_unread_only: If True, only process unread emails on first run
		"""
		check_interval = interval or EMAIL_CHECK_INTERVAL
		
		print(f"Starting email monitoring for {self.email_address}")
		print(f"Checking every {check_interval} seconds")
		
		if EMAIL_SENDERS:
			print(f"Monitoring emails from: {', '.join(EMAIL_SENDERS)}")
		
		if EMAIL_SUBJECTS:
			print(f"Monitoring emails with subjects containing: {', '.join(EMAIL_SUBJECTS)}")
		
		print("Emails will trigger if they are from ANY of these senders OR")
		print("contain ANY of these subject keywords.")
		
		if initial_unread_only and self.first_run:
			print("Initial check: only processing UNREAD emails")
			# Force unread only on first run if specified
			self.first_run = False
		
		try:
			while True:
				matches = self.check_for_triggers(callback)
				if matches:
					print(f"Found {len(matches)} matching emails")
				else:
					print("No new matching emails found")
				time.sleep(check_interval)
		except KeyboardInterrupt:
			print("Monitoring stopped")

# For testing this module directly
if __name__ == "__main__":
	def print_email(msg):
		print(f"Found matching email: {msg.get('From')} - {msg.get('Subject')}")
	
	monitor = GmailMonitor()
	
	import argparse
	parser = argparse.ArgumentParser(description='Test Gmail monitoring')
	parser.add_argument('--all', action='store_true', help='Check all emails, not just unread ones')
	parser.add_argument('--monitor', action='store_true', help='Run continuous monitoring')
	args = parser.parse_args()
	
	if args.all:
		# Allow checking all emails for testing
		print("Testing with ALL emails (including already read ones)...")
		monitor.first_run = True
	else:
		print("Testing with only UNREAD emails...")
		monitor.first_run = False
	
	if args.monitor:
		# Run continuous monitoring
		print("Starting continuous monitoring...")
		monitor.monitor_continuously(print_email, initial_unread_only=not args.all)
	else:
		# Test a single check
		print("Checking for emails once...")
		matches = monitor.check_for_triggers(print_email)
		print(f"Found {len(matches)} matching emails")
