'''
Created on Jan 27, 2012

@author: yati
'''
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 400, 400

# This is the maximum radius our resulting circle can have.
# Though the other already present circles may have portions outside the 
# viewport, our result, by definition, must fit in the viewport somehow.
MAX_RADIUS = min(WINDOW_WIDTH, WINDOW_HEIGHT) / 5

# Now, the encoding scheme for the chromosomes. 
# There may be 2 ways(actually many more, but I'll stick to these 2) to encode
# a chromosome:
# > As a triple (cx, cy, radius) [(cx, cy) -> center co-ordinates]
# > As a concatenation of fixed length bit strings, e.g., for length
#   4, (3, 4, 6) in the above scheme becomes |0011|0100|0110|
#   The length can be easily obtained using the MAX_RADIUS setting above.

ENC_TRIPLE, ENC_BITSTRING = 0, 1

ENCODING_SCHEME = ENC_BITSTRING

# I used bin() here, one may even take a log to the base 2.
BITSTRING_LENGTH = len(bin(int(MAX_RADIUS))[2:])

if ENCODING_SCHEME == ENC_BITSTRING:
    MUTATION_RATE = 0.001
    CROSSOVER_RATE = 0.7
    # Number of generations to go before we start thinking of the solution
    NUM_GENERATIONS = 300
# The mutation rate for plain numbers is much higher than that for bits:
elif ENCODING_SCHEME == ENC_TRIPLE:
    # Mutation rate is much higher for plain numerals than it is for bits.
    MUTATION_RATE = 0.1
    CROSSOVER_RATE = 0.7
    # Number of generations to go before we start thinking of the solution
    NUM_GENERATIONS = 500

# This is the maximum perturbation for mutating an element under the ENC_TRIPLE
# scheme. Borrowed this concept from the Neural Network example program 
# SmartSweepers by Fup.
MAX_PERTURBATION = 0.3

POP_SIZE = 300

# The number of fixed, predrawn circles on the screen - drawn in red.
NUM_FIXED_CIRCLES = 10
RANDOM_FIXED_CIRCLES = True

FIXED_CIRCLES = ((0,0,50),
                 (500,500,100),
                 (300,450,150),
                 (600,700,150),
                 (600,400,100),
                 )



FIXED_CIRCLE_COLOUR = (255,0,0) # Red
SOLUTION_CIRCLE_COLOUR = (0, 255, 0)  # Green

# This is set to true if every chromsome generated is to be checked for the 
# viewport constraints - i.e., r <= cx <= (WINDOW_WIDTH - r), and 
# (r <= cy <= WINDOW_HEIGHT - r). Values are clamped in ga_main() if any of these 
# conditions fail to hold.
CLAMP_NEW = True

# Setting this to True will remember the best chromosome from from each generation
# and the solution, in the end, is the best of these bests. Not quite "pure" GA, 
# but works beautifully in this case - especially with the ENC_TRIPLE encoding and 
# a large (>500) POP_SIZE. 
BEST_OF_THE_BEST = True
#------------------------------------------------------------------------------ 

