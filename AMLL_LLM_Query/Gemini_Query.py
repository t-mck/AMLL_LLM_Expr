from AMLL_LLM_Connection import AMLL_LLM_Connection
from AMLL_LLM_Query import AMLL_LLM_Query


class Gemini_Query(AMLL_LLM_Query):
    def __init__(self, model_connection: AMLL_LLM_Connection, model_variant: str):
        """

        :param model_connection: (AMLL_LLM_Connection) Connection to GPT client
        :param model_variant: (str) the variant of GPT to use
        """
        super().__init__(model_connection=model_connection, model_variant=model_variant)
        self.acceptable_model_variants = ["gemini-pro"]
        self.acceptable_model_variant_check(model_variant=model_variant)

    def query_single(self, prompt: str) -> str:
        """
        Query one model with a single prompt in a single chat session. This is useful when you do not want the model to
        remember what you have asked it previously (e.g., if you want it to repeated answer the same question to test
        the range of responses it gives.)

        :param prompt: (str) The prompt in string form
        :return: (str) The model's response in string form
        """
        model = self.model_connection.GenerativeModel(self.model_variant)
        return model.generate_content(prompt)

    def query_stream(self, prompts: list) -> list[str]:
        """
        Query one model with a series of prompts in a single chat session. This is useful for a progressive dialog.

        :param prompts: (list) List of prompts in string form
        :return: list of responses in string forms
        """
        model = self.model_connection.GenerativeModel(self.model_variant)
        chat = model.start_chat(history=[])
        for prompt in prompts:
            chat.send_message(prompt)
        responses = chat.history

        return responses

    def query_chat(self):
        pass
