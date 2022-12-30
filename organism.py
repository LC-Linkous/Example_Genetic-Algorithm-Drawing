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

            #choice(list(set([x for x in range(0, 9)]) - set(to_exclude)))
            #rx = choice(list(set([x for x in range(0, self.rows)]) - set(range(156, 230))))
            #ry = choice(list(set([x for x in range(0, self.cols)]) - set(range(145, 241))))
            #print("rx ", rx, " ry ", ry)


            #print("rx ", rx, " ry ", ry)
            # get the bit at self.chromosomes[x][y]
            #presence = self.chromosomes[x][y]

            #freq function. 
            # fDiff = targetF -freq
            fDiff = targetFreq - freq
        
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
       
            if gDiff >= 0:
                gainBoost = gDiff

            # spawn function
            spawn = spawnRate + gainBoost
            
            action = spawnRate-cullRate

            
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
            


    

 

        return Organism(self.chromosomes, self.rows, self.cols)

