# Imports
from tkinter import *
import random

# Finals
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
CELL_SIZE = 25
ROWS = CANVAS_WIDTH // CELL_SIZE
COLS = CANVAS_HEIGHT // CELL_SIZE
GRADUAL_VELOCITY_INCREASE = 1 + 1 / 1e10
FOOD_RESPAWN_TIME = 5000 # In milliseconds
SNAKE_BODY_COLOR = "green"
SNAKE_HEAD_COLOR = "#32CD32"
OBSTACLE_COLOR = "gray"
LEVELS = {
    1: {"init_length": 2, "score_req": 10, "snake_velocity": 5.0, "obstacles_amount": 0},
    2: {"init_length": 2, "score_req": 14, "snake_velocity": 5.21, "obstacles_amount": 1},
    3: {"init_length": 2, "score_req": 17, "snake_velocity": 5.42, "obstacles_amount": 2},
    4: {"init_length": 2, "score_req": 21, "snake_velocity": 5.62, "obstacles_amount": 3},
    5: {"init_length": 2, "score_req": 24, "snake_velocity": 5.83, "obstacles_amount": 3},
    6: {"init_length": 2, "score_req": 28, "snake_velocity": 6.04, "obstacles_amount": 4},
    7: {"init_length": 2, "score_req": 31, "snake_velocity": 6.25, "obstacles_amount": 5},
    8: {"init_length": 3, "score_req": 35, "snake_velocity": 6.46, "obstacles_amount": 6},
    9: {"init_length": 3, "score_req": 38, "snake_velocity": 6.67, "obstacles_amount": 6},
    10: {"init_length": 3, "score_req": 42, "snake_velocity": 6.88, "obstacles_amount": 7},
    11: {"init_length": 3, "score_req": 45, "snake_velocity": 7.08, "obstacles_amount": 8},
    12: {"init_length": 3, "score_req": 49, "snake_velocity": 7.29, "obstacles_amount": 9},
    13: {"init_length": 3, "score_req": 52, "snake_velocity": 7.5, "obstacles_amount": 10},
    14: {"init_length": 4, "score_req": 56, "snake_velocity": 7.71, "obstacles_amount": 10},
    15: {"init_length": 4, "score_req": 59, "snake_velocity": 7.92, "obstacles_amount": 11},
    16: {"init_length": 4, "score_req": 63, "snake_velocity": 8.12, "obstacles_amount": 12},
    17: {"init_length": 4, "score_req": 66, "snake_velocity": 8.33, "obstacles_amount": 13},
    18: {"init_length": 4, "score_req": 70, "snake_velocity": 8.54, "obstacles_amount": 14},
    19: {"init_length": 5, "score_req": 73, "snake_velocity": 8.75, "obstacles_amount": 15},
    20: {"init_length": 5, "score_req": 77, "snake_velocity": 8.96, "obstacles_amount": 16},
    21: {"init_length": 5, "score_req": 81, "snake_velocity": 9.17, "obstacles_amount": 17},
    22: {"init_length": 5, "score_req": 85, "snake_velocity": 9.38, "obstacles_amount": 18},
    23: {"init_length": 5, "score_req": 89, "snake_velocity": 9.58, "obstacles_amount": 19},
    24: {"init_length": 5, "score_req": 94, "snake_velocity": 9.79, "obstacles_amount": 20},
    25: {"init_length": 5, "score_req": 100, "snake_velocity": 10.0, "obstacles_amount": 20},
}

# Globals
CURRENT_LEVEL = 1
MAXIMUM_UNLOCKED_LEVEL = 1
TIME_ELAPSED = 0

# Objects
class Level:
    def __init__(self, level : int):
        self.level = level
        self.current_score = 0
        self.score_req = LEVELS[level]["score_req"]
        self.obstacles_amount = LEVELS[level]["obstacles_amount"]
        self.score_text = Label(window, text=f"Score: {self.current_score} / {self.score_req}", font=("Arial", 16))
        self.canvas = Canvas(window, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, background="black")
        self.snake = None
        self.food = None
        self.food_timer = None
        self.running = True
        self.obstacles = []

    def build_level(self):
        level_title = Label(window, text=f"Level: {self.level}", font=("Arial", 20))
        level_title.pack(pady=5)

        self.score_text.pack(pady=5)
        self.canvas.pack()

        back_button = Button(window, text="BACK", command=self.back_menu)
        back_button.pack(pady=5)

        window.bind('<Left>', lambda event: self.snake.change_direction(get_direction('left')))
        window.bind('<Right>', lambda event: self.snake.change_direction(get_direction('right')))
        window.bind('<Up>', lambda event: self.snake.change_direction(get_direction('up')))
        window.bind('<Down>', lambda event: self.snake.change_direction(get_direction('down')))
        window.bind('<a>', lambda event: self.snake.change_direction(get_direction('left')))
        window.bind('<d>', lambda event: self.snake.change_direction(get_direction('right')))
        window.bind('<w>', lambda event: self.snake.change_direction(get_direction('up')))
        window.bind('<s>', lambda event: self.snake.change_direction(get_direction('down')))

        self.generate_obstacles()
        self.snake = Snake(self)
        self.spawn_food()
        window.after(1000, self.snake_move_loop)
        window.after(1000, self.time_elapse_loop)

    def generate_obstacles(self):
        for i in range(self.obstacles_amount):
            self.obstacles.append(Obstacle(self))

    def spawn_food(self):
        if not self.running:
            return

        if self.food_timer:
            window.after_cancel(self.food_timer)
        if self.food:
            self.canvas.delete(self.food.ui)

        self.food = generate_food(self)
        self.food_timer = window.after(FOOD_RESPAWN_TIME, self.spawn_food)  # Respawn food after 5 seconds

    def snake_move_loop(self):
        if self.running:
            self.snake.move()
            window.after(int(1000 / self.snake.velocity), self.snake_move_loop)

    def time_elapse_loop(self):
        if self.running:
            global TIME_ELAPSED
            TIME_ELAPSED += 1
            window.after(1000, self.time_elapse_loop)

    def back_menu(self):
        self.running = False

        show_menu()

    def game_over(self):
        self.running = False

        show_game_over(self.snake.length, self.current_score)

    def level_completed(self):
        self.running = False
        clear_current_scene()

        global CURRENT_LEVEL, MAXIMUM_UNLOCKED_LEVEL
        CURRENT_LEVEL = self.level + 1
        MAXIMUM_UNLOCKED_LEVEL = max(CURRENT_LEVEL, MAXIMUM_UNLOCKED_LEVEL)

        self.show_level_intermission()

    def show_level_intermission(self):
        clear_current_scene()

        title = Label(window, text=f"Level {self.level} completed!", font=("Arial", 30))
        title.pack(pady=115)

        subtitle = Label(window, text=f"Going to the next level...", font=("Arial", 20))
        subtitle.pack(pady=10)

        window.after(1500, self.next_level)

    def next_level(self):
        clear_current_scene()
        if self.level + 1 <= len(LEVELS):
            Level(self.level + 1).build_level()
        else:
            show_game_completion()

class Snake:
    def __init__(self, level : Level):
        self.level = level
        self.velocity = LEVELS[level.level]["snake_velocity"]
        self.length = LEVELS[level.level]["init_length"]
        self.direction = get_direction(generate_direction())
        self.next_direction = self.direction
        self.parts_coord = []
        self.parts_ui = []
        self.grow_by = 0

        # Generate initial position
        while True:
            self.x = random.randint(self.length + 1, ROWS - self.length - 1)
            self.y = random.randint(self.length + 1, COLS - self.length - 1)

            if all(
                [self.x + self.direction[0] * i, self.y + self.direction[1] * i] not in obstacle.parts_coord
                for obstacle in self.level.obstacles
                for i in range(self.length + 1)
            ):
                break

        for i in range(self.length):
            part_ui = self.level.canvas.create_rectangle(
                self.x * CELL_SIZE,
                self.y * CELL_SIZE,
                (self.x + 1) * CELL_SIZE,
                (self.y + 1) * CELL_SIZE,
                fill=SNAKE_BODY_COLOR if i != self.length - 1 else SNAKE_HEAD_COLOR
            )
            self.parts_ui.append(part_ui)
            self.parts_coord.append([self.x, self.y])

            if i != self.length - 1:
                self.x += self.direction[0]
                self.y += self.direction[1]

    def move(self):
        self.direction = self.next_direction
        self.x += self.direction[0]
        self.y += self.direction[1]

        if self.check_collision():
            return

        if self.parts_ui:
            self.level.canvas.itemconfig(self.parts_ui[-1], fill=SNAKE_BODY_COLOR)

        part_ui = self.level.canvas.create_rectangle(
            self.x * CELL_SIZE,
            self.y * CELL_SIZE,
            (self.x + 1) * CELL_SIZE,
            (self.y + 1) * CELL_SIZE,
            fill=SNAKE_HEAD_COLOR
        )
        self.parts_ui.append(part_ui)
        self.parts_coord.append([self.x, self.y])

        food_result = self.check_food()
        growth_from_food, score_from_food = food_result[0], food_result[1]
        self.grow_by += growth_from_food
        self.level.current_score += score_from_food
        self.level.score_text.config(text=f"Score: {self.level.current_score} / {self.level.score_req}")

        if self.grow_by > 0:
            self.grow_by -= 1
            self.length += 1
        else:
            self.level.canvas.delete(self.parts_ui[0])
            self.parts_ui.pop(0)
            self.parts_coord.pop(0)

        if self.level.current_score >= self.level.score_req:
            self.level.level_completed()
            
        self.velocity *= GRADUAL_VELOCITY_INCREASE

    def change_direction(self, direction : list):
        if self.direction[0] != -direction[0] or self.direction[1] != -direction[1]:
            self.next_direction = direction

    def check_collision(self):
        if self.x < 0 or self.x >= COLS or self.y < 0 or self.y >= ROWS:
            self.level.game_over()
            return True
        elif [self.x, self.y] in self.parts_coord[1:]:
            self.level.game_over()
            return True
        for obstacle in self.level.obstacles:
            if [self.x, self.y] in obstacle.parts_coord:
                self.level.game_over()
                return True

    def check_food(self):
        for part_coord in self.parts_coord:
            if part_coord[0] == self.level.food.x and part_coord[1] == self.level.food.y:
                self.level.food.do_effect() # If there are any effects, revert after some time
                length_inc = self.level.food.length_increase
                score_inc = self.level.food.score

                self.level.spawn_food() # Generate new food

                return [length_inc, score_inc]
        return [0, 0]

class Food:
    def __init__(self, level : Level):
        while True:
            self.x = random.randint(0, COLS - 1)
            self.y = random.randint(0, ROWS - 1)

            if [self.x, self.y] not in level.snake.parts_coord and all([self.x, self.y] not in obstacle.parts_coord for obstacle in level.obstacles):
                break

        self.level = level
        self.color = "white"
        self.length_increase = 0
        self.velocity_buff_multi = 0
        self.velocity_buff_duration = 0
        self.ui = level.canvas.create_rectangle(
            self.x * CELL_SIZE,
            self.y * CELL_SIZE,
            (self.x + 1) * CELL_SIZE,
            (self.y + 1) * CELL_SIZE,
            fill=self.color
        )

    def do_effect(self):
        self.level.snake.velocity *= self.velocity_buff_multi

        if self.velocity_buff_multi != 1:
            window.after(self.velocity_buff_duration, self.revert_velocity_buff)

    def revert_velocity_buff(self):
        self.level.snake.velocity /= self.velocity_buff_multi
        print("Removed buff")

# Length: 1, Base Score: 1
class Apple(Food):
    def __init__(self, level : Level):
        super().__init__(level)
        self.color = "red"
        self.length_increase = 1
        self.score = 1
        self.velocity_buff_multi = 1
        level.canvas.itemconfig(self.ui, fill=self.color)

# Length: 2, Base Score: 3
class Orange(Food):
    def __init__(self, level : Level):
        super().__init__(level)
        self.color = "orange"
        self.length_increase = 2
        self.score = 3
        self.velocity_buff_multi = 1
        level.canvas.itemconfig(self.ui, fill=self.color)

# Length: 3, Base Score: 5
class Grape(Food):
    def __init__(self, level : Level):
        super().__init__(level)
        self.color = "magenta"
        self.length_increase = 2
        self.score = 5
        self.velocity_buff_multi = 1
        level.canvas.itemconfig(self.ui, fill=self.color)

# Velocity: x1.125, Base Score: 2
class Pepper(Food):
    def __init__(self, level : Level):
        super().__init__(level)
        self.color = "yellow"
        self.length_increase = 0
        self.score = 2
        self.velocity_buff_multi = 1.125
        self.velocity_buff_duration = 3000
        level.canvas.itemconfig(self.ui, fill=self.color)

# Velocity: x0.75, Base Score: 2
class Salt(Food):
    def __init__(self, level : Level):
        super().__init__(level)
        self.color = "cyan"
        self.length_increase = 0
        self.score = 2
        self.velocity_buff_multi = 0.75
        self.velocity_buff_duration = 3000
        level.canvas.itemconfig(self.ui, fill=self.color)

# Obstacles are generated randomly with varying lengths and size
class Obstacle:
    def __init__(self, level : Level):
        self.length = random.randint(1, ROWS // 4)
        self.direction = get_direction(generate_direction())
        self.parts_coord = []
        self.parts_ui = []

        self.x = random.randint(self.length - 1, ROWS - self.length + 1)
        self.y = random.randint(self.length - 1, COLS - self.length + 1)

        for i in range(self.length):
            part_ui = level.canvas.create_rectangle(
                self.x * CELL_SIZE,
                self.y * CELL_SIZE,
                (self.x + 1) * CELL_SIZE,
                (self.y + 1) * CELL_SIZE,
                fill=OBSTACLE_COLOR
            )
            self.parts_ui.append(part_ui)
            self.parts_coord.append([self.x, self.y])

            if i != self.length - 1:
                self.x += self.direction[0]
                self.y += self.direction[1]

# General Game Functions
def start_game(level : int):
    clear_current_scene()

    global TIME_ELAPSED, CURRENT_LEVEL
    TIME_ELAPSED = 0
    CURRENT_LEVEL = level

    if CURRENT_LEVEL <= len(LEVELS):
        Level(CURRENT_LEVEL).build_level()
    else:
        show_game_completion()

def generate_food(level : Level):
    food_classes = [Apple, Orange, Grape, Pepper, Salt]
    spawn_chances = [0.35, 0.25, 0.1, 0.15, 0.15] # Total 100%
    return random.choices(food_classes, weights=spawn_chances, k=1)[0](level)

def generate_direction():
    match random.randint(0, 3):
        case 0:
            return 'up'
        case 1:
            return 'down'
        case 2:
            return 'left'
        case 3:
            return 'right'

def get_direction(direction : str):  # Get the (x,y) pair of the direction
    match direction:
        case 'up':
            return [0, -1]
        case 'down':
            return [0, 1]
        case 'left':
            return [-1, 0]
        case 'right':
            return [1, 0]

# UIs
def show_menu():
    clear_current_scene()

    menu_title = Label(window, text="Snek Gem", font=("Arial", 30))
    menu_start = Button(window, text="START", command=show_level_selection, font=("Arial", 15), width=10)
    menu_exit = Button(window, text="EXIT", command=window.destroy, font=("Arial", 15), width=10)

    menu_title.pack(pady=100)
    menu_start.pack(pady=10)
    menu_exit.pack(pady=10)

def show_level_selection():
    clear_current_scene()

    title = Label(window, text="Level Selection", font=("Arial", 20))
    title.pack(pady=60)

    canvas = Canvas(window)
    canvas.pack(fill=BOTH, padx=15)

    columns = 5
    for i in range(len(LEVELS)):
        row = (i // columns)
        column = i % columns
        button = Button(canvas, text=f"Level {i+1}", command=lambda level=i+1: start_game(level), font=("Arial", 12))
        button.grid(row=row, column=column, padx=10, pady=10)

        if (i+1) > MAXIMUM_UNLOCKED_LEVEL:
            button.config(state=DISABLED, text="Level 🔒")

def show_game_over(max_length : int, score_achieved : int):
    clear_current_scene()

    global TIME_ELAPSED
    game_over_title = Label(window, text="GAME OVER", font=("Arial", 30))
    game_over_score_achieved = Label(window, text=f"SCORE ACHIEVED: {score_achieved}", font=("Arial", 20))
    game_over_max_length = Label(window, text=f"MAX LENGTH: {max_length}", font=("Arial", 20))
    game_over_time_elapsed = Label(window, text=f"TIME ELAPSED: {TIME_ELAPSED}s", font=("Arial", 20))
    game_over_retry = Button(window, text="RETRY", command=lambda level = CURRENT_LEVEL: start_game(level), font=("Arial", 15), width=10)
    game_over_back_menu = Button(window, text="EXIT", command=show_menu, font=("Arial", 15), width=10)

    game_over_title.pack(pady=60)
    game_over_score_achieved.pack(pady=15)
    game_over_max_length.pack(pady=15)
    game_over_time_elapsed.pack(pady=15)
    game_over_retry.pack(pady=10)
    game_over_back_menu.pack(pady=10)

def show_game_completion():
    clear_current_scene()

    title = Label(window, text=f"You completed ALL {len(LEVELS)} levels", font=("Arial", 25))
    back = Button(window, text="RETURN TO MENU", command=show_menu, font=("Arial", 15), width=20)

    title.pack(pady=125)
    back.pack(pady=25)

def clear_current_scene():
    for child in window.winfo_children():
        child.destroy()

# Setups
window = Tk()
window.title("Snek Gem")
window.resizable(False, False)
window.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT + 125}")

show_menu()

window.mainloop()