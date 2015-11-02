import random

INVALID = "X"

# Parameters for schedule generation
TYPES = (
    ["C", "C", "C", "C", "C", "B", "L", "S"],
    #["C", "C", "C", "C", "B", "L", "S"],
    #["C", "C", "C", "C", "C", "B", "L"],
    #["C", "C", "C", "C", "B", "L"],
)
TOTAL_MINI_BLOCKS = 78 # from 8:30 am to 3:00 pm
MIN_CLASS_LENGTH = 6
NUM_CLASS_LENGTHS = 2

MIN_LUNCH_LENGTH = 5
MIN_STUDENT_LIFE_LENGTH = 3 # 15 mins
MIN_BREAK_LENGTH = 2 # 10 mins

ONE_BLOCK_MAX = ("B", "L", "S")

# Parameters for fitness calculation
IDEAL_LUNCH_TIME = 45 # 12:15 pm
IDEAL_BREAK_TIME = 18 # 10:00 am
IDEAL_STUDENT_LIFE_TIME = 18 # 10:00 am

IDEAL_LUNCH_LENGTH = 12 # 60 mins
IDEAL_CLASS_LENGTH = 12 # ask colton


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

# lower is better, apparently
def fitness(schedule):
    fitness = 0
    
    fitness += abs(IDEAL_LUNCH_TIME - s_index_of(schedule, "L"))
    fitness += abs(IDEAL_BREAK_TIME - s_index_of(schedule, "B"))
    
    sl_index = s_index_of(schedule, "S")
    if sl_index != -1:
        fitness += abs(IDEAL_STUDENT_LIFE_TIME - sl_index)
        
    fitness += abs(IDEAL_LUNCH_LENGTH - s_value_of(schedule, "L"))
    
    return fitness
    
def s_index_of(schedule, name):
    index = 0
    for block in schedule:
        if block[0] == name:
            return index
        index += block[1]
    return -1

def s_value_of(schedule, name):
    for block in schedule:
        if block[0] == name:
            return block[1]
    return -1

def s_values(schedule, name):
    result = []
    for block in schedule:
        if block[0] == name:
            result.append(block[1])
    return result
        
        
def population(count):
    return [individual() for x in range(0, count)]
        
        
def evolve(population, pct_retain=0.2, prob_random_select=0.07, prob_mutate=0.02):
    graded = [(fitness(x), x) for x in population]
    graded = [x[1] for x in sorted(graded)]
    
    parents = graded[:int(len(graded)*pct_retain)]
    
    for item in population:
        if prob_random_select > random.random():
            parents.append(item)
            
    for i in range(0, len(parents)):
        if prob_mutate > random.random():
            parents[i] = mate(parents[i], individual())
            
    children = []
    for x in range(0, len(population) - len(parents)):
        parent_left = parents[random.randint(0, len(parents) - 1)]
        parent_right = parents[random.randint(0, len(parents) - 1)]
        children.append(mate(parent_left, parent_right))
        
    result = parents + children
    return result


def mate(left, right):
    for name in ONE_BLOCK_MAX:
        if 0.5 > random.random():
            left = s_remove(left, name)
        else:
            right = s_remove(right, name)
    
    result = []
    for i in range(0, min(len(left), len(right))):
        if right[i][0] in ONE_BLOCK_MAX and left[i][0] in ONE_BLOCK_MAX:
            # Both blocks need to be in child
            result.append(left[i])
            result.append(right[i])
        else:
            # One or neither of blocks need to be in child
            if left[i][0] in ONE_BLOCK_MAX or right[i][0] == INVALID:
                next_item = left[i]
            elif right[i][0] in ONE_BLOCK_MAX or left[i][0] == INVALID:
                next_item = right[i]
            elif 0.5 > random.random():
                next_item = left[i]
            else:
                next_item = right[i]

            if next_item[0] != INVALID:
                result.append(next_item)
        
    if len(left) != len(right):
        last = left[-1:] if len(left) > len(right) else right[-1:]
        if last[0] != INVALID and (last[0] in ONE_BLOCK_MAX or 0.5 > random.random()):
            result += last
            
    return result
    
def s_remove(sched, name):
    result = []
    for item in sched:
        if item[0] != name:
            result.append(item)
        else:
            result.append((INVALID, 0))
    return result
    
    
def main():
    pop = population(1000)
    for i in range(1, 10):
        print "gen", i
        pop = evolve(pop)
    print "\n\nresults\n"
    for item in [x[1] for x in sorted([(fitness(x), x) for x in pop])][:10]:
        print fitness(item), item
        
main()