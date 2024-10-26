from langchain_ollama import OllamaLLM  # Importing the LLM interface
from langchain_core.prompts import ChatPromptTemplate  # For templating the prompts
from genai_model.prompt_templates import FINANCIAL_ADVISOR_PROMPT


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
        return response  # Assuming the response is already in dictionary format


if __name__ == "__main__":
    content = "I'm 27 years old female . with housing debt of 59 lakhs . 60 % of income goes into EMI , I have 28275 " \
              "goes into RD . Now My salary raised from 18.8 to 22 please help my finances."
    print(FinancialAdvisor().parse_with_llama(content=content))
