import os
import pandas as pd
import requests

#if it is in radlex, return the url
def is_in_radlex(df_radlex, string):
    locate_in_radlex = (df_radlex["Synonym0"] == string) | (
                df_radlex["Synonym1"] == string) | (df_radlex["Synonym2"] == string) | (df_radlex["Synonym3"] == string)

    index_with_true = locate_in_radlex.idxmax() if locate_in_radlex.any() else None

    if index_with_true:
        owl_url = df_radlex.loc[index_with_true, "Class ID"]
        return owl_url
    else:
        return ''

#if it is in NCI Thesaurus, return the url
def is_in_nci_thesaurus(df_nci,string):
    locate_in_nci = (df_nci["Synonym0"] == string) | (
                df_nci["Synonym1"] == string) | (df_nci["Synonym2"] == string) | \
                    (df_nci["Synonym3"] == string)

    index_with_true = locate_in_nci.idxmax() if locate_in_nci.any() else None

    if index_with_true:
        owl_url = "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#" + df_nci.loc[index_with_true, "id"]
        return owl_url
    else:
        return ''


def is_in_umls(string):
    # see https://documentation.uts.nlm.nih.gov/rest/rest-api-cookbook/python-scripts.html#get-concepts-for-a-list-of-strings
    apikey = 'a018c862-4475-480a-8397-59b3511f5f90'
    version = '2022AA'
    sabs = ['SNOMEDCT_US','LNC','NCI']   #see sabs list here: https://documentation.uts.nlm.nih.gov/rest/relations/
    ttys =['PT', 'SY']  #preferred term, synonym
    base_uri = 'https://uts-ws.nlm.nih.gov'
    page = 1
    path = '/search/' + version
    query = {'string': string, 'apiKey': apikey, 'rootSource': sabs, 'termType': ttys, 'pageNumber': page, 'searchType': 'exact'}
    output = requests.get(base_uri + path, params=query)
    output.encoding = 'utf-8'
    outputJson = output.json()
    results = (([outputJson['result']])[0])['results']

    if len(results) == 0:
        return ''
    else:
        return results[0]['ui']




