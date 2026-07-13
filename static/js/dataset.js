// ===========================================
// Dataset Collection
// ===========================================

document.addEventListener("DOMContentLoaded", function () {

    const startBtn = document.getElementById("startCollection");
    const stopBtn = document.getElementById("stopCollection");

    const gestureInput = document.getElementById("gestureName");
    const imageInput = document.getElementById("imageCount");

    const progressBar = document.getElementById("collectionProgress");
    const statusText = document.getElementById("collectionStatus");
    const counter = document.getElementById("imageCounter");

    if (!startBtn) return;

    startBtn.addEventListener("click", function () {

        const gesture = gestureInput.value.trim();
        const total = imageInput.value;

        if (gesture === "") {

            alert("Enter Gesture Name");
            return;

        }

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

            if (data.status === "success") {

                startBtn.disabled = true;
                stopBtn.disabled = false;

                statusText.innerHTML = "Collecting...";

            }

        });

    });

    stopBtn.addEventListener("click", function () {

        fetch("/stop_collection")

        .then(res => res.json())

        .then(data => {

            startBtn.disabled = false;
            stopBtn.disabled = true;

            statusText.innerHTML = "Stopped";

        });

    });

});

// ===========================================
// Live Collection Status
// ===========================================

function updateCollectionStatus() {

    fetch("/collection_status")
    .then(res => res.json())
    .then(data => {

        const progressBar = document.getElementById("collectionProgress");
        const counter = document.getElementById("imageCounter");
        const status = document.getElementById("collectionStatus");

        if (!progressBar) return;

        const total = data.total;
        const current = data.current;

        let percent = 0;

        if (total > 0) {
            percent = Math.round((current / total) * 100);
        }

        progressBar.style.width = percent + "%";
        progressBar.innerHTML = percent + "%";

        counter.innerHTML = current + " / " + total;

        if (data.collecting) {

            status.innerHTML = "Collecting Images...";

        } else {

            if (current >= total && total > 0) {

                status.innerHTML = "Collection Completed ✅";

                document.getElementById("startCollection").disabled = false;
                document.getElementById("stopCollection").disabled = true;

            }

        }

    });

}

setInterval(updateCollectionStatus, 300);

// ===========================================
// Dataset Information
// ===========================================

function loadDatasetInfo() {

    fetch("/dataset_info")
    .then(res => res.json())
    .then(data => {

        // Summary Cards

        document.getElementById("totalClasses").innerHTML = data.summary.classes;
        document.getElementById("totalImages").innerHTML = data.summary.images;
        document.getElementById("trainingImages").innerHTML = data.summary.training;
        document.getElementById("testingImages").innerHTML = data.summary.testing;

        // Dataset Table

        const tbody = document.getElementById("datasetTableBody");

        if (!tbody) return;

        tbody.innerHTML = "";

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

                <td class="action-icons">

                    <i class="bi bi-eye"></i>

                    <i class="bi bi-trash"></i>

                </td>

            </tr>

            `;

        });

    });

}

setInterval(loadDatasetInfo, 1000);

loadDatasetInfo();