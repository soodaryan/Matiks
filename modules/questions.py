from datasets import load_dataset
import random
import pandas as pd


class RandomDataset:
    def __init__(self, name):
        self.dataset = load_dataset(name, 'main', split='train')
        self.data = pd.DataFrame(self.dataset)

    def get_random_sample(self, num=1):
        n = random.randint(1, len(self.data))
        sample = self.data.sample(num, random_state=n)

        return sample['question'].values.tolist()