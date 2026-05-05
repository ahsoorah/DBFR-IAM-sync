import csv
import time
from playwright.sync_api import sync_playwright

"""
Identity & Access Management (IAM) Synchronization Suite
-------------------------------------------------------
A specialized browser automation utility designed to audit and synchronize 
user identities across enterprise SaaS platforms. 

Capabilities:
- Automated Account Harvesting: Scrapes dynamic profile URLs from paginated tables.
- Identity Mapping: Correlates disparate data points to generate standardized usernames.
- Batch Update Engine: Performs surgical UI interactions to update user profiles.
- Human-in-the-Loop (HITL): Utilizes manual authentication bypass to maintain 
  security without storing sensitive credentials in code.
"""

class IAMSyncTool:
    def __init__(self, input_csv='mapped_identity_data.csv'):
        self.input_csv = input_csv
        # Sanitized list of role-based accounts to skip
        self.protected_keywords = ["Admin", "TechSupport", "System", "Service"]
        self.target_domain = "@enterprise-org.com"

    def harvest_accounts(self, directory_url):
        """
        Step 1: Scrapes the user directory to map display names to unique profile URLs.
        Necessary for SPAs where URLs are generated via unique UUIDs.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(directory_url)
            
            print(f"--- Action Required ---")
            print(f"Please log in manually. Once the user grid is visible, press ENTER here.")
            input()

            user_data = []
            while True:
                print(f"Harvesting current page... (Total: {len(user_data)})")
                
                # Target grid rows specifically
                rows = page.locator('div[class*="result-row"]').all()
                
                for row in rows:
                    try:
                        name = row.locator('span.ellipsis').first.inner_text().strip()
                        
                        # Interaction triggers a URL change to the unique user profile
                        row.click()
                        page.wait_for_load_state("networkidle")
                        
                        profile_url = page.url
                        # Standardizing the URL to point directly to the account settings tab
                        if "/person/" in profile_url and not profile_url.endswith("/account"):
                            profile_url = profile_url.rstrip("/") + "/account"
                        
                        user_data.append({"Name": name, "URL": profile_url})
                        
                        # Return to the directory list
                        page.go_back()
                        page.wait_for_selector('div[class*="result-row"]')
                    except Exception:
                        continue
                
                # Navigation: Check for 'Next' button to handle pagination
                next_button = page.locator('button:has-text("Next")')
                if next_button.is_visible() and not next_button.is_disabled():
                    next_button.click()
                    time.sleep(2) # Buffer for grid refresh
                else:
                    break

            self._export_data(user_data)
            browser.close()

    def update_identities(self, dry_run=True):
        """
        Step 2: Iterates through mapped data to update usernames based on email prefixes.
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            print("--- Action Required ---")
            print("Please log in. Press ENTER in this console once authenticated.")
            input()

            with open(self.input_csv, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row['Name']
                    url = row['URL']

                    # Safety Check: Skip administrative or protected accounts
                    if any(key.upper() in name.upper() for key in self.protected_keywords):
                        print(f"Skipping Protected Account: {name}")
                        continue

                    try:
                        page.goto(url, wait_until="networkidle")
                        page.wait_for_selector('button:has-text("Edit")')
                        
                        # Extraction: Locate the enterprise email to determine the new username
                        email_el = page.locator(f'span:has-text("{self.target_domain}")').first
                        email = email_el.inner_text().strip()
                        new_username = email.split('@')[0].lower()

                        # Transformation: Execute the update
                        page.click('button:has-text("Edit")')
                        page.wait_for_selector('input[name="username"]')
                        page.fill('input[name="username"]', new_username)
                        
                        if not dry_run:
                            page.click('button:has-text("Save")')
                            print(f"Updated: {name} -> {new_username}")
                        else:
                            page.click('button:has-text("Cancel")')
                            print(f"Dry run (no changes saved) for: {new_username}")

                        time.sleep(1.5) # Rate limiting to ensure UI stability

                    except Exception as e:
                        print(f"Error processing {name}. Moving to next record.")
                        continue

            print("--- Batch Update Complete ---")
            browser.close()

    def _export_data(self, data):
        """Helper to write harvested URLs to a CSV for staging."""
        if data:
            with open(self.input_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["Name", "URL"])
                writer.writeheader()
                writer.writerows(data)
            print(f"Success: Mapped {len(data)} identities to {self.input_csv}")

if __name__ == "__main__":
    # Portfolio Usage Example
    sync_tool = IAMSyncTool()
    
    # To harvest:
    # sync_tool.harvest_accounts("https://example-saas-platform.com/personnel")
    
    # To update:
    # sync_tool.update_identities(dry_run=True)