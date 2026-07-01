import random

def generate_questions(stream):
    question_bank = {
        "Power BI": [
            {
                "topic": "Power BI",
                "difficulty": "Medium",
                "question": "Which Power BI component is used to publish reports and dashboards to the cloud?",
                "options": [
                    "Power BI Desktop",
                    "Power BI Service",
                    "Power BI Report Server",
                    "Power BI Mobile"
                ],
                "correct_answer": "Power BI Service"
            },
            {
                "topic": "Power BI",
                "difficulty": "Medium",
                "question": "Which language is used in Power BI to write calculations for measures and calculated columns?",
                "options": [
                    "SQL",
                    "M",
                    "DAX",
                    "Python"
                ],
                "correct_answer": "DAX"
            },
            {
                "topic": "Power BI",
                "difficulty": "Medium",
                "question": "What is the main purpose of Power Query in Power BI?",
                "options": [
                    "Create visualizations",
                    "Transform and load data",
                    "Build data models",
                    "Publish dashboards"
                ],
                "correct_answer": "Transform and load data"
            },
            {
                "topic": "Power BI",
                "difficulty": "Medium",
                "question": "Which view in Power BI Desktop is used to create relationships between tables?",
                "options": [
                    "Report View",
                    "Data View",
                    "Model View",
                    "Query View"
                ],
                "correct_answer": "Model View"
            },
            {
                "topic": "Power BI",
                "difficulty": "Medium",
                "question": "Which visual type is best for showing trends over time?",
                "options": [
                    "Pie chart",
                    "Line chart",
                    "Treemap",
                    "Card"
                ],
                "correct_answer": "Line chart"
            }
        ],
        "SQL": [
            {
                "topic": "SQL",
                "difficulty": "Medium",
                "question": "Which SQL clause is used to filter rows in a SELECT statement?",
                "options": [
                    "GROUP BY",
                    "ORDER BY",
                    "WHERE",
                    "HAVING"
                ],
                "correct_answer": "WHERE"
            },
            {
                "topic": "SQL",
                "difficulty": "Medium",
                "question": "Which statement removes rows from a table?",
                "options": [
                    "DROP",
                    "DELETE",
                    "TRUNCATE",
                    "REMOVE"
                ],
                "correct_answer": "DELETE"
            }
        ],
        "Python": [
            {
                "topic": "Python",
                "difficulty": "Medium",
                "question": "Which Python library is most commonly used for data analysis?",
                "options": [
                    "NumPy",
                    "Pandas",
                    "Matplotlib",
                    "Scikit-learn"
                ],
                "correct_answer": "Pandas"
            }
        ],
        "Excel": [
            {
                "topic": "Excel",
                "difficulty": "Medium",
                "question": "Which function calculates the average of a range in Excel?",
                "options": [
                    "SUM",
                    "AVERAGE",
                    "COUNT",
                    "MIN"
                ],
                "correct_answer": "AVERAGE"
            }
        ],
        "Statistics": [
            {
                "topic": "Statistics",
                "difficulty": "Medium",
                "question": "Which measure describes how far values spread from the mean?",
                "options": [
                    "Range",
                    "Variance",
                    "Median",
                    "Mode"
                ],
                "correct_answer": "Variance"
            }
        ],
        "Data Visualization": [
            {
                "topic": "Data Visualization",
                "difficulty": "Medium",
                "question": "Which chart type is best for comparing categories across a single metric?",
                "options": [
                    "Line chart",
                    "Scatter plot",
                    "Bar chart",
                    "Pie chart"
                ],
                "correct_answer": "Bar chart"
            }
        ],
        "Business Analytics": [
            {
                "topic": "Business Analytics",
                "difficulty": "Medium",
                "question": "Which practice uses data to improve business decisions?",
                "options": [
                    "Data entry",
                    "Data governance",
                    "Business analytics",
                    "Network security"
                ],
                "correct_answer": "Business analytics"
            }
        ]
    }

    stream_lower = stream.lower() if stream else ""
    if "power bi" in stream_lower or "data analyst" in stream_lower or "business analyst" in stream_lower:
        topics = ["Power BI", "Business Analytics", "SQL", "Python", "Excel"]
    else:
        topics = list(question_bank.keys())

    pool = []
    for topic in topics:
        pool.extend(question_bank.get(topic, []))

    total_questions = min(100, len(pool))
    sampled_questions = random.sample(pool, total_questions)

    questions = []
    for idx, template in enumerate(sampled_questions, start=1):
        questions.append({
            "id": idx,
            "topic": template["topic"],
            "difficulty": template["difficulty"],
            "question": template["question"],
            "options": template["options"],
            "correct_answer": template["correct_answer"]
        })

    return questions
