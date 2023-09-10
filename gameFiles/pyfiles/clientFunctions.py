import pickle, pygame, json
from gameFiles.configs.paths import *

#version file
with open(versionJsonPath, "r") as f:
    version = json.load(f)

#log creator
def log(msg):
    with open('saves/log.txt', 'w') as f:
        f.write(msg)
        print(msg)
        
#convert 1000 -> 1k ...
#usage: reNumberer(game.storage[item])+game.abbreviate[item]
def reNumberer(num):
    for unit in ['','K','M']:
        if abs(num) < 1000.0:
            return f"{num:6.2f}{unit}"
        num /= 1000.0
    return f"{num:6.2f}B"
