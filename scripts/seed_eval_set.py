import json, os

EXAMPLES = [
    {"question": "Quel est l'objet du document 1 ?", "answer": "document"},
    {"question": "Quel est l'auteur mentionné ?", "answer": "auteur"},
]

with open("data/eval_set.json", "w", encoding="utf-8") as f:
    json.dump(EXAMPLES, f, ensure_ascii=False, indent=2)
print("Wrote data/eval_set.json")
