import re
import spacy
from . import config

nlp = spacy.load(config.SPACY_MODEL)

# predicate patterns: (regex, predicate_name, subject_group, object_group)
FAMILY_TERMS = {
    "brother": "is_brother_of", "sister": "is_sister_of",
    "mother": "is_mother_of", "father": "is_father_of",
    "husband": "is_husband_of", "wife": "is_wife_of",
    "son": "is_son_of", "daughter": "is_daughter_of",
    "friend": "is_friend_of",
}

FAMILY_PATTERN = re.compile(
    r"\bmy\s+(" + "|".join(FAMILY_TERMS.keys()) + r")\s+(?:named\s+|called\s+)?([A-Z][a-zA-Z]+)",
    re.IGNORECASE,
)

JOB_PATTERN = re.compile(
    r"([A-Z][a-zA-Z]+)\s+(?:just\s+|recently\s+)?(?:works at|works for|is employed at|"
    r"got a job at|started (?:a\s+)?(?:new\s+)?job at)\s+((?:[A-Z][a-zA-Z0-9&]*\s?)+)",
)

LIVES_PATTERN = re.compile(
    r"([A-Z][a-zA-Z]+)\s+lives? in\s+((?:[A-Z][a-zA-Z]*\s?)+)",
)

def extract_entities(text: str):
    """Return spaCy-detected named entities: [(text, label), ...]"""
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]


def extract_relations(text: str, speaker: str = "Me"):
    """
    Pattern-match relation triples out of a sentence.
    Returns list of dicts: {subject, predicate, object, subject_type, object_type}
    `speaker` is who said this line -- used to resolve "my brother" to a real subject.
    """
    relations = []

    for match in FAMILY_PATTERN.finditer(text):
        relation_word, name = match.groups()
        predicate = FAMILY_TERMS[relation_word.lower()]
        relations.append({
            "subject": name, "predicate": predicate, "object": speaker,
            "subject_type": "person", "object_type": "person",
        })

    for match in JOB_PATTERN.finditer(text):
        name, org = match.groups()
        relations.append({
            "subject": name, "predicate": "works_at", "object": org.strip(),
            "subject_type": "person", "object_type": "org",
        })

    for match in LIVES_PATTERN.finditer(text):
        name, place = match.groups()
        relations.append({
            "subject": name, "predicate": "lives_in", "object": place.strip(),
            "subject_type": "person", "object_type": "location",
        })
        
    return relations