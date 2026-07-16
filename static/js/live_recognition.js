document.addEventListener("DOMContentLoaded", function () {

    console.log("Live Recognition Loaded");

    // ============================
    // Elements
    // ============================

    const predictionBox = document.getElementById("predictionBox");
    const confidenceValue = document.getElementById("confidenceValue");
    const fpsValue = document.getElementById("fpsValue");
    const recentPredictionList = document.getElementById("recentPredictionList");

        function loadPrediction() {

        fetch("/prediction")

        .then(response => response.json())

        .then(data => {

            predictionBox.innerHTML = "✋ " + data.gesture;

            confidenceValue.innerHTML = data.confidence + "%";

            fpsValue.innerHTML = data.fps;

            recentPredictionList.innerHTML = "";

            if (data.recent.length === 0) {

                recentPredictionList.innerHTML =
                    "<li>No Prediction Yet</li>";

            } else {

                data.recent.slice().reverse().forEach(item => {

                    recentPredictionList.innerHTML += `
                        <li>
                            <strong>${item.gesture}</strong>
                            (${item.confidence}%)
                            <br>
                            <small>${item.time}</small>
                        </li>
                    `;

                });

            }

        })

        .catch(error => {

            console.error(error);

        });

    }

    loadPrediction();

    setInterval(loadPrediction, 500);

});
