"""
We will define several tools here for usage including
1. SQL Server
2. Web Browser
3. Interpreter
4. Search Engine
5. Calculator
6. Mapping functions
7. Graphical API
"""

import requests
from dotenv import dotenv_values
from tool_use_package.tools.base_tool import BaseTool

__secrets = dotenv_values('.env')

class WebSearch(BaseTool):
    """
    TODO: extend BaseTool to support additional parameters
    """
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
                if not resp['query']['bad_results']:
                    
                    if "web" in resp["web"]["results"]:
                        for result in resp["web"]["results"]:
                            res.append(result.get("description", ""))            
                    
                    if "web" in resp["web"]["results"]:
                        for result in resp["web"]["results"]:
                            res.append(result.get("description", ""))            
            return "\n".join(res)

        except requests.ConnectionError:
            return "\n".join([{ "title": "Connection Error", "description": "Error retrieving result", "type": "Error" }])