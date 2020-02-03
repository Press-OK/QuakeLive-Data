#=============================================================
# This class holds information of a single entity
#=============================================================
class Entity:

    def __init__(self, entitydata=None):

        # If the class wasn't initialized properly, do nothing
        if not entitydata:
            return None

        # Holds entity name
        self.name = ""
        # Holds all lines of data (str)
        self.lines = entitydata
        # Boolean whether or not this entity has an origin
        self.hasOrigin = False
        # Origin coords
        self.origin = {
            "x": 0,
            "y": 0,
            "z": 0,
        }

        # Get the entity origin if there is one
        for line in self.lines:
            if '"origin"' in line:
                self.hasOrigin = True
                #"origin" "-64 1440 -232"
                lineArray = line.split()
                self.origin["x"] = float(lineArray[1][1:])
                self.origin["y"] = float(lineArray[2])
                self.origin["z"] = float(lineArray[3][:-1])

    def GetOrigin(self):
        return [self.origin["x"], self.origin["y"], self.origin["z"]]