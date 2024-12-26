from modules.llms import OpenAI
from lib.prompts import category_prompt, category_format


class Categorization:
    def __init__(self):
        self.openai = OpenAI()

    def categorize_question(self, question: str):
        prompt = category_prompt.format(question, category_format)
        try:
            response = eval(self.openai.query(prompt))
            return {
                "superclass": response["superclass"],
                "subclass": response["subclass"]
            }
        except Exception as e:
            print(f"Error categorizing question: {e}")
            return {"superclass": None, "subclass": None}


if __name__ == "__main__":
    categorizer = Categorization()

    # Sample Questions
    prime_question = "From the list of numbers [29, 42, 37, 49, 53], identify the prime numbers."
    currency_question = "A traveler exchanged 500 USD into INR at a rate of 1 USD = 75 INR. Later, the exchange rate changed to 1 USD = 80 INR. If they exchanged the same amount back into USD, how much would they have in USD now?"
    algebra_question = "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?"

    questions = [prime_question, currency_question, algebra_question]
    for question in questions:
        result = categorizer.categorize_question(question)
        print(f"Question: {question}")
        print(f"Superclass: {result['superclass']}")
        print(f"Subclass: {result['subclass']}\n")
