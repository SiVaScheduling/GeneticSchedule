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
MIN_STUDENT_LIFE_LENGTH = 3
MIN_BREAK_LENGTH = 2

def individual():
    shuffled_blocks = TYPES[random.randint(0, len(TYPES) - 1)]
    random.shuffle(shuffled_blocks)
    
    min_sl_length = MIN_STUDENT_LIFE_LENGTH if "S" in shuffled_blocks else 0
    max_length = (TOTAL_MINI_BLOCKS - MIN_LUNCH_LENGTH - MIN_BREAK_LENGTH - min_sl_length) / shuffled_blocks.count("C")
    class_lengths = [random.randint(MIN_CLASS_LENGTH, max_length) for x in range(0, NUM_CLASS_LENGTHS)]
    
    schedule = []
    total_length = 0
    for block in shuffled_blocks:
        length = -1
        if block == "C":
            length = class_lengths[random.randint(0, NUM_CLASS_LENGTHS - 1)]
            total_length += length
        schedule.append((block, length))
    
    max_lunch_length = TOTAL_MINI_BLOCKS - total_length - MIN_BREAK_LENGTH - min_sl_length
    lunch_length = random.randint(MIN_LUNCH_LENGTH, max_lunch_length) if MIN_LUNCH_LENGTH < max_lunch_length else max_lunch_length
    
    total_length += lunch_length
    
    max_break_length = TOTAL_MINI_BLOCKS - total_length - min_sl_length
    break_length = max_break_length if min_sl_length == 0 else random.randint(MIN_BREAK_LENGTH, max_break_length)
    
    total_length += break_length
    
    max_student_life_length = TOTAL_MINI_BLOCKS - total_length
    student_life_length = max_student_life_length
    
    for i in range(0, len(schedule)):
        block = schedule[i][0]
        length = schedule[i][1]
        if block == "L":
            length = lunch_length
        elif block == "B":
            length = break_length
        elif block == "S":
            length = student_life_length
        schedule[i] = (block, length)
        
    return schedule
    
    
def main():
    for x in range(1, 11):
        ind = individual()
        total = 0
        for item in ind:
            total += item[1]
        print "\n", x, len(ind), total, ind
        
main()