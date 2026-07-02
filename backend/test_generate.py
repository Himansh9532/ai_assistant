from services.ai_service import generate_questions

q = generate_questions('')
print('returned:', len(q))
texts = [x['question'] for x in q]
print('unique:', len(set(texts)))
for i,t in enumerate(texts, start=1):
    print(i, t)
