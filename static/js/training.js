// ===========================================
// Chart
// ===========================================

const ctx = document
    .getElementById("trainingChart")
    .getContext("2d");

const accuracyData = [];

const lossData = [];

const epochLabels = [];

const chart = new Chart(ctx, {

    type: "line",

    data: {

        labels: epochLabels,

        datasets: [

            {

                label: "Accuracy",

                data: accuracyData,

                borderColor: "#10B981",

                backgroundColor: "transparent",

                borderWidth: 3,

                tension: .3

            },

            {

                label: "Loss",

                data: lossData,

                borderColor: "#EF4444",

                backgroundColor: "transparent",

                borderWidth: 3,

                tension: .3

            }

        ]

    },

    options:{

        responsive:true,

        maintainAspectRatio:false,

        animation:false,

        interaction:{
            mode:"index",
            intersect:false
        },

        plugins:{

            legend:{
                labels:{
                    color:"white"
                }
            },

            zoom:{

                pan:{
                    enabled:true,
                    mode:"xy"
                },

                zoom:{

                    wheel:{
                        enabled:true
                    },

                    pinch:{
                        enabled:true
                    },

                    drag:{
                        enabled:true
                    },

                    mode:"xy"

                }

            }

        },

        scales:{

            x:{
                ticks:{
                    color:"white"
                }
            },

            y:{
                beginAtZero:true,

                ticks:{
                    color:"white"
                }
            }

        }

    }

});

// ===========================================
// Elements
// ===========================================

const startBtn = document.getElementById("startTrainingBtn");
const stopBtn = document.getElementById("stopTrainingBtn");

const exportBtn = document.getElementById("exportModelBtn");
const downloadPNGBtn = document.getElementById("downloadPNGBtn");
const downloadJSONBtn = document.getElementById("downloadJSONBtn");
const downloadCSVBtn = document.getElementById("downloadCSVBtn");

const zoomInBtn = document.getElementById("zoomInBtn");
const zoomOutBtn = document.getElementById("zoomOutBtn");
const resetZoomBtn = document.getElementById("resetZoomBtn");
const fullscreenBtn = document.getElementById("fullscreenBtn");

const progressFill = document.getElementById("progressFill");
const progressPercent = document.getElementById("progressPercent");

const epochText = document.getElementById("epochText");
const accuracyValue = document.getElementById("accuracyValue");
const lossValue = document.getElementById("lossValue");
const valAccuracyValue = document.getElementById("valAccuracyValue");

const trainingLogs = document.getElementById("trainingLogs");

// ===========================================
// Training Status Polling
// ===========================================

let polling = null;


// ===========================================
// Start Training
// ===========================================

startBtn.addEventListener("click", async () => {

    startBtn.disabled = true;
    stopBtn.disabled = false;

    startBtn.innerHTML =
        '<i class="bi bi-hourglass-split"></i> Training...';

    trainingLogs.innerHTML = "";

    const response = await fetch(

        "/start_training",

        {

            method: "POST"

        }

    );

    const result = await response.json();

    console.log(result);

    startPolling();

});

// ===========================================
// Stop Training
// ===========================================

stopBtn.addEventListener("click", async () => {

    await fetch("/stop_training", {

        method: "POST"

    });

    stopBtn.disabled = true;

});

// ===========================================
// Poll Training Status
// ===========================================

function startPolling() {

    if (polling !== null) {

        clearInterval(

            polling

        );

    }

    polling = setInterval(

        loadTrainingStatus,

        500

    );

}

// ===========================================
// Load Status
// ===========================================

async function loadTrainingStatus() {

    const response = await fetch(

        "/training_status"

    );

    const data = await response.json();

    updateUI(

        data

    );

    if (

        epochLabels.length < data.epoch

    ){

        epochLabels.push(

            data.epoch

        );

        accuracyData.push(

            (data.accuracy*100)

        );

        lossData.push(

            data.loss

        );

        chart.update();

    } 

    if (!data.running) {

        clearInterval(polling);

        startBtn.disabled = false;

        stopBtn.disabled = true;

        exportBtn.disabled = false;

        startBtn.innerHTML =
            '<i class="bi bi-play-fill"></i> Start Training';

    } 
 
}

// ===========================================
// Update UI
// ===========================================

function updateUI(data) {

    progressFill.style.width =

        data.progress + "%";


    progressPercent.innerHTML =

        data.progress + "%";


    epochText.innerHTML =

        "Epoch : " +

        data.epoch +

        " / " +

        data.total_epochs;


    accuracyValue.innerHTML =

        (data.accuracy * 100).toFixed(2)

        + "%";


    lossValue.innerHTML =

        Number(data.loss).toFixed(4);


    valAccuracyValue.innerHTML =

        (data.val_accuracy * 100).toFixed(2)

        + "%";


    if (

        trainingLogs.lastMessage !==

        data.message

    ) {

        trainingLogs.innerHTML +=

            `<p>✔ ${data.message}</p>`;

        trainingLogs.scrollTop =

            trainingLogs.scrollHeight;

        trainingLogs.lastMessage =

            data.message;

    }

}

// ===========================================
// Export Model
// ===========================================

exportBtn.addEventListener("click", () => {

    window.location.href = "/export_model";

});

// ===========================================
// Download Graph as PNG
// ===========================================

downloadPNGBtn.addEventListener("click", () => {

    const canvas = document.getElementById("trainingChart");

    const image = canvas.toDataURL("image/png");

    const link = document.createElement("a");

    link.href = image;

    link.download = "training_graph.png";

    link.click();

});

// ===========================================
// Download JSON
// ===========================================

downloadJSONBtn.addEventListener("click",()=>{

    window.location.href =
    "/download_training_json";

});

// ===========================================
// Download CSV
// ===========================================

downloadCSVBtn.addEventListener("click", () => {

    window.location.href =
        "/download_training_csv";

});

// ===========================================
// Zoom In
// ===========================================

zoomInBtn.addEventListener("click",()=>{

    chart.zoom(1.2);

});

// ===========================================
// Zoom Out
// ===========================================

zoomOutBtn.addEventListener("click",()=>{

    chart.zoom(0.8);

});

// ===========================================
// Reset Zoom
// ===========================================

resetZoomBtn.addEventListener("click",()=>{

    chart.resetZoom();

});

// ===========================================
// Full Screen
// ===========================================

fullscreenBtn.addEventListener("click",()=>{

    document.querySelector(".chart-card")
    .requestFullscreen();

});

const clearLogsBtn = document.getElementById("clearLogsBtn");

clearLogsBtn.addEventListener("click", () => {

    trainingLogs.innerHTML = `
        <p>
            <span class="log-time">00:00</span>
            Waiting for training...
        </p>
    `;

});

function loadSystemInfo(){

    fetch("/system_info")

    .then(res => res.json())

    .then(data => {

        document.getElementById("cpuUsage").innerHTML =
            data.cpu + "%";

        document.getElementById("ramUsage").innerHTML =
            data.ram_used + " / " +
            data.ram_total + " GB";

        document.getElementById("deviceName").innerHTML =
            data.device || "CPU";

    });

}

setInterval(loadSystemInfo,1000);

loadSystemInfo();

function loadDatasetInfo(){

    fetch("/dataset_info")

    .then(res => res.json())

    .then(data => {

        const summary = data.summary;
        const table = data.table;

        // Dataset

        document.getElementById("datasetName").innerHTML =
            "Custom Gesture Dataset";

        document.getElementById("totalImages").innerHTML =
            summary.images;

        // Classes

        document.getElementById("totalClasses").innerHTML =
            summary.classes;

        // Gesture Names

        let names = table.map(item => item.gesture);

        if(names.length > 3){

            document.getElementById("classNames").innerHTML =
                names.slice(0,3).join(", ") +
                " +" + (names.length-3) + " more";

        }

        else{

            document.getElementById("classNames").innerHTML =
                names.join(", ");

        }

        // Train / Test

        document.getElementById("splitInfo").innerHTML =
            summary.training +
            " / " +
            summary.testing +
            " Images";

    });

}

// ===========================================
// Auto Load Existing Status
// ===========================================

loadTrainingStatus();

loadDatasetInfo();

setInterval(loadDatasetInfo,2000);