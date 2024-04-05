from AMLL_LLM_Connection.AMLL_LLM_Connection import AMLL_LLM_Connection


class AMLL_LLM_Query:
    def __init__(self, model_connection: AMLL_LLM_Connection, model_variant: str):
        self.model_connection = model_connection.get_connection()
        self.model_variant = model_variant
        self.acceptable_model_variants = None

    def acceptable_model_variant_check(self, model_variant: str) -> None:
        """
        This function checks that the model variant is one of the acceptable varieties for the LLM that is being used.
        :param model_variant: (str)
        :raise ValueError: If the model variant is not acceptable
        """
        if model_variant not in self.acceptable_model_variants:
            raise ValueError(f"The model variant {model_variant} is not acceptable. The acceptable model variants are: "
                             f"{self.acceptable_model_variants}")

    def query_single(self, prompt) -> str:
        pass

    def query_stream(self, prompts) -> list[str]:
        pass

    def query_chat(self) -> list[str]:
        pass
