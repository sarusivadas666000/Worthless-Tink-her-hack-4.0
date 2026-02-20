const API_URL = 'http://127.0.0.1:8000';

// DOM Elements
const initialImageInput = document.getElementById('initialImage');
const finalImageInput = document.getElementById('finalImage');
const uploadBox1 = document.getElementById('uploadBox1');
const uploadBox2 = document.getElementById('uploadBox2');
const preview1 = document.getElementById('preview1');
const preview2 = document.getElementById('preview2');
const generateBtn = document.getElementById('generateBtn');
const downloadBtn = document.getElementById('downloadBtn');
const statusMessage = document.getElementById('statusMessage');
const videoPreview = document.getElementById('videoPreview');
const videoElement = document.getElementById('video');

let generatedVideoBlob = null;
let initialImageFile = null;
let finalImageFile = null;

// Initialize event listeners
document.addEventListener('DOMContentLoaded', () => {
    // File input events
    uploadBox1.addEventListener('click', () => initialImageInput.click());
    uploadBox2.addEventListener('click', () => finalImageInput.click());
    
    initialImageInput.addEventListener('change', handleInitialImageSelect);
    finalImageInput.addEventListener('change', handleFinalImageSelect);
    
    // Generate button
    generateBtn.addEventListener('click', generateVideo);
    downloadBtn.addEventListener('click', downloadVideo);
    
    // Drag and drop
    setupDragAndDrop(uploadBox1, initialImageInput);
    setupDragAndDrop(uploadBox2, finalImageInput);
    
    // Load available effects from backend
    loadAvailableEffects();
});

function setupDragAndDrop(box, input) {
    box.addEventListener('dragover', (e) => {
        e.preventDefault();
        box.classList.add('dragover');
    });
    
    box.addEventListener('dragleave', () => {
        box.classList.remove('dragover');
    });
    
    box.addEventListener('drop', (e) => {
        e.preventDefault();
        box.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            input.files = files;
            const event = new Event('change', { bubbles: true });
            input.dispatchEvent(event);
        }
    });
}

function handleInitialImageSelect(e) {
    const file = e.target.files[0];
    if (file && validateImage(file)) {
        initialImageFile = file;
        displayPreview(file, preview1);
        updateGenerateButton();
    }
}

function handleFinalImageSelect(e) {
    const file = e.target.files[0];
    if (file && validateImage(file)) {
        finalImageFile = file;
        displayPreview(file, preview2);
        updateGenerateButton();
    }
}

function validateImage(file) {
    const allowedTypes = ['image/jpeg', 'image/png'];
    const maxSize = 10 * 1024 * 1024; // 10MB
    
    if (!allowedTypes.includes(file.type)) {
        showStatus('error', 'Invalid image type. Only JPG and PNG are allowed.');
        return false;
    }
    
    if (file.size > maxSize) {
        showStatus('error', 'Image size exceeds 10MB limit.');
        return false;
    }
    
    return true;
}

function displayPreview(file, previewContainer) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewContainer.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
    };
    reader.readAsDataURL(file);
}

function updateGenerateButton() {
    if (initialImageFile && finalImageFile) {
        generateBtn.disabled = false;
    } else {
        generateBtn.disabled = true;
    }
}

function getSelectedEffects() {
    const effects = {};
    const checkboxes = document.querySelectorAll('.effect-checkbox input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        const parts = checkbox.id.split('effect');
        const effectName = checkbox.value;
        effects[effectName] = checkbox.checked;
    });
    
    return effects;
}

async function generateVideo() {
    if (!initialImageFile || !finalImageFile) {
        showStatus('error', 'Please upload both images first.');
        return;
    }
    
    generateBtn.classList.add('loading');
    generateBtn.disabled = true;
    videoPreview.style.display = 'none';
    downloadBtn.style.display = 'none';
    
    try {
        // Get selected effects
        const selectedEffects = getSelectedEffects();
        const hasAnyEffect = Object.values(selectedEffects).some(val => val);
        
        if (!hasAnyEffect) {
            showStatus('info', 'No effects selected. Using basic transition.');
        }
        
        showStatus('info', 'Generating 3D video with cinematic effects... This may take 1-2 minutes');
        
        const formData = new FormData();
        formData.append('initial_image', initialImageFile);
        formData.append('final_image', finalImageFile);
        
        // Add effects as JSON query parameter
        const effectsJson = JSON.stringify(selectedEffects);
        const url = `${API_URL}/generate-video?effects=${encodeURIComponent(effectsJson)}`;
        
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
        });
        
        if (!response.ok) {
            let errorMessage = `HTTP Error: ${response.status}`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorMessage;
            } catch (e) {
                // Ignore JSON parse errors
            }
            throw new Error(errorMessage);
        }
        
        generatedVideoBlob = await response.blob();
        
        // Display video
        const videoURL = URL.createObjectURL(generatedVideoBlob);
        videoElement.src = videoURL;
        videoPreview.style.display = 'block';
        downloadBtn.style.display = 'inline-block';
        
        showStatus('success', '3D video generated successfully! Ready to download.');
    } catch (error) {
        console.error('Error:', error);
        showStatus('error', `Failed to generate video: ${error.message}`);
    } finally {
        generateBtn.classList.remove('loading');
        generateBtn.disabled = false;
    }
}

function downloadVideo() {
    if (!generatedVideoBlob) {
        showStatus('error', 'No video to download.');
        return;
    }
    
    const url = URL.createObjectURL(generatedVideoBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'product_video_3d.mp4';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    showStatus('success', 'Video downloaded successfully!');
}

function showStatus(type, message) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message show ${type}`;
    
    // Auto-hide after 5 seconds for success messages
    if (type === 'success') {
        setTimeout(() => {
            statusMessage.classList.remove('show');
        }, 5000);
    }
}

// Load effects from backend
async function loadAvailableEffects() {
    try {
        const response = await fetch(`${API_URL}/effects`);
        if (response.ok) {
            const data = await response.json();
            console.log('Available 3D effects:', data);
        }
    } catch (error) {
        console.warn('Could not load effects from backend:', error);
    }
}

// Check API connectivity on page load
async function checkAPI() {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            const data = await response.json();
            console.log('✓ Backend API connected:', data.service);
        }
    } catch (error) {
        console.warn('⚠ Backend API not accessible at', API_URL);
        showStatus('error', 'Backend API not accessible. Is the server running?');
    }
}

window.addEventListener('load', checkAPI);


