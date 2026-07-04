let currentQuestion = 0;
let questions = [];
let answers = {};

let timerSeconds = 40 * 60;
let timerInterval = null;

let switchCount = 0;
const maxSwitchCount = 10;

let cameraWarningCount = 0;
const maxCameraWarnings = 10;

let examClosed = false;

let cameraStream = null;
let motionDetectionInterval = null;

let lastSwitchTime = 0;
let cameraWarmup = true;

// NEW: camera permission retry tracking
let cameraRetryCount = 0;
const maxCameraRetries = 3;
let switchDetectionStarted = false;

// ---- FIX: motion-detection tuning ----
// Old warmup (3s) was too short: webcams often take 5-8s to settle
// auto-focus / auto-exposure / white-balance, which produced a burst
// of false "motion" right after warmup ended and closed the exam
// within ~15 seconds of starting it.
const CAMERA_WARMUP_MS = 150000;      // was 3000
const MOTION_THRESHOLD = 0.30;      // was 0.25 (slightly less sensitive)
const REQUIRED_CONSECUTIVE_HITS = 2; // require 2 consecutive high-motion
                                      // frames before counting a warning,
                                      // instead of reacting to a single spike
let consecutiveMotionHits = 0;

async function loadQuestions() {

    try {

        const response = await fetch(
            "/exam/generate/Data%20Analyst"
        );

        const data = await response.json();

        questions = data.questions || data;

        if (!questions || questions.length === 0) {
            alert("No questions received from server.");
            return;
        }

        if (questions.length > 50) {
            questions = questions.slice(0, 50);
        }

        createPalette();
        renderQuestion();
        startTimer();

        // Camera permission FIRST
        await setupCamera();

        // NOTE: switch detection is now started INSIDE setupCamera()
        // only once the camera is actually granted (see setupCamera()).
        // This avoids counting a tab/window blur caused by the browser's
        // own permission popup as a "switch" violation, and avoids
        // starting detection before the user has had a chance to
        // grant camera access.

    } catch (error) {

        console.error(error);
        alert("Unable to load questions from backend.");

    }

}

function startTimer() {

    if (timerInterval) {
        clearInterval(timerInterval);
    }

    updateTimerDisplay();

    timerInterval = setInterval(() => {

        timerSeconds--;

        if (timerSeconds <= 0) {

            clearInterval(timerInterval);

            timerSeconds = 0;

            updateTimerDisplay();

            alert("Time is up! Your exam will be submitted automatically.");

            submitExam();

            return;
        }

        updateTimerDisplay();

    }, 1000);

}

function updateTimerDisplay() {

    const minutes = String(
        Math.floor(timerSeconds / 60)
    ).padStart(2, "0");

    const seconds = String(
        timerSeconds % 60
    ).padStart(2, "0");

    document.getElementById("timer").textContent =
        `${minutes}:${seconds}`;

}

async function setupCamera() {

    const statusEl =
        document.getElementById("cameraStatusText");

    const warningEl =
        document.getElementById("warningMessage");

    if (
        !navigator.mediaDevices ||
        !navigator.mediaDevices.getUserMedia
    ) {

        if (statusEl) {
            statusEl.textContent =
                "Camera is not supported on this browser.";
        }

        showCameraRetryUI(
            "Your browser does not support camera access. Please use Chrome or Microsoft Edge.."
        );

        return;

    }

    try {

        cameraStream =
            await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: false
            });

        const video =
            document.getElementById("cameraVideo");

        if (video) {
            video.srcObject = cameraStream;

            // Ensure the camera feed is always visible to the user
            video.autoplay = true;
            video.muted = true;
            video.setAttribute("playsinline", "");
            video.classList.remove("d-none");
            video.style.display = "block";

            // Fallback sizing in case no CSS gives the video a size,
            // so the user's face is always visible on screen.
            if (!video.style.width) {
                video.style.width = "160px";
            }

            if (!video.style.height) {
                video.style.height = "120px";
            }

            video.style.objectFit = "cover";
            video.style.borderRadius = "8px";
            video.style.border = "2px solid #0d6efd";

            video.play().catch(() => {
                // Autoplay might be blocked until user interacts;
                // this is harmless, video will start on first interaction.
            });
        }

        if (statusEl) {
            statusEl.textContent =
                "Camera enabled.";
        }

        if (warningEl) {
            warningEl.classList.add("d-none");
            warningEl.innerHTML = "";
        }

        // Camera successfully granted, reset retry counter
        cameraRetryCount = 0;

        startMotionDetection();

        // Start switch detection only now that camera is confirmed
        if (!switchDetectionStarted) {
            setupSwitchDetection();
            switchDetectionStarted = true;
        }

    } catch (error) {

        console.error(error);

        if (statusEl) {
            statusEl.textContent =
                "Camera unavailable.";
        }

        cameraRetryCount++;

        if (cameraRetryCount >= maxCameraRetries) {

            // Only close the exam after repeated failed attempts
            if (warningEl) {

                warningEl.classList.remove(
                    "d-none",
                    "alert-warning"
                );

                warningEl.classList.add(
                    "alert-danger"
                );

                warningEl.textContent =
                    "Camera access repeatedly denied. Exam cannot continue.";
            }

            closeExam();
            return;
        }

        showCameraRetryUI(
            "Camera permission was denied or the camera is turned off. Please turn on your camera or allow camera access, then click the button below."
        );

    }

}

function showCameraRetryUI(message) {

    const warningEl =
        document.getElementById("warningMessage");

    if (!warningEl) return;

    warningEl.classList.remove(
        "d-none",
        "alert-danger"
    );

    warningEl.classList.add(
        "alert-warning"
    );

    warningEl.innerHTML = `
        ${message}
        <br>
        <button
            class="btn btn-sm btn-primary mt-2"
            onclick="retryCamera()">
            Enable Camera / Retry
        </button>
    `;

}

async function retryCamera() {
    await setupCamera();
}

function startMotionDetection() {

    const videoEl = document.getElementById("cameraVideo");

    if (!videoEl) return;

    // Avoid stacking multiple detection loops if retried
    if (motionDetectionInterval) {
        clearInterval(motionDetectionInterval);
        motionDetectionInterval = null;
    }

    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    let previousFrame = null;

    // FIX: longer warmup so auto-focus/auto-exposure settles before
    // we start comparing frames, and reset the consecutive-hit counter.
    cameraWarmup = true;
    consecutiveMotionHits = 0;

    setTimeout(() => {
        cameraWarmup = false;
    }, CAMERA_WARMUP_MS);

    motionDetectionInterval = setInterval(() => {

        if (examClosed) return;

        if (videoEl.readyState < 2) return;

        canvas.width = videoEl.videoWidth || 320;
        canvas.height = videoEl.videoHeight || 240;

        ctx.drawImage(
            videoEl,
            0,
            0,
            canvas.width,
            canvas.height
        );

        const currentFrame = ctx.getImageData(
            0,
            0,
            canvas.width,
            canvas.height
        );

        if (previousFrame && !cameraWarmup) {

            const motion = calculateFrameDifference(
                previousFrame.data,
                currentFrame.data
            );

            console.log("Motion:", motion);

            if (motion > MOTION_THRESHOLD) {

                // FIX: require the motion to stay high for a couple of
                // consecutive checks before treating it as a real
                // violation. A single spike (light flicker, brief
                // auto-exposure correction, etc.) no longer counts.
                consecutiveMotionHits++;

                if (consecutiveMotionHits >= REQUIRED_CONSECUTIVE_HITS) {
                    incrementCameraWarning();
                    consecutiveMotionHits = 0;
                }

            } else {
                consecutiveMotionHits = 0;
            }

        }

        previousFrame = currentFrame;

    }, 1500);

}

function calculateFrameDifference(prevData, currData) {

    let diffCount = 0;

    const length = Math.min(
        prevData.length,
        currData.length
    );

    for (let i = 0; i < length; i += 4) {

        const rDiff = Math.abs(
            prevData[i] - currData[i]
        );

        const gDiff = Math.abs(
            prevData[i + 1] - currData[i + 1]
        );

        const bDiff = Math.abs(
            prevData[i + 2] - currData[i + 2]
        );

        const pixelDiff =
            (rDiff + gDiff + bDiff) / 3;

        if (pixelDiff > 50) {
            diffCount++;
        }

    }

    return diffCount / (length / 4);

}

function incrementCameraWarning() {

    if (examClosed) return;

    cameraWarningCount++;

    console.log(
        "Camera Warning:",
        cameraWarningCount
    );

    const warningEl =
        document.getElementById("warningMessage");

    if (!warningEl) return;

    if (cameraWarningCount >= maxCameraWarnings) {

        warningEl.classList.remove(
            "d-none",
            "alert-warning"
        );

        warningEl.classList.add(
            "alert-danger"
        );

        warningEl.textContent =
            "Too much movement detected. Exam will close automatically.";

        closeExam();

        return;

    }

    warningEl.classList.remove(
        "d-none",
        "alert-danger"
    );

    warningEl.classList.add(
        "alert-warning"
    );

    warningEl.textContent =
        `Movement detected (${cameraWarningCount}/${maxCameraWarnings}). Please remain in front of the camera.`;

}

function stopCamera() {

    if (motionDetectionInterval) {

        clearInterval(
            motionDetectionInterval
        );

        motionDetectionInterval = null;

    }

    if (cameraStream) {

        cameraStream
            .getTracks()
            .forEach(track => track.stop());

        cameraStream = null;

    }

}
function setupSwitchDetection() {

    // Prevent duplicate listeners
    document.removeEventListener(
        "visibilitychange",
        handleSwitchEvent
    );

    // NOTE: We intentionally do NOT listen to the window "blur" event.
    // "blur" fires for many things that are NOT a real tab/app switch —
    // clicking the camera/notification permission icon, OS notifications,
    // opening DevTools, clicking into the video element, etc. This caused
    // false-positive switch counts even when the user never left the tab.
    // "visibilitychange" (document.hidden) is a much more reliable signal
    // for an actual tab switch, minimize, or app switch.

    document.addEventListener(
        "visibilitychange",
        handleSwitchEvent
    );

}

function handleSwitchEvent(event) {

    if (examClosed) return;

    // Only count when the tab/page actually becomes hidden
    if (!document.hidden) {
        return;
    }

    const now = Date.now();

    // Debounce rapid duplicate events
    if (now - lastSwitchTime < 700) {
        return;
    }

    lastSwitchTime = now;

    switchCount++;

    console.log(
        "Switch Count:",
        switchCount
    );

    updateSwitchWarning();

}

function updateSwitchWarning() {

    const warningEl =
        document.getElementById("warningMessage");

    // Remaining warnings counts DOWN: 10, 9, 8, 7 ... 1, then close
    const remaining = maxSwitchCount - switchCount + 1;

    if (switchCount >= maxSwitchCount) {

        if (warningEl) {

            warningEl.classList.remove(
                "d-none",
                "alert-warning"
            );

            warningEl.classList.add(
                "alert-danger"
            );

            warningEl.textContent =
                "You switched tabs too many times. The exam will now be submitted automatically.";
        }

        showSwitchPopup(
           "Exam is Being Closed!",
           "You switched tabs too many times. Your exam will now be submitted automatically.",
            true
        );

        closeExam();

        return;

    }

    if (warningEl) {

        warningEl.classList.remove(
            "d-none",
            "alert-danger"
        );

        warningEl.classList.add(
            "alert-warning"
        );

        warningEl.textContent =
            `Warning: You left the exam. Remaining warnings: ${remaining}.`;
    }

    showSwitchPopup(
        "Tab Switch Detected!",
        `You switched tabs. Remaining warnings: ${remaining}`,
        false
    );

}

function showSwitchPopup(title, message, isFinal) {

    // Reuse a single popup element instead of stacking multiple
    let popup = document.getElementById("tabSwitchPopup");

    if (!popup) {

        popup = document.createElement("div");
        popup.id = "tabSwitchPopup";

        popup.style.position = "fixed";
        popup.style.top = "0";
        popup.style.left = "0";
        popup.style.width = "100%";
        popup.style.height = "100%";
        popup.style.display = "flex";
        popup.style.alignItems = "center";
        popup.style.justifyContent = "center";
        popup.style.background = "rgba(0, 0, 0, 0.6)";
        popup.style.zIndex = "99999";

        document.body.appendChild(popup);

    }

    popup.innerHTML = `
        <div style="
            background: #fff;
            padding: 30px 40px;
            border-radius: 10px;
            text-align: center;
            max-width: 400px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.4);
            border: 3px solid ${isFinal ? "#dc3545" : "#ffc107"};
        ">
            <h4 style="color: ${isFinal ? "#dc3545" : "#856404"}; margin-bottom: 15px;">
                ${title}
            </h4>
            <p style="margin-bottom: 20px; font-size: 16px;">
                ${message}
            </p>
            ${
                isFinal
                    ? ""
                    : `<button
                        class="btn btn-primary"
                        onclick="document.getElementById('tabSwitchPopup').remove()">
                        OK, Continue Exam
                       </button>`
            }
        </div>
    `;

    popup.style.display = "flex";

    // Auto-dismiss non-final warnings after 4 seconds if user doesn't click OK
    if (!isFinal) {

        clearTimeout(popup._autoDismissTimer);

        popup._autoDismissTimer = setTimeout(() => {

            const el = document.getElementById("tabSwitchPopup");

            if (el) {
                el.remove();
            }

        }, 4000);

    }

}

function closeExam() {

    if (examClosed) return;

    console.log("Exam Closed");

    console.trace();

    examClosed = true;

    if (timerInterval) {

        clearInterval(timerInterval);

        timerInterval = null;

    }

    stopCamera();

    disableExamControls();

    setTimeout(() => {

        submitExam();

    }, 1000);

}

function disableExamControls() {

    document.querySelectorAll("button").forEach(button => {
        button.disabled = true;
    });

    const optionsArea =
        document.getElementById("optionsArea");

    if (optionsArea) {

        optionsArea.innerHTML = `
            <div class="alert alert-danger">
                Exam closed due to repeated rule violations.
            </div>
        `;

    }

}
function renderQuestion() {

    if (!questions[currentQuestion]) return;

    const q = questions[currentQuestion];

    document.getElementById(
        "questionNumber"
    ).innerHTML =
        `Question ${currentQuestion + 1} of ${questions.length}`;

    document.getElementById(
        "questionText"
    ).innerHTML = q.question;

    let html = "";

    q.options.forEach((option, index) => {

        const inputId = `answer-${currentQuestion}-${index}`;

        const checked =
            answers[currentQuestion] === option
                ? "checked"
                : "";

        html += `
            <div class="form-check mt-3">

                <input
                    class="form-check-input"
                    type="radio"
                    id="${inputId}"
                    name="answer"
                    value="${option}"
                    ${checked}
                    onchange="saveAnswer('${option.replace(/'/g, "\\'")}')">

                <label
                    class="form-check-label ${checked ? "selected" : ""}"
                    for="${inputId}">

                    ${option}

                </label>

            </div>
        `;

    });

    document.getElementById(
        "optionsArea"
    ).innerHTML = html;

    updatePaletteSelection();

}

function saveAnswer(answer) {

    answers[currentQuestion] = answer;

    localStorage.setItem(
        "answers",
        JSON.stringify(answers)
    );

    updatePaletteSelection();

}

function nextQuestion() {

    if (currentQuestion < questions.length - 1) {

        currentQuestion++;

        renderQuestion();

    }

}

function previousQuestion() {

    if (currentQuestion > 0) {

        currentQuestion--;

        renderQuestion();

    }

}

function createPalette() {

    let html = "";

    for (let i = 0; i < questions.length; i++) {

        html += `

            <button
                id="palette-${i}"
                class="btn btn-outline-primary m-1"
                onclick="jump(${i})">

                ${i + 1}

            </button>

        `;

    }

    document.getElementById(
        "palette"
    ).innerHTML = html;

    updatePaletteSelection();

}

function updatePaletteSelection() {

    for (let i = 0; i < questions.length; i++) {

        const button =
            document.getElementById(`palette-${i}`);

        if (!button) continue;

        button.classList.remove(
            "palette-current",
            "palette-answered",
            "palette-unanswered"
        );

        if (i === currentQuestion) {

            button.classList.add(
                "palette-current"
            );

        }
        else if (answers[i]) {

            button.classList.add(
                "palette-answered"
            );

        }
        else {

            button.classList.add(
                "palette-unanswered"
            );

        }

    }

}

function jump(index) {

    currentQuestion = index;

    renderQuestion();

}

async function submitExam() {

    // FIX: this guard previously did nothing (empty block, no return),
    // so it was possible for submitExam() to fire twice — once from
    // closeExam()'s setTimeout and again from something else (e.g. the
    // timer callback) racing with it. Now it actually short-circuits.
    if (examClosed && timerInterval === null && submitExam._alreadySubmitting) {
        return;
    }
    submitExam._alreadySubmitting = true;

    if (timerInterval) {

        clearInterval(timerInterval);

        timerInterval = null;

    }

    stopCamera();

    try {

        const response = await fetch(
            "/result/submit",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    answers: answers,
                    questions: questions
                })
            }
        );

        const result =
            await response.json();

        localStorage.setItem(
            "result",
            JSON.stringify(result)
        );

        window.location.href =
            "/result";

    }
    catch (error) {

        console.error(error);

        alert(
            "Unable to submit exam."
        );

    }

}

loadQuestions();