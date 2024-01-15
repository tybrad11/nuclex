import pandas as pd
import os
import csv
import re
from utils import is_in_radlex, is_in_nci_thesaurus, is_in_umls

"""
This file contains scripts for converting from one format of csv (hierarchy style, where col1 is parent class, col2 is 
child class, col3 is grandchild class, etc) to a format that is easier to convert into owl (class_name, parent_class)
"""

def index_of_substring(substring, string_list):
    matches = [i for i, string in enumerate(string_list) if substring in string]
    return matches


def make_concepts_lower_case(value):
    # but keep words that are all capital, or isotopes
    # if it's all upper, don't change it
    if not value.isupper():
        # if it's multiple words
        strings = value.rstrip().split(' ')
        new_strings = strings.copy()
        print(new_strings)
        for i, s in enumerate(strings):
            # if it's an isotope, F-18, Cu-64, etc
            if len(s) > 2:
                if s[1] == '-' or s[2] == '-':
                    new_strings[i] = s
                # don't change if it's all upper
                elif s.isupper():
                    new_strings[i] = s
                else:
                    new_strings[i] = s.lower()
            else:
                new_strings[i] = s.lower()
        value = " ".join(new_strings)  # concatenate back together

    return value


# input nuclex and output nuclex
input_csv = os.path.join(r"C:\Users\tjb129\Downloads\NucLex & Common Data Elements - Theranostics.csv")
output_csv = os.path.join(r"C:\Users\tjb129\Downloads\NucLex_new.csv")

# for determining if term is in other ontology
path_radlex = os.path.join(
    r"\\onfnas01.uwhis.hosp.wisc.edu\radiology\Research\Bradshaw\Tyler\nuclex\radlex_owl\Radlex_separate_synonyms.xls")
path_nci = os.path.join(
    r"\\onfnas01.uwhis.hosp.wisc.edu\radiology\Research\Bradshaw\Tyler\nuclex\nci_thesaurus_owl\Thesaurus_curated.csv")
df_radlex = pd.read_excel(path_radlex)
df_nci = pd.read_csv(path_nci)

with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # skip a few lines
    next(reader)
    next(reader)

    # Write header row
    writer.writerow(
        ['NucLex_NID', 'Preferred_name', 'Parent_class_id', 'Parent_class_name', 'RadLex_RID', 'NCI_Thesaurus_Code',
         'UMLS_CUI'])
    # write first entry, radlex entity
    writer.writerow(['NID000001', 'RadLex entity', 'owl:Thing', 'owl:Thing', 'http://www.radlex.org/RID/#RID1', '', ''])

    # store the parent classes through the loop
    parent_classes_name = ['RadLex entity', '1', '2', '3', '4', '5', '6', '7']
    parent_classes_id = ['NID000001', '1', '2', '3', '4', '5', '6', '7']

    for row in reader:

        for ind in range(7):
            value = row[ind]
            if value:
                value = make_concepts_lower_case(value)
                parent_classes_name[ind + 1] = value
                parent_classes_id[ind + 1] = row[7]
                save_value = value
                save_id = row[7]
                save_parent_name = parent_classes_name[ind]
                save_parent_id = parent_classes_id[ind]

        # free_text_comment = row[12]
        # if free_test_comment:
        #     strings = re.split(r",| {1,}", free_text_comment.strip())  # Split by comma or one or more spaces
        #     radlex_match = index_of_substring("radlex.org", strings)
        #     umls_match = index_of_substring("radlex.org", strings)
        #     nci_thes_match = index_of_substring("radlex.org", strings)
        #     snomed_match = index_of_substring("radlex.org", strings)
        #     other_match = index_of_substring("radlex.org", strings)

        radlex_id = is_in_radlex(df_radlex, save_value)
        nci_id = is_in_nci_thesaurus(df_nci, save_value)
        umls_cui = is_in_umls(save_value)

        f = writer.writerow([save_id, save_value, save_parent_id, save_parent_name, radlex_id, nci_id, umls_cui])


