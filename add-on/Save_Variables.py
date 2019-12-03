bl_info = {
    'name': 'Saved Variables',
    'category': 'All'
}

import bpy

class SamplePanel(bpy.types.Panel):
    bl_idname = "panel.sample_panel"
    bl_label = "Panel for variable change"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        self.layout.prop(bpy.context.screen.sample_vars, 'variable1')
        self.layout.prop(bpy.context.screen.sample_vars, 'variable2')

class SampleVariables(bpy.types.PropertyGroup):
    variable1: bpy.props.IntProperty(
        name="Var1",
        description="Sample variable 1",
        default=2
    )
    variable2: bpy.props.BoolProperty(
        name="Var2",
        description="Sample variable 2",
        default=True
    )

def register():
    bpy.utils.register_class(SamplePanel)
    bpy.utils.register_class(SampleVariables)
    bpy.types.Screen.sample_vars = bpy.props.PointerProperty(type=SampleVariables)

def unregister():
    del bpy.types.Screen.sample_vars
    bpy.utils.unregister_class(SampleVariables)
    bpy.utils.unregister_class(SamplePanel)

if __name__ == "__main__":
    register()