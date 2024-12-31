// Fetch and display available modules and sites
async function fetchModulesAndSites() {
    const response = await fetch('/api/modules');
    const data = await response.json();

    const enabledModulesList = document.getElementById('enabled-modules');
    const disabledModulesList = document.getElementById('disabled-modules');
    const enabledSitesList = document.getElementById('enabled-sites');
    const disabledSitesList = document.getElementById('disabled-sites');
    const itemSelect = document.getElementById('item-select');

    // Clear previous lists
    enabledModulesList.innerHTML = '';
    disabledModulesList.innerHTML = '';
    enabledSitesList.innerHTML = '';
    disabledSitesList.innerHTML = '';
    itemSelect.innerHTML = '<option value="">-- Select an item --</option>';

    // Populate modules
    data.modules.enabled.forEach(module => {
        const listItem = document.createElement('li');
        listItem.textContent = module;
        const enableButton = document.createElement('button');
        enableButton.textContent = 'Disable';
        enableButton.onclick = () => toggleItem(module, 'module', 'disable');
        listItem.appendChild(enableButton);
        enabledModulesList.appendChild(listItem);

        const option = document.createElement('option');
        option.value = module;
        option.textContent = module;
        itemSelect.appendChild(option);
    });

    data.modules.disabled.forEach(module => {
        const listItem = document.createElement('li');
        listItem.textContent = module;
        const disableButton = document.createElement('button');
        disableButton.textContent = 'Enable';
        disableButton.onclick = () => toggleItem(module, 'module', 'enable');
        listItem.appendChild(disableButton);
        disabledModulesList.appendChild(listItem);
    });

    // Populate sites
    data.sites.enabled.forEach(site => {
        const listItem = document.createElement('li');
        listItem.textContent = site;
        const enableButton = document.createElement('button');
        enableButton.textContent = 'Disable';
        enableButton.onclick = () => toggleItem(site, 'site', 'disable');
        listItem.appendChild(enableButton);
        enabledSitesList.appendChild(listItem);
    });

    data.sites.disabled.forEach(site => {
        const listItem = document.createElement('li');
        listItem.textContent = site;
        const disableButton = document.createElement('button');
        disableButton.textContent = 'Enable';
        disableButton.onclick = () => toggleItem(site, 'site', 'enable');
        listItem.appendChild(disableButton);
        disabledSitesList.appendChild(listItem);
    });
}

// Toggle a module or site
async function toggleItem(item, type, action) {
    const response = await fetch('/api/toggle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item, type, action })
    });

    const data = await response.json();
    alert(data.message);
    fetchModulesAndSites();
}

// Load configuration of a selected module or site
// async function loadConfig(item) {
//     if (!item) return;

//     const type = item.includes('default') || item.includes('inner-tunnel') ? 'site' : 'module';

//     const response = await fetch(`/api/view-config/${type}/${item}`);
//     const data = await response.json();

//     if (data.error) {
//         alert(data.error);
//         return;
//     }

//     document.getElementById('item-config').value = data.config;
// }
async function loadConfig(item) {
    if (!item) return;

    let type;

    if (item === 'radiusd.conf') {
        type = 'radiusd';
    } else {
        type = item.includes('default') || item.includes('inner-tunnel') ? 'site' : 'module';
    }

    const url = `/api/view-config/${type}/${item}`;
    console.log("Fetching URL:", url);  

    try {
        const response = await fetch(url);
        console.log("Response status:", response.status); 
        const data = await response.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        document.getElementById('item-config').value = data.config;
    } catch (error) {
        console.error("Error loading config:", error);
        alert("Error loading configuration. Please try again.");
    }
}

// Save edited configuration
async function saveConfig() {
    const item = document.getElementById('item-select').value;
    const newConfig = document.getElementById('item-config').value;

    if (!item) {
        alert('Please select an item.');
        return;
    }

    const type = item.includes('default') || item.includes('inner-tunnel') ? 'site' : 'module';

    const response = await fetch(`/api/save-config/${type}/${item}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ config: newConfig })
    });

    const data = await response.json();
    alert(data.message);
}
// Function to open the configuration editor
function openConfigEditor() {

    document.getElementById('editor-container').style.display = 'block';


    fetch('/api/load-radiusd')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {

                document.getElementById('radiusd-config').value = data.content;
            }
        })
        .catch(error => {
            console.error("Error loading configuration:", error);
            alert("Error loading configuration. Please try again.");
        });
}

// Function to save the modified configuration
function saveRadConfig() {
    const newConfig = document.getElementById('radiusd-config').value;
    
    if (!newConfig) {
        alert("No content to save.");
        return;
    }

    // Send the updated configuration to the Flask backend to save
    fetch('/api/save-radiusd', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: newConfig })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error("Error saving configuration:", error);
        alert("Error saving configuration. Please try again.");
    });
}



// Toggle the visibility of the section
function toggleVisibility(sectionId) {
    const section = document.getElementById(sectionId);
    section.classList.toggle('hidden');
}

function adjustTextarea(textarea) {
    // Reset the height to recalculate based on content
    textarea.style.height = 'auto';
    // Adjust height to fit content
    textarea.style.height = `${textarea.scrollHeight}px`;
}



// Fetch the list of site-enabled configurations and populate the dropdown
async function loadSiteDropdown() {
    try {
        const response = await fetch('/api/get-site-enabled');
        const data = await response.json();

        if (data.sites && data.sites.length > 0) {
            const siteSelect = document.getElementById('site-select');

            siteSelect.innerHTML = '<option value="">-- Select a site --</option>';


            data.sites.forEach(site => {
                const option = document.createElement('option');
                option.value = site;
                option.textContent = site;
                siteSelect.appendChild(option);
            });
        } else {
            console.log('No site-enabled configurations found.');
        }
    } catch (error) {
        console.error('Error fetching site-enabled configurations:', error);
    }
}

// Load the selected site-enabled configuration
async function loadSiteConfig(siteName) {
    if (!siteName) return;

    try {
        const response = await fetch(`/api/view-enabled-site/${siteName}`);
        const data = await response.json();

        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById('site-config').value = data.config;
        }
    } catch (error) {
        console.error('Error loading site configuration:', error);
    }
}

// Save the edited site-enabled configuration
async function saveSiteConfig() {
    const siteName = document.getElementById('site-select').value;
    const newConfig = document.getElementById('site-config').value;

    if (!siteName) {
        alert('Please select a site.');
        return;
    }

    try {
        const response = await fetch(`/api/save-enabled-site/${siteName}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ config: newConfig }),
        });

        const data = await response.json();
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error saving site configuration:', error);
    }
}

// Initialize the site dropdown on page load
window.onload = loadSiteDropdown;


// Initialize the dashboard
fetchModulesAndSites();
