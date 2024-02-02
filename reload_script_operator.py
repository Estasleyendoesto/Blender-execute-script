bl_info = {
    "name": "Reload Script",
    "author" : "Estasleyendoesto",
    "description" : "Reload Modified Texts in Data API",
    "blender" : (4, 0, 0),
    "version" : (1, 0, 0),
    "location" : "F3 > text.reload_script",
    "warning" : "This operator reload all scripts modified on Text Data of current file",
    "category": "Misc",
}

import bpy

class ReloadScriptOperator(bpy.types.Operator):
    bl_idname = "text.reload_script"
    bl_label = "Reload Script"
    
    def execute(self, context):     
        for text in bpy.data.texts:
            if text.is_in_memory:
                continue
        
            if text.is_modified:
                with open(text.filepath, 'r') as fi:
                    new_text = fi.read()
                    
                text.from_string(new_text)  
                
                def get_area():
                    for screen in bpy.data.screens:
                        for area in screen.areas:
                            if area.type == "TEXT_EDITOR":
                                return area      
                
                context_override = {} 
                context_override["edit_text"] = text 
                
                space = next(space for space in get_area().spaces if space.type == "TEXT_EDITOR")
                context_override["space_data"] = space    
                
                with bpy.context.temp_override(**context_override):
                    bpy.ops.text.save()    
                    bpy.ops.text.run_script()
                    
                    self.report({"INFO"}, "Saved and reloaded: %s" % text.name)

                    
        return {'FINISHED'}
    
     
def register():
    bpy.utils.register_class(ReloadScriptOperator)
    
def unregister():
    bpy.utils.unregister_class(ReloadScriptOperator)
    
if __name__ == "__main__":
    register()