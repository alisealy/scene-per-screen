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


# Modal operator for changing scenes
class WM_OT_modal_workspace_scene(bpy.types.Operator):
    bl_idname = "wm.modal_workspace_scene"
    bl_label = "Each Workspace Remembers A Scene"
    
    def __init__(self):
        print("Start")
        
    def __del__(self):
        print("End")
    
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            if not (self.lastScreen == context.screen):
                # save the screen/scene pair for the previous workspace before we change anything
                self.lastScreen.per_screen_vars.scene = context.scene.name
                
                # if the remembered scene exists, switch to that.
                memory = context.screen.per_screen_vars.scene
                if memory in bpy.data.scenes:
                    context.window.scene = bpy.data.scenes[memory]
                # make a note of what screen we are on now
                self.lastScreen = context.screen
        
        return {'PASS_THROUGH'}
    
    def invoke(self, context, event):
        self.lastScreen = context.window.screen
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


# wrapper operator, sets a custom context and calls the modal operator
class WM_OT_modal_workspace_scene_wrapper(bpy.types.Operator):
    bl_idname = "wm.modal_workspace_scene_wrapper"
    bl_label = "dummy operator for modal_workspace_scene"
    
    def execute(self, context):
        win = context.window_manager.windows[0]
        override = {
            'window': win,
            'workspace': win.workspace,
            'screen': win.screen,
            'scene': win.scene
        }
        bpy.ops.wm.modal_workspace_scene(override, 'INVOKE_DEFAULT')
        return {'FINISHED'}


# addon preferences panel, with a button to start the modal operator
class testingAddOnPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator_context = 'INVOKE_DEFAULT'
        row.operator('wm.modal_workspace_scene_wrapper', text="enable automatic scene switching")


addon_keymaps = []


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
    
    # Now register the modal operator, wrapper, and preferences panel
    bpy.utils.register_class(WM_OT_modal_workspace_scene)
    bpy.utils.register_class(WM_OT_modal_workspace_scene_wrapper)
    bpy.utils.register_class(testingAddOnPreferences)
    
    # execute the modal operator (only use if running as a script)
    #bpy.ops.wm.modal_workspace_scene('INVOKE_DEFAULT')


def unregister():
    # First un-register the modal operator
    bpy.utils.unregister_class(testingAddOnPreferences)
    bpy.utils.unregister_class(WM_OT_modal_workspace_scene_wrapper)
    bpy.utils.unregister_class(WM_OT_modal_workspace_scene)
    
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


