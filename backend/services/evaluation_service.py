def evaluate_exam(questions, answers):

    total_questions = len(questions)

    correct_answers = 0

    topic_scores = {}

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

    percentage = round(
        (correct_answers / total_questions) * 100,
        2
    )

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

    strong_topics = []
    weak_topics = []

    for topic, score_data in topic_scores.items():

        topic_percentage = (
            score_data["correct"] /
            score_data["total"]
        ) * 100

        if topic_percentage >= 70:
            strong_topics.append(topic)
        else:
            weak_topics.append(topic)

    feedback = f"""
Strengths:
{', '.join(strong_topics) if strong_topics else 'None'}

Areas for Improvement:
{', '.join(weak_topics) if weak_topics else 'None'}

Recommended Learning Topics:
Focus on weak areas and practice more MCQs.
"""

    return {
        "score": correct_answers,
        "total_questions": total_questions,
        "percentage": percentage,
        "grade": grade,
        "feedback": feedback,
        "topic_scores": topic_scores
    }