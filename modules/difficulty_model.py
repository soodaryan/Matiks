class DifficultyModel:
    def __init__(self):
        self.category_weight = {
            "Arithmetic Sequences" : 4,
            "Geometric Sequences" : 14,
            "Mixed Sequences" : 15,
            "Prime Numbers" : 12,
            "Factorisation Problems" : 6,
            "Odd One Out" : 1,
            "Number Puzzle" : 3,
            "Time and Work Problems" : 9,
            "BODMAS" : 5,
            "Algebra" : 10,
            "Profit and Loss" : 8,
            "Probability and Statistics" : 13,
            "Currency and Exchange" : 7,
            "Geometry" : 11,
            "Calendar Problems" : 2,
        }


    def calculate_score(self, resp, category):
        try:
            topic_complexity_weight = self.category_weight[category]

            num_vars = len(resp['variable_relations']['variables'])
            num_steps = len(resp['solution'].split("."))
            rel = list(resp['variable_relations']['relations'].values())

            num_mul_or_division_steps = 0
            num_add_or_subtract_steps = 0

            for i in rel:
                if '+' in i or '-' in i:
                    num_add_or_subtract_steps += 1
                    
                if '/' in i or '*' in i :
                    num_add_or_subtract_steps += 1
            
            diff_score = 2.5*topic_complexity_weight + 1.5*num_vars + 0.5*num_steps + 0.5*num_add_or_subtract_steps + num_mul_or_division_steps

            return diff_score
        
        except:
            print(f"{category} not in defined category")
            raise TypeError("Program exit with code -1")