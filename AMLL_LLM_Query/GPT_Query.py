from AMLL_LLM_Connection import AMLL_LLM_Connection
from AMLL_LLM_Query import AMLL_LLM_Query


class GPT_Query(AMLL_LLM_Query):
    def __init__(self, model_connection: AMLL_LLM_Connection, model_variant: str):
        """

        :param model_connection: (AMLL_LLM_Connection) Connection to GPT client
        :param model_variant: (str) the variant of GPT to use
        """
        super().__init__(model_connection=model_connection, model_variant=model_variant)
        self.acceptable_model_variants = ["gpt-4", "gpt-4-turbo-preview", "gpt-4-vision-preview", "gpt-3.5-turbo",
                                          "text-embedding-3-large", "whisper-1", "tts-1", "tts-1-hd"]
        self.acceptable_model_variant_check(model_variant=model_variant)

    def query_single(self, prompt: str) -> str:
        """
        Query one model with a single prompt in a single chat session. This is useful when you do not want the model to
        remember what you have asked it previously (e.g., if you want i to repeated answer the same question to test
        the range of responses it gives.)

        :param prompt: (str) The prompt in string form
        :return: (str) The model's response in string form
        """
        response = self.model_connection.chat.completions.create(
            model=self.model_variant,
            messages=[{"role": "user",
                       "content": prompt}]
        )
        output = response.choices[0].message.content
        return output

    def query_stream(self, prompts: list) -> list[str]:
        """
        Query one model with a series of prompts in a single chat session. This is useful for a progressive dialog.

        :param prompts: (list) List of prompts in string form
        :return: list of responses in string forms
        """
        messages = []
        for prompt in prompts:
            msg = {"role": "user",
                   "content": prompt}
            messages.append(msg)

        stream = self.model_connection.chat.completions.create(
            model=self.model_variant,
            messages=messages,
            stream=True
        )
        outputs = []
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                out = chunk.choices[0].delta.content
                outputs.append(out)

        return outputs

    def query_chat(self) -> list[str]:
        pass
