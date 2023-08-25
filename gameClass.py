from paths import *
import json

with open("values.json", "r") as f:
    values= json.load(f)

class Game:
    def __init__(self):
        global values
        #default gameState variables
        self.downMenuIsUnlocked=False
        self.prevDownMenuIsUnlocked=False
        self.upgradeMenuIsUnlocked=False
        self.prevUpgradeMenuIsUnlocked=False
        self.storageMenuIsUnlocked = True
        self.whatIsSelected = ""

        #initial values
        self.materialList = ["money", "wood", "food", "stone"]
        self.storage = values["initialValues"]["storage"]

        #initial lvls
        self.lvlStates = values["initialValues"]["lvls"]

    def activateDownMenu(self):
        self.downMenuIsUnlocked = True
        return self.whatIsSelected

    def deactivateDownMenu(self):
        self.downMenuIsUnlocked = False
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

        #self.upgradeMenuIsUnlocked = not self.upgradeMenuIsUnlocked
        if self.upgradeMenuIsUnlocked:
            self.upgradeMenuIsUnlocked=False
        else:
            self.upgradeMenuIsUnlocked=True

    #True if it paid and False if not affordable
    def upgradeConfirmed(self):
        if self.calculateAffordable(values["prices"][self.whatIsSelected][self.lvlStates[self.whatIsSelected]+1]["price"]):
            self.payPrice(values["prices"][self.whatIsSelected][self.lvlStates[self.whatIsSelected]+1]["price"])
            self.lvlStates[self.whatIsSelected]+=1
            return True
        else:
            return False

    def infoPressed(self):
        print("i")

    def calculateGains(self, dT):

        #self.storage["money"]=round(self.storage["wood"]+dT*,3)

        #wood+=forest
        self.storage["wood"]=round(self.storage["wood"]+dT*values["incomes"]["forest"][self.lvlStates["forest"]]["income"],3)

        #food += farm
        self.storage["food"]=round(self.storage["food"]+dT*values["incomes"]["farm"][self.lvlStates["farm"]]["income"],3)

        # stone += quarry
        self.storage["stone"]=round(self.storage["stone"]+dT*values["incomes"]["quarry"][self.lvlStates["quarry"]]["income"],3)
