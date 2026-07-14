from src.extractor import extract_entities, extract_relations

text = "My brother James just started a new job at Google. James lives in Seattle."

print("Entities:", extract_entities(text))
print("Relations:")
for r in extract_relations(text):
    print(" ", r)