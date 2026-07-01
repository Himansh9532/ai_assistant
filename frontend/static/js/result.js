const result = JSON.parse(localStorage.getItem("result"));

const scoreArea = document.getElementById("scoreArea");
const percentageArea = document.getElementById("percentageArea");
const gradeArea = document.getElementById("gradeArea");
const feedbackArea = document.getElementById("feedbackArea");
const topicsArea = document.getElementById("topics");

if (!result) {
    if (scoreArea) scoreArea.textContent = "Score: --";
    if (percentageArea) percentageArea.textContent = "Percentage: --";
    if (gradeArea) gradeArea.textContent = "Grade: --";
    if (feedbackArea) feedbackArea.textContent = "Result not found or session expired.";
    if (topicsArea) topicsArea.innerHTML = "";
} else {
    if (scoreArea) scoreArea.textContent = `Score: ${result.score}/${result.total_questions}`;
    if (percentageArea) percentageArea.textContent = `Percentage: ${result.percentage}%`;
    if (gradeArea) gradeArea.textContent = `Grade: ${result.grade}`;
    if (feedbackArea) feedbackArea.textContent = result.feedback || "No feedback available.";

    if (topicsArea) {
        let html = "";
        for (const topic in result.topic_scores) {
            const data = result.topic_scores[topic];
            html += `
                <div class="mb-2">
                    <strong>${topic}</strong>: ${data.correct} / ${data.total}
                </div>
            `;
        }
        topicsArea.innerHTML = html || "No topic details available.";
    }

    const downloadBtn = document.getElementById("downloadResultBtn");
    if (downloadBtn) {
        downloadBtn.addEventListener("click", () => {
            const text = [
                `Assessment Result`,
                `Score: ${result.score}/${result.total_questions}`,
                `Percentage: ${result.percentage}%`,
                `Grade: ${result.grade}`,
                ``,
                `Topics:`,
                ...Object.keys(result.topic_scores).map(topic =>
                    `${topic}: ${result.topic_scores[topic].correct} / ${result.topic_scores[topic].total}`
                ),
                ``,
                `AI Feedback:`,
                result.feedback || "No feedback available."
            ].join("\n");

            const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "assessment_result.txt";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }
}
