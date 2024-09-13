import random

def soil_factors2():
    return {
        'nitrogen': random.randint(0, 50),
        'phosphorus': random.randint(0, 50),
        'potassium': random.randint(0, 50)
    }
