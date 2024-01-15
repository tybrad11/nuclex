import pandas as pd

"""
compare different noun chunk counts from different journal types, determine if they are in radlex already
must have radlex downloaded (separate synonyms)
"""

#set read paths
path_radiology = '/mnt/tjb129/Bradshaw2/Tyler/nuclex/nuc_med_articles/from_pmc_non_nucmed/noun_counts_trimmed.csv'
path_nucmed = '/mnt/tjb129/Bradshaw2/Tyler/nuclex/nuc_med_articles/from_pmc/noun_counts_nucmed_trimmed.csv'
path_radlex = '/mnt/tjb129/Bradshaw2/Tyler/nuclex/radlex_owl/Radlex_separate_synonyms.xls'
#set save paths
path_unique_nucmed_words = '/mnt/tjb129/Bradshaw2/Tyler/nuclex/nuc_med_articles/from_pmc/noun_counts_nucmed_trimmed_unique.csv'
path_nucmed_overrepresented_words = '/mnt/tjb129/Bradshaw2/Tyler/nuclex/nuc_med_articles/from_pmc/noun_counts_nucmed_trimmed_overrepresented.csv'


#read data
df_rad = pd.read_csv(path_radiology)
df_nm = pd.read_csv(path_nucmed)
df_radlex = pd.read_excel(path_radlex)

#get the words that only appear in the nuc med corpus
unique_words = df_nm[~df_nm['String'].isin(df_rad['String'])]
#words that are already in radlex
# Create a mask to check if the word is present
mask = df_radlex['Synonym0'].isin(unique_words['String']) | df_radlex['Synonym1'].isin(unique_words['String']) | df_radlex['Synonym2'].isin(unique_words['String'])
# Add a column indicating if word is in radlex
unique_words['radlex'] = unique_words['String'].isin(df_radlex.loc[mask, ['Synonym0', 'Synonym1', 'Synonym2']].stack())
#save
unique_words.to_csv(path_unique_nucmed_words)


#get the words that have more frequency in nuc med than in radiology
factor_param = 3
merged_data = pd.merge(df_nm,df_rad, on='String')
#remove cases that are numbers -- not needed
merged_data['String'] = merged_data['String'].astype(str)
merged_data = merged_data[~merged_data['String'].str.match(r'^\d+(\.\d+)?$')]
# Create a new column to indicate if the percent frequency is higher
merged_data['overrepresented_nm'] = merged_data['Fraction_x'] > (factor_param * merged_data['Fraction_y'])

# Filter the data to get the words with higher frequency
words_with_higher_frequency = merged_data.loc[merged_data['overrepresented_nm']]

#words that are already in radlex
# words_with_higher_frequency['radlex'] = words_with_higher_frequency['String'].isin(df_radlex['Preferred Label'])
mask2 = df_radlex['Synonym0'].isin(words_with_higher_frequency['String']) | df_radlex['Synonym1'].isin(words_with_higher_frequency['String']) | df_radlex['Synonym2'].isin(words_with_higher_frequency['String'])
words_with_higher_frequency['radlex'] = words_with_higher_frequency['String'].isin(df_radlex.loc[mask2, ['Synonym0', 'Synonym1', 'Synonym2']].stack())

# Save the filtered words to a new CSV file
words_with_higher_frequency.to_csv(path_nucmed_overrepresented_words, index=False)


