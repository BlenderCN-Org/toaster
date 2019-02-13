import bpy
from math import  sqrt
from mathutils import Vector, Color
from . ray import Ray


# http://excamera.com/sphinx/article-srgb.html
def s2lin(color):
    a = 0.055
    return Color([x * (1.0 / 12.92) if x <= 0.04045 else pow((x + a) * (1.0 / (1 + a)), 2.4) for x in color])


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

    def color(self, ray):
        t= self.hit_sphere(Vector((0, 0, -1)), 0.5, ray)
        if t > 0:
            N=Vector(ray.point_at_parameter(t)-Vector((0,0,-1))).normalized()
            return(Color( (N+Vector((1,1,1))) * 0.5 ))


        # blend the y-value of direction
        unit_direction = ray.direction.normalized()
        t = 0.5 * (unit_direction.y + 1.0)
        return Color(Vector((1.0, 1.0, 1.0)).lerp(Vector((0.5, 0.7, 1.0)), t))

    def hit_sphere(self, center, radius, ray):

        oc = ray.origin - center
        a = ray.direction.dot(ray.direction)
        b = 2 * oc.dot(ray.direction)
        c = oc.dot(oc) - radius * radius

        discriminant = b * b - 4 * a * c

        if discriminant < 0: return -1.0
        else: return (-b - sqrt(discriminant)) / (2 * a)


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

        lower_left_corner = Vector((-2.0, -1.0, -1.0))
        horizontal = Vector((4.0, 0.0, 0.0))
        vertical = Vector((0.0, 2.0, 0.0))
        origin = Vector((0.0, 0.0, 0.0))

        for j in range(0, ny):
            for i in range(0, nx):
                u = float(i) / float(nx)
                v = float(j) / float(ny)

                # simple camera
                ray = Ray(origin=origin, direction=lower_left_corner + horizontal * u + vertical * v)
                col = self.color(ray)

                # update framebuffer
                col = s2lin(col)
                framebuffer[pixel] = (col.r, col.g, col.b, 1.0)
                pixel += 1

            if j % 100 == 0 :
                layer.rect=framebuffer
                self.update_result(result)

        layer.rect = framebuffer
        self.end_result(result)
