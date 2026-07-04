def evaluate_exam(questions, answers):

    total_questions = len(questions)

    if total_questions == 0:
        return {
            "score": 0,
            "total_questions": 0,
            "percentage": 0,
            "grade": "N/A",
            "feedback": "No questions were available for evaluation.",
            "topic_scores": {}
        }

    correct_answers = 0
    topic_scores = {}

    # Evaluate answers
    for index, question in enumerate(questions):

        selected_answer = answers.get(str(index))
        correct_answer = question.get("correct_answer")
        topic = question.get("topic", "General")

        if topic not in topic_scores:
            topic_scores[topic] = {
                "correct": 0,
                "total": 0
            }

        topic_scores[topic]["total"] += 1

        if selected_answer == correct_answer:
            correct_answers += 1
            topic_scores[topic]["correct"] += 1

    # Overall Percentage
    percentage = round(
        (correct_answers / total_questions) * 100,
        2
    )

    # Grade Calculation
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    # Topic Analysis
    strong_topics = []
    average_topics = []
    weak_topics = []

    for topic, score_data in topic_scores.items():

        topic_percentage = round(
            (
                score_data["correct"] /
                score_data["total"]
            ) * 100,
            2
        )

        topic_scores[topic]["percentage"] = topic_percentage

        if topic_percentage >= 75:
            strong_topics.append(topic)

        elif topic_percentage >= 50:
            average_topics.append(topic)

        else:
            weak_topics.append(topic)

    # Feedback Messages
    strengths_message = (
        ", ".join(strong_topics)
        if strong_topics
        else "No strong areas identified yet."
    )

    improvement_message = (
        ", ".join(weak_topics)
        if weak_topics
        else "No major weak areas found."
    )

    if weak_topics:
        recommended_topics = (
            f"Focus more on: {', '.join(weak_topics)}."
        )
    else:
        recommended_topics = (
            "Keep practicing to maintain your excellent performance."
        )

    feedback = f"""
Strengths:
{strengths_message}

Areas for Improvement:
{improvement_message}

Recommended Learning Topics:
{recommended_topics}
"""

    return {
        "score": correct_answers,
        "total_questions": total_questions,
        "percentage": percentage,
        "grade": grade,
        "feedback": feedback,
        "topic_scores": topic_scores,
        "strong_topics": strong_topics,
        "average_topics": average_topics,
        "weak_topics": weak_topics
    }