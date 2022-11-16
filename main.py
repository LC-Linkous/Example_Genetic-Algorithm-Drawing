##--------------------------------------------------------------------\
#   GA_Drawing_Example
#   'main.py'
#   Main file for driving project. Create GUI and image evolver instances
#   modified from: https://cosmiccoding.com.au/tutorials/genetic_part_one
#
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   October 30, 2022
##--------------------------------------------------------------------\

# python lib imports
import wx.lib.mixins.inspection as wit

# project file imports
from GFrame import GFrame
from evolve_image import EvolveImage

def main():
    # img = "images/starrynight.jpg"
    # outputDir = "output-starry/"
    img = "images/pearl.png"
    outputDir = "output-pearl/"
    title = "GA Drawing:" + img
    #GUI
    app = wit.InspectableApp()
    GF = GFrame(None, title=title)
    GF.setImageAndFit(img) #fit the intial image to the screen
    GF.clearScreen()
    refImage = GF.getRefImage() #get the scaled reference image copy
    GF.Show()

    #image evolver
    EI = EvolveImage(refImage) # access to reference image
    EI.addGUI(GF) #access to GUI for redraw
    EI.setEvolutionParams(mutationRate=0.03, scaleFactor=0.25, spawnChance=0.20, removeChance=0.03)
    EI.setPopulationParams(singleOrg=False, numOrganisms=10, numGenes=10, numFeatures=6)
    EI.setSimulationParams(steps=100000, imgUpdate=200, outputDir=outputDir, saveFile="save.json") #save.npy if single
    EI.createPopulation()
    EI.startSimulation()

    app.MainLoop()



if __name__ == '__main__':
    main()
