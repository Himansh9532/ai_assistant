let currentQuestion = 0;
let questions = [];
let answers = {};

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

        createPalette();

        renderQuestion();

    }
    catch (error) {

        console.error(error);

        alert("Unable to load questions from backend.");

    }
}

function renderQuestion() {

    if (!questions[currentQuestion]) {
        return;
    }

    const q = questions[currentQuestion];

    document.getElementById(
        "questionNumber"
    ).innerHTML =
        `Question ${currentQuestion + 1} of ${questions.length}`;

    document.getElementById(
        "questionText"
    ).innerHTML = q.question;

    let html = "";

    q.options.forEach((option) => {

        const checked =
            answers[currentQuestion] === option
                ? "checked"
                : "";

        html += `
        <div class="form-check mt-3">

            <input
                type="radio"
                name="answer"
                value="${option}"
                ${checked}
                onchange="saveAnswer(this.value)"
                class="form-check-input">

            <label class="form-check-label">
                ${option}
            </label>

        </div>
        `;
    });

    document.getElementById(
        "optionsArea"
    ).innerHTML = html;
}

function saveAnswer(answer) {

    answers[currentQuestion] = answer;

    localStorage.setItem(
        "answers",
        JSON.stringify(answers)
    );
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
            class="btn btn-outline-primary m-1"
            onclick="jump(${i})">

            ${i + 1}

        </button>
        `;
    }

    document.getElementById(
        "palette"
    ).innerHTML = html;
}

function jump(index) {

    currentQuestion = index;

    renderQuestion();
}

async function submitExam() {

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

        const result = await response.json();

        localStorage.setItem(
            "result",
            JSON.stringify(result)
        );

        window.location.href = "/result";

    }
    catch (error) {

        console.error(error);

        alert("Unable to submit exam.");

    }
}

loadQuestions();