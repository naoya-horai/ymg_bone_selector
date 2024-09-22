# import library
import bpy
from bpy.types import Panel,Operator,PropertyGroup

# basic info
bl_info = {
   "name": "ymg_bone_selector",
   "author": "ymgmcmc",
   "version": (1, 0, 0),
   "blender": (4, 2, ),
   "location": "3D View",
   "description": "ymgmcmc",
   "warning": "",
   "support": "COMMUNITY",
   "wiki_url": "",
   "tracker_url": "",
   "category": "Object"
}

#init props
class MyInputs(PropertyGroup):
    armaturename:bpy.props.StringProperty(
        name="Armature_Name",
        subtype="ARMATURE NAME",
        defaule="Armature"
    )

    deselectall:bpy.props.BoolProperty(
        name="deselect_all",
        default=False
    )
   
#init panels
class MainPanel(Panel):
    bl_label = "ymg_bone_selector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ymgaddon"


    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.myinputs,"armaturename")
        layout.prop(context.scene.myinputs,"deselectall")
        layout.operator(BONE_Selector.bl_idname, text="select")

#select bone
class BONE_Selector(Operator):
    bl_idname = "ymg_bone_selector.operator"
    bl_label = "Select"
    
    def execute(self, context):
        root_name = context.scene.myinputs.armaturename
        vertex_groups = []

        selected_objects = bpy.context.selected_objects

        for selected_object in selected_objects:
            vertex_groups.append(selected_object.vertex_groups)

        if context.scene.myinputs.deselectall:
            for bone in bpy.data.objects[root_name].data.bones:
                bone.select = False
                bone.select_head = False
                bone.select_tail = False

        for v_groups in vertex_groups:
            for v_group in v_groups:
                print(v_group.name)
                bone = bpy.data.objects[root_name].data.bones[v_group.name]
                bone.select = True
                bone.select_head = True
                bone.select_tail = True
                while bone.parent:
                    nb = bone.parent
                    nb.select = True
                    nb.select_head = True
                    nb.select_tail = True
                    bone = nb
        return {"FINISHED"}
        
#class list for register
classes = [MyInputs,MainPanel,BONE_Selector]

#register to blender
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.myinputs = bpy.props.PointerProperty(type=MyInputs)


#unregister from blender
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.myinputs

#entry point
if __name__ == "__main__":
    register()

        