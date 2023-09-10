import os

iconTexturePath= os.path.abspath("gameFiles/assets/icon.ico")

#Buildings
buildingsGenericTexturePath = os.path.abspath("gameFiles/assets/textures/buildings/") + "\\"
thGenericTexturePath = os.path.abspath("gameFiles/assets/textures/buildings/TH/") + "\\"
forestGenericTexturePath = os.path.abspath("gameFiles/assets/textures/buildings/forest/") + "\\"
farmGenericTexturePath = os.path.abspath("gameFiles/assets/textures/buildings/farm/") + "\\"
quarryGenericTexturePath = os.path.abspath("gameFiles/assets/textures/buildings/quarry/") + "\\"
internalMarketGenericTexturePath = os.path.abspath("gameFiles/assets/textures/buildings/internalMarket/") + "\\"

#storage
moneyTexturePath= os.path.abspath("gameFiles/assets/textures/storage/money.png")
woodTexturePath= os.path.abspath("gameFiles/assets/textures/storage/wood.png")
foodTexturePath= os.path.abspath("gameFiles/assets/textures/storage/food.png")
stoneTexturePath= os.path.abspath("gameFiles/assets/textures/storage/stone.png")

#Menus
acceptTexturePath = os.path.abspath("gameFiles/assets/textures/menus/accept.png")
cancelTexturePath = os.path.abspath("gameFiles/assets/textures/menus/cancel.png")
addTexturePath = os.path.abspath("gameFiles/assets/textures/menus/add.png")
subtractTexturePath = os.path.abspath("gameFiles/assets/textures/menus/subtract.png")
populationTexturePath= os.path.abspath("gameFiles/assets/textures/menus/down_menu/population.png")
downgradeTexturePath = os.path.abspath("gameFiles/assets/textures/menus/down_menu/downgrade.png")
enterBuildingTexturePath = os.path.abspath("gameFiles/assets/textures/menus/down_menu/enterBuilding.png")
##info
infoTexturePath = os.path.abspath("gameFiles/assets/textures/menus/down_menu/info/info.png")
infoLockedTexturePath = os.path.abspath("gameFiles/assets/textures/menus/down_menu/info/info_locked.png")
##upgrade
upgradeTexturePath = os.path.abspath("gameFiles/assets/textures/menus/down_menu/upgrade/upgrade.png")
upgradeLockedTexturePath = os.path.abspath("gameFiles/assets/textures/menus/down_menu/upgrade/upgrade_locked.png")

loadTexturePath = os.path.abspath("gameFiles/assets/textures/menus/load.png")
saveTexturePath = os.path.abspath("gameFiles/assets/textures/menus/save.png")
newSaveTexturePath = os.path.abspath("gameFiles/assets/textures/menus/newSave.png")
resumeTexturePath = os.path.abspath("gameFiles/assets/textures/menus/resume.png")

#configs
valuesJsonPath = os.path.abspath("gameFiles/configs/values.json")
versionJsonPath = os.path.abspath("gameFiles/configs/version.json")
configJsonPath = os.path.abspath("gameFiles/configs/config.json")
##langs
langsJsonPath={
    "EN": os.path.abspath("gameFiles/configs/langs/EN.json")
}

#fonts
arialFontPath= os.path.abspath("gameFiles/assets/fonts/arial.ttf")

#save
savePath= os.path.abspath("saves/save.pkl")