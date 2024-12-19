from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import torch
from torch.nn.parallel import DataParallel


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
        
        self.model = DataParallel(self.model)

        self.model.generation_config = GenerationConfig.from_pretrained(model_name)
        self.model.generation_config.pad_token_id = self.model.generation_config.eos_token_id


    def generate_solution(self, question):
        msgs = [
            {"role": "user", "content": question + "\nPlease reason step by step, and put your final answer within \\boxed{}."}
        ]
        
        input_tensor = self.tokenizer.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt")
        outputs = self.model.generate(input_tensor.to(self.model.device), max_new_tokens=1000)

        result = self.tokenizer.decode(outputs[0][input_tensor.shape[1]:], skip_special_tokens=True)

        return result