import random

TYPES = (
    ["C", "C", "C", "C", "C", "B", "L", "T"],
    ["C", "C", "C", "C", "B", "L", "T"],
    ["C", "C", "C", "C", "C", "B", "L"],
    ["C", "C", "C", "C", "B", "L"],
)

def individual():
    ordered_types = TYPES[random.randint(0, len(TYPES) - 1)]
    random.shuffle(ordered_types)
    return ordered_types
    
    
def main():
    for x in range(1, 100):
        print individual()
        
main()