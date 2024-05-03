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
import sqlite3
from dotenv import dotenv_values
from tool_use_package.tools.base_tool import BaseTool
from tool_use_package.prompt_constructors import construct_format_sql_tool_for_claude_prompt

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
                print(resp)
                if not resp['query']['bad_results']:                        
                    if 'web' in resp:
                        for result in resp['web']['results']:
                            if "description" in result: # Adding context
                                res.append(result['description'])                                                     
                    elif 'news' in resp:
                        for result in resp['news']['results']:
                            if 'description' in result: # Adding context
                                res.append(result['description'])        
            return "\n".join(res)

        except requests.ConnectionError:
            return "\n".join([{ "title": "Connection Error", "description": "Error retrieving result", "type": "Error" }])
        

# Adding a weather tool
class WeatherTool(BaseTool):
    """ Retrieve the weather of a given city"""        
    def use_tool(self, city: str):
        """
        Gets the lat and log of the given city and use this to predict the weather
        from the open-metro API
        """

        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": "city", "format": "json", "limit": 1}

        response = requests.get(url, params=params).json()

        if response:
            lat = response[0]["lat"]
            long = response[0]["lon"]
        else:
            raise ValueError("Couldn't find the lat,long of the given place")
        
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true"
        response = requests.get(url).json()
        if response:
            print(response)
            clear_json = {
                            "current_weather_units" : response['current_weather_units'],
                            "current_weather" : response['current_weather']
                          }
            return clear_json
        
        raise ValueError("The lat, long didn't fetch the weather correctly or something else went wrong")
