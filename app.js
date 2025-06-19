let currentShirt = 'shirt1';
let shirtScale = 1.0;
const shirts = {
    shirt1: { image: null, width: 300, height: 400 },
    shirt2: { image: null, height: 400 },
    shirt3: { image: null, height: 400 }
};

// Initialize MediaPipe Pose
const pose = new Pose({
    locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
    }
});

pose.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});

// Setup camera and canvas
const video = document.getElementById('input-video');
const canvas = document.getElementById('output-canvas');
const ctx = canvas.getContext('2d');

// Load shirt images
Object.keys(shirts).forEach(shirtId => {
    const img = new Image();
    img.src = `shirts/${shirtId}.png`;
    img.onload = () => {
        shirts[shirtId].image = img;
        shirts[shirtId].width = img.width * (shirts[shirtId].height / img.height);
    };
});

// Initialize camera
const camera = new Camera(video, {
    onFrame: async () => {
        await pose.send({image: video});
    },
    width: 640,
    height: 480
});

camera.start();

// Handle pose detection results
pose.onResults((results) => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (results.poseLandmarks) {
        const shoulders = {
            left: results.poseLandmarks[11],
            right: results.poseLandmarks[12]
        };
        
        const shoulderWidth = Math.abs(shoulders.right.x - shoulders.left.x) * canvas.width;
        const shirtWidth = shoulderWidth * 1.5 * (shirtScale / 100);
        
        const centerX = (shoulders.left.x + shoulders.right.x) / 2 * canvas.width;
        const centerY = (shoulders.left.y + shoulders.right.y) / 2 * canvas.height;
        
        if (shirts[currentShirt].image) {
            const shirtHeight = shirtWidth * (shirts[currentShirt].height / shirts[currentShirt].width);
            
            ctx.drawImage(
                shirts[currentShirt].image,
                centerX - shirtWidth / 2,
                centerY - shirtHeight / 3,
                shirtWidth,
                shirtHeight
            );
        }
    }
});

// UI Controls
function selectShirt(shirtId) {
    currentShirt = shirtId;
}

const sizeSlider = document.getElementById('size-slider');
const sizeValue = document.getElementById('size-value');

sizeSlider.addEventListener('input', (e) => {
    shirtScale = e.target.value;
    sizeValue.textContent = `${shirtScale}%`;
});

// Add WebSocket connection to communicate with Python
const ws = new WebSocket('ws://localhost:8765');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    currentShirt = data.current_shirt;
    shirtScale = data.scale;
    sizeValue.textContent = `${shirtScale}%`;
    sizeSlider.value = shirtScale;
};