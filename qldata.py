#=============================================================
# Quake Live Map Data Generator
# by PressOK
#
# Reads all *.map files from a directory and aggregates data
# about items, spawns, lighting, pits, etc.
#=============================================================

import os
from mapclass import Map
from entityclass import Entity

# Holds all of the loaded maps
maps = []

#=============================================================
# Entry point of the script
#=============================================================
def main():
    LoadMaps("./maps/")

    # Print some map data
    print("[GNRL]\tMap data...")
    tabsize = 32
    for m in maps:
        print("     |\t\t" + m.name.upper() + ":")
        print("     |\t\t\tMap area (X*Y*Z)".ljust(tabsize) +
            str(round(m.mapArea / (10**9))) + " billion u^3")
        print("     |\t\t\tMap footprint (X*Y)".ljust(tabsize) +
            str(round(m.mapFootprint / (10**6))) + " million u^2")
        print("     |")
        print("     |\t\t\tSpawns:".ljust(tabsize) +
            str(m.entityCount["info_player_deathmatch"]))
        print("     |\t\t\t  'Spawn space'".ljust(tabsize) +
            str(round(m.mapFootprint / m.entityCount["info_player_deathmatch"] / 1000)) + " thousand u^2")
        print("     |")
        print("     |\t\t\tEntities:".ljust(tabsize) +
            str(len(m.entities)))
        print("     |\t\t\t  HP available".ljust(tabsize) +
            str(m.entityCount["item_health_small"]*5 + m.entityCount["item_health"]*25 +
                m.entityCount["item_health_large"]*50 + m.entityCount["item_health_mega"]*100))
        print("     |\t\t\t  AP available".ljust(tabsize) +
            str(m.entityCount["item_armor_shard"]*5 + m.entityCount["item_armor_jacket"]*25 +
                m.entityCount["item_armor_combat"]*50 + m.entityCount["item_armor_body"]*100))
        print("     |")

    trackedEntities = Map().TrackedEntitiesList()
    print("[TEST]\tAverage distances between entity types...")
    tabsize = 32
    for m in maps:
        print("     |\t\t" + m.name.upper() + ":")
        for entName in trackedEntities:
            hasEnt = False
            mapDistanceDict = {}
            for ent1 in m.entities:
                if ent1.name == entName and ent1.hasOrigin:
                    hasEnt = True
                    for ent2 in m.entities:
                        if ent2.hasOrigin:
                            if ent2.name not in mapDistanceDict:
                                mapDistanceDict[ent2.name] = GetDistance(ent1, ent2)
                            else:
                                mapDistanceDict[ent2.name] = (mapDistanceDict[ent2.name] + GetDistance(ent1, ent2)) / 2
            for dictEntry in mapDistanceDict:
                print("     |\t\t\t" + entName + " <--> " + dictEntry + ": " + str(round(mapDistanceDict[dictEntry])))


#=============================================================
# Loads all the map files in the ./maps/ directory, cleans up
# the incoming data and then parses it into a Map class object
#=============================================================
def LoadMaps(dir):
    print("\n[MAIN]\tLoading maps...")

    # Load all map files
    count = 0
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".map"):
                print("     |\t\t" + file)
                newMapFullPath = dir + file
                newMapData = []
                newMapFile = open(newMapFullPath, "r")
                for line in newMapFile:
                    newMapData.append(line)
                newMapFile.close()
                m = Map(newMapData)
                m.name = file[:-4]
                maps.append(m)
                count += 1
    print("     |\t" + str(count) + " maps loaded.\n")
    print("     |")


def GetDistance(ent1: Entity, ent2: Entity):
    # Make sure both entities have an origin
    if ent1.hasOrigin == False or ent2.hasOrigin == False:
        return None
    else:
        return abs(ent1.origin["x"] - ent2.origin["x"]) +abs(ent1.origin["y"] - ent2.origin["y"]) + abs(ent1.origin["z"] - ent2.origin["z"])


if __name__=="__main__":
   main()