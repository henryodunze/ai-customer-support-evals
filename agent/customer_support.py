import json

from pathlib import Path
from openai import OpenAI

from agent.prompts import SYSTEM_PROMPT
from config.settings import OPENAI_API_KEY, OPENAI_MODEL


class CustomerSupportAgent:
    """
    Customer support agent that uses OpenAI to answer questions
    based on company policies.
    """
    def __init__(self):

        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

        self.model = OPENAI_MODEL

        self.company_policies = self._load_policies()

    def _load_policies(self) -> dict:
        """
        Load company policies from JSON file.
        
        Returns:
            dict: Company policies data
        """
        project_root = Path(__file__).resolve().parent.parent

        policies_path = (
            project_root / "data" / "company_policies.json"
        )

        with open(policies_path, "r", encoding="utf-8") as file:
            return json.load(file)
    
    def respond(self, customer_message: str) -> str:
        """
        Generate a response to a customer message based on company policies.
        
        Args:
            customer_message: The customer's message
            
        Returns:
            str: The agent's response
        """
        system_prompt = SYSTEM_PROMPT.format(
            company_policies=json.dumps(
                self.company_policies,
                indent=2
            )
        )

        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=customer_message
        )

        return response.output_text


if __name__ == "__main__":
    """
    Run the customer support agent interactively.
    """
    agent = CustomerSupportAgent()

    customer_message = input(
        "Customer: "
    )

    response = agent.respond(
        customer_message
    )

    print(f"\nNovaStore Support: {response}")