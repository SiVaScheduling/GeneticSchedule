import random

# Evolution parameters
NUM_INDIVIDUALS = 100000
NUM_GENERATIONS = 10

# Character for invalid class periods
INVALID = "X"

# Parameters for schedule generation
TYPES = (
    #["C", "C", "C", "C", "C", "B", "L", "S"],
    #["C", "C", "C", "C", "B", "L", "S"],
    #["C", "C", "C", "C", "C", "B", "L"],
    ["C", "C", "C", "C", "B", "L"],
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
IDEAL_BREAK_LENGTH = 4 # 20 mins
IDEAL_STUDENT_LIFE_LENGTH = 6 # 30 mins
IDEAL_CLASS_LENGTH = 12 # ask colton


def individual():
    """Randomly generates a schedule using the provided constants."""
    shuffled_blocks = TYPES[random.randint(0, len(TYPES) - 1)]
    random.shuffle(shuffled_blocks)
    
    # Shortest student life block possible
    min_sl_length = MIN_STUDENT_LIFE_LENGTH if "S" in shuffled_blocks else 0
    # Max length of classes
    max_length = (
        TOTAL_MINI_BLOCKS - MIN_LUNCH_LENGTH -
        MIN_BREAK_LENGTH - min_sl_length
    ) / shuffled_blocks.count("C")
    # Generate actual class lengths
    class_lengths = [
        random.randint(MIN_CLASS_LENGTH, max_length) for
        x in range(0, NUM_CLASS_LENGTHS)
    ]
    
    # Fill schedule with named blocks and class lengths
    schedule = []
    total_length = 0
    for block in shuffled_blocks:
        length = -1
        if block == "C":
            length = class_lengths[random.randint(0, NUM_CLASS_LENGTHS - 1)]
            total_length += length
        schedule.append((block, length))
    
    # Generate length of lunch period
    max_lunch_length = TOTAL_MINI_BLOCKS - total_length - MIN_BREAK_LENGTH - min_sl_length
    lunch_length = random.randint(MIN_LUNCH_LENGTH, max_lunch_length) if MIN_LUNCH_LENGTH < max_lunch_length else max_lunch_length
    
    total_length += lunch_length
    
    # Generate length of break period
    max_break_length = TOTAL_MINI_BLOCKS - total_length - min_sl_length
    break_length = max_break_length if min_sl_length == 0 else random.randint(MIN_BREAK_LENGTH, max_break_length)
    
    total_length += break_length
    
    # Generate length of student life period
    max_student_life_length = TOTAL_MINI_BLOCKS - total_length
    student_life_length = max_student_life_length
    
    # Assign break, lunch, and student life lengths to their periods
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


def fitness(schedule):
    """Returns a number describing how well the inputted schedule fits the
    desired parameters. The closer the score is to 0, the better the inputted
    schedule fits the parameters.
    """
    fitness = 0
    
    # Better score for ideal lunch & break time
    fitness += abs(IDEAL_LUNCH_TIME - s_index_of(schedule, "L"))
    fitness += abs(IDEAL_BREAK_TIME - s_index_of(schedule, "B"))
    
    # Better score for ideal student life time (if exists)
    sl_index = s_index_of(schedule, "S")
    if sl_index != -1:
        fitness += abs(IDEAL_STUDENT_LIFE_TIME - sl_index)
        
    # Better score for better lunch & break period length
    fitness += abs(IDEAL_LUNCH_LENGTH - s_value_of(schedule, "L"))
    fitness += abs(IDEAL_BREAK_LENGTH - s_value_of(schedule, "B"))
    fitness += abs(IDEAL_STUDENT_LIFE_LENGTH - s_value_of(schedule, "S"))
    
    # Decrease score when classes are different lengths
    fitness += 100 * (len(s_values_unique(schedule, "C")) - 1)
    
    fitness += 100 * abs(TOTAL_MINI_BLOCKS - s_length(schedule))
    
    return fitness
    
def s_index_of(schedule, name):
    """Returns the index of the first occurrence of a given period in the
    given schedule.
    """
    index = 0
    for block in schedule:
        if block[0] == name:
            return index
        index += block[1]
        
    # return -1 if not found
    return -1

def s_value_of(schedule, name):
    """Returns the value (length) of the first occurrence of a given period in the
    given schedule.
    """
    for block in schedule:
        if block[0] == name:
            return block[1]
        
    # return -1 if not found
    return -1

def s_values(schedule, name):
    """Returns a list of the values of a given period in the
    given schedule.
    """
    result = []
    for block in schedule:
        if block[0] == name:
            result.append(block[1])
    return result

def s_values_unique(schedule, name):
    """Returns a list of the unique values of a given period in the
    given schedule.
    """
    result = []
    for block in schedule:
        if block[0] == name and block[1] not in result:
            result.append(block[1])
    return result

def s_length(schedule):
    """Returns the length of the given schedule."""
    index = 0
    for block in schedule:
        index += block[1]
    return index
        
        
def population(count):
    """Generates a list of randomly generated schedules of the
    given length.
    """
    return [individual() for x in range(0, count)]
        
        
def evolve(population, pct_retain=0.2, prob_random_select=0.07, prob_mutate=0.02):
    """Creates the next generation of a given population with the
    given parameters.
    """
    
    # list of individuals ordered by fitness
    graded = [(fitness(x), x) for x in population]
    graded = [x[1] for x in sorted(graded)]
    
    # a portion of the most fit individuals become parents
    parents = graded[:int(len(graded)*pct_retain)]
    
    # add a random sample from the remaining population to the parents
    for item in population:
        if prob_random_select > random.random():
            parents.append(item)
        
    # mutate (generate randomly) a portion of the parents
    for i in range(0, len(parents)):
        if prob_mutate > random.random():
            parents[i] = mate(parents[i], individual())
            
    # create a population of children by randomly 'mating' parents
    children = []
    for x in range(0, len(population) - len(parents)):
        parent_left = parents[random.randint(0, len(parents) - 1)]
        parent_right = parents[random.randint(0, len(parents) - 1)]
        children.append(mate(parent_left, parent_right))
        
    # return both the parents and the children for the next generation
    result = parents + children
    return result


def mate(left, right):
    """Combines the two provided schedules into one 'child' schedule."""
    
    # Remove duplicates of blocks that can only occur once (lunch, break, etc)
    for name in ONE_BLOCK_MAX:
        if 0.5 > random.random():
            left = s_remove(left, name)
        else:
            right = s_remove(right, name)
    
    # Add a class from either left or right in each new spot
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
                # Only add block if it's valid
                result.append(next_item)
        
    # randomly add the last block if it's valid
    if len(left) != len(right):
        last = left[-1:] if len(left) > len(right) else right[-1:]
        if last[0] != INVALID and (last[0] in ONE_BLOCK_MAX or 0.5 > random.random()):
            result += last
            
    return result
    
def s_remove(schedule, name):
    """Removes all occurrences of a given period in the given schedule."""
    result = []
    for item in schedule:
        if item[0] != name:
            result.append(item)
        else:
            result.append((INVALID, 0))
    return result
    
    
def main():
    # Evolve a population of NUM_INDIVIDUALS for NUM_GENERATIONS
    pop = population(NUM_INDIVIDUALS)
    for i in range(1, NUM_GENERATIONS):
        print "gen", i
        pop = evolve(pop)
        
    # print 10 best schedules
    print "\n\nresults\n"
    for item in [x[1] for x in sorted([(fitness(x), x) for x in pop])][:10]:
        print fitness(item), item
        
main()