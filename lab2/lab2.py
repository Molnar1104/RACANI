import pyglet
import os
import random



fire_texture = pyglet.image.load("vatra_transparent2.png")
smoke_texture = pyglet.image.load("smoke_transparent.png")
# image = pyglet.resource.image("vatra.png")
grid = pyglet.image.ImageGrid(fire_texture, rows = 8, columns=8)
reordered_frames = []

for row in reversed(range(4)):
    for col in range(4):
        frame = grid[(3 - row) * 4 + col]
        reordered_frames.append(frame)
grid = reordered_frames
frames = [pyglet.image.AnimationFrame(image, 0.1) for image in grid]  
fire_animation = pyglet.image.Animation.from_image_sequence(grid, duration=0.05, loop = True) 

class FireParticle:
    def __init__(self, x, y, lifespan):
        self.x = x
        self.y = y
        self.lifespan = lifespan
        self.alive = True
        fire_sprite = pyglet.sprite.Sprite(fire_animation, x = self.x, y = self.y)
        self.sprite = fire_sprite
        self.sprite.scale = 3.0
        self.sprite.opacity = 255
    def update(self, dt):
        if self.alive:
            self.lifespan -= dt
            if self.lifespan <= 0:
                self.alive = False
            self.x += random.uniform(-1, 1)
            self.y += random.uniform(-0.5,0.5)
    def draw(self):
        if self.alive:
            self.sprite.x = self.x
            self.sprite.y = self.y
            # self.sprite.scale = random.uniform(0.95, 1.05) 
            self.sprite.scale = 1

            self.sprite.draw()
            # pyglet.graphics.draw(1,pyglet.gl.GL_POINTS, ("v2f", (self.x, self.y)))

class SmokeParticle:
    def __init__(self, x, y, lifespan):
        self.x = x
        self.y = y
        self.lifespan = lifespan
        self.alive = True
        self.velocity_y = random.uniform(0.5, 1.5) 
        self.sprite = pyglet.sprite.Sprite(smoke_texture, x=self.x, y=self.y)
        self.sprite.opacity = random.randint(140, 195)

    def update(self, dt):
        if self.alive:
            self.lifespan -= dt
            if self.lifespan <= 0:
                self.alive = False
            self.y += self.velocity_y  
            self.sprite.opacity = max(0, self.sprite.opacity - 1)

    def draw(self):
        if self.alive:
            self.sprite.x = self.x
            self.sprite.y = self.y
            self.sprite.scale = 0.75
            self.sprite.draw()

class FireParticleEmitter:
    def __init__(self):
        self.particles = []

    def emit(self, x, y):
        self.particles.append(FireParticle(x, y, random.uniform(2.0, 3.0)))

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self):
        for particle in self.particles:
            particle.draw()

class SmokeParticleEmitter:
    def __init__(self):
        self.particles = []

    def emit(self, x, y):
        self.particles.append(SmokeParticle(x, y, random.uniform(3.0, 4.0)))

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        self.particles = [p for p in self.particles if p.alive]

    def draw(self):
        for particle in self.particles:
            particle.draw()


window  = pyglet.window.Window(width = 800, height = 600)
fire_emitter = FireParticleEmitter()
smoke_emitter = SmokeParticleEmitter()
# print(f'Current working directory: {os.getcwd()}')
offset = 50
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    fire_emitter.emit(x, y) 
    smoke_emitter.emit(x, y + offset)
@window.event
def on_draw():
    window.clear()
    # pyglet.gl.glClearColor(1, 1, 1, 1) 

    fire_emitter.draw()
    smoke_emitter.draw()

def update(dt):
    fire_emitter.update(dt)
    smoke_emitter.update(dt)

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()