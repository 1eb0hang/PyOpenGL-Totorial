from OpenGL import GL
from OpenGL.GL import shaders #import compileProgram, compileShader
import pygame as pg
import numpy as np

class Triangle:
    def __init__(self):

        # x, y, z, r, b, b
        self.verticies = (
        -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
         0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
         0.0,  0.5, 0.0, 0.0, 0.0, 1.0
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
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, GL.ctypes.c_voidp(0))

        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, GL.ctypes.c_voidp(12))

    def destroy(self):

        GL.glDeleteVertexArrays(1, (self.vao,))
        GL.glDeleteBuffers(1, (self.vao,))


class App:
    def __init__(self):

        pg.init()

        pg.display.set_mode((640,480), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        #initialize opengl
        GL.glClearColor(0.1,0.1,0.1,1)

        print(GL.glGetString(GL.GL_VERSION))

        self.triangle = Triangle()
        self.shader = self.createShader(
            vert_shader_path="C:\\Dev\\Python\\OpenGL\\Tutorial\\no2\\vertex.glsl",
            frag_shader_path="C:\\Dev\\Python\\OpenGL\\Tutorial\\no2\\fragment.glsl"
        )

        GL.glUseProgram(self.shader)

        self.main()

    def createShader(self, vert_shader_path, frag_shader_path):

        with open(vert_shader_path, "rt") as file:
            vert_src = file.readlines()

        with open(frag_shader_path, "rt") as file:
            frag_src = file.readlines()
        vs = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        fs = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)

        print(f"vs: {vs}\nfs: {fs}\n")
        
        vs_obj = GL.glShaderSource(vs, "".join(vert_src))
        fs_obj = GL.glShaderSource(fs, "".join(frag_src))
        
        print(f"vs_obj: {vs_obj}\nfs_obj: {fs_obj}\n")

        vs_shader = GL.glCompileShader(vs)
        fs_shader = GL.glCompileShader(fs)

        print(f"vs_shader: {vs_shader}\nfs_shader: {fs_shader}\n")

        program = GL.glCreateProgram()
        GL.glAttachShader(program, vs)
        GL.glAttachShader(program, fs)

        GL.glLinkProgram(program)

        GL.glValidateProgram(program)

        #vert = compileShader(vert_src, GL.GL_VERTEX_SHADER)
        #frag = compileShader(frag_src, GL.GL_FRAGMENT_SHADER)
        # print(f"vert: {vert}\nfrag: {frag}")
        
        
        #shader = compileProgram(
        #    vert,
        #    frag
        #)
        print(str(program))
        return program

    def main(self):
        running = True
        while(running):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False

            GL.glClear(GL.GL_COLOR_BUFFER_BIT)

            GL.glUseProgram(self.shader)
            GL.glBindVertexArray(self.triangle.vao)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.triangle.vertex_count)

            pg.display.flip()

            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.triangle.destroy()
        GL.glDeleteProgram(self.shader)
        pg.quit()

if __name__ == "__main__":
    app = App()
