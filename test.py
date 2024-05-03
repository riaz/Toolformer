import requests
from bs4.element import Comment
from bs4 import BeautifulSoup
from dotenv import dotenv_values

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(string=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

class Test:
    def use_tool(self, query):
            """
            This tool makes use of the brave API to take in a query and return the results as a list
            """
            ENDPOINT = "https://api.search.brave.com"
            API_PATH = "res/v1/web/search"

            URL  = f"{ENDPOINT}/{API_PATH}?q={query}"
            __secrets = dotenv_values('.env')
            headers = {
                'X-Subscription-Token': __secrets['BRAVE_API'],
                'Accept-Encoding': 'gzip',
                'Accept': 'application/json'
            }


            try:
                res = []
                response = requests.request('GET', URL, headers=headers, data={})
                if response.status_code == 200:
                    resp = response.json()
                    #print(resp)
                    if not resp['query']['bad_results']:
                        
                        if "web" in resp:
                            for result in resp["web"]["results"]:
                                if "url" in result: # Adding context
                                    page_content = requests.get(result["url"])
                                    if page_content.status_code == 200:
                                        res.append(text_from_html(page_content.content))                                                        
                        elif "news" in resp:
                            for result in resp["news"]["results"]:
                                if "url" in result: # Adding context
                                    page_content = requests.get(result["url"])
                                    if page_content.status_code == 200:
                                        res.append(text_from_html(page_content.content))                             
                #print("Search Response", res)         
                return "\n".join(res)

            except requests.ConnectionError:
                return "\n".join([{ "title": "Connection Error", "description": "Error retrieving result", "type": "Error" }])
            
if __name__ == '__main__':
    t = Test()
    print(t.use_tool("Latest news in San Francisco"))