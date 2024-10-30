from pico2d import *
from statemachine import StateMachine
import time
from grass import Grass


class Idle:
    @staticmethod
    def enter(boy):
        boy.action = boy.IDLE
        boy.frame = 0
        boy.dir = 0  # stop any movement in Idle
        print('Boy Idle Enter')

    @staticmethod
    def exit(boy):
        print('Boy Idle Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, 300, 100, 100, boy.x, boy.y)

    @staticmethod
    def handle_event(boy, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            boy.dir = 1  # AutoRun 시작 방향을 오른쪽으로 설정
            boy.state_machine.change_state(AutoRun)
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            boy.dir = -1 if event.key == SDLK_LEFT else 1
            boy.state_machine.change_state(Run)


class AutoRun:
    @staticmethod
    def enter(boy):
        boy.action = boy.RUN
        boy.start_time = time.time()
        boy.dir = 1 if boy.dir == 0 else boy.dir  # 방향 유지, 기본은 오른쪽
        boy.speed = 300  # 속도 증가 (300으로 설정)
        boy.scale = 1.5  # 크기 확대
        print('Boy AutoRun Enter')

    @staticmethod
    def exit(boy):
        boy.scale = 1  # 크기 복구
        boy.speed = 100  # 속도 복구
        print('Boy AutoRun Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * boy.speed * 0.02

        # 화면 끝에 도달 시 방향 전환
        if boy.x < 50 or boy.x > 750:
            boy.dir *= -1  # 방향 반전

        # 5초 후 Idle 상태로 복귀
        if time.time() - boy.start_time > 5:
            boy.state_machine.change_state(Idle)

    @staticmethod
    def draw(boy):
        width = int(100 * boy.scale)
        height = int(100 * boy.scale)
        flip = boy.dir == -1  # 왼쪽으로 이동 시 flip=True
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, 0, 'h' if flip else '', boy.x, boy.y, width, height)

    @staticmethod
    def handle_event(boy, event):
        if event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            # 방향키를 누르면 Run 상태로 전환하면서 방향 전환
            boy.dir = -1 if event.key == SDLK_LEFT else 1
            boy.state_machine.change_state(Run)


class Run:
    @staticmethod
    def enter(boy):
        boy.action = boy.RUN
        boy.frame = 0
        boy.speed = 100  # Run 모드의 속도
        print('Boy Run Enter')

    @staticmethod
    def exit(boy):
        print('Boy Run Exit')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5

    @staticmethod
    def draw(boy):
        flip = boy.dir == -1  # 왼쪽으로 이동 시 flip=True
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, 0, 'h' if flip else '', boy.x, boy.y, 100, 100)

    @staticmethod
    def handle_event(boy, event):
        if event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            # 방향키 입력 시 이동 방향 전환
            boy.dir = -1 if event.key == SDLK_LEFT else 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            boy.state_machine.change_state(AutoRun)


class Boy:
    IDLE, RUN, DASH, SLEEP = 0, 1, 2, 3

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = self.IDLE
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.grass = load_image('grass.png')  # Load grass image
        self.speed = 100  # 기본 속도
        self.scale = 1  # 기본 크기

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(event)
        if isinstance(self.state_machine.cur_state, AutoRun):
            AutoRun.handle_event(self, event)

    def draw(self):
        self.grass.draw(400, 30)  # Draw grass at (400, 30)
        self.state_machine.cur_state.draw(self)


def main():
    open_canvas(800, 600)
    boy = Boy()
    running = True

    while running:
        clear_canvas()
        boy.update()
        boy.draw()

        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
            else:
                boy.handle_event(event)

        update_canvas()
        delay(0.03)

    close_canvas()


if __name__ == '__main__':
    main()
