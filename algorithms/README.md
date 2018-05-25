# Algorithms

Each file in this folder holds an algorithm that tries to find a solution: a set of routes. 

What follows here is a guid on how to run each algorithm. 


### Genetic
This algorithm 
The population size is set to 50, and it will create up to 10 generations. This because testing showed that almost no improvement happens after the 10th generation. This algorithm is, unfortunately, quite time consuming, so the above parameters return a reasonable solution. 

### Greedy

This algorithm finds the shortest path between critical stations. It does not look at non-critical stations. This algorithm can be used to generate a starting point for the hillclimber and simulated annealing algorithms (see below). 

### Hillclimber

This hillclimber algorithm is almost two algorithms in disguise. 

### Random

This algorithm generates a random solution. By default, this algorithm is run a 1000 times. The number of trains this algorithm uses is also random. 

### Simulated Annealing

