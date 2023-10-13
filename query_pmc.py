import requests
import os
import xml.etree.ElementTree as ET
import config


# Set the search query parameters
# for query rules, see https://dataguide.nlm.nih.gov/edirect/esearch.html
#and https://dataguide.nlm.nih.gov/eutilities/utilities.html#esearch-formatting-parameters
# journals = ['J Nucl Med', 'Eur J Nucl Med Mol Imaging', 'EJNMMI Phys', 'EJNMMI Res', 'Clin Nucl Med']
journals = ['Radiology', 'JACC Cardiovasc Imaging', 'Radiographics', 'Magn Reson Med', 'Neuroimage']


for journal_query in journals:
    for j in range(2018,2023):
        query_date = str(j)
        query = '"' + journal_query + '"[Journal] AND "' + query_date + '"[pdat]'

        retmax = 500  # Number of articles to retrieve (adjust as needed)

        # Make the API request
        base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
        params = {
            'db': 'pmc',
            'term': query,
            'retmax': retmax,
            'retmode': 'xml',
            'api_key': api_key
        }
        response = requests.get(base_url, params=params)

        # Parse the XML response
        root = ET.fromstring(response.text)
        article_ids = [id_elem.text for id_elem in root.findall('.//IdList/Id')]

        # Create a directory to store the downloaded articles
        output_dir = '/mnt/tjb129/Bradshaw2/Tyler/nuclex/nuc_med_articles/from_pmc/' + journal_query.replace(' ','_') + query_date
        os.makedirs(output_dir, exist_ok=True)

        # Loop through the article IDs and download the full text
        for article_id in article_ids:
            fetch_url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
            fetch_params = {
                'db': 'pmc',
                'id': article_id,
                'retmode': 'xml',
                'api_key': api_key
            }
            try:
                fetch_response = requests.get(fetch_url, params=fetch_params)
                article_xml = fetch_response.text

                # Parse the article XML and extract the title and abstract
                article_root = ET.fromstring(article_xml)
                title_element = article_root.find('.//front/article-meta/title-group/article-title')
                if title_element is not None:
                    title = ET.tostring(title_element, encoding='unicode', method='text')

                # Try multiple paths to extract the abstract
                abstract_element = None
                abstract = None
                abstract_paths = [
                    './/abstract/p',  # Path 1
                    './/abstract'  # Path 2
                ]
                for path in abstract_paths:
                    abstract_element = article_root.find(path)
                    if abstract_element is not None:
                        abstract = ET.tostring(abstract_element, encoding='unicode', method='text')
                        breakfetch_response = requests.get(fetch_url, params=fetch_params)
                article_xml = fetch_response.text

                # Parse the article XML and extract the title and abstract
                article_root = ET.fromstring(article_xml)
                title_element = article_root.find('.//front/article-meta/title-group/article-title')
                if title_element is not None:
                    title = ET.tostring(title_element, encoding='unicode', method='text')

                # Try multiple paths to extract the abstract
                abstract_element = None
                abstract = None
                abstract_paths = [
                    './/abstract/p',  # Path 1
                    './/abstract'  # Path 2
                ]
                for path in abstract_paths:
                    abstract_element = article_root.find(path)
                    if abstract_element is not None:
                        abstract = ET.tostring(abstract_element, encoding='unicode', method='text')
                        break



                body_element = article_root.find('.//body')
                if body_element is not None:
                    body = ET.tostring(body_element, encoding='unicode', method='text')
                else:
                    body = None
                    continue  #skip this case

                doi_element = article_root.find(".//article-id[@pub-id-type='doi']")
                if doi_element is not None:
                    doi = ET.tostring(doi_element, encoding='unicode', method='text')
                else:
                    doi = None

                # Check if title and abstract elements exist
                title = title if title_element is not None else 'N/A'
                abstract = abstract if abstract is not None else 'N/A'
                body = body if body is not None else 'N/A'

                # Create a text file and save the title and abstract
                output_file = os.path.join(output_dir, f'{article_id}.txt')
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f'Title: {title}\n\n')
                    f.write(f'doi: {doi}\n\n')
                    f.write(f'Year: {query_date}\n\n')
                    f.write(f'Abstract: {abstract}\n')
                    f.write(f'Body: {body}\n')

                print(f'Saved article ID {article_id} to {output_file}')
            except:
                print('Failed to retrieve ', str(article_id))