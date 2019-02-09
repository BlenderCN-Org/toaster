import bpy
# Have to import everything with classes which need to be registered

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

class CustomRenderEngine(bpy.types.RenderEngine):
    # These three members are used by blender to set up the
    # RenderEngine; define its internal name, visible name and capabilities.
    bl_idname = "custom_renderer"
    bl_label = "Flat Color Renderer"
    bl_use_preview = True

    # This is the only method called by blender, in this example
    # we use it to detect preview rendering and call the implementation
    # in another method.
    def render(self, sc):
        print("Hello, rendering")
        scene=bpy.data.scenes[0]
        scale = scene.render.resolution_percentage / 100.0
        self.size_x = int(scene.render.resolution_x * scale)
        self.size_y = int(scene.render.resolution_y * scale)

        if self.is_preview:
            self.render_preview(scene)
        else:
            self.render_scene(scene)

    # In this example, we fill the preview renders with a flat green color.
    def render_preview(self, scene):
        pixel_count = self.size_x * self.size_y

        # The framebuffer is defined as a list of pixels, each pixel
        # itself being a list of R,G,B,A values
        green_rect = [[0.0, 1.0, 0.0, 1.0]] * pixel_count

        # Here we write the pixel values to the RenderResult
        result = self.begin_result(0, 0, self.size_x, self.size_y)
        layer = result.layers[0].passes["Combined"]
        layer.rect = green_rect
        self.end_result(result)

    # In this example, we fill the full renders with a flat blue color.
    def render_scene(self, scene):
        pixel_count = self.size_x * self.size_y

        # The framebuffer is defined as a list of pixels, each pixel
        # itself being a list of R,G,B,A values
        blue_rect = [[0.0, 0.0, 1.0, 1.0]] * pixel_count

        # Here we write the pixel values to the RenderResult
        result = self.begin_result(0, 0, self.size_x, self.size_y)
        layer = result.layers[0].passes["Combined"]
        layer.rect = blue_rect
        self.end_result(result)


def register():
    print("Hello, REGISTER*************")
    # Register the RenderEngine
    bpy.utils.register_class(CustomRenderEngine)

    # RenderEngines also need to tell UI Panels that they are compatible
    # Otherwise most of the UI will be empty when the engine is selected.
    # In this example, we need to see the main render image button and
    # the material preview panel.
    #from bl_ui import (
    #    properties_render,
    #    properties_material,
    #)
    #properties_render.RENDER_PT_render.COMPAT_ENGINES.add(CustomRenderEngine.bl_idname)
    #properties_material.MATERIAL_PT_preview.COMPAT_ENGINES.add(CustomRenderEngine.bl_idname)


def unregister():
    bpy.utils.unregister_class(CustomRenderEngine)

    #from bl_ui import (
    #    properties_render,
    #    properties_material,
    #)
    #properties_render.RENDER_PT_render.COMPAT_ENGINES.remove(CustomRenderEngine.bl_idname)
    #properties_material.MATERIAL_PT_preview.COMPAT_ENGINES.remove(CustomRenderEngine.bl_idname)


if __name__ == "__main__":
    register()