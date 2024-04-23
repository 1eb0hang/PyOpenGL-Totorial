import os

# TODO:move to file
class SimpleComponet:
    import np
    def __init__(self, psoition, velocity):
        self.position = np.array(position, dtype=np.float32)
        self.velocity = np.array(velocity, dtype=np.float32)


# TODO:move to file
class SentientComponent:
    import np
    def __init__(self, position, eulers, health):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.velocity = np.array([0,0,0], dtype=np.float32)
        self.state = "stable" #probably make into enum class
        self.health = health # int
        self.canShoot = True
        self.reloading = False
        self.reloadTime = 0

# TODO:move to file
class Scene:
    def __init__(self):
        self.enemy_spawn_rate= 0.1
        self.powerups_spawn_rate= 0.05
        self.enemy_shoot_rate = 0.1
        self.player = SentientComponent(
            position=[0,0,0],
            eulers=[0 90, 0],
            health=36
        )

        self.enemies = []
        self.bullets=[]
        self.powerups=[]

    def update(self, rate):
        pass

    def move_player(self, sPos):
        pass


# TODO:move to file
class App:
    import pygame as pg
    def __init__(self, screen_width, screen_height):
        self.witdh, self.height =  screen_width, screen_height
        
        self.renderer = GraphicsEngine()
        
        self.scene = Scene()

        self.last_time = pg.time.get_ticks()
        self.current_time = 0
        self.num_frames = 0
        self.frame_rate = 0
        self.light_count = 0

        self.main_loop()
        
    
    def main_loop(self):
        running = True
        while(running):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
                elif (event.type == PG.KEYDOWN):
                    if (event.key == pg.K_ESCAPE):
                        running = False
            
            self.handle_keys()
            self.scene.update(self.frame_time*0.05)
            self.renderer.render(self.scene)

            self.calculate_frame_rate()
        
        self.quit()
    
    def handle_keys(self):
        keys = pg.key.get_pressed()


    def calculate_frame_rate(self):
        self.current_time = pg.time.get_ticks()
        delta = self.current_time - self.last_time
    
        if(delta >= 1000):
            


    def quit(self):
        pass

def Main():
    pass

if __name__ == "__main__":
    Main()
