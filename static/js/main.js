// ===========================================
// GestureAI - Main JavaScript
// ===========================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("GestureAI Loaded Successfully");

    // ============================
    // Elements
    // ============================
    const loadingPopup = document.getElementById("cameraLoadingPopup");
    const cameraFeed = document.getElementById("cameraFeed");
    const placeholder = document.getElementById("cameraPlaceholder");
    const cameraScreen = document.getElementById("cameraScreen");

    const startBtn = document.getElementById("startCamera");
    const stopBtn = document.getElementById("stopCamera");
    const captureBtn = document.getElementById("captureBtn");
    const fullscreenBtn = document.getElementById("fullscreenBtn");

    const cameraStatus = document.getElementById("cameraStatus");
    const fpsValue = document.getElementById("fpsValue");

    // ============================
    // Camera Status
    // ============================

    function updateCameraStatus(running) {

        if (!cameraStatus) return;

        if (running) {
            cameraStatus.innerHTML = "Running";
            cameraStatus.classList.remove("offline");
            cameraStatus.classList.add("online");
        } else {
            cameraStatus.innerHTML = "Stopped";
            cameraStatus.classList.remove("online");
            cameraStatus.classList.add("offline");
        }
    }

    // ============================
    // Start Camera
    // ============================

    if (startBtn) {

        startBtn.addEventListener("click", function () {
            
            loadingPopup.style.display = "block";
            fetch("/start_camera")
                .then(res => res.json())
                .then(data => {

                    if (data.status === "started") {

                        cameraFeed.src = "/video_feed?" + new Date().getTime();
                        cameraFeed.onload = function () {
                        loadingPopup.style.display = "none";
                        };

                        cameraFeed.style.display = "block";
                        placeholder.style.display = "none";

                        startBtn.disabled = true;
                        stopBtn.disabled = false;
                        captureBtn.disabled = false;

                        updateCameraStatus(true);

                    } else {
                        loadingPopup.style.display = "none";
                        alert("Unable to Start Camera");

                    }

                });

        });

    }

    // ============================
    // Stop Camera
    // ============================

    if (stopBtn) {

        stopBtn.addEventListener("click", function () {

            fetch("/stop_camera")
                .then(res => res.json())
                .then(data => {

                    if (data.status === "stopped") {

                        cameraFeed.src = "";

                        cameraFeed.style.display = "none";
                        placeholder.style.display = "flex";

                        startBtn.disabled = false;
                        stopBtn.disabled = true;
                        captureBtn.disabled = true;

                        updateCameraStatus(false);

                    }

                });

        });

    }

    // ============================
    // Capture Image
    // ============================

    if (captureBtn) {

        captureBtn.addEventListener("click", function () {

            fetch("/capture")
                .then(res => res.json())
                .then(data => {

                    if (data.status === "success") {

                        alert("✅ Image Saved Successfully\n\n" + data.filename);

                    } else {

                        alert("❌ Capture Failed");

                    }

                });

        });

    }

    // ============================
    // Fullscreen
    // ============================

    if (fullscreenBtn && cameraScreen) {

        fullscreenBtn.addEventListener("click", function () {

            if (!document.fullscreenElement) {

                cameraScreen.requestFullscreen();

            } else {

                document.exitFullscreen();

            }

        });

    }

    // ============================
    // FPS Counter
    // ============================

    let frames = 0;
    let lastTime = performance.now();

    if (cameraFeed) {

        cameraFeed.onload = function () {
            frames++;
        };

    }

    setInterval(function () {

        const now = performance.now();

        const fps = Math.round(frames * 1000 / (now - lastTime));

        if (fpsValue)
            fpsValue.innerHTML = fps;

        frames = 0;
        lastTime = now;

    }, 1000);

//     // ============================
// // Live Status
// // ============================

// function updateStatus(){

//     fetch("/status")
//     .then(res=>res.json())
//     .then(data=>{

//         if(document.getElementById("predictionBox"))
//             document.getElementById("predictionBox").innerHTML="✋ "+data.prediction;

//         if(document.getElementById("confidenceValue"))
//             document.getElementById("confidenceValue").innerHTML=data.confidence;

//         if(document.getElementById("fpsValue"))
//             document.getElementById("fpsValue").innerHTML=data.fps;

//         if(document.getElementById("modelStatus"))
//             document.getElementById("modelStatus").innerHTML=data.model;

//     });

// }

// setInterval(updateStatus,500);

});