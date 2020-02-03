import re
from entityclass import Entity

#=============================================================
# This class parses and stores all the data for an individual
# map file.
#=============================================================
class Map:

    def __init__(self, mapdata=None):

        # If the class wasn't initialized properly, do nothing,
        # this is just so that methods of the class can be used
        # without initializing an entire map I guess
        if not mapdata:
            return None

        # Holds the map name
        self.name = ""
        # Holds all lines of data (str)
        self.lines = mapdata
        # List of entities in the map
        self.entities = []
        # List of entities in the map
        self.entityCount = {}
        # Index of the last line of the worldspawn
        self.worldSpawnEnd = 0
        # Holds the map bounds coordinates
        self.mapBounds = {
            "minX": 0,
            "minY": 0,
            "minZ": 0,
            "maxX": 0,
            "maxY": 0,
            "maxZ": 0,
        }
        # Holds the map area in cubed units
        self.mapArea = 0
        # Holds the map footprint in squared units
        self.mapFootprint = 0

        # Remove comments and empty lines from the map data
        for line in self.lines:
            if line.strip()[0:2] == "//" or not line:
                self.lines.remove(line)

        # Initialize the tracked entity dictionary
        for ent in self.TrackedEntitiesList():
            self.entityCount[ent] = 0

        # Collect all the tracked entities from the raw map data
        for lineIndex in range(len(self.lines)):
            for ent in self.TrackedEntitiesList():
                if ('"classname" "' + ent + '"') in self.lines[lineIndex]:

                    line = self.lines[lineIndex]

                    # Extract the entity lines
                    newEntLines = []
                    startIndex = lineIndex
                    while self.lines[startIndex-1][0] != "{":
                        startIndex -= 1
                    endIndex = startIndex
                    openedParens = 0
                    while self.lines[endIndex+1][0] != "}" and openedParens == 0:
                        if self.lines[endIndex+1][0] == "{":
                            openedParens += 1
                        elif self.lines[endIndex+1][0] == "}":
                            openedParens -= 1
                        endIndex += 1
                    for entityLine in self.lines[startIndex:endIndex]:
                        newEntLines.append(entityLine)

                    # Check for presence of exlusionary flags and abandon
                    # the entity if it's not for our game mode/settings
                    includeEntity = True
                    for entityLine in newEntLines:
                        if '"notteam" "1"' in entityLine or '"not_gametype" "ft"' in entityLine:
                            includeEntity = False
                            break

                    if includeEntity:
                        # Initialize new entity class
                        e = Entity(newEntLines)
                        e.name = ent
                        # Create add the found entity to the entity list
                        self.entities.append(e)
                        # Add the found entity to the running totals
                        self.entityCount[ent] += 1

        # Determine the end of the worldspawn entity (contains all
        # basic brushes and patches)
        openedParens = 0
        for lineIndex in range(len(self.lines)):
            if (self.lines[lineIndex][0] == "{"):
                openedParens += 1
            elif (self.lines[lineIndex][0] == "}"):
                openedParens -= 1
                if openedParens == 0:
                    self.worldSpawnEnd = lineIndex
                    break

        # Determine the map size by finding the lowest XYZ coords
        # and the highest XYZ coords
        # Could be improved since some maps have brushes way
        # outside of the playable area...
        tempMinX = tempMinY = tempMinZ = 99999999.0
        tempMaxX = tempMaxY = tempMaxZ = 0.0

        # Analyze all BRUSHES
        pat = re.compile("^\\t*\\( -*\\d+\\.*\\d* -*\\d+\\.*\\d* -*\\d+\\.*\\d* \\)")
        for line in self.lines[0:self.worldSpawnEnd]:
            if pat.match(line):
                lineArray = line.split()
                # First coord
                if float(lineArray[1]) < tempMinX:
                    tempMinX = float(lineArray[1])
                if float(lineArray[1]) > tempMaxX:
                    tempMaxX = float(lineArray[1])
                if float(lineArray[2]) < tempMinY:
                    tempMinY = float(lineArray[2])
                if float(lineArray[2]) > tempMaxY:
                    tempMaxY = float(lineArray[2])
                if float(lineArray[3]) < tempMinZ:
                    tempMinZ = float(lineArray[3])
                if float(lineArray[3]) > tempMaxZ:
                    tempMaxZ = float(lineArray[3])
                # Second coord
                if float(lineArray[6]) < tempMinX:
                    tempMinX = float(lineArray[6])
                if float(lineArray[6]) > tempMaxX:
                    tempMaxX = float(lineArray[6])
                if float(lineArray[7]) < tempMinY:
                    tempMinY = float(lineArray[7])
                if float(lineArray[7]) > tempMaxY:
                    tempMaxY = float(lineArray[7])
                if float(lineArray[8]) < tempMinZ:
                    tempMinZ = float(lineArray[8])
                if float(lineArray[8]) > tempMaxZ:
                    tempMaxZ = float(lineArray[8])
                # Third coord
                if float(lineArray[11]) < tempMinX:
                    tempMinX = float(lineArray[11])
                if float(lineArray[11]) > tempMaxX:
                    tempMaxX = float(lineArray[11])
                if float(lineArray[12]) < tempMinY:
                    tempMinY = float(lineArray[12])
                if float(lineArray[12]) > tempMaxY:
                    tempMaxY = float(lineArray[12])
                if float(lineArray[13]) < tempMinZ:
                    tempMinZ = float(lineArray[13])
                if float(lineArray[13]) > tempMaxZ:
                    tempMaxZ = float(lineArray[13])

        # Analyze all PATCHES
        pat = re.compile("^\\t*\\( \\( -*\\d+\\.*\\d*")
        for line in self.lines[0:self.worldSpawnEnd]:
            if pat.match(line):
                lineArray = line.split()
                # First coord
                if float(lineArray[2]) < tempMinX:
                    tempMinX = float(lineArray[2])
                if float(lineArray[2]) > tempMaxX:
                    tempMaxX = float(lineArray[2])
                if float(lineArray[3]) < tempMinY:
                    tempMinY = float(lineArray[3])
                if float(lineArray[3]) > tempMaxY:
                    tempMaxY = float(lineArray[3])
                if float(lineArray[4]) < tempMinZ:
                    tempMinZ = float(lineArray[4])
                if float(lineArray[4]) > tempMaxZ:
                    tempMaxZ = float(lineArray[4])
                # Second coord
                if float(lineArray[9]) < tempMinX:
                    tempMinX = float(lineArray[9])
                if float(lineArray[9]) > tempMaxX:
                    tempMaxX = float(lineArray[9])
                if float(lineArray[10]) < tempMinY:
                    tempMinY = float(lineArray[10])
                if float(lineArray[10]) > tempMaxY:
                    tempMaxY = float(lineArray[10])
                if float(lineArray[11]) < tempMinZ:
                    tempMinZ = float(lineArray[11])
                if float(lineArray[11]) > tempMaxZ:
                    tempMaxZ = float(lineArray[11])
                # Third coord
                if float(lineArray[16]) < tempMinX:
                    tempMinX = float(lineArray[16])
                if float(lineArray[16]) > tempMaxX:
                    tempMaxX = float(lineArray[16])
                if float(lineArray[17]) < tempMinY:
                    tempMinY = float(lineArray[17])
                if float(lineArray[17]) > tempMaxY:
                    tempMaxY = float(lineArray[17])
                if float(lineArray[18]) < tempMinZ:
                    tempMinZ = float(lineArray[18])
                if float(lineArray[18]) > tempMaxZ:
                    tempMaxZ = float(lineArray[18])

        self.mapBounds["minX"] = tempMinX
        self.mapBounds["minY"] = tempMinY
        self.mapBounds["minZ"] = tempMinZ
        self.mapBounds["maxX"] = tempMaxX
        self.mapBounds["maxY"] = tempMaxY
        self.mapBounds["maxZ"] = tempMaxZ
        self.mapFootprint = (tempMaxX - tempMinX) * (tempMaxY - tempMinY)
        self.mapArea = self.mapFootprint * (tempMaxZ - tempMinZ)

    #=============================================================
    # I don't know where else to put this but it's annoyingly big.
    # Just a list of all the possible entities by name.
    #=============================================================
    def TrackedEntitiesList(self):
        return [
            "ammo_belt",
            "ammo_bfg",
            "ammo_bullets",
            "ammo_cells",
            "ammo_grenades",
            "ammo_hmg",
            "ammo_lightning",
            "ammo_mines",
            "ammo_nails",
            "ammo_pack",
            "ammo_rockets",
            "ammo_shells",
            "ammo_slugs",
            "func_bobbling",
            "func_button",
            "func_door",
            "func_group",
            "func_pendulum",
            "func_plat",
            "func_rotating",
            "func_static",
            "func_timer",
            "func_train",
            "holdable_invulnerability",
            "holdable_kamikaze",
            "holdable_medkit",
            "holdable_teleporter",
            "info_camp",
            "info_notnull",
            "info_null",
            "info_player_deathmatch",
            "info_player_intermission",
            "info_player_start",
            "info_tour_point",
            "path_corner",
            "race_point",
            "item_ammoregen",
            "item_armor_body",
            "item_armor_combat",
            "item_armor_jacket",
            "item_armor_shard",
            "item_botroam",
            "item_doubler",
            "item_enviro",
            "item_flight",
            "item_guard",
            "item_haste",
            "item_health",
            "item_health_large",
            "item_health_mega",
            "item_health_small",
            "item_invis",
            "item_key_gold",
            "item_key_master",
            "item_key_silver",
            "item_quad",
            "item_regen",
            "item_scout",
            "misc_model",
            "misc_portal_camera",
            "misc_portal_surface",
            "misc_teleporter_dest",
            "shooter_grenade",
            "shooter_plasma",
            "shooter_rocket",
            "target_cvar",
            "target_delay",
            "target_give",
            "target_kill",
            "target_location",
            "target_position",
            "target_print",
            "target_push",
            "target_relay",
            "target_remove_powerups",
            "target_score",
            "target_speaker",
            "target_teleporter",
            "team_blueobelisk",
            "team_CTF_blueflag",
            "team_CTF_blueplayer",
            "team_CTF_bluespawn",
            "team_CTF_neutralflag",
            "team_CTF_redflag",
            "team_CTF_redplayer",
            "team_CTF_redspawn",
            "team_dom_point",
            "team_neutralobelisk",
            "team_redobelisk",
            "trigger_always",
            "trigger_hurt",
            "trigger_multiple",
            "trigger_push",
            "trigger_teleport",
            "_decal",
            "_skybox",
            "advertisement",
            "light",
            "lightjunior",
            "weapon_bfg",
            "weapon_chaingun",
            "weapon_gauntlet",
            "weapon_grapplinghook",
            "weapon_grenadelauncher",
            "weapon_hmg",
            "weapon_lightning",
            "weapon_machinegun",
            "weapon_nailgun",
            "weapon_plasmagun",
            "weapon_prox_launcher",
            "weapon_railgun",
            "weapon_rocketlauncher",
            "weapon_shotgun",
            # "worldspawn"
        ]