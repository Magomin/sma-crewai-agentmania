import os
import json
from langchain.tools import tool

import os
import json

import os
import json

class JsonParserTool:
    name: str = "JsonParserTool"
    description: str = "Tool to read and process a single JSON file."

    @staticmethod
    def extract_data_from_json(file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    @tool("Search within a PDF using my custom tool")
    def myjsontool(self, file_path: str):
        """
        Extract data from a specified JSON file.

        Parameters:
        - file_path (str): The path to the JSON file.

        Returns:
        - A dictionary containing the filename and data from the specified JSON file.
        """
        file_path = file_path.strip('"')
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        if not file_path.endswith('.json'):
            return "Invalid file type. Only JSON files are supported."
        
        data = self.extract_data_from_json(file_path)
        return {'filename': os.path.basename(file_path), 'data': data}

