from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch


class SolutionModel:
    def __init__(self):
        model_name = "deepseek-ai/deepseek-math-7b-instruct"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=torch.float16,
                    device_map="auto",
                    # offload_folder="data"
                )

        self.model.generation_config = GenerationConfig.from_pretrained(model_name)
        self.model.generation_config.pad_token_id = self.model.generation_config.eos_token_id


    def generate_solution(self, question):
        msgs = [
            {"role": "user", "content": question + "\n" + r"You are a maths expert. Please solve the following problem step by step in a logical and concise manner. Use clear and simple equations to explain the solution. Provide a summary of the final answer within a single paragraph, and ensure the final answer is enclosed within \boxed{} only. "}
        ]
        
        input_tensor = self.tokenizer.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt")
        outputs = self.model.generate(input_tensor.to(self.model.device), max_new_tokens=1000)

        result = self.tokenizer.decode(outputs[0][input_tensor.shape[1]:], skip_special_tokens=True)

        return result