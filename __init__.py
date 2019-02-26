import bpy

# Have to import everything with classes which need to be registered
#from . euclid import *
from . engine.toaster import ToasterRenderEngine
#from bl_ui.properties_render import RENDER_PT_render

bl_info = {
    "name": "Toaster",
    "author": "Jean-Francois Romang (jromang)",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "category": "Render",
    "location": "Info header, render engine menu",
    "description": "Toaster renderer",
    "warning": "",
    "wiki_url": "https://github.com/jromang/toaster/wiki",
    "tracker_url": "https://github.com/jromang/toaster/issues/new",
}

def draw_panel(self, context):
    layout = self.layout
    scene = context.scene

    if context.engine=="toaster_renderer":
        view = context.space_data
        cscene = scene.cycles
        layout.prop(cscene, "preview_pause", icon="PAUSE", text="")


def register():
    print("Hello, REGISTER*************")
    # Register the RenderEngine
    bpy.utils.register_class(ToasterRenderEngine)

    # RenderEngines also need to tell UI Panels that they are compatible
    # Otherwise most of the UI will be empty when the engine is selected.
    # In this example, we need to see the main render image button and
    # the material preview panel.
    #from bl_ui import (
    #    properties_render,
        #properties_material,
    #)
    #properties_render.RENDER_PT_render.COMPAT_ENGINES.add(ToasterRenderEngine.bl_idname)
    bpy.types.RENDER_PT_context.append(draw_panel)
    #properties_material.MATERIAL_PT_preview.COMPAT_ENGINES.add(CustomRenderEngine.bl_idname)


def unregister():
    bpy.utils.unregister_class(ToasterRenderEngine)

    #from bl_ui import (
    #    properties_render,
    #    properties_material,
    #)
    #properties_render.RENDER_PT_render.COMPAT_ENGINES.remove(CustomRenderEngine.bl_idname)
    bpy.types.RENDER_PT_context.remove(draw_panel)
    #properties_material.MATERIAL_PT_preview.COMPAT_ENGINES.remove(CustomRenderEngine.bl_idname)


if __name__ == "__main__":
    register()
