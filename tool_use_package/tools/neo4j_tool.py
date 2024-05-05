# Import required external packages
import neo4j # Change this to whatever package you need for making your conn string.
import os # For deleting our db file at the end

# Import the requisite BaseTool and ToolUser classes, as well as some helpers.
from .base_tool import BaseTool
from ..tool_user import ToolUser
from ..prompt_constructors import construct_format_sql_tool_for_claude_prompt

# Define our custom Neo4J Tool by inheriting BaseTool and defining its use_tool() method. In this case we also override its format_tool_for_claude method to provide some additional detail.
class CypherTool(BaseTool):
    """A tool that can run Cypher queries against a graph database. 
        driver is the neo4j driver and db_name is the neo4j database we will run queries against
    """

    def __init__(self, name, description, parameters, driver, db_name):
        """
        The driver is the neo4j driver, which is used to get the schema for the table
        """
        super().__init__(name, description, parameters)
        self.driver = driver
        self.db_name = db_name       
    
    def use_tool(self, cypher_query):
        """Executes a query against the given database connection."""
       
        with self.driver.session(database=self.database) as session:
            results = session.run(cypher_query)                        
        return results
    
    def format_tool_for_claude(self):
        """Overriding the base class format_tool_for_claude in this case, which we don't always do. Returns a formatted representation of the tool suitable for the Claude system prompt.""" #TODO: Test if we even need to do this vs putting schema in the description.
        
        return construct_format_sql_tool_for_claude_prompt(self.name, self.description, self.parameters, self.driver, self.db_name)