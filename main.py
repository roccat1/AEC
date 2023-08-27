#Afers Exteriors Capitalitzats

#Llibreries
import pygame, json, time

#arxius
from paths import *
import button
import gameClass

#import values
with open(valuesJsonPath, "r") as f:
    values= json.load(f)
with open(versionJsonPath, "r") as f:
    version= json.load(f)

# pygame setup
pygame.init()
resolution=[1280,720]
screen = pygame.display.set_mode((resolution[0], resolution[1]))
clock = pygame.time.Clock()
pygame.display.set_caption('Afers Exteriors Capitalitzats (AEC)')
pygame_icon = pygame.image.load(iconTexturePath)
pygame.display.set_icon(pygame_icon)
running = True
giantFont = pygame.font.SysFont("Arial", 100)
font = pygame.font.SysFont("Arial", 36)
fontSmall = pygame.font.SysFont("Arial", 26)
dT=0

game = gameClass.Game()

#create surfaces
buildingNameSurf = font.render(game.whatIsSelected, True, "white")
infoLvlSurf = font.render("", True, "white")

populationSurf = fontSmall.render(str(game.population), True, "black")
warningSurf = giantFont.render("Warning", True, "red")

storageSurfs = {
    "money": fontSmall.render(str(round(game.storage["money"])), True, "black"),
    "wood": fontSmall.render(str(round(game.storage["wood"])), True, "black"),
    "food": fontSmall.render(str(round(game.storage["food"])), True, "black"),
    "stone": fontSmall.render(str(round(game.storage["stone"])), True, "black")
}

textMenuSurfs = []

#Creacio de models
#buildings
thModel = button.Button(resolution[0]/2-40, resolution[1]/2-40, pygame.image.load(thGenericTexturePath + str(values["initialValues"]["lvls"]["TH"]) + ".png").convert_alpha(), 1)
forestModel = button.Button(resolution[0]/2-140, resolution[1]/2-40, pygame.image.load(forestGenericTexturePath + str(values["initialValues"]["lvls"]["forest"]) + ".png").convert_alpha(), 1)
farmModel = button.Button(resolution[0]/2-40, resolution[1]/2-140, pygame.image.load(farmGenericTexturePath + str(values["initialValues"]["lvls"]["farm"]) + ".png").convert_alpha(), 1)
quarryModel = button.Button(resolution[0]/2+60, resolution[1]/2-40, pygame.image.load(quarryGenericTexturePath + str(values["initialValues"]["lvls"]["quarry"]) + ".png").convert_alpha(), 1)

#buttons
infoModel = button.Button(resolution[0]/2+40, resolution[1]-100, pygame.image.load(infoTexturePath).convert_alpha(), 1)
upgradeModel = button.Button(resolution[0]/2-120, resolution[1]-100, pygame.image.load(upgradeTexturePath).convert_alpha(), 1)
#=
confirmUpgradeModel = button.Button(resolution[0]/2+80, resolution[1]/2+80, pygame.image.load(acceptTexturePath).convert_alpha(), 1)
cancelUpgradeModel = button.Button(resolution[0]/2-160, resolution[1]/2+80, pygame.image.load(cancelTexturePath).convert_alpha(), 1)
cancelCenterInfoModel = button.Button(resolution[0]/2-40, resolution[1]/2+80, pygame.image.load(cancelTexturePath).convert_alpha(), 1)

addCitizenModel = button.Button(resolution[0]/2+80, resolution[1]/2-20, pygame.image.load(addTexturePath).convert_alpha(), 1)
subtractCitizenModel = button.Button(resolution[0]/2-160, resolution[1]/2-20, pygame.image.load(subtractTexturePath).convert_alpha(), 1)


#images storage
moneyModel = button.Button(20, 20, pygame.image.load(moneyTexturePath).convert_alpha(), 0.7)
woodModel = button.Button(20, 110, pygame.image.load(woodTexturePath).convert_alpha(), 0.7)
foodModel = button.Button(20, 200, pygame.image.load(foodTexturePath).convert_alpha(), 0.7)
stoneModel = button.Button(20, 290, pygame.image.load(stoneTexturePath).convert_alpha(), 0.7)

class Building:
    def __init__(self, model):
        self.model = model
    def onClick(self, name):
        global game, buildingNameSurf, infoLvlSurf
        #if is a new selection
        if game.whatIsSelected != name:
            #change internal and external selection name
            game.whatIsSelected = name

            #change surfaces and activateDownMenu()
            buildingNameSurf = font.render(game.activateDownMenu(), True, "white")
            updateInfoLvlLabel()

        #if is a deselection do it reverse
        else:
            game.whatIsSelected = ""

            buildingNameSurf = font.render(game.deactivateDownMenu(), True, "white")
            infoLvlSurf = font.render("", True, "white")
            
#models to full object instances
buildings = {
    "TH": Building(thModel),
    "forest": Building(forestModel),
    "farm": Building(farmModel),
    "quarry": Building(quarryModel)
}

def updateInfoLvlLabel():
    global infoLvlSurf, game

    infoLvlSurf = font.render(str(game.lvlStates[game.whatIsSelected]), True, "white")

#Main loop
while running:
    #events
    for event in pygame.event.get():
        #X
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.active=not game.active
            if event.key == pygame.K_F1:
                game.updating=not game.updating

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    if game.active:

        ####################################################################
        #update storage
        if game.updating:
            game.calculateGains(dT)
            '''
            returnChain = game.calculateGains(dT)

            for i in returnChain:
                if i == "lostPopulation":
                    initialTimeLostPopulation = time.time()
                    game.displayWarning = True
                    warningSurf = giantFont.render("Citizens RAN AWAY", True, "red", "black")

                    '''

        #buildings
        if game.displayCity:
            #draw buildings and check clicks
            if buildings["TH"].model.draw(screen):
                buildings["TH"].onClick("TH")
            if buildings["forest"].model.draw(screen):
                buildings["forest"].onClick("forest")
            if buildings["farm"].model.draw(screen):
                buildings["farm"].onClick("farm")
            if buildings["quarry"].model.draw(screen):
                buildings["quarry"].onClick("quarry")
        else:
            #upgrade menu
            if game.displayUpgradeMenu:
                textMenuSurfs=[]
                for item in game.materialList:
                    if item in values["prices"][game.whatIsSelected][game.lvlStates[game.whatIsSelected]+1]["price"]:
                        textMenuSurfs.append(font.render("You need " + str(values["prices"][game.whatIsSelected][game.lvlStates[game.whatIsSelected]+1]["price"][item])+" of "+ item, True, "black"))
                #background
                pygame.draw.rect(screen, "white", pygame.Rect(resolution[0]/4, resolution[1]/4, (resolution[0]/4)*2, (resolution[1]/4)*2), border_radius=50)
                #display texts
                i=0
                for surf in textMenuSurfs:
                    screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, resolution[1]/2 - 120 + i - surf.get_height() // 2))
                    i+=35

                #confirm or cancel
                if confirmUpgradeModel.draw(screen):
                    #affordable?
                    if game.upgradeConfirmed():
                        buildings[game.whatIsSelected].model.image=pygame.image.load(buildingsGenericTexturePath + game.whatIsSelected + "/" + str(game.lvlStates[game.whatIsSelected]) + ".png")
                        game.deactivateDownMenu()
                        game.displayUpgradeMenu=False
                        game.whatIsSelected = ""
                        game.displayCity=True
                    else:
                        textMenuSurfs=[font.render("Not affordable", True, "black")]
                elif cancelUpgradeModel.draw(screen):
                    game.displayUpgradeMenu=False
                    game.displayCity=True

            #first upgrade menu th
            if game.displayUpgradeMeaningTHMenu:
                #crate the texts for prices
                textMenuSurfs=[font.render(f'capacity: {values["stats"]["TH"][(game.lvlStates["TH"])]["populationCapacity"]} -> {values["stats"]["TH"][(game.lvlStates["TH"])+1]["populationCapacity"]} citizens costing each per sec: ', True, "black")]
                for item in game.materialList:
                    if item in values["citizens"]["costSecond"][game.lvlStates["TH"]+1]:
                        textMenuSurfs.append(font.render(str(values["citizens"]["costSecond"][game.lvlStates["TH"]+1][item])+" of "+ item, True, "black"))

                #background
                pygame.draw.rect(screen, "white", pygame.Rect(resolution[0]/4, resolution[1]/4, (resolution[0]/4)*2, (resolution[1]/4)*2), border_radius=50)
                #display texts
                i=0
                for surf in textMenuSurfs:
                    screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, resolution[1]/2 - 120 + i - surf.get_height() // 2))
                    i+=35

                #confirm or cancel
                if confirmUpgradeModel.draw(screen):
                    game.displayUpgradeMeaningTHMenu = False
                    game.displayUpgradeMenu = True
                elif cancelUpgradeModel.draw(screen):
                    game.displayUpgradeMeaningTHMenu=False
                    game.displayCity=True

            #TH i
            if game.displayTHInfoMenu:
                #cost
                if not game.notAffordableShown:
                    textMenuSurfs=[]
                    line="The cost per citizen is "
                    for item in game.materialList:
                        if item in values["citizens"]["costSecond"]:
                            line+=str(str(values["citizens"]["costSecond"][item])+" " + item + "/s ")
                    textMenuSurfs.append(font.render(line, True, "black"))

                    line="Each new citizen costs "
                    for item in game.materialList:
                        if item in values["citizens"]["costNew"]:
                            line+=str(str(values["citizens"]["costNew"][item])+" of " + item + " ")
                    line+="NO REFUNDS"
                    textMenuSurfs.append(font.render(line, True, "black"))

                #background
                pygame.draw.rect(screen, "white", pygame.Rect(resolution[0]/5, resolution[1]/4, (resolution[0]/5)*3, (resolution[1]/4)*2), border_radius=50)

                #+
                if addCitizenModel.draw(screen):
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
                if subtractCitizenModel.draw(screen):
                    if game.population>1:
                        if game.occupiedPopulation<game.population:
                            game.population-=1
                        else:
                            textMenuSurfs=[font.render("You have all the citizens occupied", True, "black")]
                            game.notAffordableShown = True
                    else:
                        textMenuSurfs=[font.render("You can't remove yourself", True, "black")]
                        game.notAffordableShown = True

                if cancelCenterInfoModel.draw(screen):
                    game.displayTHInfoMenu=False
                    game.displayCity=True
                    game.notAffordableShown = False
                
                #display texts
                i=0
                for surf in textMenuSurfs:
                    screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, resolution[1]/2 - 120 + i - surf.get_height() // 2))
                    i+=35

            #building i
            if game.displayBuildingInfoMenu:
                #crate the texts for prices
                if not game.notAffordableShown:
                    textMenuSurfs=[]
                    line=f'Each citizen produces {str(values["stats"][game.whatIsSelected][game.lvlStates[game.whatIsSelected]]["income"])}/s REFUNDABLE'
                    textMenuSurfs.append(font.render(line, True, "black"))
                    line=f'This building have {str(game.populationOccupation[game.whatIsSelected])} citizens'
                    textMenuSurfs.append(font.render(line, True, "black"))
                    line=f'Capacity: {str(values["stats"][game.whatIsSelected][game.lvlStates[game.whatIsSelected]]["populationCapacity"])} citizens'
                    textMenuSurfs.append(font.render(line, True, "black"))

                #background
                pygame.draw.rect(screen, "white", pygame.Rect(resolution[0]/5, resolution[1]/4, (resolution[0]/5)*3, (resolution[1]/4)*2), border_radius=50)

                if addCitizenModel.draw(screen):
                    if game.population>game.occupiedPopulation:
                        if values["stats"][game.whatIsSelected][game.lvlStates[game.whatIsSelected]]["populationCapacity"]>game.populationOccupation[game.whatIsSelected]:
                            game.occupiedPopulation+=1
                            game.populationOccupation[game.whatIsSelected]+=1
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

                if subtractCitizenModel.draw(screen):
                    if game.populationOccupation[game.whatIsSelected]>0:
                        game.populationOccupation[game.whatIsSelected]-=1
                        game.occupiedPopulation-=1

                if cancelCenterInfoModel.draw(screen):
                    game.displayBuildingInfoMenu=False
                    game.displayCity=True
                    game.notAffordableShown = False
                
                #display texts
                i=0
                for surf in textMenuSurfs:
                    screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, resolution[1]/2 - 120 + i - surf.get_height() // 2))
                    i+=35

        #downmenu
        if game.displayDownMenu:
            #lvl and name
            screen.blit(infoLvlSurf,(resolution[0]/2 - 80 - infoLvlSurf.get_width() // 2, resolution[1] - 120 - infoLvlSurf.get_height() // 2))
            screen.blit(buildingNameSurf,(resolution[0]/2 - buildingNameSurf.get_width() // 2, resolution[1] - 140 - buildingNameSurf.get_height() // 2))
            #is info pressed?
            if infoModel.draw(screen):
                game.infoPressed()
            #is upgrade pressed?
            if upgradeModel.draw(screen):
                game.upgradePressed()

        #storage side menu
        if game.displayStorageMenu:
            #background
            pygame.draw.rect(screen, "white", pygame.Rect(10, 10, 200, 400), border_radius=5)
            #images
            moneyModel.draw(screen)
            woodModel.draw(screen)
            foodModel.draw(screen)
            stoneModel.draw(screen)

            #display values
            i=0
            for item in game.materialList:
                storageSurfs[item] = fontSmall.render(str(round(game.storage[item])) + " Δ " + str(game.realGains[item]) + "/s", True, "black")
                screen.blit(storageSurfs[item],(80,30+i))
                i+=90
        
        #population
        if game.displayPopulationMenu:
            #background
            pygame.draw.rect(screen, "white", pygame.Rect(resolution[0]/2-150, 10, 300, 120), border_radius=5)

            #population
            textMenuSurfsPopulationMenu=[]
            textMenuSurfsPopulationMenu.append(fontSmall.render(str(game.population) + " Citizens", True, "black"))
            
            #costSecond
            line="Cost: "
            for item in game.materialList:
                if item in values["citizens"]["costSecond"][game.lvlStates["TH"]]:
                    line+=str(str(values["citizens"]["costSecond"][game.lvlStates["TH"]][item]*(game.population-1)) + " " + item + "/s ")
            textMenuSurfsPopulationMenu.append(fontSmall.render(line, True, "black"))

            #occupied citizens
            line=f"You have {game.occupiedPopulation} occupied citizens"
            textMenuSurfsPopulationMenu.append(fontSmall.render(line, True, "black"))
            
            #display
            i=0
            for surf in textMenuSurfsPopulationMenu:
                screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, 30+i - surf.get_height() // 2))
                i+=35

        if not game.updating:
            surf=font.render("SEMIPAUSE (F1) if doesn't work your citizens cant survive, solve it (check Δ to be +)", True, "black")
            screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, 200 - surf.get_height() // 2))

        ####################################################################
    
    #pausemenu
    else:
        surf=giantFont.render("PAUSE", True, "black")
        screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, resolution[1]/2 - surf.get_height() // 2))
        surf=fontSmall.render(version["version"], True, "black")
        screen.blit(surf,(resolution[0] - 3 - surf.get_width(), resolution[1] - surf.get_height()))

    # flip() the display to put your work on screen
    pygame.display.flip()

    #dT + limit fps
    dT = clock.tick(30)/1000  # limits FPS to 60
    #print(f"FPS: {round(clock.get_fps(), 1)}")

pygame.quit()
