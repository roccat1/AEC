from paths import *
import json

with open(valuesJsonPath, "r") as f:
    values= json.load(f)

class Game:
    def __init__(self):
        global values

        self.active=True
        self.updating=True

        #default gameState variables
        self.displayDownMenu=False
        self.displayStorageMenu = True
        self.displayPopulationMenu = True
        self.displayCity = True
        self.displayWarning = False
        '''
        populationTH
        populationInfo
        upgradeMeaningTH
        upgrade
        info
        downgrade
        internalMarket
        '''
        self.activeMenu=None

        '''
        TH
        farm
        quarry
        forest
        internalMarket
        '''
        self.selectedBuilding = ""

        self.notAffordableShown=False

        #initial values
        self.materialList = ["money", "wood", "food", "stone"]
        self.primaryMaterialsList = ["wood", "food", "stone"]
        self.materialToBuilding={
            "wood": "forest",
            "food": "farm",
            "stone": "quarry"
        }
        self.buildingToMaterial={
            "forest": "wood",
            "farm": "food",
            "quarry": "stone"
        }
        self.storage = values["initialValues"]["storage"]
        self.population = values["initialValues"]["population"]
        self.occupiedPopulation = 0
        self.populationOccupation = {
            "forest": 0,
            "farm": 0,
            "quarry": 0
        }
        self.realGains = {
            "wood": 0,
            "food": 0,
            "stone": 0
        }
        self.abbreviate = {
            "money": "$",
            "wood": "WO",
            "food": "FO",
            "stone": "ST"
        }

        #initial lvls
        self.lvlStates = values["initialValues"]["lvls"]

    def activateDownMenu(self):
        self.displayDownMenu = True
        return self.selectedBuilding

    def deactivateDownMenu(self):
        self.displayDownMenu = False
        return ""
    
    def calculateAffordable(self, price):
        for item in self.materialList:
            if item in price:
                if self.storage[item] >= price[item]:
                    pass
                else:
                    return False
        return True
    
    def payPrice(self, price):
        for item in self.materialList:
            if item in price:
                self.storage[item] -= price[item]

    #True if it paid and False if not affordable
    def upgradeConfirmed(self):
        if self.calculateAffordable(values["prices"][self.selectedBuilding][self.lvlStates[self.selectedBuilding]+1]["price"]):
            self.payPrice(values["prices"][self.selectedBuilding][self.lvlStates[self.selectedBuilding]+1]["price"])
            self.lvlStates[self.selectedBuilding]+=1
            return True
        else:
            return False

    def calcNextInstantMaterial(self, material, dT):
        if material=="wood": 
            return round(self.storage["wood"]+dT*values["stats"]["forest"][self.lvlStates["forest"]]["income"]*self.populationOccupation["forest"],3)
        elif material=="food":
            return round(self.storage["food"]+dT*values["stats"]["farm"][self.lvlStates["farm"]]["income"]*self.populationOccupation["farm"],3)
        elif material=="stone":
            return round(self.storage["stone"]+dT*values["stats"]["quarry"][self.lvlStates["quarry"]]["income"]*self.populationOccupation["quarry"],3)

    def calculateGains(self, dT): 
        initialStorage={}
        for item in self.materialList:
            initialStorage[item]=self.storage[item]

        #costSecond population
        for item in self.materialList:
            if item in values["citizens"]["costSecond"][self.lvlStates["TH"]]:
                if self.calcNextInstantMaterial(item, dT)-(dT*values["citizens"]["costSecond"][self.lvlStates["TH"]][item]*(self.population-1))<0:
                    self.updating=False
                    return ""
        for item in self.materialList:
            if item in values["citizens"]["costSecond"][self.lvlStates["TH"]]:
                self.storage[item]=round(self.storage[item]-dT*values["citizens"]["costSecond"][self.lvlStates["TH"]][item]*(self.population-1),3)

        #wood+=forest*dT*workingPeople
        
        for item in self.primaryMaterialsList:
            self.storage[item]=self.calcNextInstantMaterial(item, dT)

        delta=0
        for item in self.materialList:
            if dT>0:
                delta=round((self.storage[item]-initialStorage[item])/dT)
            self.realGains[item]=delta