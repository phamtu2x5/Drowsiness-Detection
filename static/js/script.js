document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const videoFeed = document.getElementById('video-feed');
    const videoPlaceholder = document.getElementById('video-placeholder');
    const detectionResults = document.getElementById('detection-results');
    const uploadForm = document.getElementById('upload-form');
    const imageInput = document.getElementById('image-input');
    const uploadResult = document.getElementById('upload-result');
    const resultImage = document.getElementById('result-image');

    let detectionInterval;
    let resultsInterval;
    let video = document.createElement('video');
    let canvas = document.createElement('canvas');
    let context = canvas.getContext('2d');

    // Request camera access
    navigator.mediaDevices.getUserMedia({ video: { width: 320, height: 240 } })
        .then(stream => {
            video.srcObject = stream;
            video.play();
            console.log("Camera access granted");
        })
        .catch(error => {
            console.error('Error accessing camera:', error);
            showAlert('Cannot access camera. Ensure HTTPS and camera permissions. Error: ' + error.message, 'danger');
        });

    // Start detection
    startBtn.addEventListener('click', function() {
        startDetection();
    });

    // Stop detection
    stopBtn.addEventListener('click', function() {
        stopDetection();
    });

    // Upload form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        uploadImage();
    });

    function startDetection() {
        if (!video.srcObject) {
            showAlert('Camera not available. Please check permissions or HTTPS.', 'danger');
            return;
        }

        fetch('/start_detection')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    startBtn.style.display = 'none';
                    stopBtn.style.display = 'inline-block';
                    
                    // Show video feed
                    videoFeed.style.display = 'block';
                    videoPlaceholder.style.display = 'none';
                    
                    // Start sending frames and polling results
                    detectionInterval = setInterval(captureAndSend, 200); // Send every 200ms
                    resultsInterval = setInterval(updateDetectionResults, 1000); // Poll every 1s
                    
                    showAlert('Detection started successfully!', 'success');
                }
            })
            .catch(error => {
                console.error('Error starting detection:', error);
                showAlert('Error starting detection. Please try again.', 'danger');
            });
    }

    function stopDetection() {
        fetch('/stop_detection')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    startBtn.style.display = 'inline-block';
                    stopBtn.style.display = 'none';
                    videoFeed.style.display = 'none';
                    videoPlaceholder.style.display = 'block';
                    
                    // Stop polling and frame sending
                    if (detectionInterval) {
                        clearInterval(detectionInterval);
                        detectionInterval = null;
                    }
                    if (resultsInterval) {
                        clearInterval(resultsInterval);
                        resultsInterval = null;
                    }
                    
                    // Clear video feed
                    videoFeed.src = '';
                    
                    // Clear results immediately
                    detectionResults.innerHTML = `
                        <div class="text-center text-muted">
                            <i class="fas fa-info-circle fa-2x mb-2"></i>
                            <p>No detection results yet</p>
                        </div>
                    `;
                    
                    showAlert('Detection stopped.', 'warning');
                }
            })
            .catch(error => {
                console.error('Error stopping detection:', error);
                showAlert('Error stopping detection.', 'danger');
            });
    }

    function captureAndSend() {
        if (!video.srcObject) {
            console.warn("No camera stream available");
            return;
        }
        
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        canvas.toBlob(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'frame.jpg');
            
            fetch('/upload_image', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Upload error:', data.error);
                    showAlert(data.error, 'danger');
                } else {
                    videoFeed.src = 'data:image/jpeg;base64,' + data.result_image;
                }
            })
            .catch(error => {
                console.error('Error sending frame:', error);
                showAlert('Error processing frame.', 'danger');
            });
        }, 'image/jpeg', 0.6); // 60% quality
    }

    function updateDetectionResults() {
        fetch('/get_detection_result')
            .then(response => response.json())
            .then(data => {
                if (data.detections && data.detections.length > 0) {
                    displayDetectionResults(data.detections);
                } else {
                    // If no detections, reset to placeholder
                    detectionResults.innerHTML = `
                        <div class="text-center text-muted">
                            <i class="fas fa-info-circle fa-2x mb-2"></i>
                            <p>No detection results yet</p>
                        </div>
                    `;
                }
            })
            .catch(error => {
                console.error('Error fetching detection results:', error);
            });
    }

    function displayDetectionResults(detections) {
        let html = '';
        
        detections.forEach(detection => {
            const confidencePercent = Math.round(detection.confidence * 100);
            const statusClass = detection.class === 'awake' ? 'awake' : 'drowsy';
            const statusIcon = detection.class === 'awake' ? 'fa-smile' : 'fa-tired';
            const statusText = detection.class === 'awake' ? 'Awake' : 'Drowsy';
            
            html += `
                <div class="detection-item ${statusClass}">
                    <div class="d-flex align-items-center">
                        <span class="status-indicator ${statusClass}"></span>
                        <div class="flex-grow-1">
                            <h6 class="mb-1">
                                <i class="fas ${statusIcon}"></i> ${statusText}
                            </h6>
                            <small>Confidence: ${confidencePercent}%</small>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        detectionResults.innerHTML = html;
    }

    function uploadImage() {
        const file = imageInput.files[0];
        if (!file) {
            showAlert('Please select an image file.', 'warning');
            return;
        }

        const formData = new FormData();
        formData.append('image', file);

        // Show loading state
        const submitBtn = uploadForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="loading"></span> Analyzing...';
        submitBtn.disabled = true;

        fetch('/upload_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Upload response:', data); // Debug response
            if (data.error) {
                showAlert(data.error, 'danger');
            } else {
                // Display result image
                resultImage.src = 'data:image/jpeg;base64,' + data.result_image;
                uploadResult.style.display = 'block';
                
                // Display detection results
                if (data.detections && data.detections.length > 0) {
                    displayDetectionResults(data.detections);
                } else {
                    showAlert('No detections found.', 'warning');
                }
                
                showAlert('Image analyzed successfully!', 'success');
            }
        })
        .catch(error => {
            console.error('Error uploading image:', error);
            showAlert('Error analyzing image. Please try again.', 'danger');
        })
        .finally(() => {
            // Reset button state
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
    }

    function showAlert(message, type) {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());

        // Create new alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at the top of the container
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    // Handle file input change
    imageInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            // Preview the selected image
            const reader = new FileReader();
            reader.onload = function(e) {
                resultImage.src = e.target.result;
                uploadResult.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
});