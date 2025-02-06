# FreeRADIUS Dashboard

**By Abid Ali**  
*DevOps Engineer at Inara Technologies*

This project is a web-based dashboard for managing FreeRADIUS configurations, enabling users to easily view, edit, and save both module and site configurations. The dashboard is built using Flask for the backend and HTML/JavaScript for the frontend. It also includes features like configuration backup before saving changes and automatic validation using `freeradius -XC` before applying any changes.

## Features

- **View Configuration**: View the configuration of FreeRADIUS modules and site-enabled configurations.
- **Edit Configuration**: Edit configurations directly through the web interface.
- **Backup Configuration**: Automatically create a backup of the current configuration before saving any changes.
- **Validation**: Ensure configurations are valid using `freeradius -XC` before saving.
- **Save Changes**: Save the changes to the original configuration files after validation.
- **Restart FreeRADIUS**: Automatically restart FreeRADIUS to apply changes after saving configurations.

## Prerequisites

- Python 3.10 or higher
- Flask
- FreeRADIUS installed and running on the server
- Web browser for accessing the dashboard
- `sudo` privileges for restarting FreeRADIUS and accessing configuration files

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/freeradius-dashboard.git
cd freeradius-dashboard
```

# Demo
![Alt Text](https://github.com/itsSwArchitect/Freeradius-Dashboard/blob/main/demo.gif)
