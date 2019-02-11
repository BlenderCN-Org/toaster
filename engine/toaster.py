import bpy


# http://excamera.com/sphinx/article-srgb.html
def s2lin(x):
    a = 0.055
    return x * (1.0 / 12.92) if x <= 0.04045 else pow((x + a) * (1.0 / (1 + a)), 2.4)


def lin2s(x):
    a = 0.055
    return x * 12.92 if x <= 0.0031308 else (1 + a) * pow(x, 1 / 2.4) - a


class ToasterRenderEngine(bpy.types.RenderEngine):
    # These three members are used by blender to set up the
    # RenderEngine; define its internal name, visible name and capabilities.
    bl_idname = "toaster_renderer"
    bl_label = "Toaster"
    bl_use_preview = True

    # This is the only method called by blender, in this example
    # we use it to detect preview rendering and call the implementation
    # in another method.
    def render(self, sc):

        scene=bpy.data.scenes[0]
        scale = scene.render.resolution_percentage / 100.0
        self.size_x = int(scene.render.resolution_x * scale)
        self.size_y = int(scene.render.resolution_y * scale)
        print("Rendering " + str(self.size_x) + "x" + str(self.size_y) + " ("+ str(scale) +" scale)")

        if self.is_preview:
            self.render_preview(scene)
        else:
            self.render_colors(scene)

    def render_colors(self, scene):
        nx = self.size_x
        ny = self.size_y
        pixel_count = self.size_x * self.size_y

        # The framebuffer is defined as a list of pixels, each pixel
        # itself being a list of R,G,B,A values
        framebuffer = [(0.0, 0.0, 0.0, 1.0)]*pixel_count

        # Here we write the pixel values to the RenderResult
        result = self.begin_result(0, 0, self.size_x, self.size_y)

        layer = result.layers[0].passes["Combined"]
        pixel = 0

        for j in range(0, ny):
            for i in range(0, nx):
                r = float(i) / float(nx)
                g = float(j) / float(ny)
                b = float(0.2)

                framebuffer[pixel]=(s2lin(r), s2lin(g), s2lin(b), 1.0)
                pixel+=1

            if j % 100 == 0 :
                layer.rect=framebuffer
                self.update_result(result)

        layer.rect = framebuffer
        self.end_result(result)

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
