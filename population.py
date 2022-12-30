##--------------------------------------------------------------------\
#   GA_Drawing_Example
#   'population.py'
#   Class for a population of organisms. Uses 1 organism with X genes to draw.
#   Contains functions for saving check points
#   modified from: https://cosmiccoding.com.au/tutorials/genetic_part_one
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   November 19, 2022
##--------------------------------------------------------------------\

# python lib imports
from colour import Color
from numpy.random import random
import numpy as np
import sys
import math
from array import *

# project file imports
from organism import Organism
import constants as c

# import antenna calculator
sys.path.insert(0, './AntennaCalculator')
from AntennaCalculator.antenna_calculator import AntennaCalculator

class Population:
    def __init__(self, parent, ref):
        self.parent = parent
        self.ref = ref
        self.w, self.h, *d = self.ref.shape

        inputParams = ['rectangular_patch', '-f', str(c.FREQ), '-er', str(c.RELATIVE_PERMITTIVITY), '-h', str(c.SUBSTRATE_HEIGHT), '--type', 'probe', '--variable_return']
        shell = AntennaCalculator(inputParams)
        args = shell.getArgs()
        #print(args)
        shell.main(args)
        [W, L, x0, y0] = shell.getCalcedParams()
        self.W_calc = self.valueConvert(W) # do 75%
        self.L_calc = self.valueConvert(L) # do 75%
        self.W = self.valueConvert(W*0.75)
        self.L = self.valueConvert(L*0.75)
        self.x0_calc = self.valueConvert(x0)
        self.y0_calc = self.valueConvert(y0)
        # print("W_calc: ", self.W_calc)
        # print("L_calc: ", self.L_calc)
        # print("W: ", self.W)
        # print("L: ", self.L)
        # print("x0_calc: ", self.x0_calc)
        # print("y0_calc: ", self.y0_calc)


        if self.W_calc > self.L_calc:
            self.rows = self.W_calc * 3
            self.cols = self.W_calc * 3
        else:
            self.rows = self.L_calc * 3
            self.cols = self.L_calc * 3
        # print("rows: ", self.rows)
        # print("cols: ", self.cols)

        self.x0 = (int(self.cols/2)+int(self.L_calc/2)-int(self.x0_calc))
        self.y0 = (int(self.rows/2))

        #evolution comparison params
        self.currentBestOrganism = None

        #user params
        self.imgUpdate = 250 # default = 250
        self.outDir = ""
        self.saveFile = ""
        self.saveSummary = ""
        self.square_length = 0.1

        # update info
        self.currentGenes = 0

    def setUserParams(self, imgUpdate=250, outdir="", saveFile="save.npy", summaryFile="organismSummary.txt"):
        self.imgUpdate = imgUpdate      # how often to save the images
        self.outDir = outdir            # directory to save everything
        self.saveFile = saveFile        # the npy file
        self.saveSummary = summaryFile  # summary of check point changes

    def drawOrganism(self, org, scale=0.3, minSize=0.01):
        # the scale and minSize are optional,
        # and should be set at START of process, or risk disrupting the process

        # draw the organism (the collection of genes) on the gui canvas
        # for each gene, the x & y are pulled and scaled,


        # bitArr -> pixel
        # 2d mat -> chrom/gene list [[x,y,w,h,pres, col]....]



        ctr=0
        # xctr=0
        # yctr=0

        # for idx in org.chromosomes:
        #     for jdx in idx:
        #         #print(org.chromosomes)
        #         # get the x,y vals
        #         x = xctr
        #         y = yctr
        #         # scale x and y and add
        #         width = c.PIX_RES # 2
        #         height = c.PIX_RES
        #         presence = jdx
        #         if presence == 1:
        #             rgb = (0,0,0) #black
        #             ctr = ctr + 1 #will become self.currentGenes
        #         else:
        #             rgb = (224,224,224) # white
                
        #         if (x == self.y0) and (y == self.x0):
        #             #print("x0, y0: ", x, y)
        #             rgb = (255,0,0)

        #         drawArr = []
        #         drawArr.append(x)
        #         drawArr.append(y)
        #         drawArr.append(width)
        #         drawArr.append(height)
        #         drawArr.append(presence)
        #         drawArr.append(rgb)
        #         self.parent.gui.addShape(drawArr)
        #         #drawArr.append(x,y,width,height,presence,rgb)
        #         #print(x,y,width,height,presence,rgb)
        #         #print(drawArr)
        #         xctr=xctr+1
        #     yctr=yctr+1
        #     xctr=0
        # yctr = 0

        for idx in org.chromosomes:
            #print("idx: ", idx)
            x = idx[0]
            y = idx[1]
            width = c.PIX_RES # 2
            height = c.PIX_RES
            presence = idx[2]
            #print("x,y,pres: ", x, y, presence)
            if presence == 1:
                rgb = (0,0,0) #black
                ctr = ctr + 1 #will become self.currentGenes
            else:
                rgb = (224,224,224) # white
            if (x == self.y0) and (y == self.x0):
                #print("x0, y0: ", x, y)
                rgb = (255,0,0)

            drawArr = []
            drawArr.append(x)
            drawArr.append(y)
            drawArr.append(width)
            drawArr.append(height)
            drawArr.append(presence)
            drawArr.append(rgb)
            self.parent.gui.addShape(drawArr)                
        
        self.currentGenes = ctr     # set counter
        #print("self.currentGenes: ", self.currentGenes)
        self.parent.gui.onPaint()   # trigger paint event                

    def valueConvert(self, val):
        return math.ceil(int(val * 10000)/2)

    def spawn(self, numGenes=1, numFeatures=3):
        # create a population of individual organisms with
        # user controlled number of genes and features
        #  random(3, 4) creates 3 genes with 4 features
        # numGenes number of genes, with a complexity of

        # in this case only a single individual is created
        #random_genes = random((numGenes, numFeatures))

        #create bitArray here: 
        # dimensions from calc: W, L, probe coords (x,y)
        # dims/res = min W and L bits. #*1.5 = # of bits used in alg
        # self.bitArray = 2d mat init to 0s <- full bitArray is chromosomes
        # For loop: for loop: flip bits in seed patch to 1
        # self.currentBestOrganism = Organism(self.bitArray)
        # calcFitness(##)

        #create bitArray here:

        # dimensions from calc: W, L, probe coords (x,y)
        # dims/res = min W and L bits. #*1.5 = # of bits used in alg

        # replace cols and rows programmatically from calc
        #cols = 402
        #rows = 404

        # bit array
        #chromosomes = [[0 for i in range(self.cols)] for j in range(self.rows)]
        chromosomes = []
        # print(chromosomes)

        #seed 
        midx = int(self.rows/2)
        midy = int(self.cols/2)
        #print("midx: ", midx, "\t midy: ", midy)
        #print("res: ", c.RES)
        #print("midx-int(40/c.RES): ", midx-int(10/c.RES))

        #inputParams = ['rectangular_patch', '-f', c.FREQ, '-er', c.RELATIVE_PERMITTIVITY, '-h', c.SUBSTRATE_HEIGHT, '--variable_return']

        #print("W: ", W, "\t L: ", L, "\t x0: ", self.x0, "\t y0: ", self.y0)
        #print(W_unpack*1000)
        #W, L, x0, y0 = AntennaCalculator(inputParams)
        #print(W)

        # ctr = 0
        # for idx in range(midx-int(self.L/2), midx+int(self.L/2)):
        #     for jdx in range(midy-int(self.W/2), midy+int(self.W/2)):
        #         chromosomes[idx][jdx] = 1
        #         #print("idx: ", idx, "\t jdx: ", jdx)
        #         ctr = ctr + 1

        #ctr = 0
        for idx in range(midx-int(self.W/2), midx+int(self.W/2)):
            for jdx in range(midy-int(self.L/2), midy+int(self.L/2)):
                # print("idx: ", idx, "\t jdx: ", jdx)
                # print("midx: ", midx, "\t midy: ", midy)
                # print("midx-idx: ", midx-idx, "\t midy-jdx: ", midy-jdx)
                # print("(midx-idx)^2: ", (midx-idx)**2, "\t (midy-jdx)^2: ", (midy-jdx)**2)
                # print("math.sqrt((midx-idx)^2 + (midy-jdx)^2): ", math.sqrt((midx-idx)**2 + (midy-jdx)**2))
                chromosomes.append([idx, jdx, 1, math.sqrt((midx-idx)**2 + (midy-jdx)**2)])
                #chromosomes.append([idx, jdx, 1, 0])
                #ctr = ctr + 1
        print("generating W", midx-int(self.W/2), "to", midx+int(self.W/2))
        print("generating L", midy-int(self.L/2), "to", midy+int(self.L/2))
        #print("chromosomes: ", chromosomes)
        #print ("chromosomes: ", chromosomes)
        #chromosomes.insert(index, [x, y, 1, math.sqrt((x-midx)^2 + (y-midy)^2)])


        #print("expected number of 1s: ", ctr)
        # print(chromosomes[0][0])
        # print(chromosomes[midx][midy])
        

        #print(chromosomes)
        self.currentBestOrganism = Organism(chrom=chromosomes, row = self.rows, col = self.cols)
        self.calcFitness(self.currentBestOrganism)

    def calcFitness(self, org):
        # fitness of new organism is calculated by drawing it and then
        # comparing to the reference (original) image.

        #update the drawing
        self.drawOrganism(org)


        #dont need the current image bc that's now display only
        # pair down if possible, but need for display not math
        image = self.parent.gui.getCurrentImage()
        #get the current image
        im = image.GetDataBuffer()
        arr = np.frombuffer(im, dtype='uint8', count=-1, offset=0)
        # convert to array
        image = np.reshape(arr, (c.PANEL_HEIGHT, c.PANEL_WIDTH, 3))
        #this stays
        org.visual = image

       
        # HFSS call
        # # simulation run
        # # data parsing
        # # getting gain and frequency (current sim)


        # do difference between Freq and Gain with the targets
        # diff = image - self.ref

        # difference functions for freqvs target and gain vs target to compare with current org
        org.fitness = 0 #-np.mean(np.abs(diff)) - 1e-5 #* org.chromosomes.shape[0]


        

    def step(self, time, mutationRate=0.01, scaleFactor=0.1, spawnChance=0.3, removeChance=0.3):
        # each step works by working like 'generations'.
        # the organism is mutated (or not) based on the user input parameters
        # If the new organism is better than the last one, we update to the new one



        #update the mutate call
        # this comparison stays
        #o = self.currentBestOrganism.mutate(mutationRate=mutationRate, scaleFactor=scaleFactor, spawnChance=spawnChance, removeChance=removeChance)
        
        o = self.currentBestOrganism.mutate()
       
        self.calcFitness(o)
        # TEMP EDIT ONLY!!!!!!!
        #if o.fitness > self.currentBestOrganism.fitness:
        self.currentBestOrganism = o
        #print("o.fitness: ", o.fitness)
        #print("self.currentBestOrganism.fitness: ", self.currentBestOrganism.fitness)
           

        #create a check point
        # + append to the summary file to keep track of what parameters are in use
        # NOTE: it is possible to change parameters and load from last check point,
        # but parameters are not always changing
        if time % self.imgUpdate == 0:
            checkpt = time/self.imgUpdate
            savePath = self.outDir + f"{time // self.imgUpdate:04d}.png"
            #save progress
            np.save(self.outDir + self.saveFile, self.currentBestOrganism.chromosomes)
            self.parent.gui.saveImage(savePath)
            print("Check point # ", checkpt, " Current number of genes: ", self.currentGenes)
            with open(self.outDir + self.saveSummary, "a", encoding="utf-8") as f:
                f.write("time: " + str(time) +
                        "\tmutation: " + str(mutationRate) +
                        "\tscale: " + str(scaleFactor) +
                        "\tspawn: " + str(spawnChance) +
                        "\tremove: " + str(removeChance) +
                        "\tgenes: " + str(self.currentGenes) + "\n")