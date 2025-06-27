from tkinter import Tk, Canvas, PhotoImage, Menu, messagebox
import random
import os
import pygame
import time

pygame.mixer.init()

obstacle_images = [
  "cacti.png",
  "cacti2.png",
  "cacti3.png"
]

ptero_images = [
  "ptero.png",
  "ptero2.png"
]

SOUND_JUMP = "jump.mp3"
SOUND_GAME_OVER = "game_over.mp3"
SOUND_POINT = "point.mp3"

INITIAL_SPEED = -7.5
SPEED_INCREMENT = 0.1
SCORE_RATE = 10
POINT_MILESTONE = 100
RECORDS_FILE = "records.txt"

class DinoGame:
  def __init__(self, master):
    self.master = master
    self.master.title("Динозаврик")
    self.master.geometry("600x400")
    self.master.resizable(False, False)
        
    self.master.bind("<space>", self.on_space_or_click)
    self.master.bind("<Button-1>", self.on_mouse_click)
    self.master.bind("<Down>", self.on_down_press)

    self.create_menu()
    self.load_images()
    self.load_sounds()
    self.setup_game()

    self.high_score = self.load_high_score()
    self.reset_game_state()
    self.first_game = True
    self.game_started = False
    
    self.show_start_screen()

  def create_menu(self):
    menubar = Menu(self.master)
    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label="Как играть?", command=self.show_help)
    help_menu.add_command(label="Об игре", command=self.show_info)
    menubar.add_cascade(label="Справка", menu=help_menu)
    
    self.master.config(menu=menubar)

  def show_help(self):
    messagebox.showinfo(title = "Справка", message = "Как играть?", detail = "- Нажмите пробел или кликните мышкой, чтобы начать!" \
    "\n- Перепрыгивайте через препятствия, нажимая пробел.\n- Уворачивайтесь от птеродактилей, нажимая клавишу ↓.\n- Чтобы вернуться к обычному бегу, нажмите ↓ еще раз.\n- Кликните мышкой, чтобы начать новую игру!")

  def show_info(self):
    messagebox.showinfo(title = "Справка", message = "Об игре", detail = "Данная игра разработана как индивидуальный проект по дисциплине «Информационные системы и технологии». Управляйте динозавриком, преодолевая препятствия и постарайтесь набрать как можно больше очков!")

  def show_start_screen(self):
    self.canvas.create_text(300, 200, text="Р-р-р! Нажми пробел, чтобы начать!", font=("Arial", 16), fill="black", tags="start_screen")

  def load_images(self):
    self.dino_run_frames = [
      PhotoImage(file="dino.png"),
      PhotoImage(file="dino2.png"),
      PhotoImage(file="dino3.png")
    ]
    self.dino_duck_frames = [
      PhotoImage(file="dino_duck.png"),
      PhotoImage(file="dino_duck2.png")
    ]
    self.dino_jump_img = PhotoImage(file="dino.png")
    self.dino_game_over_img = PhotoImage(file="dino4.png")
    self.cloud_image = PhotoImage(file="cloud.png")
    self.cloud_image2 = PhotoImage(file="cloud2.png")
    self.bg = PhotoImage(file="bg.png")
    self.ground_texture = PhotoImage(file="texture.png")

  def load_sounds(self):
    self.sound_jump = pygame.mixer.Sound(SOUND_JUMP)
    self.sound_game_over = pygame.mixer.Sound(SOUND_GAME_OVER)
    self.sound_point = pygame.mixer.Sound(SOUND_POINT)

  def setup_game(self):
    self.canvas = Canvas(self.master, bg="white", width=600, height=400)
    self.canvas.pack()
    self.canvas.create_image(300, 200, image=self.bg)

  def reset_game_state(self):
    self.speed = INITIAL_SPEED
    self.score = 0
    self.last_score_time = 0
    self.is_game_over = True
    self.jumping = False
    self.ducking = False
    self.velocity = 0
    self.current_frame = 0
    self.animation_counter = 0
    self.ptero_frame = 0
    self.ptero_animation_counter = 0

    self.canvas.delete("all")
    self.canvas.create_image(300, 200, image=self.bg)
    self.ground1 = self.canvas.create_image(0, 315, image=self.ground_texture, anchor='nw')
    self.ground2 = self.canvas.create_image(600, 315, image=self.ground_texture, anchor='nw')
    self.cloud1 = self.canvas.create_image(700, 110, image=self.cloud_image)
    self.cloud2 = self.canvas.create_image(1000, 140, image=self.cloud_image2)
    self.dino = self.canvas.create_image(100, 310, image=self.dino_run_frames[0])
    self.score_text = self.canvas.create_text(590, 10, text="Счёт: 0", font=("Arial", 14), fill="black", anchor="ne")
    self.high_score_text = self.canvas.create_text(590, 40, text=f"Рекорд: {self.high_score}", font=("Arial", 14), fill="black", anchor="ne")

  def load_high_score(self):
    if os.path.exists(RECORDS_FILE):
      with open(RECORDS_FILE, 'r') as f:
        return int(f.read())
    return 0

  def save_high_score(self):
    with open(RECORDS_FILE, 'w') as f:
      f.write(str(self.high_score))

  def start_game(self):
    self.canvas.delete("start_screen")
    self.reset_game_state()
    self.is_game_over = False
    self.game_started = True
    self.last_score_time = time.time()
    self.create_obstacle()
    self.update_game()

  def on_space_or_click(self, event):
    if not self.game_started:
      self.start_game()
    elif not self.is_game_over and not self.ducking:
      self.jump()

  def on_mouse_click(self, event):
    if not self.game_started:
      self.start_game()
    elif self.is_game_over:
      self.start_game()

  def on_down_press(self, event):
    if not self.is_game_over and not self.jumping:
      self.ducking = not self.ducking
      if self.ducking:
        self.canvas.coords(self.dino, 100, 320)
      else:
        self.canvas.coords(self.dino, 100, 310)

  def create_obstacle(self):
    self.is_ptero = random.random() < 0.3
    if self.is_ptero:
      self.ptero_height = random.choice([240, 280, 290])
      self.cactiPic = PhotoImage(file=random.choice(ptero_images))
      self.obstacle = self.canvas.create_image(800, self.ptero_height, image=self.cactiPic)
    else:
      self.cactiPic = PhotoImage(file=random.choice(obstacle_images))
      self.obstacle = self.canvas.create_image(800, 310, image=self.cactiPic)

  def jump(self):
    if not self.jumping and not self.is_game_over:
      self.jumping = True
      self.velocity = -14
      self.gravity = 0.7
      self.canvas.itemconfig(self.dino, image=self.dino_jump_img)
      self.sound_jump.play()

  def update_game(self):
    if not self.is_game_over:
      current_time = time.time()
      time_elapsed = current_time - self.last_score_time
      new_score = int(self.score + time_elapsed * SCORE_RATE)
      if new_score // POINT_MILESTONE > self.score // POINT_MILESTONE:
        self.sound_point.play()
      if new_score != self.score:
        self.score = new_score
        self.last_score_time = current_time
        self.update_score()
      
      if not self.jumping and not self.ducking:
        self.animation_counter += 1
        if self.animation_counter % 4 == 0:
          self.current_frame = (self.current_frame + 1) % len(self.dino_run_frames)
          self.canvas.itemconfig(self.dino, image=self.dino_run_frames[self.current_frame])
      elif self.ducking:
        self.animation_counter += 1
        if self.animation_counter % 4 == 0:
          self.current_frame = (self.current_frame + 1) % len(self.dino_duck_frames)
          self.canvas.itemconfig(self.dino, image=self.dino_duck_frames[self.current_frame])
      
      if self.is_ptero and hasattr(self, "obstacle"):
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
        self.speed -= SPEED_INCREMENT
        self.create_obstacle()
      
      self.move_clouds()
      self.move_ground()
      self.master.after(16, self.update_game)

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

    dino_img = self.dino_jump_img if self.jumping else self.dino_run_frames[0] if not self.ducking else self.dino_duck_frames[0]
    dino_width = dino_img.width()
    dino_height = dino_img.height()
    dino_collision_width = dino_width * 0.8
    dino_x_offset = (dino_width - dino_collision_width) / 2
    dino_collision_height = dino_height * 0.7 if not self.ducking else dino_height * 0.5

    obstacle_width = self.cactiPic.width()
    obstacle_height = self.cactiPic.height()

    if self.is_ptero:
      if self.ptero_height == 240 and self.ducking:
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
      if self.is_ptero and self.ptero_height > 240:
        if self.jumping and dino_coords[1] < obstacle_coords[1] + obstacle_height / 2:
          return False
      return True
    return False

  def game_over(self):
    self.is_game_over = True
    if self.ducking:
      self.canvas.coords(self.dino, 100, 310)
    self.canvas.itemconfig(self.dino, image=self.dino_game_over_img)
    self.canvas.create_text(300, 200, text="Конец игры!", font=("Arial", 16), fill="black")
    self.canvas.create_text(300, 230, text="Кликните мышкой, чтобы начать заново!", font=("Arial", 16), fill="black")
    self.sound_game_over.play()
    if self.score > self.high_score:
      self.high_score = self.score
      self.save_high_score()
      self.canvas.itemconfig(self.high_score_text, text=f"Рекорд: {self.high_score}")

  def update_score(self):
    self.canvas.itemconfig(self.score_text, text=f"Счёт: {self.score}")

if __name__ == "__main__":
  root = Tk()
  game = DinoGame(root)
  root.mainloop()
