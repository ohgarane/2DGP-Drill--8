class StateMachine:
    def __init__(self, o):
        self.o = o
        self.cur_state = None

    def start(self, state):
        self.cur_state = state
        self.cur_state.enter(self.o)

    def update(self):
        self.cur_state.do(self.o)

    def draw(self):
        self.cur_state.draw(self.o)

    def change_state(self, new_state):
        if self.cur_state:
            self.cur_state.exit(self.o)
        self.cur_state = new_state
        self.cur_state.enter(self.o)

    def handle_event(self, event):
        if hasattr(self.cur_state, 'handle_event'):
            self.cur_state.handle_event(self.o, event)
