FreeRADIUS Dashboard
By Abid Ali
DevOps Engineer at Inara Technologies

This project is a web-based dashboard for managing FreeRADIUS configurations, enabling users to easily view, edit, and save both module and site configurations. The dashboard is built using Flask for the backend and HTML/JavaScript for the frontend. It also includes features like configuration backup before saving changes and automatic validation using freeradius -XC before applying any changes.

Features
View Configuration: View the configuration of FreeRADIUS modules and site-enabled configurations.
Edit Configuration: Edit configurations directly through the web interface.
Backup Configuration: Automatically create a backup of the current configuration before saving any changes.
Validation: Ensure configurations are valid using freeradius -XC before saving.
Save Changes: Save the changes to the original configuration files after validation.
Restart FreeRADIUS: Automatically restart FreeRADIUS to apply changes after saving configurations.
Prerequisites
Python 3.10 or higher
Flask
FreeRADIUS installed and running on the server
Web browser for accessing the dashboard
sudo privileges for restarting FreeRADIUS and accessing configuration files
Installation
1. Clone the repository
bash
Copy code
git clone https://github.com/yourusername/freeradius-dashboard.git
cd freeradius-dashboard
2. Create a Python virtual environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
3. Install required dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure FreeRADIUS paths
Ensure that the following variables in app.py are set to the correct paths for your FreeRADIUS installation:

python
Copy code
MODS_AVAILABLE_PATH = "/etc/freeradius/3.0/mods-available"
SITES_AVAILABLE_PATH = "/etc/freeradius/3.0/sites-available"
5. Run the Flask application
bash
Copy code
flask run --host=0.0.0.0 --port=5000
The application will be available at http://<server-ip>:5000.

Usage
Open a web browser and navigate to http://<server-ip>:5000.
The dashboard allows you to:
View and edit FreeRADIUS module and site configurations.
Save the edited configurations after validating with freeradius -XC.
Backup the original configuration before saving any changes.
Restart FreeRADIUS automatically after saving configurations.
Backup and Save Process
When editing a configuration (module or site), a backup of the current configuration is created in the same directory with a .bak extension.
Before saving any changes, the configuration is validated with the command freeradius -XC.
If the validation is successful, the new configuration is saved, and FreeRADIUS is restarted.
If the validation fails, an error message is displayed, and the configuration is not saved.
Troubleshooting
1. Error: Configuration Validation Failed
Ensure that your configuration syntax is correct before attempting to save changes. You can manually run freeradius -XC from the command line to check for syntax errors.

2. Error: Permission Denied
Make sure that the Flask application is running with the necessary permissions to access the FreeRADIUS configuration files and restart the FreeRADIUS service. You may need to run the application as a superuser or adjust file permissions.