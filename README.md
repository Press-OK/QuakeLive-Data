# QuakeLive-Data
A Python tool for parsing Quake map files (.BSP) and returning various details about the maps

# Purpose
After some debate with map-makers regarding optimal design in Quake Live, it needed to be broken down into a science. This tool outputs various details about the Meshes and Entities contained within a .bsp map file, which allowed us to correlate high-rated maps with their contents. The results were a standard set of rules to follow for new map creation and "best practices."

# Results
I was able to determine how health-pickup distribution was the deciding factor in the pace, balance, and "fun-factor" of the map, with a specific focus on the FreezeTag game mode which has some different back-and-forth dynamics.
As an unexpected bonus, it also allowed us to identify some "problem maps" which had a lot of garbage meshes sitting outside the play area which the designers had left in. This allowed us to reduce some of the maps' overhead in-game and also marginally reduce filesizes.

# But it's 2020, Quake 3 was released over 20 years ago
Yes, but it's still the best AFPS game.
