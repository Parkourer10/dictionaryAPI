# Dictionary API
a simple FastAPI dictionary API that serves definitions, parts of speech, and example usages of english words by querying a local duckdb database. Access the api [here](https://dictionary.fonders.org/)

## Structure of an example word defination:
```json
{
  "word": "cat",
  "language": "English",
  "entries": [
    {
      "part_of_speech": "noun",
      "definitions": [
        { "text": "A small domesticated carnivorous mammal." },
        { "text": "A malicious or spiteful woman." }
      ]
    }
  ],
  "examples": [
    "The cat chased the mouse.",
    "She acted like a real cat at the meeting."
  ]
}


```
