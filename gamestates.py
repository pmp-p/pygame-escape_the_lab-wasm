
#===========================================================================



def state_float():
    pass

def state_exit():
    States.current = None

def state_fullscreen(mode=0):
    global full_screen

    if mode>0:
        States.full_screen = not States.full_screen

    if mode<0:
        States.full_screen = False

    print("state_fullscreen N/I")



class States:
    states = {"exit":state_exit, "float":state_float, "fullscreen": state_fullscreen}
    current = None
    name = "float"
    has_changed = False
    clear_change = False
    last = "float"
    full_screen = False
    instances = {}

    def __init__(self, name):
        if self.states.get(name, None) is None:
            try:
                self.instances[name] = vars(__import__('__main__'))[name]()
                self.states[name] = self.instances[name].draw

                print(f"Game State {name=} ready !")
            except KeyError:
                print(f"Game State {name=} not ready yet")

        self.state = name

    def __call__(self):
        self.select(self.state)



    @classmethod
    def select(cls, state):
        if state != cls.name:
            if cls.states.get(state, None) is None:
                cls(state)

            instance = cls.instances.get(state, cls)

            if hasattr(cls.instances, "on_select"):
                #TODO allow abort
                instance.on_select(cls.name)

            cls.last = cls.name
            cls.name = state
            cls.current = cls.states[state]
            cls.has_changed = True

    @classmethod
    def on_select(cls, last):
        print("state: ", cls.name, "=>", state )

    @classmethod
    def changed(cls, *args):
        cls.clear_change = True
        if cls.has_changed:
            return cls.last not in args
        return False


    @classmethod
    def draw(cls):
        if cls.current:
            if cls.clear_change:
                cls.has_changed = False

            cls.base.screen.fill((0, 0, 0))
            cls.current()
            if cls.current:
                cls.base.display.update()

        return cls.current


    @classmethod
    def previous(cls):
        cls.select(cls.last)


#===========================================================================



