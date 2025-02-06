class DifficultyModel:
    def __init__(self):
        self.category_weight = {
            "Arithmetic Sequences": 4/15,
            "Geometric Sequences": 14/15,
            "Mixed Sequences": 15/15,
            "Prime Numbers": 12/15,
            "Factorisation Problems": 6/15,
            "Odd One Out": 1/15,
            "Number Puzzle": 3/15,
            "Time and Work Problems": 9/15,
            "BODMAS": 5/15,
            "Algebra": 10/15,
            "Profit and Loss": 8/15,
            "Probability and Statistics": 13/15,
            "Currency and Exchange": 7/15,
            "Area and Perimeter": 11/15,
            "Volumne": 11/15,
            "Angles":11/15,
            "Triangles":11/15,
            "Circles":11/15,
            "Quadrilaterals":11/15,
            "Spatial Reasoning":11/15,
            "Calendar Problems": 2/15,
        }

    def is_prime(self, n):
        if n < 2:
            return False
        
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
            
        return True
    
    def analyze_numbers(self, numbers):
        score = 0
        
        for num in numbers:  
            if 70 >= num > 30:
                score += 1
            
            if num > 70:
                score += 2
                
            if num != 0 and num not in [1, 2, 5, 10, 25, 50, 100]:
            	if num % 2 != 0 and num % 5 != 0:
            		score += 1
            
            # Prime numbers are typically harder
            if self.is_prime(int(num)):
                score += 2
        scaled_score = score
        return scaled_score
    
    
    def calculate_score(self, resp, category):
        try:
            topic_complexity_weight = self.category_weight[category]
            
            num_vars = len(resp['variable_relations']['variables'])
            num_steps = len(resp['variable_relations']['relations'])
            rel = list(resp['variable_relations']['relations'].values())
            
            num_mul_or_division_steps = 0
            num_add_or_subtract_steps = 0
            
            for i in rel:
                if '+' in i or '-' in i:
                    num_add_or_subtract_steps += 1
                if '/' in i or '*' in i:
                    num_mul_or_division_steps += 1
            
            diff_score = 5 * topic_complexity_weight +  1.5 * num_vars + num_add_or_subtract_steps + 2 * num_mul_or_division_steps
            scaled_diff_score = (diff_score / 40) * 15
            
            return round(scaled_diff_score,2)
               
        except:
            print(f"{category} not in defined category")
            raise TypeError("Program exit with code -1")
        
        
    def update_score(self, values, template_difficulty):
        numerical_complexity = self.analyze_numbers(values.values())

        return template_difficulty+numerical_complexity