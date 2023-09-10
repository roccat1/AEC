import json
import gameFiles.pyfiles.button as button
from gameFiles.pyfiles.fonts import *
#config file
with open(configJsonPath, "r") as f:
    config = json.load(f)
#values file
with open(valuesJsonPath, "r") as f:
    values = json.load(f)
resolution=[config["resolution"]["width"],config["resolution"]["height"]]

#most of the models used in a class
class Models:
    def __init__(self):
        #surfs for the nums of the storage menu
        self.storageSurfs = {
            "money": fontSmall.render("", True, "black"),
            "wood": fontSmall.render("", True, "black"),
            "food": fontSmall.render("", True, "black"),
            "stone": fontSmall.render("", True, "black")
        }

        #Creacio de models
        #buildings
        self.thModel = button.Button(resolution[0]/2-40, resolution[1]/2-40, pygame.image.load(thGenericTexturePath + str(values["initialValues"]["lvls"]["TH"]) + ".png").convert_alpha(), 1)
        self.forestModel = button.Button(resolution[0]/2-140, resolution[1]/2-40, pygame.image.load(forestGenericTexturePath + str(values["initialValues"]["lvls"]["forest"]) + ".png").convert_alpha(), 1)
        self.farmModel = button.Button(resolution[0]/2-40, resolution[1]/2-140, pygame.image.load(farmGenericTexturePath + str(values["initialValues"]["lvls"]["farm"]) + ".png").convert_alpha(), 1)
        self.quarryModel = button.Button(resolution[0]/2+60, resolution[1]/2-40, pygame.image.load(quarryGenericTexturePath + str(values["initialValues"]["lvls"]["quarry"]) + ".png").convert_alpha(), 1)
        self.internalMarketModel = button.Button(resolution[0]/2-40, resolution[1]/2+60, pygame.image.load(internalMarketGenericTexturePath + str(values["initialValues"]["lvls"]["internalMarket"]) + ".png").convert_alpha(), 1)

        #downmenu #-160-40+80 #-220-100+20+140
        self.downgradeModel = button.Button(resolution[0]/2-220, resolution[1]-100, pygame.image.load(downgradeTexturePath).convert_alpha(), 1)
        self.upgradeModel = button.Button(resolution[0]/2+20, resolution[1]-100, pygame.image.load(upgradeTexturePath).convert_alpha(), 1)
        self.infoModel = button.Button(resolution[0]/2-100, resolution[1]-100, pygame.image.load(infoTexturePath).convert_alpha(), 1)
        self.populationModel = button.Button(resolution[0]/2+140, resolution[1]-100, pygame.image.load(populationTexturePath).convert_alpha(), 1)
        self.enterBuildingModel = button.Button(resolution[0]/2+140, resolution[1]-100, pygame.image.load(enterBuildingTexturePath).convert_alpha(), 1)
        
        #menu icons
        self.confirmUpgradeModel = button.Button(resolution[0]/2+80, resolution[1]/2+80, pygame.image.load(acceptTexturePath).convert_alpha(), 1)
        self.cancelUpgradeModel = button.Button(resolution[0]/2-160, resolution[1]/2+80, pygame.image.load(cancelTexturePath).convert_alpha(), 1)
        self.cancelCenterModel = button.Button(resolution[0]/2-40, resolution[1]/2+80, pygame.image.load(cancelTexturePath).convert_alpha(), 1)

        self.addCitizenModel = button.Button(resolution[0]/2+80, resolution[1]/2-20, pygame.image.load(addTexturePath).convert_alpha(), 1)
        self.subtractCitizenModel = button.Button(resolution[0]/2-160, resolution[1]/2-20, pygame.image.load(subtractTexturePath).convert_alpha(), 1)
        self.loadModel = button.Button(resolution[0]/2-250, resolution[1]/2-150, pygame.image.load(loadTexturePath).convert_alpha(), 1)
        self.saveModel = button.Button(resolution[0]/2-250, resolution[1]/2+50, pygame.image.load(saveTexturePath).convert_alpha(), 1)
        self.newSaveModel = button.Button(resolution[0]/2-250, resolution[1]/2-150, pygame.image.load(newSaveTexturePath).convert_alpha(), 1)
        self.resumeModel = button.Button(resolution[0]/2-250, resolution[1]/2+50, pygame.image.load(resumeTexturePath).convert_alpha(), 1)

        #images storage
        self.moneyModel = button.Button(20, 20, pygame.image.load(moneyTexturePath).convert_alpha(), 0.7)
        self.woodModel = button.Button(20, 100, pygame.image.load(woodTexturePath).convert_alpha(), 0.7)
        self.foodModel = button.Button(20, 180, pygame.image.load(foodTexturePath).convert_alpha(), 0.7)
        self.stoneModel = button.Button(20, 260, pygame.image.load(stoneTexturePath).convert_alpha(), 0.7)

        self.saveSurf = font.render("", True, "black")