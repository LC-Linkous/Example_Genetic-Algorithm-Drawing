##--------------------------------------------------------------------\
#   GA_Drawing_Example
#   'organism.py'
#   Class with smallest instance of a genetic algorithm
#   modified from: https://cosmiccoding.com.au/tutorials/genetic_part_one
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   November 19, 2022
##--------------------------------------------------------------------\

import numpy as np
from numpy.random import choice, random, normal
import random
import math

class Organism:
    def __init__(self, chrom, row, col):
        self.chromosomes = chrom # bitArray: [[#,#,#], [#,#,#]....]
        self.rows = row
        self.cols = col
        #print("org init chrom: ", self.chromosomes[35][35])

    def mutate(self, freq=0, gain=0, targetFreq=3.55e9, minGain=3): # , freq, gain, targetFreq=2.4e9, minGain=4):
        # Inputs:
        # USE DEFAULT INPUTS. Call with mutate()
        #  freq = a randomly generated number below
        #  gain = a randomly generated number below
        #  targetFreq = the ideal resonant frequency of the project. hardset. do not change
        #  minGain = the minimum gain for a patch. hardset. do not change.

        freq = random.uniform(2.5e9,4.5e9) #limit range on these
        gain = random.uniform(2,5) #limit range on these
        #targetFreq = 3.55e9 # these vals are set in the default func call
        #minGain = 3

        #for testing.
        # generate random freq between 2.5G and 4.5G
        # generate random gain between 2 and 5


        # create some kind of hardcoded spawn rate and cull rate
        # these will need to be adjusted
        baseSpawn = 0.25 # 25% chance
        baseCull = 0.1
        # so there's some value to these vars incase they're called before being created in the funcs below
        spawnRate = baseSpawn
        cullRate = baseCull

        
        #for i in range(100):
        ctr_neighbor = 0
        ctr_spawn = 0
        #rx = int(self.rows/2)
        #ry = int(self.cols/2)
        print("length ", len(self.chromosomes))
        while(ctr_spawn < 100):
            # get shape of self.chromosomes to set range of x and y random numbers
            #x = np.random.randint(0, len(self.chromosomes)) # rows
            #y = np.random.randint(0, len(self.chromosomes[0])) #cols

            #while((156-2 < rx <= 241-2) and (145-2 < ry <= 230-2)):
            rx = np.random.randint(0, self.rows) # rows (L)
            ry = np.random.randint(0, self.cols) #cols (W)
            #print("rx ", rx, " ry ", ry)
            # get the bit at self.chromosomes[x][y]
            #presence = self.chromosomes[x][y]

            #freq function. 
            # fDiff = targetF -freq
            fDiff = targetFreq - freq
            # use fDiff to create a scaling function
            # alpha = some equation based on fDiff like (1-fDiff/targetF)
            # there's probably some proper equation for this
            # if fDiff >= 0:
            #   frequency is too low, so increase spawn and decrease cull rates with an alpha (scale) val
            #   an example:
            #       s = baseSpawn+alpha OR adusted base on the alpha val equation to make this between 0 and 1
            #       c = baseCull- alpha
            # else: (fDiff < 0)
            #   frequency is too high. do the same as above but in reverse. lower Spawn, increase cull
            if fDiff >= 0:
                spawnRate = baseSpawn + fDiff/targetFreq
                cullRate = baseCull - fDiff/targetFreq
            else:
                spawnRate = baseSpawn - fDiff/targetFreq
                cullRate = baseCull + fDiff/targetFreq

            #gain function.
            # this is a spawn boost only
            # gDiff = minGain - gain
            gDiff = minGain - gain
            # gainBoost = 0 by default
            gainBoost = 0
            # if gDiff >= 0:
            #   gain is too low, so increase spawn rate
            #   an example:
            #       s = baseSpawn+gDiff
            # else: (gDiff < 0)
            #   gain is too high. do nothing
            if gDiff >= 0:
                gainBoost = gDiff

            # spawn function
            spawn = spawnRate + gainBoost
            
            action = spawnRate-cullRate

            # if presence == 1:
            #     if action < 0:
            #         self.chromosomes[x][y] = 0
            # else:
            #     if action >= 0:
            #         self.chromosomes[x][y] = 1

            # scan if nearby
            # for idx in self.chromosomes:
            #     if (rx - 2 < idx[0] <= rx + 2) and (rx != idx[0]):
            #         if (ry - 2 < idx[1] <= ry + 2) and (ry != idx[1]):
            #             for tdx in self.chromosomes:
            #                 if (tdx[0] == rx):
            #                     if (tdx[1] == ry):
            #                         raise StopIteration
            #             if action >= 0:
            #                 self.chromosomes.append([rx,ry,1,math.sqrt((int(self.rows/2)-rx)**2 + (int(self.cols/2)-ry)**2)])
            #                 raise StopIteration
            
            
            ctr_neighbor = 0
            #print("length ", len(self.chromosomes))
            for idx in self.chromosomes:
                
                #print("for")
                if idx[0] == rx:
                    if idx[1] == ry:
                        #print("break")
                        break
                #if ((145 < ry <=241) and (145 < rx <= 230)):
                #    break
                #print("rx ", rx, " ry ", ry, " idx[0] ", idx[0], " idx[1] ", idx[1])
                if ((rx - 2) < idx[0] < (rx + 3)) and (rx != idx[0]):
                    if ((ry - 2) < idx[1] < (ry + 3)) and (ry != idx[1]):
                        ctr_neighbor += 1
                        #print("neighbor")
                if rx == idx[0] and ry==idx[1]:
                    print("!!!!!!")
            
            if (ctr_neighbor > 2):
                #if(ctr_neighbor>6):
                    #print("appending rx ", rx, "ry ", ry, "ctr_neighbor ", ctr_neighbor)
                #if (145 < ry <=241) and (145 < rx <= 230):
                #    print("inside the internal patch")
                self.chromosomes.append([rx,ry,1,math.sqrt((int(self.rows/2)-rx)**2 + (int(self.cols/2)-ry)**2)])
                #print(self.chromosomes[-1])
                ctr_spawn += 1
                #print("length ", len(self.chromosomes),"\n")
                #ctr_neighbor = 0

                            #print("nearby")
                            #print ("rx: ", rx, "ry: ", ry)
                            #print ("idx[0]: ", idx[0], "idx[1]: ", idx[1])
                            #if action < 0:
                            #    self.chromosomes.remove(idx)
                            #else:
                                #raise StopIteration

                #print("length of chrom:: ", len(self.chromosomes))
                #print("rx: ", rx, "ry: ", ry)

                            
                    

                                #idx[2] = 1
                                #idx[3] = math.sqrt((int(self.rows/2)-rx)**2 + (int(self.cols/2)-ry)**2)
                    # if idx[0] == x and idx[1] == y:
                    #     if action < 0:
                    #         self.chromosomes.remove(idx)
                    #     else:
                    #         idx[2] = 1
                    #         idx[3] = math.sqrt((int(self.rows/2)-x)**2 + (int(self.cols/2)-y)**2)
                    #     break

                #if action >= 0:
                #   self.chromosomes.append([x,y,1,math.sqrt((int(self.parent.rows/2)-x)**2 + (int(self.parent.cols/2)-y)**2)])

                #

        # for loop to do 100 times.

            # get shape of self.chromosomes to set range of x and y random numbers
            
            #generate x and y as random nums. 0 to size of dimension
            # check if max number is index or length (i.e. 400 vs 399)

            # get the bit at self.chromosomes[x][y]

            #freq function. 
            # fDiff = targetF -freq
            # use fDiff to create a scaling function
            # alpha = some equation based on fDiff like (1-fDiff/targetF)
            # there's probably some proper equation for this
            # if fDiff >= 0:
            #   frequency is too low, so increase spawn and decrease cull rates with an alpha (scale) val
            #   an example:
            #       s = baseSpawn+alpha OR adusted base on the alpha val equation to make this between 0 and 1
            #       c = baseCull- alpha
            # else: (fDiff < 0)
            #   frequency is too high. do the same as above but in reverse. lower Spawn, increase cull

            #gain function.
            # this is a spawn boost only
            # gDiff = minGain - gain
            # gainBoost = 0 by default
            # if gDiff >=0:
            #   gain is too low, so increase spawn rate based on neighbors
            #   get the # of neighbors for 2 rows around the bit. need to compensate for if at edge of matrix
            #   gainBoost = some equation where more neighbors means more boost
            # 
            # else:
            # nothing. gainBoost = 0 still. no else function


            #take the vales from the frequency and gain functions, and make equation for actual spawn and cull rates
            # spawnRate = s + gainBoost
            # cullRate = c  (and gain might actually need to adjust cull too, so leave space for this)

            # action to take:
            # action = spawnRate-cullRate
            # if action is positive, it'll spawn. if it's negative, it's a cull        

            #check bit value for presence
            # if presence ==1: 
            #   if action >=0:
            #       #nothing. there's something there and it's a spawn.
            #   else:
            #       #cull. 
            # else: (presence ==0)
            #   if action >=0:
            #       #add
            #   else:
            #       #nothing. nothing there and it's a cull 
 

        return Organism(self.chromosomes, self.rows, self.cols)












    # LEAVE FOR REFERENCE:

    # def mutate(self, mutationRate=0.01, scaleFactor=0.3, spawnChance=0.3, removeChance=0.3):
    #     #inputs are the chances for mutation and spawn, and the std dev.

    #     #make a static copy of the current chromosomes
    #     chromosome = np.copy(self.chromosome)
    #     #get num of gene and features
    #     n_gene, n_feats = chromosome.shape

    #     #random() generates a number [0,1).
    #     # if the number is less than the spawn rate, a gene is either added or removed
    #     # if the number is greater than the spawn rate, the organism mutates a gene

    #     randomNum = random()
    #     if randomNum < spawnChance:
    #         # add or remove a gene
    #         if randomNum < removeChance*spawnChance:
    #             chromosome = np.delete(chromosome, choice(n_gene), axis=0)
    #         else:
    #             # adding a new gene is done by blending two existing 'parent' genes
    #             # into a new one. This is done to increase the chances of getting a
    #             # relevant gene instead of starting over from scratch.
    #             # this blending is the key to making this a 'genetic' algorithm

    #             a, b = choice(n_gene, 2, replace=False)
    #             gene = np.atleast_2d(0.5 * (chromosome[a, :] + chromosome[b, :]))
    #             gene += scaleFactor * normal(size=(1, gene.size))
    #             gene[:, 2] *= 0.2
    #             chromosome = np.append(chromosome, gene, axis=0)

    #     else:
    #         # mutate
    #         # As more mutations occur, they become less dramatic
    #         # This tuning keeps the development of the organism heading in
    #         # the same direction and reduces the 'randomness' that
    #         # worked early on
    #         num_mutations = 1 + int(mutationRate * chromosome.size)
    #         #update rate
    #         # make sure that it's never below a minimum threshold
    #         updateRate = scaleFactor / (1 + int(mutationRate * chromosome.size)) + 2e-6
    #         ##updateRate = tuning / num_mutations
    #         # for all of the potential mutations,
    #         # pull a gene and feature from the chromosomes, and update
    #         # choice() chooses a random instance from a sequence
    #         # normal () draws random samples from a Gaussian distribution
    #         for i in range(num_mutations):
    #             chromosome[choice(n_gene), choice(n_feats)] += normal() * updateRate

    #     #self.chromosome = np.clip(chromosome, 0, 1) 
    #     return Organism(chromosome)
