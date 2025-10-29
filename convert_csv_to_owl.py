# import os
# import csv, types
# from owlready2 import *

# nuclex_iri = 'http://webprotege.stanford.edu/NucLex'
# nuclex_owl_path = os.path.join(r"H:\Data\NucLex_OWLs", "NucLex_new_Oct2025.owl")
# nuclex_classes_path = os.path.join(r"H:\Data\NucLex_OWLs", "NucLex_classes_new_Oct2025.owl")

# #create the base class and attributes, if it hasn't already been done
# if not os.path.isfile(nuclex_owl_path):
    
#    # onto = Ontology(nuclex_iri)

#     onto = get_ontology(nuclex_iri)    
#     with onto:
#         class Preferred_name(AnnotationProperty):
#             range = [str]
#         class Parent_class_name(AnnotationProperty):
#             range = [str]
#         class RadLex_RID(AnnotationProperty):
#             range = [str]
#         class NCI_Thesaurus_Code(AnnotationProperty):
#             range = [str]
#         class UMLS_CUI(AnnotationProperty):
#             range = [str]
#         #RadLex_entity class
#         class NID000001(Thing):
#             pass
#     onto.save(nuclex_owl_path)
#     onto.destroy(update_relation = True, update_is_a = True)

# path_to_csv = os.path.join(r"C:\Users\tjb129\Downloads", "NucLex_new_Oct2025.csv")


# onto = get_ontology(nuclex_owl_path).load()
# # onto_classes = get_ontology(nuclex_iri)
# # onto_classes.imported_ontologies.append(onto)
# f = open(path_to_csv)
# reader = csv.reader(f)
# next(reader)
# with onto:
#     for i, row in enumerate(reader):
#         print('')
#         print(i)
#         print(row)
#         NucLex_NID, Preferred_name, Parent_class_id, Parent_class_name, RadLex_RID, NCI_Thesaurus_Code, UMLS_CUI  = row
#         if Parent_class_id: 
#             Parent_class_id = onto[Parent_class_id]
#         else: 
#             Parent_class_id = Thing
#         Class = types.new_class(NucLex_NID, (Parent_class_id,))
#         if Preferred_name:
#             Class.Preferred_name = Preferred_name
#         if Parent_class_name:
#             Class.Parent_class_name = Parent_class_name
#         if RadLex_RID:
#             Class.RadLex_RID = RadLex_RID
#         if NCI_Thesaurus_Code:
#             Class.NCI_Thesaurus_Code = NCI_Thesaurus_Code
#         if UMLS_CUI:
#             Class.UMLS_CUI = UMLS_CUI
# # onto_classes.save(nuclex_classes_path)
# onto.save(nuclex_owl_path)

# onto = get_ontology(nuclex_owl_path).load()
# f = open(path_to_csv)
# reader = csv.reader(f)
# next(reader)

# with onto:
#     for row in reader:
#         NucLex_NID, Preferred_name, Parent_class_id, Parent_class_name, RadLex_RID, NCI_Thesaurus_Code, UMLS_CUI  = row
#         if Parent_class_id:
#             new_class = types.new_class(NucLex_NID, (Parent_class_id,))
#         else:
#             new_class = types.new_class(NucLex_NID, (Thing,))

#         # Create properties for attributes
#         if Preferred_name:
#             onto.FunctionalProperty(Preferred_name, DataType=str)  # Adjust DataType if needed
#             new_class.is_a.append(onto[Preferred_name].some(str))  # Link class to property
#         if Parent_class_name:
#             onto.FunctionalProperty(Parent_class_name, DataType=str)
#             new_class.is_a.append(onto[Parent_class_name].some(str))
#         if RadLex_RID:
#             onto.FunctionalProperty(RadLex_RID, DataType=str)
#             new_class.is_a.append(onto[RadLex_RID].some(str))

# onto.save(nuclex_classes_path)



# onto.save(file=".owl", format="rdfxml")




import os
import csv, types
from owlready2 import *

# Suppress the Cython warning if it's bothersome, though it's just informational
# import owlready2
# owlready2.set_options(warn_old_cython = False)

nuclex_iri = 'http://webprotege.stanford.edu/NucLex'
nuclex_owl_path = os.path.join(r"H:\Data\NucLex_OWLs", "NucLex_new_Oct2025.owl")
path_to_csv = os.path.join(r"C:\Users\tjb129\Downloads", "NucLex_new_Oct2025.csv")

# 1. Create the base ontology with annotation properties ONLY if it doesn't exist
if not os.path.isfile(nuclex_owl_path):
    print(f"Base ontology file not found. Creating new one at: {nuclex_owl_path}")
    
    # This is the fix: Start directly with get_ontology()
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
        
        # Define the root class
        class NID000001(Thing):
            pass
            
    onto.save(nuclex_owl_path)
    print("Base ontology saved.")
    # No need to destroy() it, we'll just load it next

# 2. Load the ontology (either the new one or the existing one)
print(f"Loading ontology from: {nuclex_owl_path}")
onto = get_ontology(nuclex_owl_path).load()

# 3. Open and read the CSV to add/update classes
print("Reading CSV and populating ontology...")
f = open(path_to_csv)
reader = csv.reader(f)
next(reader) # Skip header row

with onto:
    for i, row in enumerate(reader):
        # Unpack the row
        NucLex_NID, Preferred_name, Parent_class_id, Parent_class_name, RadLex_RID, NCI_Thesaurus_Code, UMLS_CUI = row

        # Determine the parent class
        if Parent_class_id:
            Parent_class = onto[Parent_class_id] # Look up parent by name
            if Parent_class is None:
                print(f"Warning: Parent class '{Parent_class_id}' not found for '{NucLex_NID}'. Defaulting to Thing.")
                Parent_class = Thing
        else: 
            Parent_class = Thing # Default to top-level Thing

        # Get the class if it exists, or create it if it doesn't
        # This handles the case where NID000001 (the root) is in the CSV
        Class = onto[NucLex_NID]
        if Class is None:
            Class = types.new_class(NucLex_NID, (Parent_class,))
        else:
            # If class already exists, just update its parent
            Class.is_a.append(Parent_class)

        # Add all annotations to the class
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

# 4. Save the final, populated ontology
print("Saving populated ontology...")
onto.save(nuclex_owl_path, format="rdfxml")
print("Process complete.")

# --- The entire second loop and final save lines from your script have been removed ---
# They were redundant and logically incorrect.



