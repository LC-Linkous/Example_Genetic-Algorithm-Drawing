##--------------------------------------------------------------------\
#   GA_Drawing_Example
#   'population.py'
#   Class for a population of organisms. Uses 1 organism with X genes to draw.
#   Contains functions for saving check points
#   modified from: https://cosmiccoding.com.au/tutorials/genetic_part_two
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   November 12, 2022
##--------------------------------------------------------------------\

# python lib imports
from colour import Color
import numpy as np
from numpy.random import choice, random, normal
import json

# project file imports
from organism import Organism
import constants as c

class Population2:
    def __init__(self, parent, ref):
        self.parent = parent
        self.ref = ref
        self.w, self.h, *d = self.ref.shape

        #evolution comparison params
        #self.currentBestOrganism = None

        self.population = []

        #user params
        self.imgUpdate = 250 # default = 250
        self.outDir = ""
        self.saveFile = ""
        self.saveSummary = ""

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

        ctr = 0
        for gene in org.chromosome:
            x, y, size, *hsl = gene     # get gene information
            draw_x = int(x * self.w)    # scale x for drawing
            draw_y = int(y * self.h)    # scale y for drawing
            draw_size = int((size * scale + minSize) * self.w) # scale size
            c = tuple(map(lambda x: int(255 * x),  Color(hsl=hsl).rgb)) #convert color vals properly
            c = np.array(c) #convert to array
            self.parent.gui.addCircle([draw_x, draw_y, draw_size, c]) #draw circle on parent GUI
            ctr = ctr + 1           # increment for report
        self.currentGenes = ctr     # set counter
        self.parent.gui.onPaint()   # trigger paint event

    def spawn(self, popSize=30, numGenes=10, numFeatures=6):
        # create a population of individual organisms with
        # user controlled number of genes and features
        #  random(3, 4) creates 3 genes with 4 features
        # numGenes number of genes, with a complexity of
        for i in range(popSize):
            organism = Organism(random((numGenes, numFeatures)))
            self.population.append(organism)
            self.calcFitness(organism)
        self.population = sorted(self.population, key=lambda x: -x.fitness)

    def calcFitness(self, org):
        # fitness of new organism is calculated by drawing it and then
        # comparing to the reference (original) image.

        # update the drawing
        self.drawOrganism(org)
        image = self.parent.gui.getCurrentImage()
        # get the current image
        im = image.GetDataBuffer()
        arr = np.frombuffer(im, dtype='uint8', count=-1, offset=0)
        # convert to array
        image = np.reshape(arr, (c.PANEL_HEIGHT, c.PANEL_WIDTH, 3))
        diff = image - self.ref
        org.fitness = -np.mean(np.abs(diff)) - 1e-5 * org.chromosome.size
        org.visual = image

    def getChild(self, a, b):
        """ Breed a and b by mixing the common length genes, keeping most from
        the first parent. """
        new_genes = []
        n_a, n_b = a.chromosome.shape[0], b.chromosome.shape[0]
        for i in range(max(n_a, n_b)):
            if i < n_a and i < n_b:
                if random() < 0.7:
                    new_genes.append(a.chromosome[i, :])
                else:
                    new_genes.append(b.chromosome[i, :])
            elif i < n_a:
                new_genes.append(a.chromosome[i, :])
            else:
                if random() < 0.3:
                    new_genes.append(b.chromosome[i, :])
            chromosome = np.array(new_genes)
        o = Organism(chromosome)
        self.calcFitness(o)
        return o

    def save(self, path):
        """ Save population to json file """
        out = [o.chromosome.tolist() for o in self.population]
        with open(path, "w") as f:
            json.dump(out, f)

    def load(self, path):
        """ Load population from json file """
        with open(path) as f:
            inp = json.load(f)
        self.population = [Organism(np.array(x)) for x in inp]
        for o in self.population:
            self.calcFitness(o)

    def mutateAndPick(self, organism, mutation, tuning, spawnChance, removeChance, attempts=10):
        # over X number of attempts, mutate and choose the best options
        # doing this over a number of attempts increases the chances
        # that you'll get a better/relevant mutation
        for i in range(attempts):
            o = organism.mutate(mutation=mutation, tuning=tuning, spawnChance=spawnChance, removeChance=removeChance)
            self.calcFitness(o)
            if o.fitness > organism.fitness:
                #returns early if there's a better mutation
                return o
        return organism

    def step(self, time, mutation=0.01, tuning=0.1, spawnChance=0.3, removeChance=0.3):
        # each step works by working like 'generations'.
        # the organism is mutated (or not) based on the user input parameters
        # If the new organism is better than the last one, we update to the new one

        # Get some children by picking the fitter parents
        new_orgs = []
        weights = 1 - np.linspace(0, 0.2, len(self.population))
        for i in range(len(self.population)):
            #make a random choice
            a, b = choice(self.population, 2, replace=True, p=weights / weights.sum())
            child = self.getChild(a, b)
            new_orgs.append(self.mutateAndPick(child, mutation, tuning, spawnChance, removeChance))

        # Calculate fitness,sort fitness, update population
        for o in new_orgs:
            self.calcFitness(o)
        sorted_orgs = sorted(new_orgs, key=lambda x: -x.fitness)
        self.population = sorted_orgs[:len(self.population)]


        #create a check point
        # + append to the summary file to keep track of what parameters are in use
        # NOTE: it is possible to change parameters and load from last check point,
        # but parameters are not always changing
        if time % self.imgUpdate == 0:
            checkpt = time/self.imgUpdate
            savePath = self.outDir + f"{time // self.imgUpdate:04d}.png"
            #save progress
            self.save(self.outDir + self.saveFile + "save.json")
            self.parent.gui.saveImage(savePath)
            print("Check point # ", checkpt, " Current number of genes: ", self.currentGenes)
            with open(self.outDir + self.saveSummary, "a", encoding="utf-8") as f:
                f.write("time: " + str(time) +
                        "\tmutation: " + str(mutation) +
                        "\tscale: " + str(tuning) +
                        "\tspawn: " + str(spawnChance) +
                        "\tremove: " + str(removeChance) +
                        "\tgenes: " + str(self.currentGenes) + "\n")