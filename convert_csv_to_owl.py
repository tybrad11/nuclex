import os
import csv, types
from owlready2 import *

"""
This file contains a script to create a NucLex OWL ontology
"""

nuclex_iri = 'http://webprotege.stanford.edu/NucLex'
nuclex_owl_path = os.path.join(r".", "NucLex.v0.1beta.owl")

# create the base class and attributes, if it hasn't already been done
if not os.path.isfile(nuclex_owl_path):
    onto = get_ontology(nuclex_iri)
    with onto:
        class Preferred_name(AnnotationProperty):
            range = [str]
        class Parent_class_name(AnnotationProperty):
            range = [str]
        class RadLex_RID(AnnotationProperty):
            range = [str]
        class NCI_Thesaurus_Code(AnnotationProperty):
            range = [str]
        class UMLS_CUI(AnnotationProperty):
            range = [str]
        # RadLex_entity class
        class NID000001(Thing):
            pass
    onto.save(nuclex_owl_path)
    onto.destroy(update_relation=True, update_is_a=True)

#path to csv (that has been converted, use convert_csv_formats.py)
path_to_csv = os.path.join(r".", "NucLex_new.csv")

onto = get_ontology(nuclex_owl_path).load()
f = open(path_to_csv)
reader = csv.reader(f)
#skip firs line
next(reader)
with onto:
    for row in reader:
        NucLex_NID, Preferred_name, Parent_class_id, Parent_class_name, RadLex_RID, NCI_Thesaurus_Code, UMLS_CUI = row
        if Parent_class_id:
            Parent_class_id = onto[Parent_class_id]
        else:
            Parent_class_id = Thing
        Class = types.new_class(NucLex_NID, (Parent_class_id,))
        if Preferred_name:
            Class.Preferred_name = Preferred_name
        if Parent_class_name:
            Class.Parent_class_name = Parent_class_name
        if RadLex_RID:
            Class.RadLex_RID = RadLex_RID
        if NCI_Thesaurus_Code:
            Class.NCI_Thesaurus_Code = NCI_Thesaurus_Code
        if UMLS_CUI:
            Class.UMLS_CUI = UMLS_CUI
# onto_classes.save(nuclex_classes_path)
onto.save(nuclex_owl_path)




