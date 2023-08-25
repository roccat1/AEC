#Afers Exteriors Capitalitzats

#Llibreries
import pygame, json, time

#arxius
from paths import *
import button
import gameClass

#import values
with open("values.json", "r") as f:
    values= json.load(f)

# pygame setup
pygame.init()
resolution=[1280,720]
screen = pygame.display.set_mode((resolution[0], resolution[1]))
clock = pygame.time.Clock()
pygame.display.set_caption('Afers Exteriors Capitalitzats (AEC)')
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
thModel = button.Button(resolution[0]/2-40, resolution[1]/2-40, pygame.image.load(thTexturePath).convert_alpha(), 1)
forestModel = button.Button(resolution[0]/2-140, resolution[1]/2-40, pygame.image.load(forestTexturePath).convert_alpha(), 1)
farmModel = button.Button(resolution[0]/2-40, resolution[1]/2-140, pygame.image.load(farmTexturePath).convert_alpha(), 1)
quarryModel = button.Button(resolution[0]/2+60, resolution[1]/2-40, pygame.image.load(quarryTexturePath).convert_alpha(), 1)

#buttons
infoModel = button.Button(resolution[0]/2+40, resolution[1]-100, pygame.image.load(infoTexturePath).convert_alpha(), 1)
upgradeModel = button.Button(resolution[0]/2-120, resolution[1]-100, pygame.image.load(upgradeTexturePath).convert_alpha(), 1)
#=
confirmUpgradeModel = button.Button(resolution[0]/2+80, resolution[1]/2+80, pygame.image.load(acceptTexturePath).convert_alpha(), 1)
cancelUpgradeModel = button.Button(resolution[0]/2-160, resolution[1]/2+80, pygame.image.load(cancelTexturePath).convert_alpha(), 1)
cancelTHInfoModel = button.Button(resolution[0]/2-40, resolution[1]/2+80, pygame.image.load(cancelTexturePath).convert_alpha(), 1)

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
th = Building(thModel)
forest = Building(forestModel)
farm = Building(farmModel)
quarry = Building(quarryModel)

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

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    ####################################################################
    #update storage
    returnChain = game.calculateGains(dT)

    for i in returnChain:
        if i == "lostPopulation":
            initialTimeLostPopulation = time.time()
            game.displayWarning = True
            warningSurf = giantFont.render("Citizens RAN AWAY", True, "red", "black")


    if game.displayCity:
        #draw buildings and check clicks
        if th.model.draw(screen):
            th.onClick("TH")
        if forest.model.draw(screen):
            forest.onClick("forest")
        if farm.model.draw(screen):
            farm.onClick("farm")
        if quarry.model.draw(screen):
            quarry.onClick("quarry")

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
    
    #if upgrade menu has toggled to true
    if game.displayUpgradeMenu and not game.prevDisplayUpgradeMenu:
        #crate the texts for prices
        textMenuSurfs=[]
        for item in game.materialList:
            if item in values["prices"][game.whatIsSelected][game.lvlStates[game.whatIsSelected]+1]["price"]:
                textMenuSurfs.append(font.render("You need " + str(values["prices"][game.whatIsSelected][game.lvlStates[game.whatIsSelected]+1]["price"][item])+" of "+ item, True, "black"))

    #upgrade menu
    if game.displayUpgradeMenu:
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
                game.deactivateDownMenu()
                game.displayUpgradeMenu=False
                game.whatIsSelected = ""
                game.displayCity=True
            else:
                textMenuSurfs=[font.render("Not affordable", True, "black")]
        elif cancelUpgradeModel.draw(screen):
            game.displayUpgradeMenu=False
            game.displayCity=True
    
    game.prevDisplayUpgradeMenu = game.displayUpgradeMenu

    #storage side menu
    if game.displayStorageMenu:
        #background
        pygame.draw.rect(screen, "white", pygame.Rect(10, 10, 170, 350), border_radius=5)
        #images
        moneyModel.draw(screen)
        woodModel.draw(screen)
        foodModel.draw(screen)
        stoneModel.draw(screen)

        #display values
        i=0
        for item in game.materialList:
            if item in game.materialToBuilding:
                storageSurfs[item] = fontSmall.render(str(round(game.storage[item])) + " - " + str(values["incomes"][game.materialToBuilding[item]][game.lvlStates[game.materialToBuilding[item]]]["income"]) + "/s", True, "black")
            else:
                storageSurfs[item] = fontSmall.render(str(round(game.storage[item])), True, "black")
            screen.blit(storageSurfs[item],(80,30+i))
            i+=90
    
    if game.displayPopulationMenu:
        pygame.draw.rect(screen, "white", pygame.Rect(resolution[0]/2-100, 10, 200, 120), border_radius=5)

        textMenuSurfsPopulationMenu=[]
        textMenuSurfsPopulationMenu.append(fontSmall.render(str(game.population) + " Citizens", True, "black"))
        
        line="Cost: "
        for item in game.materialList:
            if item in values["citizens"]["costSecond"]:
                line+=str(str(values["citizens"]["costSecond"][item]*game.population) + " " + item + "/s ")
        textMenuSurfsPopulationMenu.append(fontSmall.render(line, True, "black"))

        line="Income: "
        for item in game.materialList:
            if item in values["citizens"]["income"]:
                line+=str(str(values["citizens"]["income"][item]*game.population) + " " + item + "/s ")
        textMenuSurfsPopulationMenu.append(fontSmall.render(line, True, "black"))
        
        i=0
        for surf in textMenuSurfsPopulationMenu:
            screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, 30+i - surf.get_height() // 2))
            i+=35

    if game.displayTHInfoMenu:
        #crate the texts for prices
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

        if addCitizenModel.draw(screen):
            if game.calculateAffordable(values["citizens"]["costNew"]):
                game.payPrice(values["citizens"]["costNew"])
                game.population+=1
            else:
                textMenuSurfs=[font.render("Not affordable", True, "black")]
                game.notAffordableShown = True

            
        if subtractCitizenModel.draw(screen):
            if game.population>0:
                game.population-=1

        if cancelTHInfoModel.draw(screen):
            game.displayTHInfoMenu=False
            game.displayCity=True
            game.notAffordableShown = False
            print("AAAa")
        
        #display texts
        i=0
        for surf in textMenuSurfs:
            screen.blit(surf,(resolution[0]/2 - surf.get_width() // 2, resolution[1]/2 - 120 + i - surf.get_height() // 2))
            i+=35

    if game.displayWarning:
        if time.time() - initialTimeLostPopulation < 2:
            screen.blit(warningSurf,(resolution[0]/2 - warningSurf.get_width() // 2, resolution[1]/2 - warningSurf.get_height() // 2))
        else:
            game.displayWarning=False

    ####################################################################

    # flip() the display to put your work on screen
    pygame.display.flip()

    #dT + limit fps
    dT = clock.tick(30)/1000  # limits FPS to 60
    #print(f"FPS: {round(clock.get_fps(), 1)}")

pygame.quit()
