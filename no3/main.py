from OpenGL import GL
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame as pg
import numpy as np


class Triangle:
    def __init__(self):

        # x, y, z, r, b, b
        self.verticies = (
        -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
         0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
         0.0,  0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0
        )

        #Opengl only takes in 32bit float types for verticies
        self.verticies = np.array(self.verticies, dtype=np.float32)

        self.vertex_count = 3

        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)

        # tells opengl to generate one buffer, and it returns the index of the generated buffer
        self.vbo = GL.glGenBuffers(1)

        #
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.verticies.nbytes, self.verticies, GL.GL_STATIC_DRAW)

        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 32, GL.ctypes.c_voidp(0))

        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 32, GL.ctypes.c_voidp(12))

        GL.glEnableVertexAttribArray(2)
        GL.glVertexAttribPointer(2, 2, GL.GL_FLOAT, GL.GL_FALSE, 32, GL.ctypes.c_voidp(24))

    def destroy(self):

        GL.glDeleteVertexArrays(1, (self.vao,))
        GL.glDeleteBuffers(1, (self.vao,))


class Material:
    """Will hold a material"""
    
    def __init__(self, filepath):
        self.texture = GL.glGenTextures(1) # will generate a buffer inwhich a texture will be stored
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        
        # texture coordinate represented as (s, t)
        # below code repeats texture if coordinate outside of texture is requested
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)

        # minifying and magnifying filter
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

        image = pg.image.load(filepath).convert_alpha()
        image_width, image_height = image.get_rect().size
        image_data = pg.image.tostring(image, "RGBA")
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, image_width, image_height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_data)
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
        

    def use_texture(self):
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

    def destroy(self):
        GL.glDeleteTextures(1, (self.texture,))

class App:
    def __init__(self):

        pg.init()

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 5)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode((640,480), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        #initialize opengl
        GL.glClearColor(0.1,0.1,0.1,1)

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        print(GL.glGetString(GL.GL_VERSION))

        self.triangle = Triangle()
        self.shader = self.createShader(
            vert_shader_path="C:\\Dev\\Python\\OpenGL\\Tutorial\\no3\\shaders\\vertex.glsl",
            frag_shader_path="C:\\Dev\\Python\\OpenGL\\Tutorial\\no3\\shaders\\fragment.glsl"
        )

        GL.glUseProgram(self.shader)
        GL.glUniform1i(GL.glGetUniformLocation(self.shader, "imageTexture"), 0)
        self.material = Material("textures/cat.png")

        self.main()

    def createShader(self, vert_shader_path, frag_shader_path):

        with open(vert_shader_path, "rt") as file:
            vert_src = file.readlines()

        with open(frag_shader_path, "rt") as file:
            frag_src = file.readlines()
        vs = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        vert = compileShader(vert_src, GL.GL_VERTEX_SHADER)
        frag = compileShader(frag_src, GL.GL_FRAGMENT_SHADER)
        # print(f"vert: {vert}\nfrag: {frag}")
        shader = compileProgram(
            vert,
            frag
        )
        print(str(shader))
        return shader

    def main(self):
        running = True
        while(running):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False

            GL.glClear(GL.GL_COLOR_BUFFER_BIT)

            GL.glUseProgram(self.shader)
            self.material.use_texture()
            GL.glBindVertexArray(self.triangle.vao)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.triangle.vertex_count)

            pg.display.flip()

            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.material.destroy()
        self.triangle.destroy()
        GL.glDeleteProgram(self.shader)
        pg.quit()

if __name__ == "__main__":
    app = App()
