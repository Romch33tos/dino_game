import tkinter as tk
import random
from tkinter import *
from PIL import Image
import shutil

speed = -5

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
        self.score_label = tk.Label(master, text="Счёт: 0")
        self.score_label.pack(pady=5, anchor="e", padx=5)
        root.protocol("WM_DELETE_WINDOW", delete)
        self.dinoPic = PhotoImage(file="Python/Программы/Игры/Dino/game_files/dino.png")
        self.canvas = tk.Canvas(master, bg="white", width=600, height=400)
        self.canvas.pack(pady=5, padx=5)
        self.dino = self.canvas.create_image(100, 300, image=self.dinoPic)
        self.obstacle = None
        self.velocity = 0
        self.gravity = 1
        self.jumping = False
        self.score = 0
        self.is_game_over = False
        self.jump_button = tk.Button(master, text="Прыжок!", command=self.jump, width=16, height=2)
        self.jump_button.pack(pady=15)
        self.canvas.bind("<KeyPress-Up>", self.jump)
        self.canvas.focus_set()
        self.create_obstacle()
        self.update_game()

    def create_obstacle(self):
        self.cactiPic = PhotoImage(file="Python/Программы/Игры/Dino/game_files/cacti.png")
        self.obstacle = self.canvas.create_image(800, 300, image=self.cactiPic)

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
                self.canvas.create_text(300, 200, text="Конец игры!", font=("Arial", 12), fill="red")
                self.jump_button.configure(text="Ещё раз?", command=self.restart_game)
            else:
                if obstacle_coords[0] < 0:
                    self.canvas.delete(self.obstacle)
                    self.score += 1
                    self.score_label.config(text=f"Счёт: {self.score}")
                    speed -= 0.5
                    self.create_obstacle()
            self.master.after(30, self.update_game)

    def check_collision(self):
        dino_coords = self.canvas.coords(self.dino)
        obstacle_coords = self.canvas.coords(self.obstacle)
        if (dino_coords[0] > obstacle_coords[0] and dino_coords[0] < obstacle_coords[2] and
            dino_coords[1] > obstacle_coords[1]):
            return True
        return False

    def restart_game(self):
        global speed
        speed = -5
        self.canvas.delete("all")
        self.create_obstacle()
        self.dino = self.canvas.create_image(100, 300, image=self.dinoPic)
        self.jump_button.configure(text="Прыжок!", command=self.jump)
        self.score = 0
        self.score_label.config(text="Счёт: 0")
        self.is_game_over = False
        self.update_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = DinoGame(root)
    root.mainloop()
