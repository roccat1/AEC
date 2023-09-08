from paths import *
import json

with open(valuesJsonPath, "r") as f:
    values= json.load(f)

class Game:
    def __init__(self):
        global values

        self.active=False
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

        self.internalMarketConfig=values["initialValues"]["internalMarketConfig"]

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
        #wood+=forest*dT*workingPeople
        if material=="wood": 
            result = (self.storage["wood"]
                         #income from generator
                         +dT*values["stats"]["forest"][self.lvlStates["forest"]]["income"]*self.populationOccupation["forest"]
                         #selling in internal market
                         -dT*self.internalMarketConfig[material]
                         )
            #pay population if necessary
            if material in values["citizens"]["costSecond"][self.lvlStates["TH"]]:
                result-=dT*values["citizens"]["costSecond"][self.lvlStates["TH"]][material]*(self.population-1)

            return result
        
        elif material=="food":
            result = (self.storage["food"]
                         #income from generator
                         +dT*values["stats"]["farm"][self.lvlStates["farm"]]["income"]*self.populationOccupation["farm"]
                         #selling in internal market
                         -dT*self.internalMarketConfig[material]
                         )
            #pay population if necessary
            if material in values["citizens"]["costSecond"][self.lvlStates["TH"]]:
                result-=dT*values["citizens"]["costSecond"][self.lvlStates["TH"]][material]*(self.population-1)
            
            return result
        
        elif material=="stone":
            result = (self.storage["stone"]
                         #income from generator
                         +dT*values["stats"]["quarry"][self.lvlStates["quarry"]]["income"]*self.populationOccupation["quarry"]
                         #selling in internal market
                         -dT*self.internalMarketConfig[material])
            #pay population if necessary
            if material in values["citizens"]["costSecond"][self.lvlStates["TH"]]:
                result-=dT*values["citizens"]["costSecond"][self.lvlStates["TH"]][material]*(self.population-1)
            
            return result
        
        elif material == "money":
            result = self.storage["money"]
            #internalMarket payments
            for item in self.primaryMaterialsList:
                result+=dT*values["internalMarket"][item]*self.internalMarketConfig[item]
            #pay population if necessary
            if material in values["citizens"]["costSecond"][self.lvlStates["TH"]]:
                result-=dT*values["citizens"]["costSecond"][self.lvlStates["TH"]][material]*(self.population-1)
            
            return result

    def calcDelta(self, material):
        return self.calcNextInstantMaterial(material, 1)-self.storage[material]


    def calculateGains(self, dT):
        
        for item in self.materialList:
            self.realGains[item]=self.calcDelta(item)

        #costSecond population
        #can afford the next instant?
        for item in self.materialList:
            if self.calcNextInstantMaterial(item, dT)<0:
                    #do if not affordable
                    self.updating=False
                    return ""
        for item in self.materialList:
            self.storage[item]=self.calcNextInstantMaterial(item, dT)

        