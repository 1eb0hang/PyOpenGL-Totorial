from OpenGL import GL
import pygame as pg

class App:
    def __init__(self):

        pg.init()
        pg.display.set_mode((640,480), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        #initialize opengl
        GL.glClearColor(0.1,0.1,0.1,1)

        self.main()

    def main(self):
        running = True
        while(running):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False

            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
            pg.display.flip()

            self.clock.tick(60)
        self.quit()

    def quit(self):
        pg.quit()

if __name__ == "__main__":
    app = App()
