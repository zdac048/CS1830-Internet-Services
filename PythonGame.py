import simplegui
import math

KEYDOWNR = False
KEYDOWNL = False
KEYDOWNU = False
KEYDOWND = False
KEYUPR = False
KEYUPL = False
KEYUPU = False
KEYUPD = False
pause = False

CANVAS_DIMS = (800, 600)
HORIZON_HEIGHT = CANVAS_DIMS[1]*0.6

class Vector:   
    def __init__(self, p=(0,0)):
        self.x = p[0]
        self.y = p[1]
        
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return not self.__eq__(other) 

    def getP(self):
        return (self.x, self.y)
    
    def copy(self):
        return Vector((self.x, self.y))
    
    def mult(self, k):
        self.x *= k
        self.y *= k
        return self
    
    def div(self, k):
        self.x /= k
        self.y /= k 
        return self 
    
    def normalise(self):
        self.x / self.length() 
        self.y/self.length()
        return self 
    
    def getNormalised(self):
        copy = self.copy()
        return copy.normalise()
    
    def add(self, other):
        self.x += other.getP()[0]
        self.y += other.getP()[1]
        return self
    
    def sub(self, other):
        self.x -= other[0]
        self.y -= other[1]
        return self

    def negate(self):
        self.x = -self.x
        self.y = -self.y
        return self
    
    def dot(self, other):
        return self.x * other[0] + self.y * other[1]
   
    def length(self):
        return math.sqrt(self.lengthSquared())
    
    def lengthSquared(self):
        return self.x * self.x + self.y * self.y
        return self
        
    """def reflect(self, normal):
        pass

    def angle(self, other):
        self = self.dot(other)  
        return self
        self = self.lengthSquared(self) 
        return self"""
##################################################################################################################
class Actor(object):
    actor_list = []
    def __init__(self, position, row, column, image):
        #Actor.actor_list.append(self)
        self.row = row
        self.column = column
        self.img = simplegui.load_image(image)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.frameheight = self.height/row
        self.framewidth = self.width/column
        self.framecentreX = self.framewidth/2
        self.framecentreY = self.frameheight/2
        self.frameIndex = (0, 0)
        
        self.player_position = position
        self.idle = True
        self.walking = False
        self.punching = False
        self.blocking = False
       
    def update(self):
        #chese work on this
        self.player_velocity = Vector()
        if keyboard.down:
            self.player_velocity.add(Vector((0, 10))) 
        if keyboard.up:
            self.player_velocity.add(Vector((0, -10))) 
        if keyboard.left:
            self.player_velocity.add(Vector((-10, 0))) 
        if keyboard.right:
            self.player_velocity.add(Vector((10, 0))) 
        self.player_position.add(self.player_velocity)
        
    def draw(self, canvas, i, j):
        canvas.draw_image(self.img, (self.framewidth*self.frameIndex[0]+self.framecentreX,
                          self.frameheight*self.frameIndex[1]+self.framecentreY), 
                         (self.framewidth, self.frameheight), 
                         (i, j), 
                         (self.framewidth, self.frameheight))
    
    
    def nextFrame(self):
            newx = self.frameIndex[0] + 1

            if newx == self.column:
                newy = self.frameIndex[1] +1
                newx = 0
            else:
                newy = self.frameIndex[1]

            if newy == self.row:
                newy = 0 

            self.frameIndex = (newx, newy) 
            
            
class Player(Actor):
    pass

class Enemy(Actor):
    def update(self):
        pass
            
class Game:
    def __init__(self):
        self.showing_menu = True
        self.running_1p_game = False
        self.running_2p_game = False
        self.showing_score = False
        self.respawn = False
    
    def game_start(self): 
        self.player1 = Player(Vector((CANVAS_DIMS[0]/2, CANVAS_DIMS[1]/2)), 1, 3, 'http://opengameart.org/sites/default/files/styles/medium/public/blue_ninja_0.png')
        self.game_timer = simplegui.create_timer(50, self.gameloop_handler)
        self.game_timer.start()
        
    def gameloop_handler(self):
        self.player1.update()
            
    def draw(self, canvas):
        global KEYDOWNR
        global KEYDOWNL
        global KEYDOWNU
        global KEYDOWND
        global KEYUPR
        global KEYUPL
        global KEYUPU
        global KEYUPD
        if self.showing_menu:
            #ajaz work on this
            frame.set_canvas_background('Aqua')
            canvas.draw_text('Fisticuffs Multiplayer or Single Game', (CANVAS_DIMS[0]/2-315, 80), 30, 'Red', 'monospace')
            canvas.draw_line([CANVAS_DIMS[0]/2-120,250],[CANVAS_DIMS[0]/2+120,250],55,'Red')
            canvas.draw_text('Single', [CANVAS_DIMS[0]/2-70,250+12], 45, 'Silver', 'monospace')
            canvas.draw_line([CANVAS_DIMS[0]/2-120,350],[CANVAS_DIMS[0]/2+120,350],55,'Red') 
            canvas.draw_text('Multiplayer', [CANVAS_DIMS[0]/2-112,360], 38 , 'Silver', 'monospace') 
            self.respawn = False
            
        if self.running_1p_game:
            canvas.draw_polygon([(0, 0), (CANVAS_DIMS[0], 0), (CANVAS_DIMS[0], CANVAS_DIMS[1]/3*2), (0, CANVAS_DIMS[1]/3*2)], 12, 'Aqua', 'Aqua')
            canvas.draw_polygon([(0, CANVAS_DIMS[1]/3*2), (CANVAS_DIMS[0], CANVAS_DIMS[1]/3*2), (800, CANVAS_DIMS[1]), (0, CANVAS_DIMS[1])], 12, 'Green', 'Green')
            if self.respawn:
                self.player1.draw(canvas, self.player1.player_position.getP()[0], self.player1.player_position.getP()[1]) 
                
            canvas.draw_text("Lives: 5", [CANVAS_DIMS[0]-120, 20], 25, 'Blue', 'monospace')
            canvas.draw_text("Score: 0", [CANVAS_DIMS[0]-280, 20], 25, 'Blue', 'monospace')
            
            
            if KEYDOWNR or KEYDOWNL or KEYDOWNU or KEYDOWND:
                if clock.transition(5):
                    self.player1.nextFrame()
                clock.tick()
                
        if self.running_2p_game:
            print 'yo'

    def mouse(self, pos): 
        global pause
        if self.showing_menu:
            pause = False 
            if (CANVAS_DIMS[0]/2-120<pos[0]<CANVAS_DIMS[0]/2+120) and (220<pos[1]<277): 
                self.showing_menu = False
                self.running_1p_game = True
                self.add_buttons = True
                self.respawn = True
                game.game_start()

                
        if self.showing_menu:
            #pause = False 
            if (CANVAS_DIMS[0]/2-120<pos[0]<CANVAS_DIMS[0]/2+120) and (319<pos[1]<376): 
                self.showing_menu = False
                self.running_2p_game = True
                self.respawn = True
                
    def quit(self):
        global pause 
        pause = True
        self.showing_menu = True
        self.running_1p_game = False
        self.running_2p_game = False
        self.showing_score = False
        self.game_timer.stop()

      
    def pause(self):
        global pause
        pause = True 
        KEYDOWNR = False
        KEYDOWNL = False
        KEYDOWNU = False
        KEYDOWND = False
    
    def resume(self):
        global pause
        pause = False
        resume = True
        KEYDOWNR = True
        KEYDOWNL = False 
        KEYDOWNU = False
        KEYDOWND = True       
        
class Keyboard:
    def __init__(self):
        self.down = False
        self.up = False
        self.left = False
        self.right = False
        self.o = False
        self.p = False
        self.w = False
        self.s = False
        self.a = False
        self.d = False
        self.f = False
        self.g = False
    
    def key_down(self, key):
        global KEYDOWNR
        global KEYDOWNL
        global KEYDOWNU
        global KEYDOWND
        global KEYUPR
        global KEYUPL
        global KEYUPU
        global KEYUPD
        global pause
        global resume
        global KEYUP
        global KEYDOWN
        
        
        if not pause:
            if key == simplegui.KEY_MAP['right']:
                self.right = True
                KEYDOWNR = True
                KEYUPR = False

            if key == simplegui.KEY_MAP['left']:
                self.left = True
                KEYDOWNL = True
                KEYUPL = False

            if key == simplegui.KEY_MAP['up']:
                self.up = True
                KEYDOWNU = True
                KEYUPU = False

            if key == simplegui.KEY_MAP['down']:
                self.down = True
                KEYDOWND = True
                KEYUPD = False

            if key == simplegui.KEY_MAP['o']:
                self.o = True               
                KEYDOWN = True
                KEYUP = False

            if key == simplegui.KEY_MAP['p']:
                self.p = True
                KEYDOWN = True
                KEYUP = False

            if key == simplegui.KEY_MAP['w']:
                self.w = True 
                KEYDOWN = True
                KEYUP = False

            if key == simplegui.KEY_MAP['s']:
                self.s = True
                KEYDOWN = True
                KEYUP = False

            if key == simplegui.KEY_MAP['a']:
                self.a = True
                KEYDOWN = True
                KEYUP = False

            if key == simplegui.KEY_MAP['d']:
                self.d = True
                KEYDOWN = True
                KEYUP = False

            if key == simplegui.KEY_MAP['f']:
                self.f = True 
                KEYDOWN = True
                KEYUP = False

            if key == simplegui.KEY_MAP['g']:
                self.g = True 
                KEYDOWN = True
                KEYUP = False
            
            
    def key_up(self, key):
        global KEYDOWNR
        global KEYDOWNL
        global KEYDOWNU
        global KEYDOWND
        global KEYUPR
        global KEYUPL
        global KEYUPU
        global KEYUPD
        global pause
        global resume
        global KEYUP
        global KEYDOWN
        
        if not pause:
            if key == simplegui.KEY_MAP['right']:
                self.right = False
                KEYUPR = True
                KEYDOWNR = False

            if key == simplegui.KEY_MAP['left']:
                self.left = False
                KEYUPL = True
                KEYDOWNL = False


            if key == simplegui.KEY_MAP['up']:
                self.up = False
                KEYUPY = True
                KEYDOWNU = False

            if key == simplegui.KEY_MAP['down']:
                self.down = False
                KEYUPD = True
                KEYDOWND = False

            if key == simplegui.KEY_MAP['o']:
                self.o = False   
                KEYUP = True
                KEYDOWN = False

            if key == simplegui.KEY_MAP['p']:
                self.p = False
                KEYUP = True
                KEYDOWN = False

            if key == simplegui.KEY_MAP['w']:
                self.w = False 
                KEYUP = True
                KEYDOWN = False

            if key == simplegui.KEY_MAP['s']:
                self.s = False
                KEYUP = True
                KEYDOWN = False

            if key == simplegui.KEY_MAP['a']:
                self.a = False
                KEYUP = True
                KEYDOWN = False

            if key == simplegui.KEY_MAP['d']:
                self.d = False
                KEYUP = True
                KEYDOWN = False

            if key == simplegui.KEY_MAP['f']:
                self.f = False 
                KEYUP = True

            if key == simplegui.KEY_MAP['g']:
                self.g = False
                KEYUP = True

            
class Clock: 
    def __init__(self):
        self.time = 0
        self.increment = 1

    def tick(self):
        self.time += self.increment 
        
    def transition(self, frameDuration):
        return self.time % frameDuration == 0
    
                      
class Interaction:
    pass

clock = Clock()
keyboard = Keyboard()
game = Game()
frame = simplegui.create_frame("SpiritImage", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.add_button("Pause", game.pause, 100)
frame.add_button("Resume", game.resume, 100)
frame.add_button("Quit", game.quit, 100)
frame.set_keydown_handler(keyboard.key_down)
frame.set_keyup_handler(keyboard.key_up)
frame.set_draw_handler(game.draw)
frame.set_mouseclick_handler(game.mouse)
game.game_start()
frame.start()