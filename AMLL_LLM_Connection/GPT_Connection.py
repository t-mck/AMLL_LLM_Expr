from openai import OpenAI
from AMLL_LLM_Connection import AMLL_LLM_Connection


class GPT_Connection(AMLL_LLM_Connection):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.connection = OpenAI(api_key=api_key)

    def get_connection(self):
        return self.connection
