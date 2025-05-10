import duckdb
import json

con = duckdb.connect("wiktionary.duckdb")

def dictionary(word: str):
    results = con.execute("""
        SELECT pos, senses, derived
        FROM words
        WHERE word = ? AND lang = 'English'
        LIMIT 5
    """, (word,)).fetchall()

    if not results:
        return None
    
    pos_entries = {}
    all_examples = []
    for pos, senses_json, derived_json in results:
        if pos not in pos_entries:
            pos_entries[pos] = {
                "part_of_speech": pos,
                "definitions": []
            }

        try:
            senses = json.loads(senses_json)
        except Exception:
            senses = []
            
        seen_glosses = set()
        for sense in senses:
            glosses = sense.get("glosses") or sense.get("gloss") or []
            if isinstance(glosses, str):
                glosses = [glosses]
            elif not isinstance(glosses, list):
                glosses = []
            for gloss in glosses:
                if gloss not in seen_glosses:
                    seen_glosses.add(gloss)
                    definition = {"text": gloss}
                    examples = sense.get("examples", [])[:3]
                    if examples:
                        all_examples.extend([example["text"] for example in examples])
                    pos_entries[pos]["definitions"].append(definition)

    for pos, entry in pos_entries.items():
        unique_definitions = {json.dumps(definition): definition for definition in entry["definitions"]}
        entry["definitions"] = list(unique_definitions.values())
        
    all_examples = list(set(all_examples))[:3]
    entries = list(pos_entries.values())
    return json.dumps({
        "word": word,
        "language": "English",
        "entries": entries,
        "examples": all_examples
    }, indent=2)
