# Copyright 2019 Alistair Sealy

# ##### BEGIN GPL LICENSE BLOCK #####
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


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
