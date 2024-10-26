from json import JSONDecodeError

from langchain_ollama import OllamaLLM  # Importing the LLM interface
from langchain_core.prompts import ChatPromptTemplate  # For templating the prompts
from genai_model.prompt_templates import FINANCIAL_ADVISOR_PROMPT, FINANCIAL_PERSONA_COLLECTOR
import json
import ast


class FinancialPersonaCollector:
    def __init__(self,  prompt_template=FINANCIAL_PERSONA_COLLECTOR):
        # Initialize the LLaMA3.2 model (Ensure that the server is running on localhost and port is correct)
        self.llm_model = OllamaLLM(model="llama3.2", host="localhost", port=11434)
        self.prompt_template = prompt_template
        self.user_data = {}  # Initialize user_data as an empty dictionary

    def parse_with_llama(self, content):
        """
        Use the LLaMA model to parse and extract specific information from the content.
        :param content: User input content.
        :return: Parsed result as a dictionary.
        """
        # Initialize the prompt template
        prompt = ChatPromptTemplate.from_template(self.prompt_template)
        chain = prompt | self.llm_model

        # Call the LLaMA model and get the response
        response = chain.invoke({"user_content": content})

        # Attempt to parse the response
        try:
            parsed_data = ast.literal_eval(response)  # Convert response to dictionary
        except (ValueError, SyntaxError) as e:
            print("Failed to decode JSON response. Response received:")
            print(response)
            parsed_data = {}  # Return an empty dictionary if parsing fails

        return parsed_data  # Return parsed data

    def collect_user_data(self):
        """
        Continuously collects user data, updating it after each prompt.
        """
        collecting_data = True

        while collecting_data:
            # Prompt user for input
            user_input = input("Please provide your financial and demographic details:\nYour response: ")

            # Parse the user input with LLaMA
            parsed_data = self.parse_with_llama(user_input)

            # Update user data with parsed information
            self.update_user_data(parsed_data)

            # Ask if the user wants to continue adding data
            continue_input = input("Would you like to add more details? (yes/no): ").strip().lower()
            collecting_data = continue_input == "yes"

        print("Final financial data collected.")
        return json.dumps(self.user_data, indent=4)

    def update_user_data(self, parsed_data):
        """
        Update user data with parsed data.
        :param parsed_data: Parsed financial data.
        """
        if isinstance(parsed_data, dict):
            # Merge the parsed data into user_data
            self.user_data.update(parsed_data)
        else:
            print("Parsed data is not in expected dictionary format. Data received:")
            print(parsed_data)


class FinancialAdvisor:
    def __init__(self, prompt_template=FINANCIAL_ADVISOR_PROMPT):
        # Initialize the LLaMA3.2 model (Ensure that the server is running on localhost and port is correct)
        self.llm_model = OllamaLLM(model="llama3.2", host="localhost", port=11434)
        self.prompt_template = prompt_template

    def parse_with_llama(self, content):
        """
        Use the LLaMA model to parse and extract specific information from the content.
        :param content: User input content.
        :return: Parsed result as a dictionary.
        """
        # Initialize the prompt template
        prompt = ChatPromptTemplate.from_template(self.prompt_template)
        chain = prompt | self.llm_model

        # Call the LLaMA model and get the response
        response = chain.invoke({"user_content": content})
        # Attempt to parse the response
        try:
            parsed_data = ast.literal_eval(response)  # Convert response to dictionary
            return parsed_data
        except (ValueError, SyntaxError, JSONDecodeError) as e:
            print("Failed to decode JSON response. Response received:")
            print(response)

            # Check if '```json' exists in the response
            if '```json' in response:
                response = response.replace('```json', '')  # Remove the '```json' part
                try:
                    return json.loads(response)  # Attempt to parse the modified response as JSON
                except json.JSONDecodeError:
                    print("Failed to decode the modified JSON response.")
                    return {}  # Return an empty dictionary if parsing fails
            elif isinstance(response, str) :
                try:
                    return json.loads(response)  # Attempt to parse the modified response as JSON
                except json.JSONDecodeError:
                    print("Failed to decode the modified JSON response.")
                    return {}  # Return an empty dictionary if parsing fails
            else:
                return


if __name__ == "__main__":
    content = "I'm 27 years old female . with housing debt of 59 lakhs . 60 % of income goes into EMI , I have 28275 goes into RD . Now My salary raised from 18.8 to 22 please help my finances."
    # print(FinancialAdvisor().parse_with_llama(content=content))
    financial_persona_json = FinancialPersonaCollector().collect_user_data()
    print("Final Financial Persona:\n", financial_persona_json)
