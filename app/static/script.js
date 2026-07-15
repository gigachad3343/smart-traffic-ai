// ======================================
// SMART TRAFFIC CONTROL AI
// script.js
// ======================================

// Traffic Chart
let trafficChart = null;

// Initialize Chart
function initTrafficChart() {

    const canvas = document.getElementById("trafficChart");

    if (!canvas) return;

    const ctx = canvas.getContext("2d");

    trafficChart = new Chart(ctx, {

        type: "line",

        data: {

            labels: [],

            datasets: [{

                label: "Vehicle Count",

                data: [],

                borderColor: "#00d4ff",

                backgroundColor: "rgba(0,212,255,0.15)",

                borderWidth: 3,

                fill: true,

                tension: 0.4,

                pointRadius: 3

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    labels: {

                        color: "white"

                    }

                }

            },

            scales: {

                x: {

                    ticks: {

                        color: "white"

                    }

                },

                y: {

                    beginAtZero: true,

                    ticks: {

                        color: "white"

                    }

                }

            }

        }

    });

}

// ======================================
// UPDATE DASHBOARD
// ======================================

async function updateDashboard() {

    try {

        const response = await fetch("/vehicle_count");

        const data = await response.json();

        document.getElementById("vehicle-count").innerText =
            data.count;

        document.getElementById("traffic-density").innerText =
            data.density;

        document.getElementById("signal-timer").innerText =
            data.signal_time + " sec";
// ======================================
// SMART INTERSECTION LIGHTS
// ======================================

const north = document.getElementById("north-light");
const south = document.getElementById("south-light");
const east = document.getElementById("east-light");
const west = document.getElementById("west-light");

if(north && south && east && west){

    // Reset all lights
    north.className = "light red";
    south.className = "light red";
    east.className = "light red";
    west.className = "light red";

    // AI decides which direction is green
    if(data.signal_time >= 45){

        north.className = "light green";
        south.className = "light green";

    }

    else if(data.signal_time >= 30){

        east.className = "light yellow";
        west.className = "light yellow";

    }

    else{

        east.className = "light green";
        west.className = "light green";

    }

}
        const signal =
            document.getElementById("signal-status");

        if (data.signal_time >= 45) {

            signal.innerHTML = "🟢 GREEN";

            signal.style.color = "#00ff88";

        }

        else if (data.signal_time >= 30) {

            signal.innerHTML = "🟡 WAIT";

            signal.style.color = "#ffc107";

        }

        else {

            signal.innerHTML = "🔴 RED";

            signal.style.color = "#ff4d4d";

        }

        const ai =
    document.getElementById("ai-status-text");

if (ai) {

    if (data.density == "HIGH") {

        ai.innerHTML =
            "🚨 Heavy Traffic Detected";

        showAIAlert("🚨 Heavy Traffic Detected");

    }

    else if (data.density == "MEDIUM") {

        ai.innerHTML =
            "⚠ Moderate Traffic";

        showAIAlert("⚠ Moderate Traffic");

    }

    else {

        ai.innerHTML =
            "✅ Traffic Flow Normal";

        showAIAlert("✅ Traffic Flow Normal");

    }

}

        // Update Chart

        if (trafficChart) {

            const now =
                new Date().toLocaleTimeString();

            trafficChart.data.labels.push(now);

            trafficChart.data.datasets[0].data.push(data.count);

            if (trafficChart.data.labels.length > 12) {

                trafficChart.data.labels.shift();

                trafficChart.data.datasets[0].data.shift();

            }

            trafficChart.update();

        }

    }

    catch (err) {

        console.log(err);

    }

}

// ======================================
// LIVE CLOCK & DATE
// ======================================

function updateClock() {

    const now = new Date();

    const time = now.toLocaleTimeString();

    const date = now.toLocaleDateString(undefined, {

        weekday: "long",

        year: "numeric",

        month: "long",

        day: "numeric"

    });

    const timeElement = document.getElementById("current-time");
    const dateElement = document.getElementById("current-date");

    if (timeElement)
        timeElement.innerText = time;

    if (dateElement)
        dateElement.innerText = date;

}

// ======================================
// AI CHAT
// ======================================

async function sendMessage() {

    const input = document.getElementById("user-message");

    const message = input.value.trim();

    if (message === "")
        return;

    const chat = document.getElementById("chat-box");

    chat.innerHTML +=
        `<p><b>You:</b> ${message}</p>`;

    input.value = "";

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                message: message

            })

        });

        const data = await response.json();

        chat.innerHTML +=
            `<p><b>AI:</b> ${data.reply}</p>`;

        chat.scrollTop = chat.scrollHeight;

    }

    catch {

        chat.innerHTML +=
            `<p><b>AI:</b> Unable to connect.</p>`;

    }

}

// ======================================
// ENTER KEY SUPPORT
// ======================================

const messageInput =
    document.getElementById("user-message");

if (messageInput) {

    messageInput.addEventListener("keypress", function(e){

        if(e.key === "Enter"){

            sendMessage();

        }

    });

}

// ======================================
// START EVERYTHING
// ======================================

window.onload = function(){

    initTrafficChart();

    updateDashboard();

    updateClock();

    setInterval(updateDashboard,1000);

    setInterval(updateClock,1000);

};

// ======================================
// PDF REPORT
// ======================================

async function downloadPDF() {

    const { jsPDF } = window.jspdf;

    const pdf = new jsPDF();

    pdf.setFontSize(18);
    pdf.text("Smart Traffic Control AI Report", 20, 20);

    pdf.setFontSize(12);

    pdf.text("Date: " + new Date().toLocaleDateString(), 20, 40);
    pdf.text("Time: " + new Date().toLocaleTimeString(), 20, 50);

    pdf.text(
        "Total Vehicles: " +
        document.getElementById("vehicle-count").innerText,
        20,
        70
    );

    pdf.text(
        "Traffic Density: " +
        document.getElementById("traffic-density").innerText,
        20,
        80
    );

    pdf.text(
        "Signal Timer: " +
        document.getElementById("signal-timer").innerText,
        20,
        90
    );

    pdf.text(
        "Signal Status: " +
        document.getElementById("signal-status").innerText,
        20,
        100
    );

    pdf.save("Traffic_Report.pdf");

}



// ======================================
// CSV REPORT
// ======================================

function downloadCSV() {

    let csv = "Date,Time,Vehicle Count,Traffic Density,Signal Timer,Signal Status\n";

    csv +=
        `"${new Date().toLocaleDateString()}","${new Date().toLocaleTimeString()}","${document.getElementById("vehicle-count").innerText}","${document.getElementById("traffic-density").innerText}","${document.getElementById("signal-timer").innerText}","${document.getElementById("signal-status").innerText}"`;

    const blob = new Blob([csv], {

        type: "text/csv"

    });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "Traffic_Report.csv";

    a.click();

    URL.revokeObjectURL(url);

}

// ======================================
// CAPTURE DASHBOARD
// ======================================

async function captureDashboard() {

    const canvas = await html2canvas(document.body);

    const link = document.createElement("a");

    link.download = "Smart_Traffic_Dashboard.png";

    link.href = canvas.toDataURL();

    link.click();

}


// ======================================
// FULL SCREEN CAMERA
// ======================================

function toggleFullscreen() {

    const video =
        document.querySelector(".video-box");

    if (!document.fullscreenElement) {

        video.requestFullscreen();

    }

    else {

        document.exitFullscreen();

    }

}
// ======================================
// AI POPUP ALERT
// ======================================

function showAIAlert(message){

    const alertBox =
        document.getElementById("ai-alert");

    const text =
        document.getElementById("ai-alert-text");

    if(!alertBox || !text) return;

    text.innerHTML = message;

    alertBox.classList.add("show");

    setTimeout(function(){

        alertBox.classList.remove("show");

    },3000);

}