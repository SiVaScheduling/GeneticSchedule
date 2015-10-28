import random

TYPES = (
    ["C", "C", "C", "C", "C", "B", "L", "S"],
    ["C", "C", "C", "C", "B", "L", "S"],
    ["C", "C", "C", "C", "C", "B", "L"],
    ["C", "C", "C", "C", "B", "L"],
)
TOTAL_MINI_BLOCKS = 78
MIN_CLASS_LENGTH = 6
NUM_CLASS_LENGTHS = 2

MIN_LUNCH_LENGTH = 5

def individual():
    shuffled_blocks = TYPES[random.randint(0, len(TYPES) - 1)]
    random.shuffle(shuffled_blocks)
    max_length = TOTAL_MINI_BLOCKS / (len(shuffled_blocks) - 2)
    class_lengths = [random.randint(MIN_CLASS_LENGTH, max_length) for x in range(0, NUM_CLASS_LENGTHS)]
    
    schedule = []
    total_length = 0
    for block in ordered_types:
        length = -1
        if block == "C":
            length = class_lengths[random.randint(0, NUM_CLASS_LENGTHS - 1)]
            total_length += length
        schedule.append((block, length))
        
    lunch_length = random.randint(MIN_LUNCH_LENGTH, TOTAL_MINI_BLOCKS - total_class_length - 2)
    total_length += lunch_length
    life_length = 
    
    
def main():
    for x in range(1, 100):
        print individual()
        
main()