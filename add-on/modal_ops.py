bl_info = {
    "name": "testing_modal_switching",
    "category": "Interface",
    "blender": (2, 80, 0)
}


import bpy


# Custom property to store scene-per-screen
class PerScreenVariables(bpy.types.PropertyGroup):
    scene: bpy.props.StringProperty(
        name="scenePerScreen",
        description="the scene for each screen (for backwards compatability with 2.79)",
        default="Scene"
    )


# Modal operator for changing scenes
class ModalWorkspaceScene(bpy.types.Operator):
    bl_idname = "wm.modal_workspace_scene"
    bl_label = "Each Workspace Remembers A Scene"
    
    def __init__(self):
        print("Start")
        
    def __del__(self):
        print("End")
    
    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            if not (self.lastWorkspace == context.workspace):
                self.keepingTrack[self.lastWorkspace] = context.scene
                if context.workspace in self.keepingTrack.keys():
                    context.window.scene = self.keepingTrack[context.workspace]
                else:
                    self.keepingTrack[context.workspace] = context.scene
                self.lastWorkspace = context.workspace
        
        return {'PASS_THROUGH'}
    
    def invoke(self, context, event):
        self.keepingTrack = {context.workspace:context.scene}
        self.lastWorkspace = context.workspace
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
    

def register():
    print("step1")
    # add custom property to store scene names
    bpy.utils.register_class(PerScreenVariables)
    bpy.types.Screen.per_screen_vars = bpy.props.PointerProperty(type=PerScreenVariables)
    print("step2")
    # Now register the modal operator
    bpy.utils.register_class(ModalWorkspaceScene)
    print("step3")
    #run the modal operator
    #bpy.ops.wm.modal_workspace_scene('INVOKE_DEFAULT')
    

def unregister():
    # First un-register the modal operator
    bpy.utils.unregister_class(ModalWorkspaceScene)
    
    # now remove the class defining the custom property and how to access it (data is still stored in .blend file though)
    del bpy.types.Screen.per_screen_vars
    bpy.utils.unregister_class(PerScreenVariables)
    
    
if __name__ == "__main__":
    register()
    
    
    
