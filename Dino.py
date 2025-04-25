from tkinter import *
import tkinter as tk
import random

obstacle_images = [
    "Python/Программы/Игры/Dino/game_files/cacti1.png",
    "Python/Программы/Игры/Dino/game_files/cacti2.png",
    "Python/Программы/Игры/Dino/game_files/cacti3.png",
    "Python/Программы/Игры/Dino/game_files/cacti4.png",
    "Python/Программы/Игры/Dino/game_files/cacti5.png"
]

ptero_images = [
    "Python/Программы/Игры/Dino/game_files/pt1.png",
    "Python/Программы/Игры/Dino/game_files/pt2.png"
]

INITIAL_SPEED = -6.5
SPEED_INCREMENT = 0.1

class DinoGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Динозаврик")
        self.master.geometry("600x400")
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self.quit_game)
        self.load_images()
        self.setup_game()
        self.reset_game_state()
        
    def load_images(self):
        self.dino_run_frames = [
            PhotoImage(file="Python/Программы/Игры/Dino/game_files/dino.png"),
            PhotoImage(file="Python/Программы/Игры/Dino/game_files/dino2.png"),
            PhotoImage(file="Python/Программы/Игры/Dino/game_files/dino3.png")
        ]
        self.dino_jump_img = PhotoImage(file="Python/Программы/Игры/Dino/game_files/dino.png")
        self.dino_game_over_img = PhotoImage(file="Python/Программы/Игры/Dino/game_files/dino5.png")
        self.cloud_image = PhotoImage(file="Python/Программы/Игры/Dino/game_files/cloud.png")
        self.cloud_image2 = PhotoImage(file="Python/Программы/Игры/Dino/game_files/cloud2.png")
        self.bg = PhotoImage(file="Python/Программы/Игры/Dino/game_files/bg.png")
        self.ground_texture = PhotoImage(file="Python/Программы/Игры/Dino/game_files/texture.png")

    def setup_game(self):
        self.canvas = tk.Canvas(self.master, bg="white", width=600, height=400)
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.pack()
        self.canvas.create_image(300, 200, image=self.bg)

    def reset_game_state(self):
        self.speed = INITIAL_SPEED
        self.score = 0
        self.is_game_over = True
        self.jumping = False
        self.velocity = 0
        self.current_frame = 0
        self.animation_counter = 0
        self.ptero_frame = 0
        self.ptero_animation_counter = 0
        self.canvas.delete("all")
        self.canvas.create_image(300, 200, image=self.bg)
        self.ground1 = self.canvas.create_image(0, 315, image=self.ground_texture, anchor='nw')
        self.ground2 = self.canvas.create_image(600, 315, image=self.ground_texture, anchor='nw')
        self.cloud1 = self.canvas.create_image(700, 50, image=self.cloud_image)
        self.cloud2 = self.canvas.create_image(1000, 80, image=self.cloud_image2)
        self.dino = self.canvas.create_image(100, 310, image=self.dino_run_frames[0])
        self.score_text = self.canvas.create_text(590, 10, text="Счёт: 0", font=("Arial", 8), fill="black", anchor="ne")

    def start_game(self):
        self.reset_game_state()
        self.is_game_over = False
        self.create_obstacle()
        self.update_game()

    def on_click(self, event):
        if self.is_game_over:
            self.start_game()
        else:
            self.jump()

    def create_obstacle(self):
        self.is_ptero = random.random() < 0.3
        if self.is_ptero:
            self.ptero_height = random.choice([220, 280, 300])
            self.cactiPic = PhotoImage(file=random.choice(ptero_images))
            self.obstacle = self.canvas.create_image(800, self.ptero_height, image=self.cactiPic)
        else:
            self.cactiPic = PhotoImage(file=random.choice(obstacle_images))
            self.obstacle = self.canvas.create_image(800, 310, image=self.cactiPic)

    def jump(self):
        if not self.jumping and not self.is_game_over:
            self.jumping = True
            self.velocity = -15
            self.gravity = 0.7
            self.canvas.itemconfig(self.dino, image=self.dino_jump_img)

    def update_game(self):
        if not self.is_game_over:
            if not self.jumping:
                self.animation_counter += 1
                if self.animation_counter % 4 == 0:
                    self.current_frame = (self.current_frame + 1) % len(self.dino_run_frames)
                    self.canvas.itemconfig(self.dino, image=self.dino_run_frames[self.current_frame])
            if self.is_ptero and self.obstacle:
                self.ptero_animation_counter += 1
                if self.ptero_animation_counter % 10 == 0:
                    self.ptero_frame = (self.ptero_frame + 1) % len(ptero_images)
                    self.cactiPic = PhotoImage(file=ptero_images[self.ptero_frame])
                    self.canvas.itemconfig(self.obstacle, image=self.cactiPic)
            if self.jumping:
                self.canvas.move(self.dino, 0, self.velocity)
                self.velocity += self.gravity
                if self.canvas.coords(self.dino)[1] >= 310:
                    self.canvas.move(self.dino, 0, 310 - self.canvas.coords(self.dino)[1])
                    self.jumping = False
                    self.canvas.itemconfig(self.dino, image=self.dino_run_frames[0])
            self.canvas.move(self.obstacle, self.speed, 0)
            obstacle_coords = self.canvas.coords(self.obstacle)
            if self.check_collision():
                self.game_over()
            elif obstacle_coords[0] < -50:
                self.canvas.delete(self.obstacle)
                self.score += 1
                self.update_score()
                self.speed -= SPEED_INCREMENT
                self.create_obstacle()
            self.move_clouds()
            self.move_ground()
            self.master.after(17, self.update_game)

    def move_clouds(self):
        self.canvas.move(self.cloud1, self.speed * 0.5, 0)
        self.canvas.move(self.cloud2, self.speed * 0.5, 0)
        if self.canvas.coords(self.cloud1)[0] < -50:
            self.canvas.move(self.cloud1, 700, 0)
        if self.canvas.coords(self.cloud2)[0] < -50:
            self.canvas.move(self.cloud2, 700, 0)

    def move_ground(self):
        self.canvas.move(self.ground1, self.speed, 0)
        self.canvas.move(self.ground2, self.speed, 0)
        if self.canvas.coords(self.ground1)[0] < -600:
            self.canvas.move(self.ground1, 1200, 0)
        if self.canvas.coords(self.ground2)[0] < -600:
            self.canvas.move(self.ground2, 1200, 0)

    def check_collision(self):
        dino_coords = self.canvas.coords(self.dino)
        obstacle_coords = self.canvas.coords(self.obstacle)
        if not dino_coords or not obstacle_coords:
            return False
        dino_img = self.dino_jump_img if self.jumping else self.dino_run_frames[0]
        dino_width = dino_img.width()
        dino_height = dino_img.height()
        dino_collision_width = dino_width * 0.8
        dino_x_offset = (dino_width - dino_collision_width) / 2
        dino_collision_height = dino_height * 0.7
        obstacle_width = self.cactiPic.width()
        obstacle_height = self.cactiPic.height()
        if self.is_ptero:
            if self.ptero_height == 220 and not self.jumping:
                return False
            obstacle_collision_width = obstacle_width * 0.7
            obstacle_x_offset = (obstacle_width - obstacle_collision_width) / 2
            obstacle_collision_height = obstacle_height * 0.7
        else:
            obstacle_collision_width = obstacle_width * 0.8
            obstacle_x_offset = (obstacle_width - obstacle_collision_width) / 2
            obstacle_collision_height = obstacle_height * 0.9
        if (dino_coords[0] + dino_collision_width - dino_x_offset > obstacle_coords[0] - obstacle_x_offset and
            dino_coords[0] + dino_x_offset < obstacle_coords[0] + obstacle_collision_width - obstacle_x_offset and
            dino_coords[1] + dino_collision_height > obstacle_coords[1] + (obstacle_height - obstacle_collision_height)):
            if self.is_ptero and self.ptero_height > 220:
                if self.jumping and dino_coords[1] < obstacle_coords[1] + obstacle_height / 2:
                    return False
            return True
        return False

    def game_over(self):
        self.is_game_over = True
        self.canvas.itemconfig(self.dino, image=self.dino_game_over_img)
        self.canvas.create_text(300, 200, text="Конец игры!", font=("Arial", 12), fill="black")

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=f"Счёт: {self.score}")

    def quit_game(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = DinoGame(root)
    root.mainloop()
