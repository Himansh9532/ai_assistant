import random

def generate_questions(stream):
    question_bank = {
        "Power BI": [
            {"topic": "Power BI", "difficulty": "Medium", "question": "Which Power BI component is used to publish reports and dashboards to the cloud?", "options": ["Power BI Desktop","Power BI Service","Power BI Report Server","Power BI Mobile"], "correct_answer": "Power BI Service"},
            {"topic": "Power BI", "difficulty": "Medium", "question": "Which language is used in Power BI to write calculations for measures and calculated columns?", "options": ["SQL","M","DAX","Python"], "correct_answer": "DAX"},
            {"topic": "Power BI", "difficulty": "Medium", "question": "What is the main purpose of Power Query in Power BI?", "options": ["Create visualizations","Transform and load data","Build data models","Publish dashboards"], "correct_answer": "Transform and load data"},
            {"topic": "Power BI", "difficulty": "Medium", "question": "Which view in Power BI Desktop is used to create relationships between tables?", "options": ["Report View","Data View","Model View","Query View"], "correct_answer": "Model View"},
            {"topic": "Power BI", "difficulty": "Medium", "question": "Which visual type is best for showing trends over time?", "options": ["Pie chart","Line chart","Treemap","Card"], "correct_answer": "Line chart"},
            {"topic": "Power BI", "difficulty": "Medium", "question": "Which feature allows you to combine data from multiple sources in Power BI?", "options": ["Power Query","Power Pivot","Power View","Power Map"], "correct_answer": "Power Query"},
            {"topic": "Power BI", "difficulty": "Easy", "question": "What file extension does Power BI Desktop save reports as?", "options": [".pbix",".pbit",".xlsx",".rpt"], "correct_answer": ".pbix"}
            ,{"topic": "Power BI", "difficulty": "Medium", "question": "Which Power BI feature allows row-level security?", "options": ["RLS","DAX","Power Query","Bookmarks"], "correct_answer": "RLS"},
            {"topic": "Power BI", "difficulty": "Medium", "question": "Which function in DAX returns the total of a column?", "options": ["SUM","TOTAL","AGGREGATE","SUMX"], "correct_answer": "SUM"}
        ],
        "SQL": [
            {"topic": "SQL", "difficulty": "Medium", "question": "Which SQL clause is used to filter rows in a SELECT statement?", "options": ["GROUP BY","ORDER BY","WHERE","HAVING"], "correct_answer": "WHERE"},
            {"topic": "SQL", "difficulty": "Medium", "question": "Which statement removes rows from a table?", "options": ["DROP","DELETE","TRUNCATE","REMOVE"], "correct_answer": "DELETE"},
            {"topic": "SQL", "difficulty": "Medium", "question": "Which function returns the number of rows in a table?", "options": ["COUNT()","SUM()","ROWNUM","LENGTH()"], "correct_answer": "COUNT()"},
            {"topic": "SQL", "difficulty": "Medium", "question": "Which JOIN returns all records from the left table and matching records from the right table?", "options": ["INNER JOIN","LEFT JOIN","RIGHT JOIN","FULL JOIN"], "correct_answer": "LEFT JOIN"},
            {"topic": "SQL", "difficulty": "Medium", "question": "Which clause is used to remove duplicate rows from query results?", "options": ["UNIQUE","DISTINCT","GROUP BY","HAVING"], "correct_answer": "DISTINCT"}
            ,{"topic": "SQL", "difficulty": "Medium", "question": "Which SQL clause is used to restrict returned rows based on aggregated values?", "options": ["WHERE","HAVING","GROUP BY","ORDER BY"], "correct_answer": "HAVING"},
            {"topic": "SQL", "difficulty": "Medium", "question": "Which SQL keyword is used to combine results from two queries?", "options": ["JOIN","UNION","MERGE","COMBINE"], "correct_answer": "UNION"}
        ],
        "Python": [
            {"topic": "Python", "difficulty": "Medium", "question": "Which Python library is most commonly used for data analysis?", "options": ["NumPy","Pandas","Matplotlib","Scikit-learn"], "correct_answer": "Pandas"},
            {"topic": "Python", "difficulty": "Medium", "question": "Which keyword is used to define a function in Python?", "options": ["def","func","function","lambda"], "correct_answer": "def"},
            {"topic": "Python", "difficulty": "Medium", "question": "Which method converts a list into a DataFrame in pandas?", "options": ["pd.DataFrame()","pd.from_list()","pd.to_frame()","pd.create()"], "correct_answer": "pd.DataFrame()"},
            {"topic": "Python", "difficulty": "Medium", "question": "Which operator is used for list comprehension filtering?", "options": ["if","where","filter","select"], "correct_answer": "if"}
            ,{"topic": "Python", "difficulty": "Medium", "question": "Which built-in function returns the length of an object in Python?", "options": ["size()","len()","count()","length()"], "correct_answer": "len()"}
        ],
        "Excel": [
            {"topic": "Excel", "difficulty": "Medium", "question": "Which function calculates the average of a range in Excel?", "options": ["SUM","AVERAGE","COUNT","MIN"], "correct_answer": "AVERAGE"},
            {"topic": "Excel", "difficulty": "Medium", "question": "Which feature performs what-if analysis in Excel?", "options": ["PivotTable","Goal Seek","Data Validation","Filter"], "correct_answer": "Goal Seek"},
            {"topic": "Excel", "difficulty": "Easy", "question": "Which key combination is used to autosum a range?", "options": ["Ctrl+S","Alt+=","Ctrl+Enter","Shift+F3"], "correct_answer": "Alt+="}
            ,{"topic": "Excel", "difficulty": "Medium", "question": "Which function looks up a value in the leftmost column and returns a value in the same row?", "options": ["VLOOKUP","HLOOKUP","INDEX","MATCH"], "correct_answer": "VLOOKUP"}
        ],
        "Statistics": [
            {"topic": "Statistics", "difficulty": "Medium", "question": "Which measure describes how far values spread from the mean?", "options": ["Range","Variance","Median","Mode"], "correct_answer": "Variance"},
            {"topic": "Statistics", "difficulty": "Medium", "question": "Which statistic is the middle value in a sorted dataset?", "options": ["Mean","Median","Mode","Range"], "correct_answer": "Median"},
            {"topic": "Statistics", "difficulty": "Medium", "question": "Which test compares means of two independent groups?", "options": ["ANOVA","Chi-square","T-test","Regression"], "correct_answer": "T-test"}
            ,{"topic": "Statistics", "difficulty": "Medium", "question": "Which distribution is symmetric and bell-shaped?", "options": ["Uniform","Normal","Poisson","Exponential"], "correct_answer": "Normal"}
        ],
        "Data Visualization": [
            {"topic": "Data Visualization", "difficulty": "Medium", "question": "Which chart type is best for comparing categories across a single metric?", "options": ["Line chart","Scatter plot","Bar chart","Pie chart"], "correct_answer": "Bar chart"},
            {"topic": "Data Visualization", "difficulty": "Easy", "question": "Which color scale is good for showing magnitude?", "options": ["Categorical","Sequential","Diverging","Nominal"], "correct_answer": "Sequential"},
            {"topic": "Data Visualization", "difficulty": "Medium", "question": "Which visualization is best for showing distribution of a single numeric variable?", "options": ["Histogram","Scatter plot","Bar chart","Heatmap"], "correct_answer": "Histogram"}
            ,{"topic": "Data Visualization", "difficulty": "Medium", "question": "Which visualization is useful for showing parts of a whole?", "options": ["Bar chart","Pie chart","Histogram","Scatter plot"], "correct_answer": "Pie chart"}
        ],
        "Business Analytics": [
            {"topic": "Business Analytics", "difficulty": "Medium", "question": "Which practice uses data to improve business decisions?", "options": ["Data entry","Data governance","Business analytics","Network security"], "correct_answer": "Business analytics"},
            {"topic": "Business Analytics", "difficulty": "Medium", "question": "Which metric is commonly used to measure customer retention?", "options": ["Churn rate","Click-through rate","Bounce rate","Impressions"], "correct_answer": "Churn rate"},
            {"topic": "Business Analytics", "difficulty": "Medium", "question": "Which analysis estimates value of future cash flows?", "options": ["Regression","Time series","Discounted cash flow","Clustering"], "correct_answer": "Discounted cash flow"}
            ,{"topic": "Business Analytics", "difficulty": "Medium", "question": "Which method segments customers into distinct groups?", "options": ["Regression","Clustering","Time series","Forecasting"], "correct_answer": "Clustering"}
        ],
        "Machine Learning": [
            {"topic": "Machine Learning", "difficulty": "Medium", "question": "Which algorithm is commonly used for classification tasks?", "options": ["Linear regression","K-means","Logistic regression","PCA"], "correct_answer": "Logistic regression"},
            {"topic": "Machine Learning", "difficulty": "Medium", "question": "Which technique reduces model overfitting by combining multiple models?", "options": ["Bagging","Feature scaling","Imputation","Normalization"], "correct_answer": "Bagging"}
            ,{"topic": "Machine Learning", "difficulty": "Medium", "question": "Which method finds groups in unlabeled data?", "options": ["Regression","Classification","Clustering","Dimensionality Reduction"], "correct_answer": "Clustering"}
        ],
        "ETL": [
            {"topic": "ETL", "difficulty": "Medium", "question": "What does ETL stand for in data engineering?", "options": ["Extract Transform Load","Evaluate Transform Load","Extract Transfer Load","Encode Transform Load"], "correct_answer": "Extract Transform Load"},
            {"topic": "ETL", "difficulty": "Medium", "question": "Which tool is commonly used for scheduled data pipelines?", "options": ["Airflow","Excel","PowerPoint","Tableau"], "correct_answer": "Airflow"}
            ,{"topic": "ETL", "difficulty": "Medium", "question": "Which storage type is commonly used for raw data landing?", "options": ["Data warehouse","Data lake","Database","Spreadsheet"], "correct_answer": "Data lake"}
        ],
        "Tableau": [
            {"topic": "Tableau", "difficulty": "Medium", "question": "Which Tableau feature allows creating calculated fields?", "options": ["Calculated Field","Data Blend","Dashboard","Story"], "correct_answer": "Calculated Field"},
            {"topic": "Tableau", "difficulty": "Easy", "question": "Which file extension is used for packaged Tableau workbooks?", "options": [".twbx",".twb",".pbix",".tde"], "correct_answer": ".twbx"}
            ,{"topic": "Tableau", "difficulty": "Medium", "question": "Which Tableau view type emphasizes narrative with multiple sheets?", "options": ["Dashboard","Story","Worksheet","Workbook"], "correct_answer": "Story"}
        ],
        "R": [
            {"topic": "R", "difficulty": "Medium", "question": "Which R function is used to create a linear model?", "options": ["lm()","glm()","model()","fit()"], "correct_answer": "lm()"},
            {"topic": "R", "difficulty": "Medium", "question": "Which package is commonly used for data manipulation in R?", "options": ["dplyr","numpy","pandas","ggplot2"], "correct_answer": "dplyr"}
            ,{"topic": "R", "difficulty": "Medium", "question": "Which plotting package in R is grammar-of-graphics based?", "options": ["ggplot2","lattice","graphics","plotly"], "correct_answer": "ggplot2"},
            {"topic": "R", "difficulty": "Medium", "question": "Which function in R reads CSV files into a dataframe?", "options": ["read.csv()","read_csv()","import_csv()","load_csv()"], "correct_answer": "read.csv()"}
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

    if not pool:
        return []

    # Number of questions to return. Do not create duplicates if pool is smaller
    # than desired — instead return all available unique questions.
    desired_total = 50
    total_questions = min(desired_total, len(pool))

    # If we have enough unique questions, sample without replacement.
    if len(pool) >= total_questions:
        sampled_questions = random.sample(pool, total_questions)
    else:
        # Fallback: return the entire pool (unique questions only).
        sampled_questions = list(pool)

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
