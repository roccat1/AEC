#Afers Exteriors Capitalitzats
'''
______________________________________
|Author: Roc Rodríguez Arumí         |
|Github: https://github.com/roccat1  |
|Email: roc.r2005@gmail.com          |
|____________________________________|
'''
#Llibreries
import pygame, json, pickle, os
from decimal import Decimal

#arxius
from paths import *
import button
import gameClass

#values file
with open(valuesJsonPath, "r") as f:
    values = json.load(f)
#version file
with open(versionJsonPath, "r") as f:
    version = json.load(f)
#config file
with open(configJsonPath, "r") as f:
    config = json.load(f)
#selected language file
with open(langsJsonPath[config["lang"]], "r") as f:
    texts = json.load(f)

mouseLPressed=False
mouseLDown=False
prevMouseLPressed=False
initialMenu=config["initialMenu"]

showFPS=config["FPS"]["show"]
maxFPS=config["FPS"]["max"]

# pygame setup
pygame.init()
resolution=[1280,720]
screen = pygame.display.set_mode((resolution[0], resolution[1]))
clock = pygame.time.Clock()
pygame.display.set_caption('Afers Exteriors Capitalitzats (AEC)')
pygame_icon = pygame.image.load(iconTexturePath)
pygame.display.set_icon(pygame_icon)
running = True

#fonts
giantFont = pygame.font.Font(arialFontPath, 100)
font = pygame.font.Font(arialFontPath, 36)
fontSmall = pygame.font.Font(arialFontPath, 20)

dT=0

game = gameClass.Game()

#log creator
def log(msg):
    with open('saves/log.txt', 'w') as f:
        f.write(msg)
        print(msg)

log("")

#convert 1000 -> 1k ...
#usage: reNumberer(game.storage[item])+game.abbreviate[item]
def reNumberer(num):
    for unit in ['','K','M']:
        if abs(num) < 1000.0:
            return f"{num:6.2f}{unit}"
        num /= 1000.0
    return f"{num:6.2f}B"

#save game by object game
def saveGame():
    global game, models
    game.active=True
    saveObject={
        "game": game
    }
    game.active=False
    with open(savePath,'wb') as f:
        pickle.dump(saveObject, f)
    return True

def loadGame():
    global game, models, buildings
    #if exists
    if os.path.isfile(savePath):
        with open(savePath, 'rb') as f:
            saveObject = pickle.load(f)
        game = saveObject["game"]
        #matching versions?
        if game.version!=version["version"]:
            log("POSSIBLE ERROR: version of the file and game does not match")
        #update buildings' sprite
        for building in buildings:
            buildings[building].model.image=pygame.image.load(buildingsGenericTexturePath + building + "/" + str(game.lvlStates[building]) + ".png")
        return True
    else:
        return False
#class for each row in the internal market
class ItemInternalMarket:
    def __init__(self, item):
        global game
        self.item=item
        self.surf2=None
        self.line=f'{item}({values["internalMarket"][item]}$/{game.abbreviate[item]}): {game.internalMarketConfig[self.item]}{game.abbreviate[item]}/s -> {game.internalMarketConfig[self.item]*values["internalMarket"][item]}$/s'
        self.surf=font.render(self.line, True, "black")
        #+- buttons
        self.addSellingItemModel = button.Button(resolution[0]/2, resolution[1]/2, pygame.image.load(addTexturePath).convert_alpha(), 0.5)
        self.subtractSellingItemModel = button.Button(resolution[0]/2, resolution[1]/2, pygame.image.load(subtractTexturePath).convert_alpha(), 0.5)
    
    #+
    def addSellingItemPressed(self):
        global game
        game.internalMarketConfig[self.item]+=1

    #-
    def subtractSellingItemPressed(self):
        global game
        if game.internalMarketConfig[self.item]>0:
            game.internalMarketConfig[self.item]-=1
    
    #update surfs
    def updateRow(self):
        global game
        self.line=f'{self.item}({values["internalMarket"][self.item]}$/{game.abbreviate[self.item]}):'
        self.surf=font.render(self.line, True, "black")
        self.line2=f'{game.internalMarketConfig[self.item]}{game.abbreviate[self.item]}/s -> {round(game.internalMarketConfig[self.item]*values["internalMarket"][self.item], 7)}$/s'
        self.surf2=font.render(self.line2, True, "black")

#create 1 row per item
rowsInternalMarket=[]
for item in game.primaryMaterialsList:
    rowsInternalMarket.append(ItemInternalMarket(item))

#most of the models used in a class
class Models:
    def __init__(self):
        global game

        #surfs for the nums of the storage menu
        self.storageSurfs = {
            "money": fontSmall.render(str(round(game.storage["money"])), True, "black"),
            "wood": fontSmall.render(str(round(game.storage["wood"])), True, "black"),
            "food": fontSmall.render(str(round(game.storage["food"])), True, "black"),
            "stone": fontSmall.render(str(round(game.storage["stone"])), True, "black")
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
        self.upgradeModel = button.Button(resolution[0]/2-100, resolution[1]-100, pygame.image.load(upgradeTexturePath).convert_alpha(), 1)
        self.infoModel = button.Button(resolution[0]/2+20, resolution[1]-100, pygame.image.load(infoTexturePath).convert_alpha(), 1)
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

models=Models()

#class for each building
class Building:
    def __init__(self, model):
        self.model = model
    def onClick(self, name):
        global game, models
        #if is a new selection
        if game.selectedBuilding != name:
            #change internal and external selection name
            game.selectedBuilding = name

            #change surfaces and activateDownMenu()
            game.activateDownMenu()

        #if is a deselection do it reverse
        else:
            game.selectedBuilding = ""

            game.deactivateDownMenu()
            
#models to full object instances
buildings = {
    "TH": Building(models.thModel),
    "forest": Building(models.forestModel),
    "farm": Building(models.farmModel),
    "quarry": Building(models.quarryModel),
    "internalMarket": Building(models.internalMarketModel)
}

textMenuSurfs=[]

#check and display menu
def displayMenu():
    global game, models, textMenuSurfs
    #background
    pygame.draw.rect(screen, "white", pygame.Rect(resolution[0]/5, resolution[1]/5 - 20, (resolution[0]/5)*3, 430), border_radius=25)
    #different menus
    #upgrade menu
    if game.activeMenu=="upgrade":
        #set surfs
        if not game.notAffordableShown:
            textMenuSurfs=[]
            #prices
            for item in game.materialList:
                if item in values["prices"][game.selectedBuilding][game.lvlStates[game.selectedBuilding]+1]["price"]:
                    textMenuSurfs.append(font.render("You need " + str(values["prices"][game.selectedBuilding][game.lvlStates[game.selectedBuilding]+1]["price"][item])+" of "+ item, True, "black"))
            #increase in income unless TH or internal market
            if game.selectedBuilding!="TH" and game.selectedBuilding!="internalMarket":
                textMenuSurfs.append(font.render(f'Income: {values["stats"][game.selectedBuilding][game.lvlStates[game.selectedBuilding]]["income"]}{game.abbreviate[game.buildingToMaterial[game.selectedBuilding]]}/s/person -> {values["stats"][game.selectedBuilding][game.lvlStates[game.selectedBuilding]+1]["income"]}{game.abbreviate[game.buildingToMaterial[game.selectedBuilding]]}/s/person', True, "black"))
        
        #confirm or cancel
        if models.confirmUpgradeModel.draw(screen, mouseLDown):
            #affordable?
            if game.upgradeConfirmed():
                game.notAffordableShown=False
                buildings[game.selectedBuilding].model.image=pygame.image.load(buildingsGenericTexturePath + game.selectedBuilding + "/" + str(game.lvlStates[game.selectedBuilding]) + ".png")
                game.activeMenu=None
                game.displayCity=True
            else:
                game.notAffordableShown=True
                textMenuSurfs=[font.render("Not affordable", True, "black")]
        elif models.cancelUpgradeModel.draw(screen, mouseLDown):
            game.notAffordableShown=False
            game.activeMenu=None
            game.displayCity=True
    
    elif game.activeMenu=="downgrade":
        if not game.notAffordableShown:
            if game.lvlStates[game.selectedBuilding]>1:
                textMenuSurfs=[font.render(f"Do you want to downgrade {game.selectedBuilding} {game.lvlStates[game.selectedBuilding]} -> {game.lvlStates[game.selectedBuilding]-1}", True, "black")]
            else:
                textMenuSurfs=[font.render("You can't downgrade your building", True, "black")]
        #confirm or cancel
        if models.confirmUpgradeModel.draw(screen, mouseLDown):
            #can downgrade?
            if game.lvlStates[game.selectedBuilding]>1:
                game.lvlStates[game.selectedBuilding]-=1
                buildings[game.selectedBuilding].model.image=pygame.image.load(buildingsGenericTexturePath + game.selectedBuilding + "/" + str(game.lvlStates[game.selectedBuilding]) + ".png")
                game.notAffordableShown=False
                game.activeMenu=None
                game.displayCity=True
            else:
                game.notAffordableShown=True
                textMenuSurfs=[font.render("You can't downgrade your building", True, "black")]
        elif models.cancelUpgradeModel.draw(screen, mouseLDown):
            game.notAffordableShown=False
            game.activeMenu=None
            game.displayCity=True

    #first upgrade menu th
    elif game.activeMenu=="upgradeMeaningTH":
        #crate the texts for prices
        textMenuSurfs=[font.render(f'capacity: {values["stats"]["TH"][(game.lvlStates["TH"])]["populationCapacity"]} -> {values["stats"]["TH"][(game.lvlStates["TH"])+1]["populationCapacity"]} citizens costing each per sec: ', True, "black")]
        for item in game.materialList:
            if item in values["citizens"]["costSecond"][game.lvlStates["TH"]+1]:
                textMenuSurfs.append(font.render(str(values["citizens"]["costSecond"][game.lvlStates["TH"]+1][item])+" of "+ item, True, "black"))

        #confirm or cancel
        if models.confirmUpgradeModel.draw(screen, mouseLDown):
            game.activeMenu="upgrade"
        elif models.cancelUpgradeModel.draw(screen, mouseLDown):
            game.activeMenu=None
            game.displayCity=True
    #TH i
    elif game.activeMenu=="populationTH":
        if not game.notAffordableShown:
            textMenuSurfs=[]
            #cost
            line="The cost per citizen is "
            for item in game.materialList:
                if item in values["citizens"]["costSecond"][game.lvlStates["TH"]]:
                    line+=str(str(values["citizens"]["costSecond"][game.lvlStates["TH"]][item])+" " + game.abbreviate[item] + "/s ")
            textMenuSurfs.append(font.render(line, True, "black"))

            line="Each new citizen costs "
            for item in game.materialList:
                if item in values["citizens"]["costNew"]:
                    line+=str(str(values["citizens"]["costNew"][item])+" of " + item + " ")
            line+="NO REFUNDS"
            textMenuSurfs.append(font.render(line, True, "black"))

        #+
        if models.addCitizenModel.draw(screen, mouseLDown):
            if game.calculateAffordable(values["citizens"]["costNew"]):
                if game.population<values["stats"]["TH"][(game.lvlStates["TH"])]["populationCapacity"]:
                    game.payPrice(values["citizens"]["costNew"])
                    game.population+=1
                else:
                    textMenuSurfs=[font.render("Not enough capacity", True, "black")]
                    game.notAffordableShown = True
            else:
                textMenuSurfs=[font.render("Not affordable", True, "black")]
                game.notAffordableShown = True

        #-
        if models.subtractCitizenModel.draw(screen, mouseLDown):
            if game.population>1:
                #are they occupied?
                if game.occupiedPopulation<game.population:
                    game.population-=1
                else:
                    textMenuSurfs=[font.render("You have all the citizens occupied", True, "black")]
                    game.notAffordableShown = True
            else:
                textMenuSurfs=[font.render("You can't remove yourself", True, "black")]
                game.notAffordableShown = True

        if models.cancelCenterModel.draw(screen, mouseLDown):
            game.activeMenu=None
            game.displayCity=True
            game.notAffordableShown = False
    #building i
    elif game.activeMenu=="populationBuilding":
        #crate the texts for prices
        if not game.notAffordableShown:
            textMenuSurfs=[]
            line=f'Each citizen produces {str(values["stats"][game.selectedBuilding][game.lvlStates[game.selectedBuilding]]["income"])}/s REFUNDABLE'
            textMenuSurfs.append(font.render(line, True, "black"))
            line=f'This building have {str(game.populationOccupation[game.selectedBuilding])} citizens'
            textMenuSurfs.append(font.render(line, True, "black"))
            line=f'Capacity: {str(values["stats"][game.selectedBuilding][game.lvlStates[game.selectedBuilding]]["populationCapacity"])} citizens'
            textMenuSurfs.append(font.render(line, True, "black"))

        if models.addCitizenModel.draw(screen, mouseLDown):
            #free population?
            if game.population>game.occupiedPopulation:
                #capacity
                if values["stats"][game.selectedBuilding][game.lvlStates[game.selectedBuilding]]["populationCapacity"]>game.populationOccupation[game.selectedBuilding]:
                    game.occupiedPopulation+=1
                    game.populationOccupation[game.selectedBuilding]+=1
                else:
                    game.notAffordableShown = True
                    textMenuSurfs=[]
                    line='Not enough capacity'
                    textMenuSurfs.append(font.render(line, True, "black"))
            else:
                game.notAffordableShown = True
                textMenuSurfs=[]
                line='Not affordable'
                textMenuSurfs.append(font.render(line, True, "black"))

        if models.subtractCitizenModel.draw(screen, mouseLDown):
            if game.populationOccupation[game.selectedBuilding]>0:
                game.populationOccupation[game.selectedBuilding]-=1
                game.occupiedPopulation-=1

        if models.cancelCenterModel.draw(screen, mouseLDown):
            game.activeMenu=None
            game.displayCity=True
            game.notAffordableShown = False
    #info
    elif game.activeMenu=="info":
        textMenuSurfs=[]
        #load text
        for text in texts["infoMenusTexts"][game.selectedBuilding]:
            textMenuSurfs.append(font.render(text, True, "black"))

        if models.cancelCenterModel.draw(screen, mouseLDown):
            game.activeMenu=None
            game.displayCity=True
    #internal market
    elif game.activeMenu=="internalMarket":
        #say price
        text="You will be charged for adding items"
        for item in game.materialList:
            if item in values["internalMarket"]["add"]:
                text+=f' {values["internalMarket"]["add"][item]} {game.abbreviate[item]}'
        surf=fontSmall.render(text, True, "black")
        screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, resolution[1]/4*3 - surf.get_height() // 2))

        if game.notAffordableShown:
            surf=font.render("Not affordable", True, "black")
            screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, resolution[1]/2 - surf.get_height() // 2))

        textMenuSurfs=[]
        textMenuSurfs2=[]
        
        #rows of items
        y=0
        for row in rowsInternalMarket:
            row.updateRow()
            #1st part of text
            textMenuSurfs.append(row.surf)
            #2nd part of text
            textMenuSurfs2.append(row.surf2)
            row.addSellingItemModel.rect.topleft=(resolution[0]/2 + 300, resolution[1]/5 + 10 + y - row.surf.get_height() // 2)
            row.subtractSellingItemModel.rect.topleft=(resolution[0]/2 + 250, resolution[1]/5 + 10 + y - row.surf.get_height() // 2)
            
            if row.addSellingItemModel.draw(screen, mouseLDown):
                if game.calculateAffordable(values["internalMarket"]["add"]):
                    game.payPrice(values["internalMarket"]["add"])
                    row.addSellingItemPressed()
                else:
                    game.notAffordableShown=True
            if row.subtractSellingItemModel.draw(screen, mouseLDown):
                row.subtractSellingItemPressed()
            y+=50

        if models.cancelCenterModel.draw(screen, mouseLDown):
            game.notAffordableShown=False
            game.activeMenu=None
            game.displayCity=True
        
        offset=50
        i=0
        for surf in textMenuSurfs:
            screen.blit(surf,(resolution[0]/5+10, resolution[1]/5 + 10 + i - surf.get_height() // 2))
            i+=offset
        offset=50
        i=0
        for surf in textMenuSurfs2:
            screen.blit(surf,(resolution[0]/2 +50 - surf.get_width() // 2, resolution[1]/5 + 10 + i - surf.get_height() // 2))
            i+=offset

        return ""
    #ERROR notification
    else:
        #crate the texts for prices
        textMenuSurfs=[font.render("ERROR: MENU OPENED WITH INVALID game.activeMenu", True, "black")]
        log("ERROR: MENU OPENED WITH INVALID game.activeMenu")

        #confirm or cancel
        if models.cancelCenterModel.draw(screen, mouseLDown):
            game.activeMenu=None
            game.displayCity=True

    #display texts
    offset=35
    i=0
    for surf in textMenuSurfs:
        screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, resolution[1]/5 + 10 + i - surf.get_height() // 2))
        i+=offset

#adjust initial menu config
if not initialMenu: 
    game.active=True
    if config["loadSaveOnStart"]:
        loadGame()

#___________________________________Main loop _____________________________________________________________________________________________________________________________________
while running:
    #mouse press calc
    mouseLPressed=pygame.mouse.get_pressed()[0] == 1
    if mouseLPressed!=prevMouseLPressed:
        if mouseLPressed:
            mouseLDown=True
        else:
            mouseLDown=False
        prevMouseLPressed=mouseLPressed
    else:
        mouseLDown=False
    
    #events
    for event in pygame.event.get():
        #X
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            #ESC
            if event.key == pygame.K_ESCAPE:
                if not initialMenu:
                    if game.activeMenu==None:
                        models.saveSurf=font.render("", True, "black")
                        game.active=not game.active
                    else:
                        game.activeMenu=None
                        game.displayCity=True
            #F1
            if event.key == pygame.K_F1:
                game.updating=not game.updating

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("gray")

    #____________________________________________________________
    if game.active:
        #update storage
        if game.updating: game.calculateGains(dT)
        #buildings
        if game.displayCity:
            #draw buildings and check clicks
            if buildings["TH"].model.draw(screen, mouseLDown):
                buildings["TH"].onClick("TH")
            if buildings["forest"].model.draw(screen, mouseLDown):
                buildings["forest"].onClick("forest")
            if buildings["farm"].model.draw(screen, mouseLDown):
                buildings["farm"].onClick("farm")
            if buildings["quarry"].model.draw(screen, mouseLDown):
                buildings["quarry"].onClick("quarry")
            if buildings["internalMarket"].model.draw(screen, mouseLDown):
                buildings["internalMarket"].onClick("internalMarket")
        else: displayMenu()
        #downmenu
        if game.displayDownMenu:
            
            #lvl and name
            surf=font.render(f"{game.selectedBuilding} (lvl {game.lvlStates[game.selectedBuilding]})", True, "black")
            screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, resolution[1] - 140 - surf.get_height() // 2))

            #is info pressed?
            if models.infoModel.draw(screen, mouseLDown):
                if game.activeMenu=="info":
                    game.activeMenu=None
                    game.displayCity=True
                else:
                    game.displayCity=False
                    game.activeMenu="info"

            #is upgrade pressed?
            if models.upgradeModel.draw(screen, mouseLDown):
                if game.activeMenu=="upgrade" or game.activeMenu=="upgradeMeaningTH":
                    game.activeMenu=None
                    game.displayCity=True
                else:
                    if game.selectedBuilding=="TH":
                        game.activeMenu="upgradeMeaningTH"
                    else:
                        game.activeMenu="upgrade"
                    game.displayCity=False

            #population
            if game.selectedBuilding!="internalMarket":
                if models.populationModel.draw(screen, mouseLDown):
                    #TH
                    if game.selectedBuilding=="TH":
                        if game.activeMenu=="populationTH":
                            game.activeMenu=None
                            game.displayCity=True
                        else:
                            game.displayCity=False
                            game.activeMenu="populationTH"
                    #generator
                    else:
                        if game.activeMenu=="populationBuilding":
                            game.activeMenu=None
                            game.displayCity=True
                        else:
                            game.displayCity=False
                            game.activeMenu="populationBuilding"
            #enter building
            if game.selectedBuilding=="internalMarket":
                if game.lvlStates["internalMarket"]>0:
                    if models.enterBuildingModel.draw(screen, mouseLDown):
                        if game.activeMenu=="internalMarket":
                            game.activeMenu=None
                            game.displayCity=True
                        else:
                            game.activeMenu="internalMarket"
                            game.displayCity=False
            #downgrade
            if game.selectedBuilding=="TH" and game.lvlStates["TH"]>1:
                if models.downgradeModel.draw(screen, mouseLDown):
                    if game.activeMenu=="downgrade":
                        game.activeMenu=None
                        game.displayCity=True
                    else:
                        game.activeMenu="downgrade"
                        game.displayCity=False

        #storage side menu
        if game.displayStorageMenu:
            #background
            pygame.draw.rect(screen, "white", pygame.Rect(10, 10, 180, 350), border_radius=5)
            #images
            models.moneyModel.draw(screen, mouseLDown)
            models.woodModel.draw(screen, mouseLDown)
            models.foodModel.draw(screen, mouseLDown)
            models.stoneModel.draw(screen, mouseLDown)

            #display values
            i=6
            for item in game.materialList:
                models.storageSurfs[item]=[]
                models.storageSurfs[item].append(fontSmall.render(reNumberer(game.storage[item])+game.abbreviate[item], True, "black"))
                models.storageSurfs[item].append(fontSmall.render("Δ" +reNumberer(game.realGains[item])+game.abbreviate[item]+"/s", True, "black"))
                y=0
                for surf in models.storageSurfs[item]:
                    screen.blit(surf,(80,20+i+y))
                    y+=20
                i+=80
            '''1.236E02
            i=6
            for item in game.materialList:
                models.storageSurfs[item]=[]
                models.storageSurfs[item].append(fontSmall.render(('%.3E' % Decimal(game.storage[item])).replace('+', '')+" "+game.abbreviate[item], True, "black"))
                models.storageSurfs[item].append(fontSmall.render("Δ" + ('%.1E' % Decimal(game.realGains[item])).replace('+', '') +" "+ game.abbreviate[item]+"/s", True, "black"))
                y=0
                for surf in models.storageSurfs[item]:
                    screen.blit(surf,(80,20+i+y))
                    y+=20
                i+=80
            '''
        
        #population
        if game.displayPopulationMenu:
            #background
            pygame.draw.rect(screen, "white", pygame.Rect(resolution[0]/2-200, 10, 400, 80), border_radius=5)

            #population
            textMenuSurfsPopulationMenu=[]
            textMenuSurfsPopulationMenu.append(fontSmall.render(str(game.population) + f" Citizens ({game.occupiedPopulation} occupied)", True, "black"))
            
            #costSecond
            line="Cost:"
            for item in game.materialList:
                if item in values["citizens"]["costSecond"][game.lvlStates["TH"]]:
                    line+=reNumberer(values["citizens"]["costSecond"][game.lvlStates["TH"]][item]*(game.population-1))+game.abbreviate[item] + "/s"
            textMenuSurfsPopulationMenu.append(fontSmall.render(line, True, "black"))
            
            #display
            i=0
            for surf in textMenuSurfsPopulationMenu:
                screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, 30+i - surf.get_height() // 2))
                i+=35

        #semipause
        if not game.updating:
            surf=fontSmall.render("SEMIPAUSE (F1) if doesn't work your citizens cant survive, solve it (check Δ to be +)", True, "black",)
            screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, -120 + resolution[1] - surf.get_height() // 2))
            #update delta
            for item in game.materialList:
                game.realGains[item]=game.calcDelta(item)
        
        #FPS
        if showFPS:
            surf=fontSmall.render(f'{round(clock.get_fps())} FPS', True, "black")
            screen.blit(surf,(resolution[0] - 3 - surf.get_width(), resolution[1] - surf.get_height()))
        
        ####################################################################

    #initial menu
    elif initialMenu:
        #title
        surf=giantFont.render("Afers Exteriors Capitalitzats", True, "black")
        screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, 50 - surf.get_height() // 2))

        #info ESC
        surf=fontSmall.render("Press ESC in the game to save game", True, "black")
        screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, 190 - surf.get_height() // 2))

        #resume
        if models.resumeModel.draw(screen, mouseLDown):
            if loadGame():
                models.saveSurf=font.render("Game loaded successfully", True, "black")
                initialMenu=False
                game.active=True
            else:
                models.saveSurf=font.render("ERROR on loading, do you have a file?", True, "black")

        #alerts
        screen.blit(models.saveSurf,(resolution[0]/2 - models.saveSurf.get_width() // 2, resolution[1]/2 - models.saveSurf.get_height() // 2))

        #new game
        if models.newSaveModel.draw(screen, mouseLDown):
            initialMenu=False
            game.active=True

        #game version
        surf=fontSmall.render(version["version"], True, "black")
        screen.blit(surf,(resolution[0] - 3 - surf.get_width(), resolution[1] - surf.get_height()))

    #pausemenu
    else:
        #Pause title
        surf=giantFont.render("PAUSE", True, "black")
        screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, 50 - surf.get_height() // 2))
        
        #save
        if models.saveModel.draw(screen, mouseLDown):
            if saveGame():
                models.saveSurf=font.render("Game saved successfully", True, "black")
            else:
                models.saveSurf=font.render("ERROR saving unsuccessful", True, "black")
        #load
        if models.loadModel.draw(screen, mouseLDown):
            if loadGame():
                models.saveSurf=font.render("Game loaded successfully", True, "black")
            else:
                models.saveSurf=font.render("ERROR on loading, do you have a file?", True, "black")
        
        #alerts
        screen.blit(models.saveSurf,(resolution[0]/2 - models.saveSurf.get_width() // 2, resolution[1]/2 - models.saveSurf.get_height() // 2))

        #Version text
        surf=fontSmall.render(version["version"], True, "black")
        screen.blit(surf,(resolution[0] - 3 - surf.get_width(), resolution[1] - surf.get_height()))

        #Exit menu text
        surf=fontSmall.render("ESC to close menu", True, "black")
        screen.blit(surf,(0, resolution[1] - surf.get_height()))

    # flip() the display to put your work on screen
    pygame.display.flip()

    #dT + limit fps
    dT = clock.tick(maxFPS)/1000  # limits FPS to 60
    #print(f"FPS: {round(clock.get_fps(), 1)}")
    
pygame.quit()