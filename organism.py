##--------------------------------------------------------------------\
#   GA_Drawing_Example
#   'organism.py'
#   Class with smallest instance of a genetic algorithm
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   October 30, 2022
##--------------------------------------------------------------------\

import numpy as np
from numpy.random import choice, random, normal

class Organism:
    def __init__(self, genes):
        self.chromosome = np.clip(genes, 0, 1)
        self.visual = None
        self.fitness = None

    def mutate(self, mutation=0.01, tuning=0.3, spawnChance=0.3, removeChance=0.3):
        #inputs are the chances for mutation and spawn, and the std dev.

        #make a static copy of the current chromosomes
        chromosome = np.copy(self.chromosome)
        #get num of gene and features
        n_gene, n_feats = chromosome.shape

        #random() generates a number [0,1).
        # if the number is less than the spawn rate, a gene is either added or removed
        # if the number is greater than the spawn rate, the organism mutates a gene

        randomNum = random()
        if randomNum < spawnChance:
            # add or remove a gene
            if randomNum < removeChance*spawnChance:
                chromosome = np.delete(chromosome, choice(n_gene), axis=0)
            else:
                # adding a new gene is done by blending two existing 'parent' genes
                # into a new one. This is done to increase the chances of getting a
                # relevant gene instead of starting over from scratch.
                # this blending is the key to making this a 'genetic' algorithm

                a, b = choice(n_gene, 2, replace=False)
                gene = np.atleast_2d(0.5 * (chromosome[a, :] + chromosome[b, :]))
                gene += tuning * normal(size=(1, gene.size))
                gene[:, 2] *= 0.2
                chromosome = np.append(chromosome, gene, axis=0)

        else:
            # mutate
            # As more mutations occur, they become less dramatic
            # This tuning keeps the development of the organism heading in
            # the same direction and reduces the 'randomness' that
            # worked early on
            num_mutations = 1 + int(mutation * chromosome.size)
            #update rate
            # make sure that it's never below a minimum threshold
            updateRate = tuning / (1 + int(mutation * chromosome.size)) + 2e-6
            ##updateRate = tuning / num_mutations
            # for all of the potential mutations,
            # pull a gene and feature from the chromosomes, and update
            # choice() chooses a random instance from a sequence
            # normal () draws random samples from a Gaussian distribution
            for i in range(num_mutations):
                chromosome[choice(n_gene), choice(n_feats)] += normal() * updateRate

        return Organism(chromosome)
