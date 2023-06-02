'''
This is code for adding skos:prefLabel to the RadLex ontology so that it displays correctly in WebProtege

'''

import os
import fileinput

# test_text_path = os.path.join(r"/mnt/tjb129/Bradshaw/Tyler/nuclex/delete_me_test.txt")
# write_text_path = os.path.join(r"/mnt/tjb129/Bradshaw/Tyler/nuclex/delete_me_test_out.txt")

input_text_path = os.path.join(r"/mnt/tjb129/Bradshaw/Tyler/nuclex/radlex_owl/RadLex_skosPrefLabel_startingTemplate.owl")
write_text_path = os.path.join(r"/mnt/tjb129/Bradshaw/Tyler/nuclex/radlex_owl/RadLex_skos_added.owl")

with open(input_text_path, 'r') as file:
    with open(write_text_path, 'w') as output_file:
        preferred_name_location = False
        for line in file:
            #first find when we're in a preferred_name section
            if '<AnnotationProperty IRI="http://www.radlex.org/RID/Preferred_name"/>' in line:
                preferred_name_location = True
            # now get the IRI
            if '<IRI>' in line and preferred_name_location == True:
                iri_string = line
            #now find the name of the preferred_name
            if '<Literal xml:lang' in line and preferred_name_location == True:
                start_name=line.find('\"en\"')+5
                end_name=line.find('</Literal>')
                name_string = line[start_name:end_name]


            #when the preferred_name section ends, start the new section with skos:prefLabel
            if '</AnnotationAssertion>' in line and preferred_name_location == True:
                output_file.write(line)

                #now write new section
                output_file.write('    <AnnotationAssertion>\n')
                output_file.write('        <AnnotationProperty IRI="http://www.w3.org/2004/02/skos/core#prefLabel"/>\n')
                output_file.write(iri_string)
                output_file.write('        <Literal>' + name_string + '</Literal>\n')
                output_file.write('    </AnnotationAssertion>\n')

                preferred_name_location = False
                name_string = ''
                iri_string = ''
            #always write out original line
            else:
                output_file.write(line)





# import owlready2 as or2
# import os
#
# # radlex_path = os.path.join(r"/mnt/tjb129/Bradshaw/Tyler/nuclex/radlex_owl", 'RadLex_original.owl')
# radlex_path = os.path.join(r"/mnt/tjb129/Bradshaw/Tyler/nuclex/nuclex_owl", 'RadLex_test1.owl')
#
#
# rl_onto = or2.get_ontology(radlex_path)
# rl_onto.load()
#
# print(list(rl_onto.classes()))
# print(list(rl_onto.annotation_properties()))
# print(list(rl_onto.object_properties()))
# print(list(rl_onto.properties()))
#
# all_classes = rl_onto.classes()
# test_class = next(all_classes)
#
# for cl in all_classes:
#     label = cl.label
#     preferred_name = cl.Preferred_name
#     cl.Radlex_label = label
#     cl.label = preferred_name
# #how to update onto.classes?
#
#
#
# # onto.save(file = "filename or fileobj", format = "rdfxml")