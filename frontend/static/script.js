document.addEventListener("DOMContentLoaded", () => {
    let currentMode = "distance";
    let currentSource = "webcam";
    let isStreaming = false;

    const modeDistanceBtn = document.getElementById("mode-distance");
    const modeSignBtn = document.getElementById("mode-sign");
    const sourceWebcamBtn = document.getElementById("source-webcam");
    const sourceVideoBtn = document.getElementById("source-video");
    const uploadContainer = document.getElementById("upload-container");
    const videoUpload = document.getElementById("video-upload");
    
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");
    
    const videoFeed = document.getElementById("video-feed");
    const idleScreen = document.getElementById("idle-screen");
    const loader = document.getElementById("loading-indicator");

    const signMetrics = document.querySelectorAll(".sign-metric");

    // Mode Toggle
    modeDistanceBtn.addEventListener("click", () => {
        currentMode = "distance";
        modeDistanceBtn.classList.add("active");
        modeSignBtn.classList.remove("active");
        signMetrics.forEach(el => el.classList.add("hidden"));
        updateStreamUrl();
    });

    modeSignBtn.addEventListener("click", () => {
        currentMode = "sign";
        modeSignBtn.classList.add("active");
        modeDistanceBtn.classList.remove("active");
        signMetrics.forEach(el => el.classList.remove("hidden"));
        updateStreamUrl();
    });

    // Source Toggle
    sourceWebcamBtn.addEventListener("click", () => {
        currentSource = "webcam";
        sourceWebcamBtn.classList.add("active");
        sourceVideoBtn.classList.remove("active");
        uploadContainer.classList.add("hidden");
        updateStreamUrl();
    });

    sourceVideoBtn.addEventListener("click", () => {
        currentSource = "video";
        sourceVideoBtn.classList.add("active");
        sourceWebcamBtn.classList.remove("active");
        uploadContainer.classList.remove("hidden");
    });

    // Handle Streaming
    startBtn.addEventListener("click", () => {
        if (currentSource === "video" && (!videoUpload.files || videoUpload.files.length === 0)) {
            alert("Please select a video file first.");
            return;
        }

        isStreaming = true;
        idleScreen.classList.add("hidden");
        loader.classList.remove("hidden");
        videoFeed.classList.add("hidden");
        startBtn.classList.add("hidden");
        stopBtn.classList.remove("hidden");

        if (currentSource === "webcam") {
            // Give it a brief delay for animation effect
            setTimeout(() => {
                const endpoint = currentMode === "distance" ? "/distance-video" : "/sign-video";
                videoFeed.src = endpoint;
                loader.classList.add("hidden");
                videoFeed.classList.remove("hidden");
            }, 800);
        } else if (currentSource === "video") {
            const formData = new FormData();
            formData.append("file", videoUpload.files[0]);
            
            // For video upload, we would normally POST the video and then stream the response
            // For this UI mockup/prototype, we'll just simulate the process
            setTimeout(() => {
                alert("Video upload processing is simulated in this UI for uploaded files. Switching to webcam demo stream.");
                const endpoint = currentMode === "distance" ? "/distance-video" : "/sign-video";
                videoFeed.src = endpoint;
                loader.classList.add("hidden");
                videoFeed.classList.remove("hidden");
            }, 1000);
        }
    });

    stopBtn.addEventListener("click", () => {
        isStreaming = false;
        videoFeed.src = "";
        videoFeed.classList.add("hidden");
        idleScreen.classList.remove("hidden");
        stopBtn.classList.add("hidden");
        startBtn.classList.remove("hidden");
    });

    function updateStreamUrl() {
        if (isStreaming && currentSource === "webcam") {
            loader.classList.remove("hidden");
            videoFeed.classList.add("hidden");
            setTimeout(() => {
                const endpoint = currentMode === "distance" ? "/distance-video" : "/sign-video";
                videoFeed.src = endpoint;
                loader.classList.add("hidden");
                videoFeed.classList.remove("hidden");
            }, 500);
        }
    }

    // Simulate metric updates (mock server events for signs)
    setInterval(() => {
        if (isStreaming && currentMode === "sign") {
            document.getElementById("sign-label").textContent = ["Speed Limit (60)", "Stop", "Yield", "No Entry"][Math.floor(Math.random()*4)];
            document.getElementById("sign-conf").textContent = (Math.random() * 20 + 80).toFixed(1) + "%";
        }
    }, 2000);
});
