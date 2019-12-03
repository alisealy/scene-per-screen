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

This script is designed to be run in blender 2.8x

If you have not done so already, open this .blend file in blender 2.79 and run the script "export_scene_per_screen.py".
That script will create a file "scene_per_screen.txt" (in the same directory as the .blend file) that contains the information of which scene goes with which screen.
This script relies on that information, so without it this script will not work.

This script first defines a custom property group "PerScreenVariables", then adds this to the definition of the "Screen" data-block stored in bpy.types.
(This means that all screens now have this custom variable which we can set for each screen)
Next the script reads the file "scene_per_screen.txt" and records all the screen/scene pairs in a python variable called "pairings".
Finally, for each screen named in "pairings", the script will assign the corresponding scene name to the custom variable "per_screen_vars.scene".

Upon saving the .blend file, this custom property will also be saved. 
NOTE: This information will not be accessible without first registering the custom property group again. This needs to be done each time blender is started, so it is best done seperately via an add-on.

"""

import bpy

class PerScreenVariables(bpy.types.PropertyGroup):
    scene: bpy.props.StringProperty(
        name="scenePerScreen",
        description="the scene for each screen (for backwards compatability with 2.79)",
        default="Scene"
    )

def register():
    bpy.utils.register_class(PerScreenVariables)
    bpy.types.Screen.per_screen_vars = bpy.props.PointerProperty(type=PerScreenVariables)

def unregister():
    del bpy.types.Screen.per_screen_vars
    bpy.utils.unregister_class(PerScreenVariables)

if __name__ == '__main__':
    register()
    
    # read the screen/scene information from the external file
    file = open(bpy.data.filepath.rstrip(bpy.path.basename(bpy.data.filepath))+"scene_per_screen.txt","r")
    pairings = [line.strip('\n').split(',') for line in file.readlines()]
    file.close()
    
    # use the custom "PerScreenVariables" property group to store this information in the .blend file
    for pair in pairings:
        bpy.data.screens[pair[0]].per_screen_vars.scene = pair[1]
    
    # report success
    print("I'm done")
