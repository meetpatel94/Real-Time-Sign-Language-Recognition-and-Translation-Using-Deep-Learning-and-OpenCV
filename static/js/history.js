document.addEventListener("DOMContentLoaded", () => {

    loadHistory();

    loadStatistics();

});

async function loadHistory() {

    const response = await fetch("/history_api");

    const data = await response.json();

    console.log(data);

}

async function loadStatistics() {

    const response = await fetch("/history_stats");

    const data = await response.json();

    console.log(data);

}