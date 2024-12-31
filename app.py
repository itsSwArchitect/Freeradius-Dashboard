
from flask import Flask, request, jsonify, render_template
import os
import subprocess
import logging
import shutil  # Make sure to import shutil

app = Flask(__name__)

# Paths to FreeRADIUS directories
MODS_AVAILABLE_PATH = "/etc/freeradius/mods-available"
MODS_ENABLED_PATH = "/etc/freeradius/mods-enabled"
SITES_AVAILABLE_PATH = "/etc/freeradius/sites-available"
SITES_ENABLED_PATH = "/etc/freeradius/sites-enabled"

RADIUSD_CONF_PATH = '/etc/freeradius/radiusd.conf'
BACKUP_DIR = '/etc/freeradius'  

@app.route('/edit-radiusd', methods=['GET'])
def edit_radiusd():
    """Serve the page to edit radiusd.conf"""
    return render_template('edit_radiusd.html')

@app.route('/api/load-radiusd', methods=['GET'])
def load_radiusd():
    """Read the content of radiusd.conf"""
    if os.path.exists(RADIUSD_CONF_PATH):
        with open(RADIUSD_CONF_PATH, 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/save-radiusd', methods=['POST'])
def save_radiusd():
    """Save the modified content of radiusd.conf and create a backup, after validation"""
    try:
     
        new_content = request.json.get('content')
        if not new_content:
            return jsonify({'error': 'No content to save'}), 400


        process = subprocess.Popen(
            ['sudo', 'freeradius', '-XC'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()


        if b"Configuration appears to be OK" not in stdout:
            return jsonify({'error': 'Configuration check failed: ' + stderr.decode()}), 400


        backup_file = os.path.join(BACKUP_DIR, 'radiusd.conf.backup')
        shutil.copy(RADIUSD_CONF_PATH, backup_file) 


        with open(RADIUSD_CONF_PATH, 'w') as f:
            f.write(new_content)
        
        return jsonify({'message': 'Configuration saved successfully'})
    
    except Exception as e:
      
        return jsonify({'error': f'Error saving configuration: {str(e)}'}), 500

# Function to list available modules and sites (from mods-available and sites-available)
def list_available(path):
    items = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):  # Skip directories
            continue
        items.append(item)
    return items

# Fetch all available modules and sites
@app.route('/api/modules', methods=['GET'])
def get_modules_and_sites():

    mods_available = list_available(MODS_AVAILABLE_PATH)
    sites_available = list_available(SITES_AVAILABLE_PATH)


    enabled_modules = os.listdir(MODS_ENABLED_PATH)
    enabled_sites = os.listdir(SITES_ENABLED_PATH)


    modules_and_sites = {
        "modules": {
            "enabled": [mod for mod in mods_available if mod in enabled_modules],
            "disabled": [mod for mod in mods_available if mod not in enabled_modules],
        },
        "sites": {
            "enabled": [site for site in sites_available if site in enabled_sites],
            "disabled": [site for site in sites_available if site not in enabled_sites],
        },
    }

    return jsonify(modules_and_sites)

# Enable or disable a module or site
@app.route('/api/toggle', methods=['POST'])
def toggle_item():
    data = request.json
    item_name = data.get('item')
    item_type = data.get('type')  # 'module' or 'site'
    action = data.get('action')  # 'enable' or 'disable'

    # Enable item (create symlink)
    if action == 'enable':
        if item_type == 'module':
            target_path = os.path.join(MODS_AVAILABLE_PATH, item_name)
            symlink_path = os.path.join(MODS_ENABLED_PATH, item_name)
        elif item_type == 'site':
            target_path = os.path.join(SITES_AVAILABLE_PATH, item_name)
            symlink_path = os.path.join(SITES_ENABLED_PATH, item_name)

        if not os.path.exists(symlink_path):
            os.symlink(target_path, symlink_path)

    # Disable item (remove symlink)
    elif action == 'disable':
        if item_type == 'module':
            symlink_path = os.path.join(MODS_ENABLED_PATH, item_name)
        elif item_type == 'site':
            symlink_path = os.path.join(SITES_ENABLED_PATH, item_name)

        if os.path.islink(symlink_path):
            os.remove(symlink_path)

    # Restart FreeRADIUS to apply changes
    subprocess.run(['systemctl', 'restart', 'freeradius'])

    return jsonify({"message": f"{item_type.capitalize()} {item_name} {action}d successfully"})


# # View the configuration of a module or site
# @app.route('/api/view-config/<item>/<item_name>', methods=['GET'])
# def view_config(item, item_name):
#     print(f"Fetching configuration for {item_name}: {item}")

#     if item == 'module':
#         config_path = os.path.join(MODS_AVAILABLE_PATH, item_name)
#     elif item == 'site':
#         config_path = os.path.join(SITES_AVAILABLE_PATH, item_name)

#     if not os.path.exists(config_path):
#         return jsonify({"error": "Item not found"}), 404
        
#     with open(config_path, 'r') as file:
#         content = file.read()

#     return jsonify({"config": content})

# View the configuration of a module or site
@app.route('/api/view-config/<item>/<item_name>', methods=['GET'])
def view_config(item, item_name):
    print(f"API Call: Fetching configuration for item '{item_name}' of type '{item}'")
    
    if item == 'module':
        config_path = os.path.join(MODS_AVAILABLE_PATH, item_name)
    elif item == 'site':
        config_path = os.path.join(SITES_AVAILABLE_PATH, item_name)
    else:
        print(f"Invalid item type: {item}")
        return jsonify({"error": "Invalid item type"}), 400

    if not os.path.exists(config_path):
        print(f"Config path not found: {config_path}")
        return jsonify({"error": "Item not found"}), 404
        
    with open(config_path, 'r') as file:
        content = file.read()

    print(f"Config loaded successfully from: {config_path}")
    return jsonify({"config": content})



# Save the edited configuration of a module or site
@app.route('/api/save-config/<item>/<item_name>', methods=['POST'])
def save_config(item, item_name):
    data = request.json
    new_content = data.get('config')

    if item == 'module':
        config_path = os.path.join(MODS_AVAILABLE_PATH, item_name)
    elif item == 'site':
        config_path = os.path.join(SITES_AVAILABLE_PATH, item_name)

    if not os.path.exists(config_path):
        return jsonify({"error": "Item not found"}), 404


    backup_path = config_path + ".bak"
    os.rename(config_path, backup_path)


    with open(config_path, 'w') as file:
        file.write(new_content)


    subprocess.run(['systemctl', 'restart', 'freeradius'])

    return jsonify({"message": f"Configuration for {item_name} saved successfully"})


# Route to get the list of site-enabled configurations
@app.route('/api/get-site-enabled', methods=['GET'])
def get_site_enabled():
    """Fetch a list of all site-enabled configurations."""
    site_files = [f for f in os.listdir(SITES_ENABLED_PATH) if os.path.isfile(os.path.join(SITES_ENABLED_PATH, f))]
    return jsonify({"sites": site_files})

# Route to view the configuration of a site-enabled file
@app.route('/api/view-enabled-site/<site_name>', methods=['GET'])
def view_enabled_site(site_name):
    """Fetch configuration of a site-enabled file."""
    config_path = os.path.join(SITES_ENABLED_PATH, site_name)

    if not os.path.exists(config_path):
        return jsonify({"error": "Item not found"}), 404

    with open(config_path, 'r') as file:
        content = file.read()

    return jsonify({"config": content})

# Save the edited configuration of a module or site
@app.route('/api/save-enabled-site/<site_name>', methods=['POST'])
def save_enabled_site(site_name):
    data = request.json
    new_content = data.get('config')

    config_path = os.path.join(SITES_AVAILABLE_PATH, site_name)

    if not os.path.exists(config_path):
        return jsonify({"error": "Item not found"}), 404


    backup_path = config_path + ".bak"
    os.rename(config_path, backup_path)


    with open(config_path, 'w') as file:
        file.write(new_content)


    subprocess.run(['systemctl', 'restart', 'freeradius'])

    return jsonify({"message": f"Configuration for {site_name} saved successfully"})




# Main route to serve the dashboard
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
######### Coded by Abid ###########