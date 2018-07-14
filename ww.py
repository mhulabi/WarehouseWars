import pygame
import pygame.mixer
import time
sounds = pygame.mixer
sounds.init()
pygame.init()
pygame.font.init()
death_sound_player = sounds.Sound("./music/player sound death.wav")
death_sound_monster = sounds.Sound("./music/Monster death.wav")
front = pygame.image.load("./images/front.png")
back2 = pygame.image.load("./images/back2.png")
surrender = pygame.image.load("./images/surrender.png")
fight = pygame.image.load("./images/fight.png")
picture = pygame.transform.scale(back2, (480, 480))
picture1 = pygame.transform.scale(front, (480, 480))
picture2 = pygame.transform.scale(surrender, (100, 50))
picture3 = pygame.transform.scale(fight, (100, 50))

large_text = pygame.font.SysFont('ALGER', 50)
small_text = pygame.font.SysFont('ALGER',20)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
white = (255, 255, 255)
black = (0, 0, 0)
clock = pygame.time.Clock()
class Actor:
    '''
    Represents an Actor in the game. Can be the Player, a Monster, boxes, wall.
    Any object in the game's grid that appears on the stage, and has an
    x- and y-coordinate.
    '''
    
    def __init__(self, icon_file, stage, x, y, delay=5):
        '''
        (Actor, str, Stage, int, int, int) -> None
        Given the name of an icon file (with the image for this Actor),
        the stage on which this Actor should appear, the x- and y-coordinates
        that it should appear on, and the speed with which it should
        update, construct an Actor object.
        '''
        
        self._icon = pygame.image.load(icon_file) # the image image to display of self
        self.set_position(x, y) # self's location on the stage
        self._stage = stage # the stage that self is on

        # the following can be used to change this Actors 'speed' relative to other
        # actors speed. See the delay method.
        self._delay = delay
        self._delay_count = 0
    
    def set_position(self, x, y):
        '''
        (Actor, int, int) -> None
        Set the position of this Actor to the given x- and y-coordinates.
        '''
        
        (self._x, self._y) = (x, y)

    def get_position(self):
        '''
        (Actor) -> tuple of two ints
        Return this Actor's x and y coordinates as a tuple.
        '''
        
        return (self._x, self._y)

    def get_icon(self):
        '''
        (Actor) -> pygame.Surface
        Return the image associated with this Actor.
        '''
        
        return self._icon

    def is_dead(self):
        '''
        (Actor) -> bool
        Return True iff this Actor is not alive.
        '''
        if self:
            self._stage.remove_actor(self)
            self._stage.game_over()
            return True
        else:
            return False

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool

        Other is an Actor telling us to move in direction (dx, dy). In this case, we just move.
        (dx,dy) is in {(1,1), (1,0), (1,-1), (0,1), (0,0), (0,-1), (-1,1), (-1,0), (-1,-1)}
    
        In the more general case, in subclasses, self will determine 
        if they will listen to other, and if so, will try to move in
        the specified direction. If the target space is occupied, then we 
        may have to ask the occupier to move.
        '''

        self.set_position(self._x + dx, self._y + dy)
        return True

    def delay(self):
        '''
        (Actor) -> bool
        Manage self's speed relative to other Actors. 
        Each time we get a chance to take a step, we delay. If our count wraps around to 0
        then we actually do something. Otherwise, we simply return from the step method.
        '''

        self._delay_count = (self._delay_count+1) % self._delay
        return self._delay_count == 0

    def step(self):
        '''
        (Actor) -> None
        Make the Actor take a single step in the animation of the game.
        self can ask the stage to help as well as ask other Actors
        to help us get our job done.
        '''

        pass

class Player(Actor):
    '''
    A Player is an Actor that can handle events. These typically come
    from the user, for example, key presses etc.
    '''

    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Player, str, Stage, int, int) -> None
        Construct a Player with given image, on the given stage, at
        x- and y- position.
        '''
        
        super().__init__(icon_file, stage, x, y)
    
    def handle_event(self, event):
        '''
        Used to register the occurrence of an event with self.
        '''
        
        pass

class KeyboardPlayer(Player):
    '''
    A KeyboardPlayer is a Player that can handle keypress events.
    '''
    
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        Construct a KeyboardPlayer. Other than the given Player information,
        a KeyboardPlayer also keeps track of the last key event that took place.
        '''
        
        super().__init__(icon_file, stage, x, y)
        self._last_event = None # we are only interested in the last event

    def handle_event(self, event):
        '''
        (KeyboardPlayer, int) -> None
        Record the last event directed at this KeyboardPlayer.
        All previous events are ignored.
        '''

        self._last_event = event

    def step(self):
        '''
        (KeyboardPlayer) -> None
        Take a single step in the animation. 
        For example: if the user asked us to move right, then we do that.
        '''
        # w : Up
        # a : Left
        # s : Down
        # d : Right
        # q : Up and Left
        # e : Up and Right
        # z : Down and Left
        # c : Down and Right
        if self._last_event is not None:
            dx, dy = None, None
            if self._last_event == pygame.K_s:
                dx, dy = 0,1
            if self._last_event == pygame.K_a:
                dx, dy = -1,0
            if self._last_event == pygame.K_d:
                dx, dy = 1,0
            if self._last_event == pygame.K_w:
                dx, dy = 0,-1
            if self._last_event == pygame.K_q:
                dx, dy = -1, -1
            if self._last_event == pygame.K_e:
                dx, dy = 1, -1
            if self._last_event == pygame.K_z:
                dx, dy = -1, 1
            if self._last_event == pygame.K_c:
                dx, dy = 1, 1
            if dx is not None and dy is not None:
                self.move(self, dx, dy) # we are asking ourself to move

            self._last_event = None


    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''

        # Where we are supposed to move.
        new_x = self._x + dx
        new_y = self._y + dy
        actor = self._stage.get_actor(new_x, new_y)
        if self._stage.is_in_bounds(new_x, new_y) and actor != None:
            if isinstance(actor, DevilMonster):
                self.is_dead()
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(death_sound_player)
            elif isinstance(actor, SuicideMonster):
                actor.is_dead()
            elif actor.move(other,dx, dy):
                super().move(self, dx, dy)
        if self._stage.is_in_bounds(new_x, new_y) and actor == None:
            super().move(other, dx, dy)
            return True
        else:
            return False


        
class Box(Actor):
    '''
    A Box Actor.
    '''
    
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Actor, str, Stage, int, int) -> None
        Construct a Box on the given stage, at given position.
        '''
        
        super().__init__(icon_file, stage, x, y)

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''

        new_x = self._x + dx
        new_y = self._y + dy
        actor = self._stage.get_actor(new_x, new_y)


        # FIX THIS ACCORDING TO LAB INSTRUCTIONS IN PART 1
        # TODO:
        # If (new_x, new_y) is on the stage, and is empty, then 
        # we simply move there. Otherwise, we ask whomever is at (new_x, new_y)
        # to move, also the same direction. If they moved, the space is now
        # empty, so we now move into (new_x, new_y). If we successfully
        # moved, then we return True, otherwise, we return False. '''

        if self._stage.is_in_bounds(new_x, new_y) and actor == None:
            super().move(other, dx, dy)
            return True
        elif self._stage.is_in_bounds(new_x, new_y) and actor.move(self, dx, dy):
            super().move(other, dx, dy)
            return True
        else:
            return False
    
# COMPLETE THIS CLASS FOR PART 2 OF LAB
class StickyBox(Actor):
    '''
        A Sticky Box Actor.
        '''

    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Actor, str, Stage, int, int) -> None
        Construct a Box on the given stage, at given position.
        '''

        super().__init__(icon_file, stage, x, y)

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''

        new_x = self._x + dx
        new_y = self._y + dy
        actor = self._stage.get_actor(new_x, new_y)

        if self._stage.is_in_bounds(new_x, new_y) and isinstance(actor, DevilMonster):
            if isinstance(actor, DevilMonster) == False:
                super().move(actor, dx, dy)
                return True
            else:
                super().move(actor, 0, 0)
                return True
        elif self._stage.is_in_bounds(new_x, new_y) and actor == None:
            super().move(self, dx, dy)
            return True
        elif self._stage.is_in_bounds(new_x, new_y) and actor.move(self, dx, dy):
            super().move(self, dx, dy)
            return True
        else:
            return False



class Wall(Actor):
    '''
    A Wall Actor
    '''

    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Actor, str, Stage, int, int) -> None
        Construct a Wall on the given stage, at given position.
        '''

        super().__init__(icon_file, stage, x, y)

    def move(self, other, dx, dy):
        return False

class Stage:
    '''
    A Stage that holds all the game's Actors (Player, monsters, boxes, etc.).
    '''
    
    def __init__(self, width, height, icon_dimension):
        '''Construct a Stage with the given dimensions.'''
        
        self._actors = [] # all actors on this stage (monsters, player, boxes, ...)
        self._player = None # a special actor, the player

        # the logical width and height of the stage
        self._width, self._height = width, height

        self._icon_dimension=icon_dimension # the pixel dimension of all actors
        # the pixel dimensions of the whole stage
        self._pixel_width = self._icon_dimension * self._width
        self._pixel_height = self._icon_dimension * self._height
        self._pixel_size = self._pixel_width, self._pixel_height

        # get a screen of the appropriate dimension to draw on
        self._screen = pygame.display.set_mode(self._pixel_size)

    def game_loop(self):
        '''This is the main loop of the game that makes the game actually work'''
        game = False
        while not game:

            pygame.time.wait(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    self.player_event(event.key)
            self.step()
            self.draw()



    def text_objects(self, text, font):
        '''This function render text to a specific color and font to be further used in the making of the game.'''
        text_surface = font.render(text, True, black)
        return text_surface, text_surface.get_rect()

    def text_display(self, text):
        '''This is a function that displays text in the game'''
        text_surf, text_rect = self.text_objects(text, large_text)
        text_rect.center = ((self._width / 2), (self._height / 2))
        self._screen.blit(text_surf, text_rect)
        pygame.display.update()


    def game_over(self):
        '''This function prints game over on the screen when the keyboard player has died.'''
        text_surf, text_rect = self.text_objects("GAME OVER", large_text)
        text_rect.center = ((self._width * 12), (self._height * 7))
        self._screen.blit(text_surf, text_rect)
        pygame.display.update()
        time.sleep(1)


    def button(self, x, y, w, h, action):
        '''
        This function creates the button used on the start menu assigning it color and fucntionality.
        x: The x location of the top left coordinate of the button box.

        y: The y location of the top left coordinate of the button box.

        w: Button width.

        h: Button height.

        ic: inactive color(when a mouse is not hovering).

        ac: active color(when a mouse is hovering).'''
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            self._screen.blit(picture3, (100, 300))
            self._screen.blit(picture2, (275,300))

            if click[0] == 1 and action != None:
                action()


    def quit_game(self):
        '''This is a function that quits the game.'''
        pygame.quit()
        quit()
        
    def start_menu(self):
        '''This function is the start menu that we use to navigate to the actual game or quit the game.'''
        start = True

        while start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            rect2 = picture.get_rect()
            self._screen.blit(picture1, rect2)



            if self.button(275, 300, 275, 300, self.quit_game):
                return True
            if self.button(100, 300, 100, 300, self.game_loop):
                return True

            pygame.display.update()


    def is_in_bounds(self, x, y):
        '''
        (Stage, int, int) -> bool
        Return True iff the position (x, y) falls within the dimensions of this Stage.'''
        
        return self.is_in_bounds_x(x) and self.is_in_bounds_y(y)

    def is_in_bounds_x(self, x):
        '''
        (Stage, int) -> bool
        Return True iff the x-coordinate given falls within the width of this Stage.
        '''
        
        return 0 <= x and x < self._width

    def is_in_bounds_y(self, y):
        '''
        (Stage, int) -> bool
        Return True iff the y-coordinate given falls within the height of this Stage.
        '''

        return 0 <= y and y < self._height

    def get_width(self):
        '''
        (Stage) -> int
        Return width of Stage.
        '''

        return self._width

    def get_height(self):
        '''
        (Stage) -> int
        Return height of Stage.
        '''
        
        return self._height

    def set_player(self, player):
        '''
        (Stage, Player) -> None
        A Player is a special actor, store a reference to this Player in the attribute
        self._player, and add the Player to the list of Actors.
        '''
        
        self._player=player
        self.add_actor(self._player)

    def remove_player(self):
        '''
        (Stage) -> None
        Remove the Player from the Stage.
        '''
        
        self.remove_actor(self._player)
        self._player = None

    def player_event(self, event):
        '''
        (Stage, int) -> None
        Send a user event to the player (this is a special Actor).
        '''
        
        self._player.handle_event(event)

    def add_actor(self, actor):
        '''
        (Stage, Actor) -> None
        Add the given actor to the Stage.
        '''

        self._actors.append(actor)

    def remove_actor(self, actor):
        '''
        (Stage, Actor) -> None
        Remove the given actor from the Stage.
        '''
        
        self._actors.remove(actor)


    def step(self):
        '''
        (Stage) -> None
        Take one step in the animation of the game. 
        Do this by asking each of the actors on this Stage to take a single step.
        '''

        for a in self._actors:
            a.step()

    def get_actors(self):
        '''
        (Stage) -> None
        Return the list of Actors on this Stage.
        '''
        
        return self._actors

    def get_actor(self, x, y):
        '''
        (Stage, int, int) -> Actor or None
        Return the first actor at coordinates (x,y).
        Or, return None if there is no Actor in that position.
        '''
        
        for a in self._actors:
            if a.get_position() == (x,y):
                return a
        return None

    def draw(self):
        '''
        (Stage) -> None
        Draw all Actors that are part of this Stage to the screen.
        '''


        rect2 = picture.get_rect()
        self._screen.blit(picture, rect2) # (0,0,0)=(r,g,b)=black
        for a in self._actors:
            icon = a.get_icon()
            (x,y) = a.get_position()
            d = self._icon_dimension
            rect = pygame.Rect(x*d, y*d, d, d)
            self._screen.blit(icon, rect)
        pygame.display.flip()


class DevilMonster(Actor):
    '''A Monster class.'''

    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a Monster.'''

        super().__init__(icon_file, stage, x, y, delay)
        self._dx = 1
        self._dy = 1

    def step(self):
        '''
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''

        v = self.is_dead()
        if v:
            self._stage.remove_actor(self)
            pygame.mixer.Sound.play(death_sound_monster)

        if not self.delay(): return
        self.move(self, self._dx, self._dy)
        return True

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        '''

        if other != self:  # Noone pushes me around
            return False

        bounce_off_edge = False

        new_x = self._x + self._dx
        new_y = self._y + self._dy

        if not self._stage.is_in_bounds_x(new_x):
            self._dx = -self._dx
            bounce_off_edge = True

        if not self._stage.is_in_bounds_y(new_y):
            self._dy = - self._dy
            bounce_off_edge = True



        # FIX THIS FOR PART 3 OF THE LAB
        # MONSTERS SHOULD BOUNCE BACK FROM BOXES AND OTHER MONSTERS
        # HINT: actor = self._stage.get_actor(new_x,new_y)
        actor = self._stage.get_actor(new_x, new_y)
        if actor != None:
            if isinstance(actor, Box):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, DevilMonster):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, SuicideMonster):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, Wall):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, StickyBox):
                return False
            elif isinstance(actor, KeyboardPlayer):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(death_sound_player)
                actor.is_dead()

        if bounce_off_edge:
            return False
        return super().move(self, self._dx, self._dy)

    def is_dead(self):
        '''
        Return whether this Monster has died.
        That is, if self is surrounded on all sides, by either Boxes or
        other Monsters.'''

        y, x = self.get_position()[1], self.get_position()[0]
        surroundings = [(0, -1), (0, 1), (1, 1), (-1, 1), (-1, 0), (-1, -1), (1, 0), (1, -1)]
        counter = 0
        for i in surroundings:
            dx = i[0]
            dy = i[1]
            real_actor = self._stage.get_actor(x + dx, y + dy)
            if isinstance(real_actor, DevilMonster):
                counter += 1
            elif isinstance(real_actor, SuicideMonster):
                counter += 1
            elif isinstance(real_actor, Wall):
                counter += 1
            elif isinstance(real_actor, StickyBox):
                counter += 1
            elif isinstance(real_actor, Box):
                counter += 1
            elif not self._stage.is_in_bounds(x + dx, y + dy):
                counter += 1
            else:
                return False
        if counter >= 8:
            return True

class DevilMonster2(Actor):
    '''A Monster class.'''

    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a Monster.'''

        super().__init__(icon_file, stage, x, y, delay)
        self._dx = 1
        self._dy = 1

    def step(self):
        '''
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''

        v = self.is_dead()
        if v:
            self._stage.remove_actor(self)
            pygame.mixer.Sound.play(death_sound_monster)

        if not self.delay(): return
        self.move(self, self._dx, self._dy)
        return True

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        '''

        if other != self:  # Noone pushes me around
            return False

        bounce_off_edge = False

        new_x = self._x + self._dx
        new_y = self._y + self._dy

        if not self._stage.is_in_bounds_x(new_x):
            self._dx = -self._dx
            bounce_off_edge = True

        if not self._stage.is_in_bounds_y(new_y):
            self._dy = - self._dy
            bounce_off_edge = True



        # FIX THIS FOR PART 3 OF THE LAB
        # MONSTERS SHOULD BOUNCE BACK FROM BOXES AND OTHER MONSTERS
        # HINT: actor = self._stage.get_actor(new_x,new_y)
        actor = self._stage.get_actor(new_x, new_y)
        if actor != None:
            if isinstance(actor, Box):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, DevilMonster):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, SuicideMonster):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, Wall):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, StickyBox):
                return False
            elif isinstance(actor, KeyboardPlayer):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(death_sound_player)
                actor.is_dead()

        if bounce_off_edge:
            return False
        return super().move(self, self._dx, self._dy)

    def is_dead(self):
        '''
        Return whether this Monster has died.
        That is, if self is surrounded on all sides, by either Boxes or
        other Monsters.'''

        y, x = self.get_position()[1], self.get_position()[0]
        surroundings = [(0, -1), (0, 1), (1, 1), (-1, 1), (-1, 0), (-1, -1), (1, 0), (1, -1)]
        counter = 0
        for i in surroundings:
            dx = i[0]
            dy = i[1]
            real_actor = self._stage.get_actor(x + dx, y + dy)
            if isinstance(real_actor, DevilMonster):
                counter += 1
            elif isinstance(real_actor, SuicideMonster):
                counter += 1
            elif isinstance(real_actor, Wall):
                counter += 1
            elif isinstance(real_actor, StickyBox):
                counter += 1
            elif isinstance(real_actor, Box):
                counter += 1
            elif not self._stage.is_in_bounds(x + dx, y + dy):
                counter += 1
            else:
                return False
        if counter >= 8:
            return True

class ExplosionMonster(Actor):
    '''An Explosion Monster class. When this monster dies its eliminates all actors in its surroundings.'''

    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a Monster.'''

        super().__init__(icon_file, stage, x, y, delay)
        self._dx = 1
        self._dy = 1

    def step(self):
        '''
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''

        v = self.is_dead()
        if v:
            self._stage.remove_actor(self)
            pygame.mixer.Sound.play(death_sound_monster)
            y, x = self.get_position()[1], self.get_position()[0]
            surroundings = [(0, -1), (0, 1), (1, 1), (-1, 1), (-1, 0), (-1, -1), (1, 0), (1, -1)]
            counter = 0
            for i in surroundings:
                dx = i[0]
                dy = i[1]
                real_actor = self._stage.get_actor(x + dx, y + dy)
                if isinstance(real_actor, DevilMonster):
                    self._stage.remove_actor(real_actor)
                elif isinstance(real_actor, SuicideMonster):
                    self._stage.remove_actor(real_actor)
                elif isinstance(real_actor, Wall):
                    self._stage.remove_actor(real_actor)
                elif isinstance(real_actor, StickyBox):
                    self._stage.remove_actor(real_actor)
                elif isinstance(real_actor, Box):
                    self._stage.remove_actor(real_actor)

        if not self.delay(): return
        self.move(self, self._dx, self._dy)
        return True

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        '''

        if other != self:  # Noone pushes me around
            return False

        bounce_off_edge = False

        new_x = self._x + self._dx
        new_y = self._y + self._dy

        if not self._stage.is_in_bounds_x(new_x):
            self._dx = -self._dx
            bounce_off_edge = True

        if not self._stage.is_in_bounds_y(new_y):
            self._dy = - self._dy
            bounce_off_edge = True



        # FIX THIS FOR PART 3 OF THE LAB
        # MONSTERS SHOULD BOUNCE BACK FROM BOXES AND OTHER MONSTERS
        # HINT: actor = self._stage.get_actor(new_x,new_y)
        actor = self._stage.get_actor(new_x, new_y)
        if actor != None:
            if isinstance(actor, Box):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, DevilMonster):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, SuicideMonster):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, Wall):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, StickyBox):
                return False
            elif isinstance(actor, KeyboardPlayer):
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(death_sound_player)
                actor.is_dead()

        if bounce_off_edge:
            return False
        return super().move(self, self._dx, self._dy)

    def is_dead(self):
        '''
        Return whether this Monster has died.
        That is, if self is surrounded on all sides, by either Boxes or
        other Monsters.'''

        y, x = self.get_position()[1], self.get_position()[0]
        surroundings = [(0, -1), (0, 1), (1, 1), (-1, 1), (-1, 0), (-1, -1), (1, 0), (1, -1)]
        counter = 0
        for i in surroundings:
            dx = i[0]
            dy = i[1]
            real_actor = self._stage.get_actor(x + dx, y + dy)
            if isinstance(real_actor, DevilMonster):
                counter += 1
            elif isinstance(real_actor, SuicideMonster):
                counter += 1
            elif isinstance(real_actor, Wall):
                counter += 1
            elif isinstance(real_actor, StickyBox):
                counter += 1
            elif isinstance(real_actor, Box):
                counter += 1
            elif not self._stage.is_in_bounds(x + dx, y + dy):
                counter += 1
            else:
                return False
        if counter >= 8:
            return True
class SuicideMonster(Actor):
    '''A Suicide Monster class. That dies if the player touches it. (this code is faulty,
    the monster dies but not always'''

    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a Monster.'''

        super().__init__(icon_file, stage, x, y, delay)
        self._dx = 1
        self._dy = 1

    def step(self):
        '''
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''


        if not self.delay(): return

        self.move(self, self._dx, self._dy)
        return True

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        '''

        if other != self:  # Noone pushes me around
            return False

        bounce_off_edge = False

        new_x = self._x + self._dx
        new_y = self._y + self._dy

        if not self._stage.is_in_bounds_x(new_x):
            self._dx = -self._dx
            bounce_off_edge = True

        if not self._stage.is_in_bounds_y(new_y):
            self._dy = - self._dy
            bounce_off_edge = True

        # FIX THIS FOR PART 3 OF THE LAB
        # MONSTERS SHOULD BOUNCE BACK FROM BOXES AND OTHER MONSTERS
        # HINT: actor = self._stage.get_actor(new_x,new_y)
        actor = self._stage.get_actor(new_x, new_y)
        if actor != None:
            if isinstance(actor, Box):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, DevilMonster):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, SuicideMonster):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, Wall):
                bounce_off_edge = True
                self._dx = - self._dx
                self._dy = - self._dy
            elif isinstance(actor, StickyBox):
                return False
            else: #isinstance(actor, KeyboardPlayer):
                self.is_dead()


        if bounce_off_edge:
            return False

        return super().move(self, self._dx, self._dy)

    def is_dead(self):
        '''
        Return whether this Monster has died.
        That is, if self is surrounded on all sides, by either Boxes or
        other Monsters.'''

        y, x = self.get_position()[1], self.get_position()[0]
        surroundings = [(0, -1), (0, 1), (1, 1), (-1, 1), (-1, 0), (-1, -1), (1, 0), (1, -1)]
        for i in surroundings:
            dx = i[0]
            dy = i[1]
            real_actor = self._stage.get_actor(x + dx, y + dy)
            if isinstance(real_actor, KeyboardPlayer):
                self._stage.remove_actor(self)
                pygame.mixer.Sound.play(death_sound_monster)
                return True
            else:
                return False






