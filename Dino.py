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

speed = -7.5

def delete():
    root.destroy()

class DinoGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Динозаврик")
        self.master.geometry("600x400")
        self.master.resizable(False, False)

        root.protocol("WM_DELETE_WINDOW", delete)

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

        self.canvas = tk.Canvas(master, bg="white", width=600, height=400)    
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_click)
        self.canvas.pack()
        
        self.canvas.create_image(300, 200, image=self.bg)

        self.ground1 = self.canvas.create_image(0, 315, image=self.ground_texture, anchor='nw')
        self.ground2 = self.canvas.create_image(600, 315, image=self.ground_texture, anchor='nw')
        self.dino = self.canvas.create_image(100, 310, image=self.dino_run_frames[0])
        self.obstacle = None
        self.velocity = 0
        self.gravity = 1
        self.jumping = False
        self.score = 0
        self.is_game_over = True
        self.current_frame = 0
        self.ptero_frame = 0
        self.is_ptero = False
        self.animation_counter = 0
        self.ptero_animation_counter = 0
        
    def start_game(self):
        global speed 
        self.is_game_over = False
        self.score = 0        
        self.speed = -7.5
        self.canvas.delete("all")
        self.canvas.create_image(300, 200, image=self.bg)
        self.ground1 = self.canvas.create_image(0, 315, image=self.ground_texture, anchor='nw')
        self.ground2 = self.canvas.create_image(600, 315, image=self.ground_texture, anchor='nw')
        
        self.cloud1 = self.canvas.create_image(700, 50, image=self.cloud_image)
        self.cloud2 = self.canvas.create_image(1000, 80, image=self.cloud_image2)
        
        self.score_text = self.canvas.create_text(590, 10, text="Счёт: 0", font=("Arial", 8), fill="black", anchor="ne")
        self.create_obstacle()
        self.dino = self.canvas.create_image(100, 310, image=self.dino_run_frames[0])
        self.update_score()
        self.update_game()

    def on_canvas_click(self, event):
        if self.is_game_over:
            self.start_game()
        else:
            self.jump()

    def create_obstacle(self):
        self.is_ptero = random.random() < 0.3
        if self.is_ptero:
            y_pos = random.choice([220, 280, 300])
            self.cactiPic = PhotoImage(file=random.choice(ptero_images))
            self.obstacle = self.canvas.create_image(800, y_pos, image=self.cactiPic)
        else:
            self.cactiPic = PhotoImage(file=random.choice(obstacle_images))
            self.obstacle = self.canvas.create_image(800, 310, image=self.cactiPic)

    def jump(self):
        if not self.jumping and not self.is_game_over:
            self.jumping = True
            self.velocity = -20
            self.canvas.itemconfig(self.dino, image=self.dino_jump_img)

    def update_game(self):
        global speed
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
                if self.canvas.coords(self.dino)[1] >= 300:
                    self.canvas.move(self.dino, 0, 300 - self.canvas.coords(self.dino)[1])
                    self.jumping = False
                    self.canvas.itemconfig(self.dino, image=self.dino_run_frames[0])

            self.canvas.move(self.obstacle, speed, 0)
            obstacle_coords = self.canvas.coords(self.obstacle)

            if self.check_collision():
                self.is_game_over = True
                self.canvas.itemconfig(self.dino, image=self.dino_game_over_img)
                self.canvas.create_text(300, 200, text="Конец игры!", font=("Arial", 12), fill="black")
                speed = -7.5         
            else:
                if obstacle_coords[0] < -50: 
                    self.canvas.delete(self.obstacle)
                    self.score += 1
                    self.update_score()  
                    speed -= 0.1 
                    self.create_obstacle()

            self.move_clouds()
            self.move_ground()
            self.master.after(17, self.update_game)

    def move_clouds(self):
        self.canvas.move(self.cloud1, speed * 0.5, 0)
        self.canvas.move(self.cloud2, speed * 0.5, 0)
        if self.canvas.coords(self.cloud1)[0] < -50:
            self.canvas.move(self.cloud1, 700, 0)
        if self.canvas.coords(self.cloud2)[0] < -50:
            self.canvas.move(self.cloud2, 700, 0)

    def move_ground(self):
        self.canvas.move(self.ground1, speed, 0)
        self.canvas.move(self.ground2, speed, 0)
        if self.canvas.coords(self.ground1)[0] < -600:
            self.canvas.move(self.ground1, 1200, 0)
        if self.canvas.coords(self.ground2)[0] < -600:
            self.canvas.move(self.ground2, 1200, 0)

    def check_collision(self):
        dino_coords = self.canvas.coords(self.dino)
        obstacle_coords = self.canvas.coords(self.obstacle)

        if not dino_coords or not obstacle_coords:
            return False

        dino_width = self.dino_jump_img.width() if self.jumping else self.dino_run_frames[0].width()
        dino_height = self.dino_jump_img.height() if self.jumping else self.dino_run_frames[0].height()

        if self.is_ptero:
            if (dino_coords[0] < obstacle_coords[0] + self.cactiPic.width() and
                dino_coords[0] + dino_width > obstacle_coords[0] and
                dino_coords[1] + dino_height > obstacle_coords[1]):
                if not self.jumping and obstacle_coords[1] == 220:
                    return False
                return True
        else:
            if (dino_coords[0] < obstacle_coords[0] + self.cactiPic.width() and
                dino_coords[0] + dino_width > obstacle_coords[0] and
                dino_coords[1] + dino_height > obstacle_coords[1]):
                return True
        return False
    
    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=f"Счёт: {self.score}")

if __name__ == "__main__":
    root = tk.Tk()
    game = DinoGame(root)
    root.mainloop()
