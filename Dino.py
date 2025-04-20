import tkinter as tk
import random

speed = -5

class DinoGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Dino Game")
        self.master.geometry("600x600")
        
        self.score_label = tk.Label(master, text="Score: 0")
        self.score_label.pack(pady = 5, anchor = "e", padx = 5)
        
        self.canvas = tk.Canvas(master, bg="white", width = 600, height=400)
        self.canvas.pack(pady = 5, padx = 5)

        self.dino = self.canvas.create_rectangle(50, 300, 100, 350, fill="green")
        self.obstacle = None
        self.velocity = 0
        self.gravity = 1
        self.jumping = False
        self.score = 0
        self.is_game_over = False

        self.jump_button = tk.Button(master, text="Jump", command=self.jump, width = 16, height = 2)
        self.jump_button.pack(pady = 15)
        
        self.canvas.bind("<KeyPress-Up>", self.jump)
        self.canvas.focus_set()

        self.create_obstacle()
        self.update_game()

    def create_obstacle(self):
        x_position = 800
        height = random.randint(50, 120)
        self.obstacle = self.canvas.create_rectangle(x_position, 350 - height, x_position + 20, 350, fill="red")

    def jump(self, event=None):
        if not self.jumping and not self.is_game_over:
            self.jumping = True
            self.velocity = -17

    def update_game(self):
        global speed
        if not self.is_game_over:
            if self.jumping:
                self.canvas.move(self.dino, 0, self.velocity)
                self.velocity += self.gravity
                if self.canvas.coords(self.dino)[1] >= 300:
                    self.canvas.move(self.dino, 0, 300 - self.canvas.coords(self.dino)[1])
                    self.jumping = False
                        
            self.canvas.move(self.obstacle, speed, 0)
            obstacle_coords = self.canvas.coords(self.obstacle)

            if self.check_collision():
                self.is_game_over = True
                self.canvas.create_text(400, 200, text="Game Over!", font=("Arial", 24), fill="red")
            else:   
                if obstacle_coords[0] < 0:
                    self.canvas.delete(self.obstacle)
                    self.score += 1
                    self.score_label.config(text=f"Score: {self.score}")
                    speed -= 0.5
                    self.create_obstacle()

            self.master.after(30, self.update_game)

    def check_collision(self):
        dino_coords = self.canvas.coords(self.dino)
        obstacle_coords = self.canvas.coords(self.obstacle)

        if (dino_coords[2] > obstacle_coords[0] and dino_coords[0] < obstacle_coords[2] and
            dino_coords[3] > obstacle_coords[1]):
            return True
        return False

    def restart_game(self):
        self.canvas.delete("all")
        self.create_obstacle()
        self.dino = self.canvas.create_rectangle(50, 300, 100, 350, fill="green")
        self.score = 0
        self.score_label.config(text="Score: 0")
        self.is_game_over = False
        self.update_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = DinoGame(root)
    root.mainloop()