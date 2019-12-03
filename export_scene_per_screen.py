"""

This script is designed to be run in blender 2.79

The script creates a new file called "scene_per_screen.txt" in the same directory as the blendfile.
It then reads the blend file, and for each screen, it writes down the name of the screen, and the name of the corresponding scene.
This is saved to the "scene_per_screen.txt" file in the following format:

screen1,scene1
screen2,scene2

etc, etc

"""

import bpy

f = open(bpy.data.filepath.rstrip(bpy.path.basename(bpy.data.filepath))+"scene_per_screen.txt", "w")
for screen in bpy.data.screens:
    f.write(screen.name + "," + screen.scene.name + "\n")
f.close()
print("done")
