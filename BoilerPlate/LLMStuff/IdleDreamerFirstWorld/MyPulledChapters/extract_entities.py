import json
from pathlib import Path
from flair.data import Sentence
from flair.models import SequenceTagger

# Load the NER tagger model
tagger = SequenceTagger.load('ner')

def extract_entities(file_path):
    with open(file_path, 'r') as file:
        text = file.read().lower()

    # Create a Flair sentence object
    sentence = Sentence(text)

    # Run the NER tagger on the sentence
    tagger.predict(sentence)

    entities = {}
    for entity in sentence.get_spans('ner'):
        label = entity.tag
        text = entity.text

        # Check if entity is a person, organization, geo-political entity or product
        if label in ['PER', 'ORG', 'LOC', 'MISC']:
            if text not in entities:
                entities[text] = {'pos': label, 'nouns': [], 'adverbs': [], 'adjectives': [], 'verbs': [], 'pronouns': []}

            # Extract related words based on their part-of-speech
            for token in entity.tokens:
                if token.pos.startswith('N') and not token.is_stop:
                    entities[text]['nouns'].append(token.text)
                elif token.pos == 'ADV':
                    entities[text]['adverbs'].append(token.text)
                elif token.pos == 'ADJ':
                    entities[text]['adjectives'].append(token.text)
                elif token.pos.startswith('V'):
                    entities[text]['verbs'].append(token.text)
                elif token.pos == 'PRON':
                    entities[text]['pronouns'].append(token.text)

    return entities

# Example usage:
folder_path = Path('.')
files = sorted([file for file in folder_path.glob('*.txt')])

# Create "Entities" folder if it doesn't exist
entities_folder = folder_path / "Entities"
entities_folder.mkdir(parents=True, exist_ok=True)

# Extract entities from each file and write to JSON
entities_dict = {}
for file in files:
    print(f"Processing file: {file}")
    entities = extract_entities(file)
    entities_dict[file.stem] = {'names': entities}

output_file = entities_folder / "entities.json"
with open(output_file, 'w') as f:
    json.dump(entities_dict, f, indent=2)

print(f"Entities written to {output_file}")