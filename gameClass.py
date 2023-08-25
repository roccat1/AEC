from paths import *
import json

with open("values.json", "r") as f:
    values= json.load(f)

class Game:
    def __init__(self):
        global values
        #default gameState variables
        self.displayDownMenu=False
        self.prevDisplayDownMenu=False
        self.displayUpgradeMenu=False
        self.prevDisplayUpgradeMenu=False

        self.displayStorageMenu = True
        self.displayPopulationMenu = True
        self.displayTHInfoMenu = False
        self.displayCity = True
        self.displayWarning = False

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
        #upgrade th

        #self.displayUpgradeMenu = not self.displayUpgradeMenu
        if self.displayUpgradeMenu:
            self.displayUpgradeMenu=False
            self.displayCity=True
        else:
            self.displayUpgradeMenu=True
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
            self.displayTHInfoMenu=True
            


    def calculateGains(self, dT):
        returnChain=[]
        for item in self.materialList:
            if item in values["citizens"]["income"]:
                self.storage[item]=round(self.storage[item]+dT*values["citizens"]["income"][item]*self.population,3)
        
        for item in self.materialList:
            if item in values["citizens"]["costSecond"]:
                if self.storage[item]-dT*values["citizens"]["costSecond"][item]*self.population <0:
                    self.population-=1
                    returnChain.append("lostPopulation")
                else:
                    self.storage[item]=round(self.storage[item]-dT*values["citizens"]["costSecond"][item]*self.population,3)

        #wood+=forest
        self.storage["wood"]=round(self.storage["wood"]+dT*values["incomes"]["forest"][self.lvlStates["forest"]]["income"],3)

        #food += farm
        self.storage["food"]=round(self.storage["food"]+dT*values["incomes"]["farm"][self.lvlStates["farm"]]["income"],3)

        # stone += quarry
        self.storage["stone"]=round(self.storage["stone"]+dT*values["incomes"]["quarry"][self.lvlStates["quarry"]]["income"],3)

        return returnChain