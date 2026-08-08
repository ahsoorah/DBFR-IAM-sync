# IAM Identity Synchronizer (Browser Automation)

Executive Summary
---
This project is an Identity & Access Management (IAM) automation utility built to synchronize user credentials across enterprise SaaS platforms. It eliminates manual data entry by programmatically harvesting unique profile identifiers and executing batch updates to align usernames with organizational standards.

Originally developed by me during a Fire Technology Internship with the City of Delray Beach Fire-Rescue (DBFR) to uphold username standards in mission-critical platforms, this tool transformed a high-volume administrative task into a streamlined, automated routine.

Business Impact
---
Operational Efficiency: Automated the standardization of 200+ personnel accounts, reducing a multi-day manual project to a 15-minute process.

Support Reduction: Significantly decreased helpdesk tickets related to login failures by ensuring 100% username consistency with municipal email addresses.

Accuracy: Removed the risk of fatfinger errors during manual account editing in a high-stakes public safety environment.

The Engineering Challenge
---
The target platform (ESO Suite) utilizes a Single-Page Application (SPA) architecture. In this environment, user profile URLs are not predictable; they are generated via unique UUIDs (Universally Unique Identifiers) that are only revealed through browser-side interactions.

The Solution: A Two-Stage Automation Pipeline
---
Account Harvesting Stage: The script utilizes Playwright to simulate a human administrator clicking through the user directory. It captures the resulting dynamic URLs and maps them to personnel names in a structured CSV staging file.

Identity Synchronization Stage: Using the harvested map, the script navigates directly to each profile, extracts the enterprise email address, and surgically updates the username field to match the email prefix (ex. jsmith@enterprise.com → jsmith).

Security & Privacy Architecture
---
Human-in-the-Loop (HITL) Authentication:

To maintain the highest security posture, this tool does not store administrative credentials or bypass Multi-Factor Authentication (MFA).

The script pauses execution for a "Human-in-the-Loop" login.

Once the administrator completes the secure MFA challenge manually, they signal the script to take control. This ensures that the automation operates within a pre-authenticated, secure session.

Sanitization Notice
---
This is a sanitized portfolio version of the production script. To comply with municipal security standards:

All personnel names and internal identifiers have been replaced with generic roles.

Organizational domains and internal URL structures have been generalized.

No live credentials or sensitive municipal infrastructure data are contained within this repository.

Technical Stack
---
Automation Framework: Playwright (Chromium)

Language: Python 3.x

Data Handling: CSV / DictReader

Environment: Designed for Windows/Linux workstations with MFA-enabled enterprise access.

How to Use
---
Install dependencies:

pip install playwright

playwright install chromium

Configuration: Open iam_sync_tool.py and ensure the target_domain matches your organization.

Run: Execute the class methods via the if __name__ == "__main__": block.

Use harvest_accounts() first to build the identity map.

Use update_identities(dry_run=True) to verify changes before committing to the database.

Author
---
Suriyah Saravanan | 
Bachelor's in Management Information Systems (MIS), Cybersecurity | 
Florida Atlantic University
