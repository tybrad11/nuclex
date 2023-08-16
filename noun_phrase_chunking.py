from flair.data import Sentence
from flair.models import SequenceTagger
import nltk
import os
import re
import csv

class FlairChunker():
    def __init__(self):
        self.chunker = SequenceTagger.load('chunk')

    def get_chunk_spans(self, s):
        sentence = Sentence(s)
        self.chunker.predict(sentence)
        spans = sentence.get_spans('np')
        return spans

def get_text_files(directory):
    text_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):  # Adjust the file extension as needed
                text_files.append(os.path.join(root, file))
    return text_files

def remove_articles(input_text):
    if input_text[:2].lower() == 'a ':
        input_text = input_text[2:]
    if input_text[:3].lower() == 'an ':
        input_text = input_text[3:]
    if input_text[:4].lower() == 'the ':
        input_text = input_text[4:]
    if input_text[:5].lower() == 'this ':
        input_text = input_text[5:]
    if input_text[:5].lower() == 'that ':
        input_text = input_text[5:]
    return input_text


flairchunker = FlairChunker()
string_counts = {}

# folders = ['/mnt/tjb129/Bradshaw2/Tyler/nuclex/nuc_med_articles/from_pmc', '/mnt/tjb129/Bradshaw2/Tyler/nuclex/nuc_med_articles/from_pmc_non_nucmed']
folders = ['/mnt/tjb129/Bradshaw2/Tyler/nuclex/nuc_med_articles/from_pmc_non_nucmed']

for folder in folders:
    text_files = get_text_files(folder)

    for file_path in text_files:
        print(file_path)
        with open(file_path, 'r') as file:
            text = file.read()
            text = re.sub(r"\s{2,}", " ", text)
        # Tokenize the text into sentences
        sentences = nltk.sent_tokenize(text)
        # print(sentences[0])


        for s in sentences:
            # print('\n Input sentence: ', s)
            spans = flairchunker.get_chunk_spans(s)
            for entity in spans:
                if entity.tag == 'NP':
                    entity_text = remove_articles(entity.text)
                    entity_text = entity_text.lower()
                    if entity_text in string_counts:
                        string_counts[entity_text] += 1
                    else:
                        string_counts[entity_text] = 1
        print('Length of string_counts: ' + str(len(string_counts)))

    sorted_counts = sorted(string_counts.items(), key=lambda x: x[1], reverse=True)

    csv_file_path = os.path.join(folder, "noun_counts.csv")

    # Save the sorted counts to a CSV file
    with open(csv_file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["String", "Count"])  # Write header
        writer.writerows(sorted_counts)  # Write rows
