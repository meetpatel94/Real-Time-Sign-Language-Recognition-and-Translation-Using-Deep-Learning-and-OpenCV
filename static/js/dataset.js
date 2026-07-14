// ===========================================
// GestureAI Dataset Module
// ===========================================

document.addEventListener("DOMContentLoaded", function () {

    // ===========================================
    // Elements
    // ===========================================

    const startBtn = document.getElementById("startCollection");
    const stopBtn = document.getElementById("stopCollection");
    const clearBtn = document.getElementById("clearCollection");
    const loadingPopup = document.getElementById("cameraLoadingPopup");

    const gestureInput = document.getElementById("gestureName");
    const imageInput = document.getElementById("imageCount");

    const cameraFeed = document.getElementById("datasetCameraFeed");
    const placeholder = document.getElementById("datasetPlaceholder");

    const progressBar = document.getElementById("collectionProgress");
    const counter = document.getElementById("imageCounter");
    const status = document.getElementById("collectionStatus");

    const cameraState = document.getElementById("cameraState");
    const collectionState = document.getElementById("collectionState");
    const savedCount = document.getElementById("savedCount");

    const currentGesture = document.getElementById("currentGesture");
    const capturedImages = document.getElementById("capturedImages");

    const handStatus = document.getElementById("handStatus");
    const datasetFPS = document.getElementById("datasetFPS");

    const datasetCameraStatus =
        document.getElementById("datasetCameraStatus");

    // ===========================================
    // States
    // ===========================================

    let cameraRunning = false;
    let collecting = false;

    // ===========================================
    // Start Collection
    // ===========================================

    startBtn.addEventListener("click", function () {

        const gesture = gestureInput.value.trim().toUpperCase();

        const total = parseInt(imageInput.value);

        if (gesture === "") {

            alert("Please Enter Gesture Name");

            gestureInput.focus();

            return;

        }

        if (total <= 0 || isNaN(total)) {

            alert("Invalid Image Count");

            imageInput.focus();

            return;

        }

        loadingPopup.style.display = "block";

        fetch("/start_collection", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                gesture: gesture,

                total: total

            })

        })

        .then(res => res.json())

        .then(data => {

            if (data.status !== "success") {

                alert("Unable to Start Collection");

                return;

            }

            cameraFeed.src =
                "/video_feed?" + new Date().getTime();

            cameraFeed.onload = function(){
            loadingPopup.style.display = "none";
            };

            cameraFeed.style.display = "block";

            placeholder.style.display = "none";

            cameraRunning = true;

            collecting = true;

            startBtn.disabled = true;

            stopBtn.disabled = false;

            clearBtn.disabled = true;

            cameraState.innerHTML = "Running";

            collectionState.innerHTML = "Collecting";

            datasetCameraStatus.innerHTML = "Running";

            status.innerHTML = "Collecting Images...";

        })

        .catch(error => {
            loadingPopup.style.display = "none";

            console.log(error);

            alert("Server Error");

        });

    });

    // ===========================================
    // Stop Collection
    // ===========================================

    stopBtn.addEventListener("click", function () {

        fetch("/stop_collection")

        .then(res => res.json())

        .then(data => {

            collecting = false;

            cameraRunning = false;

            cameraFeed.src = "";

            cameraFeed.style.display = "none";

            placeholder.style.display = "flex";

            startBtn.disabled = false;

            stopBtn.disabled = true;

            clearBtn.disabled = false;

            cameraState.innerHTML = "Stopped";

            collectionState.innerHTML = "Stopped";

            datasetCameraStatus.innerHTML = "Stopped";

            status.innerHTML = "Collection Stopped";

        });

    });
        // ===========================================
    // Clear Collection
    // ===========================================

    clearBtn.addEventListener("click", function () {

        fetch("/clear_collection")

        .then(res => res.json())

        .then(data => {

            gestureInput.value = "";

            imageInput.value = 500;

            cameraFeed.src = "";

            cameraFeed.style.display = "none";

            placeholder.style.display = "flex";

            progressBar.style.width = "0%";

            progressBar.innerHTML = "0%";

            counter.innerHTML = "0 / 0";

            status.innerHTML = "Waiting to Start...";

            cameraState.innerHTML = "Stopped";

            collectionState.innerHTML = "Waiting";

            datasetCameraStatus.innerHTML = "Stopped";

            savedCount.innerHTML = "0";

            currentGesture.innerHTML = "-";

            capturedImages.innerHTML = "0";

            handStatus.innerHTML = "Not Detected";

            datasetFPS.innerHTML = "0";

            startBtn.disabled = false;

            stopBtn.disabled = true;

            clearBtn.disabled = true;

            collecting = false;

            cameraRunning = false;

        });

    });

    // ===========================================
    // Live Collection Status
    // ===========================================

    function updateCollectionStatus() {

        fetch("/collection_status")

        .then(res => res.json())

        .then(data => {

            let current = data.current;

            let target = data.target;

            let percent = 0;

            if (target > 0) {

                percent = Math.round((current / target) * 100);

            }

            if (percent > 100) {

                percent = 100;

            }

            progressBar.style.width = percent + "%";

            progressBar.innerHTML = percent + "%";

            counter.innerHTML = current + " / " + target;

            savedCount.innerHTML = current;

            capturedImages.innerHTML = current;

            currentGesture.innerHTML =
                data.gesture === "" ? "-" : data.gesture;

            if (data.running) {

                collectionState.innerHTML = "Collecting";

                status.innerHTML = "Collecting Images...";

            }

            else {

                if (target > 0 && current >= target) {

                    collectionState.innerHTML = "Completed";

                    status.innerHTML = "Collection Completed";

                    startBtn.disabled = false;

                    stopBtn.disabled = true;

                    clearBtn.disabled = false;

                }

            }

        });

    }

    // ===========================================
    // Live Camera Status
    // ===========================================

    function updateCameraStatus() {

        fetch("/status")

        .then(res => res.json())

        .then(data => {

            handStatus.innerHTML =
                data.hand ? "Detected" : "Not Detected";

            datasetFPS.innerHTML = data.fps;

            if (data.camera) {

                cameraState.innerHTML = "Running";

                datasetCameraStatus.innerHTML = "Running";

            }

            else {

                cameraState.innerHTML = "Stopped";

                datasetCameraStatus.innerHTML = "Stopped";

            }

        });

    }

    setInterval(updateCollectionStatus,300);

    setInterval(updateCameraStatus,200);
        // ===========================================
    // Dataset Information
    // ===========================================

    function loadDatasetInfo() {

        fetch("/dataset_info")

        .then(res => res.json())

        .then(data => {

            document.getElementById("totalClasses").innerHTML =
                data.summary.classes;

            document.getElementById("totalImages").innerHTML =
                data.summary.images;

            document.getElementById("trainingImages").innerHTML =
                data.summary.training;

            document.getElementById("testingImages").innerHTML =
                data.summary.testing;

            const tbody =
                document.getElementById("datasetTableBody");

            tbody.innerHTML = "";

            if (data.table.length === 0) {

                tbody.innerHTML = `
                    <tr>
                        <td colspan="6">
                            No Dataset Available
                        </td>
                    </tr>
                `;

                return;

            }

            data.table.forEach(item => {
 
                tbody.innerHTML += `

                    <tr>

                        <td>${item.gesture}</td>

                        <td>${item.images}</td>

                        <td>${item.training}</td>

                        <td>${item.testing}</td>

                        <td>

                            <span class="ready">

                                ${item.status}

                            </span>

                        </td>

                        <td>

                            <button
                                class="btn btn-sm btn-outline-info viewGesture"
                                data-gesture="${item.gesture}">

                                <i class="bi bi-eye"></i>

                            </button>

                            <button
                                class="btn btn-sm btn-outline-danger deleteGesture"
                                data-gesture="${item.gesture}">

                                <i class="bi bi-trash"></i>

                            </button>

                        </td>

                    </tr>

                `; 

            });
            // 
            // ===========================================
            // Delete Gesture
            // ===========================================

            document.querySelectorAll(".deleteGesture").forEach(button => {

                button.onclick = function () {

                    const gesture = this.dataset.gesture;

                    if (!confirm(`Delete "${gesture}" dataset?`)) {

                        return;

                    }

                    fetch("/delete_gesture", {

                        method: "POST",

                        headers: {

                            "Content-Type": "application/json"

                        },

                        body: JSON.stringify({

                            gesture: gesture

                        })

                    })

                    .then(res => res.json())

                    .then(data => {

                        if (data.status === "success") {

                            alert("Dataset Deleted Successfully");

                            loadDatasetInfo();

                        }

                        else {

                            alert("Unable to Delete Dataset");

                        }

                    });

                };

            });

            // ===========================================
            // View Gesture Images
            // ===========================================

            document.querySelectorAll(".viewGesture").forEach(button => {

                button.onclick = function () {

                    const gesture = this.dataset.gesture;

                    fetch("/view_gesture/" + gesture)

                    .then(res => res.json())

                    .then(data => {

                        const grid =
                        document.getElementById("gestureImageGrid");

                        grid.innerHTML = "";

                        if(data.images.length===0){

                            grid.innerHTML=`

                            <div class="col-12">

                                <div class="alert alert-warning text-center shadow-sm">

                                    <i class="bi bi-exclamation-triangle-fill fs-2"></i>

                                    <h4 class="mt-3 mb-2">

                                        No Images Available

                                    </h4>

                                    <p class="mb-0">

                                        This gesture dataset is empty.<br>

                                        Please collect images first.

                                    </p>

                                </div>

                            </div>

                            `;

                            const modal = new bootstrap.Modal(

                                document.getElementById("viewImagesModal")

                            );

                            modal.show();

                            return;

                        }

                        data.images.forEach(image=>{

                            grid.innerHTML+=`

                            <div class="col-lg-3 col-md-4 col-6">

                                <img

                                    src="/dataset_image/${gesture}/${image}"

                                    class="img-fluid"

                                >

                            </div>

                            `;

                        });

                        const modal =
                        new bootstrap.Modal(

                            document.getElementById("viewImagesModal")

                        );

                        modal.show();

                    });

                };

            });  

        });

    }

    // ===========================================
    // Search Gesture
    // ===========================================

    const searchBox =
        document.getElementById("searchGesture");

    searchBox.addEventListener("keyup", function () {

        let value =
            this.value.toUpperCase();

        let rows =
            document.querySelectorAll("#datasetTableBody tr");

        rows.forEach(row => {

            let text =
                row.innerText.toUpperCase();

            row.style.display =
                text.includes(value)
                ? ""
                : "none";

        });

    });

    // ===========================================
    // Auto Refresh
    // ===========================================

    setInterval(loadDatasetInfo,1000);

    updateCollectionStatus();

    updateCameraStatus();

    loadDatasetInfo();

});