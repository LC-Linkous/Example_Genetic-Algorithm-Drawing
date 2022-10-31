##--------------------------------------------------------------------\
#   GA_Drawing_Example
#   'main.py'
#   Main file for driving project. Create GUI and image evolver instances
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   October 30, 2022
##--------------------------------------------------------------------\

# python lib imports
import wx.lib.mixins.inspection as wit

# project file imports
from GFrame import GFrame
from evolve_image import EvolveImage

def main():
    img = "images/starrynight.jpg"
    outputDir = "output-starry/"
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
    EI.setEvolutionParams(mutationRate=0.07, scaleFactor=0.25, spawnChance=0.20, removeChance=0.03)
    EI.setSimulationParams(steps=1500000, imgUpdate=1000, outputDir=outputDir, saveFile="save.npy")
    EI.createPopulation()
    EI.startSimulation()

    app.MainLoop()



if __name__ == '__main__':
    main()
