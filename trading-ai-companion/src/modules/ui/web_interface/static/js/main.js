// Main JavaScript for Trading AI Companion

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
    
    // Setup event listeners
    setupEventListeners();
});

function initializeApp() {
    // Load initial data
    loadSystemStatus();
    loadModels();
    
    // Set up periodic updates
    setInterval(loadSystemStatus, 5000); // Update every 5 seconds
    setInterval(loadModels, 10000); // Update every 10 seconds
}

function setupEventListeners() {
    // Form submission
    const settingsForm = document.getElementById('settings-form');
    if (settingsForm) {
        settingsForm.addEventListener('submit', saveSettings);
    }
}

function loadSystemStatus() {
    fetch('/api/status')
        .then(response => response.json())
        .then(data => {
            updateStatusDisplay(data);
        })
        .catch(error => {
            console.error('Error loading system status:', error);
        });
}

function loadModels() {
    fetch('/api/models')
        .then(response => response.json())
        .then(data => {
            updateModelsDisplay(data);
        })
        .catch(error => {
            console.error('Error loading models:', error);
        });
}

function updateStatusDisplay(data) {
    const statusElement = document.getElementById('system-status');
    if (statusElement) {
        statusElement.innerHTML = `
            <p>Status: <span class="${data.status === 'running' ? 'status-ok' : 'status-error'}">${data.status}</span></p>
            <p>MT5 Connected: <span class="${data.mt5_connected ? 'status-ok' : 'status-warning'}">${data.mt5_connected ? 'Yes' : 'No'}</span></p>
            <p>Models Available: ${data.models_available}</p>
        `;
    }
}

function updateModelsDisplay(data) {
    const modelsElement = document.getElementById('models-status');
    if (modelsElement) {
        if (data && data.length > 0) {
            const modelList = data.map(model => 
                `<li>${model.name} (modified: ${new Date(model.modified_at).toLocaleString()})</li>`
            ).join('');
            modelsElement.innerHTML = `<ul>${modelList}</ul>`;
        } else {
            modelsElement.innerHTML = '<p>No models available</p>';
        }
    }
}

function saveSettings(event) {
    event.preventDefault();
    
    // Collect form data
    const formData = new FormData(event.target);
    const settings = {};
    for (let [key, value] of formData.entries()) {
        settings[key] = value;
    }
    
    // Send to server (placeholder)
    console.log('Saving settings:', settings);
    alert('Settings saved successfully!');
}

// Add CSS classes for status indicators
const style = document.createElement('style');
style.textContent = `
    .status-ok { color: green; font-weight: bold; }
    .status-warning { color: orange; font-weight: bold; }
    .status-error { color: red; font-weight: bold; }
`;
document.head.appendChild(style);
