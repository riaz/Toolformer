"""
General Guide to tool making
"""

1. Create  a class inheriting BaseTool
2. The use_tool -> is the main function that takes the transformed response based on (format_claude...) transformer
3. the query is the transformed response post applying format_claude...
4. hence, when the actual query run with the modified prompt - we get a cypher query for example
5. inside the use_tool -> we can transform the cypher query to actual results.