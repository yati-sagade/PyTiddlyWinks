'''
Created on Jan 27, 2012

@author: yati
'''
from settings import *
from util import *
from random import random, randint
from copy import copy
from sevensegment import SevenSegmentDisplay
import pygame
import sys
import pygame.gfxdraw

pygame.init()
#-------------------------------------------------------------------------------
class GeneticAlgorithmError(Exception):
    pass
#-------------------------------------------------------------------------------
class Chromosome(list):
    '''
    The chromosome class. Subclasses list so that the chromosome "elements" - 
    bits or actual numbers can be accessed transparently.
    See settings.py - the encoding section to see the different encoding
    possibilities. This class will use settings.ENCODING_SCHEME to appropriately
    encode the data(which is basically the center co-ordinates and the radius).
    '''
    def __init__(self, data, fitness):
        '''
        ctor - data must be a triple (cx, cy, radius) under the ENC_TRIPLE
        scheme and a str of bits for ENC_BITSTRING.
        fitness is the GA fitness of this chromosome.
        '''
        if ENCODING_SCHEME == ENC_BITSTRING:
            for bit in data:
                self.append(int(bit))
                
        elif ENCODING_SCHEME == ENC_TRIPLE:
            self.extend(data[:3])
        
        else:
            raise GeneticAlgorithmError('invalid ENCODING_SCHEME value in settings')
        
        self.fitness = fitness
    
    def decode(self):
        '''
        return a triple - (cx, cy, radius) that this chromosome stands for.
        '''
        if ENCODING_SCHEME == ENC_TRIPLE:
            return self
        
        elif ENCODING_SCHEME == ENC_BITSTRING:
            s = ''.join(map(str, self))
            ctr = 0
            ret = []
            for i in range(3):
                ret.append(s[ctr:(ctr + BITSTRING_LENGTH)])
                ctr += BITSTRING_LENGTH
            
            # Return a tuple of base10 representations of values currently in ret. 
            return tuple(map(lambda x: int(x, 2), ret))
        
        raise GeneticAlgorithmError('invalid ENCODING_SCHEME value in settings')    
#-------------------------------------------------------------------------------
def encode(data):
    '''
    takes a triple and returns the bitstring representing the same, respecting
    the BITSTRING_LENGTH setting
    '''
    if ENCODING_SCHEME == ENC_TRIPLE:
        return data
    elif ENCODING_SCHEME == ENC_BITSTRING:
        ret = ''
        for i in data:
            rep = bin(int(i))[2:]
            ret += ('0' * (BITSTRING_LENGTH - len(rep))) + rep
    else:
        raise GeneticAlgorithmError('invalid ENCODING_SCHEME value in settings')    
    
    return ret
#-------------------------------------------------------------------------------
def crossover(offspring1, offspring2):
    '''
    performs crossover between the given two offsprings depending on the
    CROSSOVER_RATE setting.
    '''
    if random() < CROSSOVER_RATE:
        cp = randint(0, len(offspring1))
        
        baby1, baby2 = (Chromosome(offspring1[:cp] + offspring2[cp:], 0),
                        Chromosome(offspring2[:cp] + offspring1[cp:], 0))
        
        return (baby1, baby2)
    # Return copies of the parents if no crossover is performed.
    return (copy(offspring1), copy(offspring2))
#-------------------------------------------------------------------------------
def mutate(chromosome):
    '''
    Depending on the MUTATION_RATE setting, mutates  `chromosome` *in place*.
    For the triple encoding scheme ENC_TRIPLE, the chosen elements are perturbed
    by an amount not greater than settings.MAX_PERTURBATION.
    Returns whether at least one mutation was done or not.
    '''
    mutated = False
    for i in range(len(chromosome)):
        if random() < MUTATION_RATE:
            mutated = True
            if ENCODING_SCHEME == ENC_BITSTRING:
                chromosome[i] = int(not chromosome[i])
            
            elif ENCODING_SCHEME == ENC_TRIPLE:
                chromosome[i] += clamped_rand() * MAX_PERTURBATION
    
    return mutated
#-------------------------------------------------------------------------------
def evaluate_fitness(chromosome, fixed_circles):
    '''
    evaluates the fitness of a chromosome as follows:
    fixed_circles is a list of triples (cx, cy, radius) for all the circles that
    are present on the window. 
    If the chromosome happens to overlap with any of the existing circles, fitness is
    set to 0, while if not so, the fitness is the radius of the circle repd by 
    the chromosome.
    '''
    this_circle = chromosome.decode()
    for circle in fixed_circles:
        if overlap(this_circle, circle):
            chromosome.fitness = 0
            return 0
    
    chromosome.fitness = this_circle[2] # the radius
    return chromosome.fitness
#-------------------------------------------------------------------------------
def roulette_select(total_fitness, population):
    fitness_slice = random() * total_fitness
    fitness_so_far = 0.0
    
    for phenotype in population:
        fitness_so_far += phenotype.fitness

        if fitness_so_far >= fitness_slice:
            return phenotype

    return None

#-------------------------------------------------------------------------------
def ga_main(fixed_circles, scr):
    '''
    The main GA routine.
    
    fixed_circles is a sequence of the fixed circles' (cx, cy, r) tuples.
    
    scr is the pygame display(of type pygame.Surface)
    
    Run a population through settings.NUM_GENERATIONS generations.
    Returns the best faring chromosome with non-zero fitness till the end, or None 
    if there is none.
    '''
    # Create initial population
    population = []
    total_fitness = 0
    for i in range(POP_SIZE):
        data = get_random_triple()
        ch = Chromosome(encode(data), 0)
        total_fitness += evaluate_fitness(ch, fixed_circles)
        population.append(ch)

    # create the SSD for showing generation count
    char_width = 15
    numchars = len(str(NUM_GENERATIONS))
    ssd = SevenSegmentDisplay(width=char_width * numchars,
                              height=2*char_width,
                              content='0' * numchars,
                              colour=(0,0,0),
                              bgcolour=(255,255,255),
                              char_width=char_width)
    
    scr.blit(ssd.surface, ssd.surface.get_rect())
    pygame.display.flip()
    
    if BEST_OF_THE_BEST:
        # to keep track of the best in each generation
        bests = []
    
    for i in range(NUM_GENERATIONS):
        # The run
        new_population = []
        total_new_fitness = 0
        while len(new_population) < POP_SIZE:
            mom, dad = (roulette_select(total_fitness, population), 
                        roulette_select(total_fitness, population))
            
            baby1, baby2 = crossover(mom, dad)
            mutate(baby1)
            mutate(baby2)
            
            if CLAMP_NEW:
                t1, t2 = baby1.decode(), baby2.decode()
                u1, u2 = clamp_triple(t1), clamp_triple(t2)
                
                if t1 != u1:
                    baby1 = Chromosome(encode(u1), 0)
                
                if t2 != u2:
                    baby2 = Chromosome(encode(u2), 0)
                
            total_new_fitness += evaluate_fitness(baby1, fixed_circles)
            total_new_fitness += evaluate_fitness(baby2, fixed_circles)
            
            new_population.append(baby1)
            new_population.append(baby2)
        
        population = new_population
        total_fitness = total_new_fitness
        # update the ssd counter
        stri = str(i)
        current = ('0' * (numchars - len(stri))) + stri
        ssd.content = current
        scr.blit(ssd.surface, ssd.surface.get_rect())
        pygame.display.flip()
        
        if BEST_OF_THE_BEST:
            bests.append(sorted(population, key=lambda x: x.fitness)[-1])
    
    if BEST_OF_THE_BEST:
        best = sorted(bests, key=lambda x: x.fitness)[-1]
    else:
        best = sorted(population, key=lambda x: x.fitness)[-1]
    
    if not best.fitness:
        return None
    
    return best        
#-------------------------------------------------------------------------------
def run_once(scr):
    '''
    Runs the the Genetic Algorithm once by calling ga_main() 
    This function mainly takes care of the rendering.
    '''
    if RANDOM_FIXED_CIRCLES:
        fixed_circles = get_non_overlapping_triples(NUM_FIXED_CIRCLES)
    else:
        fixed_circles = FIXED_CIRCLES
    
    scr.fill((255, 255, 255))
    
    for circle in fixed_circles:
        x, y, r = map(lambda x: int(round(x)), circle)
        pygame.gfxdraw.aacircle(scr, x, y, r, FIXED_CIRCLE_COLOUR)
    
    pygame.display.flip()
    
    best = ga_main(fixed_circles, scr)
    
    if best:
        x, y, r = map(lambda x: int(round(x)),best.decode())
        pygame.gfxdraw.aacircle(scr, x, y, r, SOLUTION_CIRCLE_COLOUR)
        pygame.display.flip()
        return True
    
    for i in range(3):
        # Visual blinking
        scr.fill((0,0,0))
        pygame.display.flip()
        pygame.time.delay(250)
        scr.fill((255,255,255))
        pygame.display.flip()
        pygame.time.delay(250)
    
    return False
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    pygame.display.set_caption('PyTiddlyWinks')
    pygame.display.set_icon(pygame.image.load('icon.png'))
    scr = pygame.display.set_mode(WINDOW_SIZE)
    
    run_once(scr)
    
    next_msg = "hit return"
    cw = 25
    next_ssd = SevenSegmentDisplay(width=len(next_msg)*cw, 
                                   height=2*cw, 
                                   char_width=cw, 
                                   content=next_msg,
                                   colour=(0,0,0),
                                   bgcolour=(255,255,255))
    
    rect = next_ssd.surface.get_rect()
    offsetx = int((WINDOW_WIDTH - next_ssd.surface.get_width()) / 2)
    offsety = int((WINDOW_HEIGHT - next_ssd.surface.get_height()) / 2)
    rect = rect.move(offsetx, offsety)
    
    scr.blit(next_ssd.surface, rect)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                        run_once(scr)
                        scr.blit(next_ssd.surface, rect)
                        pygame.display.flip()
                        
            pygame.display.flip()
        
#-------------------------------------------------------------------------------
    


    
    
    
