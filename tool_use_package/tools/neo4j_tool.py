# Import required external packages
import neo4j # Change this to whatever package you need for making your conn string.
import pandas as pd
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
        self.schema =  self.get_schema()
    
    def use_tool(self, query):
        """Executes a query against the given database connection."""
        print(query) # I expect this to be cypher code due to the prompts
        records, *_ = self.driver.execute_query(query, database=self.db_name)
        #print(records)
        data = []
        for record in records:
            if isinstance(record, neo4j._data.Record):
                for k, v in record.items():
                    if isinstance(v, str) or isinstance(v, int):                    
                        key = k.split('.')[-1] if '.' in k else k
                        data.append({key: v})
                    elif isinstance(v, neo4j.graph.Node):
                        data.append(v)
                    else:
                        print("Unknown type", type(v))
        df = pd.DataFrame.from_records(data)
        print(df.to_json())
        return df.to_json()
    
    def format_tool_for_claude(self):
        """Overriding the base class format_tool_for_claude in this case, which we don't always do. Returns a formatted representation of the tool suitable for the Claude system prompt.""" #TODO: Test if we even need to do this vs putting schema in the description.
        
        return construct_format_sql_tool_for_claude_prompt(self.name, self.description, self.parameters, self.driver, self.db_name)
    
    def get_schema(self) -> str:
        with self.driver.session(database=self.db_name) as session:
            response = session.run("CALL db.schema.visualization()")
            
            nodes = []
            relationships = []

            for res in response:
                for val in res.values():
                    for comp in val: # here val is either array of node or relationship
                        #print(type(comp))                
                        if isinstance(comp, neo4j.graph.Node):
                            nodes.append(list(comp.labels)[0])
                        else:
                            relationships.append(("(:{src})-[{rel}]->(:{dst})".format(src=list(comp.start_node.labels)[0], rel=comp.type, dst=list(comp.end_node.labels)[0])))
            node_str = "\n".join(nodes)
            relation_str = "\n".join(relationships)

            return "\n".join(["Nodes:\n", node_str, "\nRelations:\n", relation_str])   