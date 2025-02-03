import requests
import xml.etree.ElementTree as ET
import typing



class ArXivFinder:

    BASE_URL = "http://export.arxiv.org/api/query?"     
    TEMPLATE = "{http://www.w3.org/2005/Atom}"    
   
    def fetch_query(self,
                    query: str, 
                    max_results: int, 
                    start: int = 0, 
                    sortBy:str = "submittedDate", 
                    sortOrder:str = "descending", 
                    prefix: str = "all") -> typing.List[dict]:
        """
        Fetches the results matching the query from ArXiv

        Source: https://info.arxiv.org/help/api/user-manual.html#query_details

        Args: 

            query: string separated by commas, describing the topics of interest
            max_results: maximum number of items to display
            start: page to start
            sortBy: sort the results accordingly ("relevance", "lastUpdatedDate", "submittedDate")
            sortOrder:  type of sort ("ascending" or "descending")
            prefix: the query to be prefixed with. Around 9 prefixes available 
            ti - Title
            au - Author
            abs - Abstract
            co - Comment
            jr - Journal Reference
            cat - Subject Category
            rn - Report Number
            id - Id (use id_list instead)
            all

        Returns: 
            result: list of all the queries matching found
        """
        query_string = '+'.join(query.split(','))
        params = {}
        params['search_query'] = ("%s:%s") % (prefix, query_string)
        params["start"] = start
        params["max_results"] = max_results
        params["sortBy"] = sortBy
        params["sortOrder"] = sortOrder
        response = requests.get(self.BASE_URL, params)
        
        if response.status_code != 200: 
            return []
        
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()
        papers = []
        for entry in root.findall(self.TEMPLATE+'entry'):
            title = entry.find(self.TEMPLATE+'title').text
            link = entry.find(self.TEMPLATE+'id').text
            summary = entry.find(self.TEMPLATE+'summary').text
            authors = [author.find(self.TEMPLATE+'name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
            published = entry.find(self.TEMPLATE+'published').text.split('T')[0]
            
            paper = {
                'title': title,
                'link': link,
                'abstract': summary,
                'authors': authors,
                'published': published
            }
            papers.append(paper)
        
        return papers

