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
        THInfo
        buildingInfo
        upgradeMeaningTH
        upgrade
        '''
        self.activeMenu=None

        self.whatIsSelected = ""

        self.notAffordableShown=False

        #initial values
        self.materialList = ["money", "wood", "food", "stone"]
        self.materialToBuilding={
            "wood": "forest",
            "food": "farm",
            "stone": "quarry"
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
        return self.whatIsSelected

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

    #toggles upgrade menu
    def upgradePressed(self):
        if self.activeMenu=="upgrade":
            self.activeMenu=None
            self.displayCity=True
        else:
            if self.whatIsSelected=="TH":
                self.activeMenu="upgradeMeaningTH"
            else:
                self.activeMenu="upgrade"
            self.displayCity=False

    #True if it paid and False if not affordable
    def upgradeConfirmed(self):
        if self.calculateAffordable(values["prices"][self.whatIsSelected][self.lvlStates[self.whatIsSelected]+1]["price"]):
            self.payPrice(values["prices"][self.whatIsSelected][self.lvlStates[self.whatIsSelected]+1]["price"])
            self.lvlStates[self.whatIsSelected]+=1
            return True
        else:
            return False

    def infoPressed(self):
        if self.whatIsSelected=="TH":
            self.displayCity=False
            self.activeMenu="THInfo"
        else:
            self.displayCity=False
            self.activeMenu="buildingInfo"

    def calculateGains(self, dT): 
        initialStorage={}
        for item in self.materialList:
            initialStorage[item]=self.storage[item]

        #costSecond population
        for item in self.materialList:
            if item in values["citizens"]["costSecond"][self.lvlStates["TH"]]:
                if self.storage[item]-dT*values["citizens"]["costSecond"][self.lvlStates["TH"]][item]*(self.population-1)<0:
                    self.updating=False
                    return ""
                else:
                    self.storage[item]=round(self.storage[item]-dT*values["citizens"]["costSecond"][self.lvlStates["TH"]][item]*(self.population-1),3)

        #wood+=forest*dT*workingPeople
        
        self.storage["wood"]=round(self.storage["wood"]+dT*values["stats"]["forest"][self.lvlStates["forest"]]["income"]*self.populationOccupation["forest"],3)
        
        #food += farm
        self.storage["food"]=round(self.storage["food"]+dT*values["stats"]["farm"][self.lvlStates["farm"]]["income"]*self.populationOccupation["farm"],3)

        # stone += quarry
        self.storage["stone"]=round(self.storage["stone"]+dT*values["stats"]["quarry"][self.lvlStates["quarry"]]["income"]*self.populationOccupation["quarry"],3)

        delta=0
        for item in self.materialList:
            if dT>0:
                delta=round((self.storage[item]-initialStorage[item])/dT)
            self.realGains[item]=delta