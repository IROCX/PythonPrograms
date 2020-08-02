import tkinter as tk
from PIL import Image, ImageTk
from random import randint

MOVE_INCREMENT = 20
moves_per_second = 7
GAME_SPEED = 1000//moves_per_second

root = tk.Tk()

def start_game():
    root.title('SnakeMania')
    root.resizable(False, False)

    board = Snake()
    board.pack()

    root.mainloop()

def ender():
    global root
    root.destroy()
    root = tk.Tk()
    root.focus_force()
    start_game()


class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=600, background='grey', highlightthickness=0)
        self.starter()
       
    def starter(self):
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]
        self.food_positions = self.set_food()
        self.score = 0

        self.direcion = 'Right'
        self.bind_all('<Key>', self.on_keypress)

        self.load_assets()
        self.create_objects()
        self.after(GAME_SPEED, self.perform_actions)


    def load_assets(self):
        try:
            self.snake_body_image = Image.open('./assets/snake.png')
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open('./assets/food.png')
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()


    def create_objects(self):
        global moves_per_second
        self.create_text(
            100, 12, text=f"Score : {self.score}, Speed : {moves_per_second}", tag='score', fill='#fff', font=('TkDefaultFont', 10)
        )

        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position,
                              image=self.snake_body, tag='snake')

        self.create_image(*self.food_positions, image=self.food, tag='food')

        self.create_rectangle(7, 27, 593, 590, outline='#ccc')

    def move_snake(self):
        head_x, head_y = self.snake_positions[0]

        if self.direcion == 'Left':
            new_head = (head_x - MOVE_INCREMENT, head_y)
        elif self.direcion == 'Right':
            new_head = (head_x + MOVE_INCREMENT, head_y)
        elif self.direcion == 'Up':
            new_head = (head_x, head_y-MOVE_INCREMENT)
        elif self.direcion == 'Down':
            new_head = (head_x, head_y+MOVE_INCREMENT)
        self.snake_positions = [new_head] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag('snake'), self.snake_positions):
            self.coords(segment, position)

    def perform_actions(self):

        if self.check_collisions():
            self.end_game()
            return

        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)

    def check_collisions(self):
        head_x, head_y = self.snake_positions[0]
        return(
            head_x in (0, 600) or head_y in (20, 600) or (
                head_x, head_y) in self.snake_positions[1:]
        )

    def on_keypress(self, e):
        new_direction = e.keysym

        all_directions = ('Up', 'Down', 'Left', 'Right')
        opposites = ({'Up', 'Down'}, {'Left', 'Right'})
        if new_direction in all_directions:
            if set([new_direction, self.direcion]) not in opposites:
                self.direcion = new_direction

    def check_food_collision(self):
        global moves_per_second
        if self.food_positions == self.snake_positions[0]:
            self.score += 10

            self.snake_positions.append(self.snake_positions[-1])

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag='snake'
            )

            self.food_positions = self.set_food()
            self.coords(self.find_withtag('food'), self.food_positions)

            if self.score % 100 == 0 and moves_per_second < 30:
                moves_per_second += 2

            score = self.find_withtag('score')
            self.itemconfigure(
                score, text=f'Score : {self.score}  Speed : {moves_per_second}', tag='score')

    def set_food(self):
        while True:
            x_pos = randint(1, 29)*MOVE_INCREMENT
            y_pos = randint(2, 29)*MOVE_INCREMENT
            food_position = (x_pos, y_pos)

            if food_position not in self.snake_positions:
                return food_position

    def end_game(self):
    
        self.create_text(
            self.winfo_width()/2,
            self.winfo_height()/2,
            text=f'Game Over!\n You scored : {self.score}\n\n Press Space to play again',
            fill='#fff',
            font=('TkDefaultFont', 24),
            tag="game_over"
        )
        self.bind_all('<Key>', self.on_space)

    
    def on_space(self, e):
        keypress = e.keysym
        if keypress == 'space':  
            ender()

start_game()
