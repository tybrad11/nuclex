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
        return 0

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
        return 0


def is_in_umls(string):
    # see https://documentation.uts.nlm.nih.gov/rest/rest-api-cookbook/python-scripts.html#get-concepts-for-a-list-of-strings
    apikey = 'a018c862-4475-480a-8397-59b3511f5f90'
    version = '2022AA'
    sabs = ['SNOMEDCT_US']
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
        return 0
    else:
        return results[0]['ui']


#main

directory_path = '/mnt/tjb129/Bradshaw2/Tyler/nuclex/'
filename = 'noun_chunks_to_add_combined_20230811.xlsx'
sheet_read = 'Curated'
sheet_write = 'Unique'

path_radlex = '/mnt/tjb129/Bradshaw2/Tyler/nuclex/radlex_owl/Radlex_separate_synonyms.xls'
path_nci =    '/mnt/tjb129/Bradshaw2/Tyler/nuclex/nci_thesaurus_owl/Thesaurus_curated.csv'

df = pd.read_excel(os.path.join(directory_path,filename), sheet_read)
df_radlex = pd.read_excel(path_radlex)
df_nci = pd.read_csv(path_nci)


# chunks = []
# chunk_generator = pd.read_csv(path_nci, chunksize=10000, errors='replace')
# for chunk in chunk_generator:
#     chunks.append(chunk)
# df_nci = pd.concat(chunks, ignore_index = True)
# df_nci = pd.read_csv(path_nci, chunksize=1000000)

filtered_df = pd.DataFrame(columns=["String", "Radlex", "UMLS", "NCI Thesaurus", "Uncertain"])

# Iterate through the rows of the initial dataframe
for index, row in df.iterrows():
    # Check if the row should be added to the filtered dataframe
    if row["To add"] == 1 :
        #if the entry already exists (was added as a synonym), need to add the "uncertain" part that was not included
        index = filtered_df[filtered_df["String"] == row["String"]].index
        if index.any():
            orig_entry  =  filtered_df.loc[index[0]]
            filtered_df.loc[index[0]] = {"String": orig_entry["String"], "Radlex": orig_entry["Radlex"], "UMLS": orig_entry["UMLS"], "NCI Thesaurus": orig_entry["NCI Thesaurus"], "Uncertain": row["Uncertain"]}
        else:
            #if it doesn't exist, append
            radlex_owl = is_in_radlex(df_radlex, row["String"])
            nci_owl = is_in_nci_thesaurus(df_nci, row["String"])
            snomod_id = is_in_umls(row['String'])
            filtered_df = pd.concat([filtered_df, pd.DataFrame({"String": row["String"], "Radlex": radlex_owl, "UMLS": snomod_id, "NCI Thesaurus": nci_owl,"Uncertain": row["Uncertain"]}, columns=filtered_df.columns, index=[0])], ignore_index=True)
    elif isinstance(row["Synonym to add"],str):
        if not (filtered_df["String"] == row["Synonym to add"]).any():
            # Append the row to the filtered dataframe
            radlex_owl = is_in_radlex(df_radlex, row["Synonym to add"])
            nci_owl = is_in_nci_thesaurus(df_nci, row["Synonym to add"])
            snomod_id = is_in_umls(row["Synonym to add"])
            filtered_df = pd.concat([filtered_df, pd.DataFrame({"String": row["Synonym to add"], "Radlex": radlex_owl, "UMLS": snomod_id, "NCI Thesaurus": nci_owl, "Uncertain": row["Uncertain"]}, columns=filtered_df.columns, index=[0])], ignore_index=True)
    else:
        continue

with pd.ExcelWriter(os.path.join(directory_path,filename), mode="a") as writer:
    filtered_df.to_excel(writer, sheet_name="Unique3",index=False)
