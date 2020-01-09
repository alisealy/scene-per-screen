
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

bl_info = {
    "name": "Scene-per-screen",
    "category": "Interface",
    "blender": (2, 80, 0)
}

import bpy
import functools

"""
Note: at the moment, the automatic scene-switching must be manually enabled from the preferences window,
this must be done every time the add-on is enabled, and every time blender is re-started. This is kinda annoying.

In the short-term the control could be moved to the main GUI window, or mapped to a shortcut, or both.

In the long term some way should be found to have this enabled automatically.
"""


#class to define custom pop-up menu for switching worspaces
class WORKSPACE_OT_select(bpy.types.Operator):
    bl_idname = "workspace.select"
    bl_label = "Select Workspace"
    bl_description = "Select workspace"
    bl_property = "workspace"

    enum_items = None

    def get_items(self, context):
        if WORKSPACE_OT_select.enum_items is None:
            enum_items = []

            for w in bpy.data.workspaces:
                identifier, name, description = \
                    w.name, w.name, w.name
                if context.workspace.name == identifier:
                    name += "|Active"
                enum_items.append((
                    identifier,
                    name,
                    description))

            WORKSPACE_OT_select.enum_items = enum_items

        return WORKSPACE_OT_select.enum_items

    workspace = bpy.props.EnumProperty(items=get_items)

    def execute(self, context):
        if not self.workspace or self.workspace not in bpy.data.workspaces:
            return {'CANCELLED'}

        context.window.workspace = bpy.data.workspaces[self.workspace]
        return {'FINISHED'}

    def invoke(self, context, event):
        WORKSPACE_OT_select.enum_items = None
        context.window_manager.invoke_search_popup(self)
        return {'FINISHED'}


# Override topbar drawing    
def my_draw_left(self, context):
    layout = self.layout

    window = context.window
    screen = context.screen

    bpy.types.TOPBAR_MT_editor_menus.draw_collapsible(context, layout)

    layout.separator()

    if not screen.show_fullscreen:
        pass
    else:
        layout.operator(
            "screen.back_to_previous",
            icon='SCREEN_BACK',
            text="Back to Previous",
        )


# Custom property to store scene-per-screen
class PerScreenVariables(bpy.types.PropertyGroup):
    scene: bpy.props.StringProperty(
        name="scenePerScreen",
        description="the scene for each screen (for backwards compatability with 2.79)",
        default="Scene"
    )


#NOTE: the modal operator has been removed, this is left for reference only
# addon preferences panel, with a button to start the modal operator
class testingAddOnPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator_context = 'INVOKE_DEFAULT'
        row.operator('wm.modal_workspace_scene_wrapper', text="enable automatic scene switching")


#lastScreen = {bpy.context.window : bpy.context.screen}
def scene_daemon(lastScreen):
    # do this stuff only for some condition we have identified
    
    # if the last screen (a variable called lastScreen) is the same as the current one, do nothing.
    #global lastScreen
    for window in bpy.context.window_manager.windows:
        if window not in lastScreen.keys():
            lastScreen[window] = window.screen
            # need to check for a memory here
        elif not (lastScreen[window] == window.screen):
            # if the screen has changed, do stuff
            
            # save the screen/scene pair for the previous workspace before we change anything
            lastScreen[window].per_screen_vars.scene = window.scene.name
            
            # if the remembered scene exists, switch to that.
            memory = window.screen.per_screen_vars.scene
            if memory in bpy.data.scenes:
                window.scene = bpy.data.scenes[memory]
            # make a note of what screen we are on now
            lastScreen[window] = window.screen
    return 0.001 #this is the delay before the function is called again


addon_keymaps = []
context_window = bpy.context.window_manager.windows[-1]
proxyname = functools.partial(scene_daemon, {context_window : context_window.screen})


def register():
    # first register the custom menu, and the associated hotkey
    bpy.utils.register_class(WORKSPACE_OT_select)
    
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(
        name='Screen Editing')
    kmi = km.keymap_items.new(
        WORKSPACE_OT_select.bl_idname, 'SPACE', 'PRESS', 
        ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))
    
    # Now we override the top-bar
    bpy.types.TOPBAR_HT_upper_bar.default_draw_left = \
        bpy.types.TOPBAR_HT_upper_bar.draw_left
    bpy.types.TOPBAR_HT_upper_bar.draw_left = my_draw_left
    
    # add custom property to store scene names
    bpy.utils.register_class(PerScreenVariables)
    bpy.types.Screen.per_screen_vars = bpy.props.PointerProperty(type=PerScreenVariables)
    
    # register the timer function
    #context = bpy.context.window_manager.windows[-1]
    bpy.app.timers.register(proxyname)
    # Note: needs to first set the scene of whatever screen is currently displaying, because that one will get reset otherwise
    

def unregister():
    # unregister the timer function
    bpy.app.timers.unregister(proxyname)
    
    # now remove the class defining the custom property and how to access it
    del bpy.types.Screen.per_screen_vars
    bpy.utils.unregister_class(PerScreenVariables)
    
    # next restore the topbar
    bpy.types.TOPBAR_HT_upper_bar.draw_left = \
        bpy.types.TOPBAR_HT_upper_bar.default_draw_left
    
    # now reset the keymap & unregister the custom menu
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)        
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(WORKSPACE_OT_select)


if __name__ == "__main__":
    register()
    # execute the modal operator
    #bpy.ops.wm.modal_workspace_scene('INVOKE_DEFAULT')


