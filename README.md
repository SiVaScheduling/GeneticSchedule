# GeneticSchedule
GeneticSchedule is a simple Python script for optimizing the Menlo School daily schedule. This program does not assign specific classes to specific times; it merely outputs when classes, lunch, break, and student life blocks should occur in the day.

# How it Works
GeneticSchedule uses a genetic algorithm to generate a large number of random schedules and then evolve these schedules over several generations.  In each generation, only the best-performing individuals survive and reproduce to form the next generation.  Fitness (how well the schedules perform) is determined by measuring the distance between the schedule's parameters (for class length, lunch time, etc) and the ideal parameters, as indivated by a survey sent out to the student body.

# Understanding the Results
For simplicity and convenience, we used a shorthand notation for describing schedules.  In the example below, you see a schedule that the script may output.

    16 [('C', 15), ('B', 4), ('C', 15), ('C', 15), ('L', 14), ('C', 15)]
    
The number on the left is the fitness of the schedule.  This number is fairly arbitrary and is mostly useful only in comparing schedules.  Inside the brackets are six items that look like <strong>('C', 15)</strong>.  These are class blocks.  The first value is a character denoting the type of block. ("C" for class, "B" for break, "S" for student life, and "L" for lunch).  The second value is the length of the class, given in 5-minutes increments.  For example, <strong>('C', 15)</strong> is a 75-minute long class.