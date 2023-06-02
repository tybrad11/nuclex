from flair.data import Sentence
from flair.models import SequenceTagger
import nltk
import os
import re


class FlairChunker():
    def __init__(self):
        self.chunker = SequenceTagger.load('chunk')

    def get_chunk_spans(self, s):
        sentence = Sentence(s)
        self.chunker.predict(sentence)
        spans = sentence.get_spans('np')
        return spans

flairchunker = FlairChunker()

folder_path = '/mnt/tjb129/Bradshaw2/Tyler/nuclex/nuc_med_articles/from_pmc/Eur_J_Nucl_Med_Mol_Imaging2018/'
file_name =  '5915494.txt'
file_path = os.path.join(folder_path, file_name)

with open(file_path, 'r') as file:
    text = file.read()
    text = re.sub(r"\s{2,}", " ", text)
# Tokenize the text into sentences
sentences = nltk.sent_tokenize(text)
print(sentences[0])




string_counts = {}
for s in sentences:
    # print('\n Input sentence: ', s)
    spans = flairchunker.get_chunk_spans(s)
    for entity in spans:
        if entity.tag == 'NP':
            if entity.text in string_counts:
                string_counts[entity.text] += 1
            else:
                string_counts[entity.text] = 1

sorted_counts = sorted(string_counts.items(), key=lambda x: x[1], reverse=True)

for string, count in sorted_counts:
    print(f"{string}: {count}")