from tkinter import *
import tkinter as tk
import random
import shutil

list = ["Python/Программы/Игры/Dino/game_files/cacti.png", 
        "Python/Программы/Игры/Dino/game_files/cacti2.png", 
        "Python/Программы/Игры/Dino/game_files/cacti3.png", 
        "Python/Программы/Игры/Dino/game_files/cacti4.png"]

speed = -6.5

shutil.unpack_archive("Python/Программы/Игры/Dino/game_files.zip", "Python/Программы/Игры/Dino/game_files")

def delete():
    shutil.rmtree("Python/Программы/Игры/Dino/game_files")
    root.destroy()

class DinoGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Динозаврик")
        self.master.geometry("600x600")
        self.master.resizable(False, False)
        
        self.score_label = tk.Label(master, text = "Счёт: 0")
        self.score_label.pack(pady = 5, anchor = "e", padx = 5)
        root.protocol("WM_DELETE_WINDOW", delete)

        self.dino_frames = [
            PhotoImage(file = "Python/Программы/Игры/Dino/game_files/dino.png"),
            PhotoImage(file = "Python/Программы/Игры/Dino/game_files/dino2.png"),
            PhotoImage(file = "Python/Программы/Игры/Dino/game_files/dino2.png"),
            PhotoImage(file = "Python/Программы/Игры/Dino/game_files/dino3.png"),
            PhotoImage(file = "Python/Программы/Игры/Dino/game_files/dino3.png"),
            PhotoImage(file = "Python/Программы/Игры/Dino/game_files/dino.png"),
            PhotoImage(file = "Python/Программы/Игры/Dino/game_files/dino.png")
        ]

        self.cloud = PhotoImage(file = "Python/Программы/Игры/Dino/game_files/cloud.png")
        self.bg = PhotoImage(file = "Python/Программы/Игры/Dino/game_files/bg.png")

        self.canvas = tk.Canvas(master, bg = "white", width = 600, height = 400)
        self.canvas.pack(pady = 5, padx = 5)

        self.canvas.create_image(300, 200, image = self.bg)
        
        self.cloud1 = self.canvas.create_image(100, 50, image = self.cloud)
        self.cloud2 = self.canvas.create_image(400, 80, image = self.cloud)

        self.dino = self.canvas.create_image(100, 310, image = self.dino_frames[0])
        self.obstacle = None
        self.velocity = 0
        self.gravity = 1
        self.jumping = False
        self.score = 0
        self.is_game_over = False
        self.current_frame = 0

        self.jump_button = tk.Button(master, text = "Прыжок!", command=self.jump, width = 16, height = 2)
        self.jump_button.pack(pady = 15)     

        self.create_obstacle()
        self.update_game()

    def create_obstacle(self):
        self.cactiPic = PhotoImage(file = random.choice(list))
        self.obstacle = self.canvas.create_image(800, 310, image = self.cactiPic)

    def jump(self, event = None):
        if not self.jumping and not self.is_game_over:
            self.jumping = True
            self.velocity = -19

    def update_game(self):
        global speed
        if not self.is_game_over:
            self.current_frame = (self.current_frame + 1) % len(self.dino_frames)
            self.canvas.itemconfig(self.dino, image=self.dino_frames[self.current_frame])

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
                self.canvas.create_text(300, 200, text="Конец игры!", font=("Arial", 12), fill="red")
                self.jump_button.configure(text="Ещё раз?", command=self.restart_game)
            else:
                if obstacle_coords[0] < 0: 
                    self.canvas.delete(self.obstacle)
                    self.score += 1
                    self.score_label.config(text=f"Счёт: {self.score}")
                    speed -= 0.2 
                    self.create_obstacle()

            self.move_clouds()   
            self.master.after(18, self.update_game)

    def move_clouds(self):
        self.canvas.move(self.cloud1, speed * 0.5, 0)
        self.canvas.move(self.cloud2, speed * 0.5, 0)

        if self.canvas.coords(self.cloud1)[0] < -50:
            self.canvas.move(self.cloud1, 700, 0)
        if self.canvas.coords(self.cloud2)[0] < -50:
            self.canvas.move(self.cloud2, 700, 0)

    def check_collision(self):
        dino_coords = self.canvas.coords(self.dino)
        obstacle_coords = self.canvas.coords(self.obstacle)
        if (dino_coords[0] < obstacle_coords[0] + self.cactiPic.width() and
            dino_coords[0] + self.dino_frames[0].width() > obstacle_coords[0] and
            dino_coords[1] + self.dino_frames[0].height() > obstacle_coords[1]):
            return True
        return False

    def restart_game(self):
        global speed
        speed = -6.5
        self.canvas.delete("all")
        self.canvas.create_image(300, 200, image=self.bg)
        self.cloud1 = self.canvas.create_image(100, 50, image=self.cloud)
        self.cloud2 = self.canvas.create_image(400, 80, image=self.cloud)
        self.create_obstacle()
        self.dino = self.canvas.create_image(100, 310, image=self.dino_frames[0])
        self.jump_button.configure(text="Прыжок!", command=self.jump)
        self.score = 0
        self.score_label.config(text="Счёт: 0")
        self.is_game_over = False
        self.current_frame = 0
        self.update_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = DinoGame(root)
    root.mainloop()
