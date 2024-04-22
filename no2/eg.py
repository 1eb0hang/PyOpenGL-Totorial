from OpenGL import GL
# from OpenGL.GL.shaders import compileProgram, compileShader
import pygame as pg
import numpy as np

if __name__ == "__main__":
    pg.init()
    pg.display.set_mode((640,480), pg.OPENGL|pg.DOUBLEBUF)
    clock = pg.time.Clock()
    GL.glClearColor(0.2,0.2,0.2,1.0)

    positions = (
         0.0,  0.5,
        -0.5, -0.5,
         0.5, -0.5
    )
    positions = np.array(positions, dtype=np.float32)

    id = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, id)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, positions.nbytes, positions, GL.GL_STATIC_DRAW)

    GL.glEnableVertexAttribArray(0)
    GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, GL.GL_FALSE, 8, GL.ctypes.c_voidp(0))

    with open("vert2.glsl", "rt") as file:
        vert_src = file.readlines()

    with open("frag2.glsl", "rt") as file:
        frag_src = file.readlines()

    # shader = compileProgram(
    #     compileShader(vert, GL.GL_VERTEX_SHADER),
    #     compileShader(frag, GL.GL_FRAGMENT_SHADER)
    # )
    program = GL.glCreateProgram()
    vert_id = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    frag_id = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)

    vert = GL.glCompileShader(GL.GL_VERTEX_SHADER, vert_id)
    GL.glShaderSource(vert_id, len(''.join(vert_src)), )


    frag = GL.glCompileShader(GL.GL_FRAGMENT_SHADER, frag_id)
    GL.glAttachShader(program, vert)
    GL.glAttachShader(program, frag)
    GL.glLinkProgram(program)
    GL.ValidateProgram(program)

    # GL.glDeleteShader(vert)
    # GL.glDeleteShader(frag)
    GL.glUseProgram(program)

    running = True
    while(running):
        for event in pg.event.get():
            if (event.type == pg.QUIT):
                running = False

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        pg.display.flip()

        clock.tick(60)

    # self.triangle.destroy()
    GL.glDeleteBuffers(1, [id])
    GL.glDeleteProgram(program)
    pg.quit()
