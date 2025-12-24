import tkinter as tk # Library GUI untuk membuat tampilan grafis
import math #  Library matematika untuk perhitungan
import random # untuk menghasilkan nilai acak
import time # untuk pengaturan waktu dan delay

class SpaceDefenderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Defender")
        self.root.resizable(True, True)
        
        # Info Frame (di atas canvas)
        info_frame = tk.Frame(root, bg='#1a1a2e', pady=5)
        info_frame.pack(fill=tk.X)
        
        # Info kiri - Stats pesawat
        left_info = tk.Frame(info_frame, bg='#1a1a2e')
        left_info.pack(side=tk.LEFT, padx=15)
        
        self.ship_scale_label = tk.Label(left_info, text="Ship Size: 1.0x", 
                                         bg='#1a1a2e', fg='#00ff00', 
                                         font=('Arial', 10, 'bold'))
        self.ship_scale_label.pack()
        
        self.ship_pos_label = tk.Label(left_info, text="Position: (400, 450)", 
                                       bg='#1a1a2e', fg='#00ffff', 
                                       font=('Arial', 9))
        self.ship_pos_label.pack()
        
        # Progress bar - tengah
        progress_container = tk.Frame(info_frame, bg='#1a1a2e')
        progress_container.pack(side=tk.LEFT, expand=True, padx=15)
        
        tk.Label(progress_container, text="Progress to Victory", 
                bg='#1a1a2e', fg='#ffffff', font=('Arial', 9, 'bold')).pack()
        
        progress_frame = tk.Frame(progress_container, bg='#333333', 
                                 width=280, height=20, relief=tk.SUNKEN, bd=2)
        progress_frame.pack(pady=2)
        progress_frame.pack_propagate(False)
        
        self.progress_bar = tk.Canvas(progress_frame, width=276, height=16, 
                                      bg='#333333', highlightthickness=0)
        self.progress_bar.pack()
        
        self.progress_text = tk.Label(progress_container, text="0 / 500", 
                                      bg='#1a1a2e', fg='#ffff00', 
                                      font=('Arial', 8, 'bold'))
        self.progress_text.pack()
        
        # Info kanan - Score
        right_info = tk.Frame(info_frame, bg='#1a1a2e')
        right_info.pack(side=tk.RIGHT, padx=15)
        
        self.score_label = tk.Label(right_info, text="Score: 0", 
                                    bg='#1a1a2e', fg='#f1c40f', 
                                    font=('Arial', 16, 'bold'))
        self.score_label.pack()
        
        # Canvas
        self.canvas = tk.Canvas(root, width=800, height=580, bg='#000033')
        self.canvas.pack()
        
        # Control Frame
        control_frame = tk.Frame(root, bg='#2c3e50', pady=5)
        control_frame.pack(fill=tk.X, padx=5)
        
        self.start_btn = tk.Button(control_frame, text="▶", command=self.start_game, 
                                   bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), 
                                   width=4, height=1)
        self.start_btn.pack(side=tk.LEFT, padx=3)
        
        self.pause_btn = tk.Button(control_frame, text="⏸", command=self.pause_game,
                                   bg='#f39c12', fg='white', font=('Arial', 10, 'bold'), 
                                   width=4, height=1)
        self.pause_btn.pack(side=tk.LEFT, padx=3)
        
        self.reset_btn = tk.Button(control_frame, text="↻", command=self.reset_game,
                                   bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'), 
                                   width=4, height=1)
        self.reset_btn.pack(side=tk.LEFT, padx=3)
        
        tk.Label(control_frame, text="Controls: ←→ Move | Space: Shoot | ↑↓ Scale", 
                bg='#2c3e50', fg='#95a5a6', font=('Arial', 9)).pack(side=tk.RIGHT, padx=8)
        
        # Game state
        self.is_playing = False
        self.game_won = False
        self.score = 0
        self.final_score = 0
        self.player = {
            'x': 400, 
            'y': 450,
            'facing': 'right',
            'scale': 1.0,
            'last_move': 0
        }
        self.bullets = []
        self.enemies = []
        self.stars = []
        self.powerups = []
        self.last_shot = 0
        self.last_powerup_spawn = 0
        
        # Initialize stars
        for _ in range(100):
            self.stars.append({
                'x': random.randint(0, 800),
                'y': random.randint(0, 580),
                'size': random.uniform(1, 3)
            })
        
        # Keyboard bindings
        self.root.bind('<Left>', lambda e: self.move_player(-20, 'left'))
        self.root.bind('<Right>', lambda e: self.move_player(20, 'right'))
        self.root.bind('<space>', lambda e: self.shoot())
        self.root.bind('<Up>', lambda e: self.scale_player(1.2))
        self.root.bind('<Down>', lambda e: self.scale_player(0.8))
        
        # Canvas click binding
        self.canvas.bind('<Button-1>', self.canvas_click)
        
        self.update_info_display()
        self.draw_start_screen()
    
    def canvas_click(self, event):
        """Handle klik di canvas"""
        if not self.is_playing and not self.game_won:
            # Area tombol START di canvas
            if 300 <= event.x <= 500 and 420 <= event.y <= 470:
                self.start_game()
        
        if self.game_won:
            # Area tombol RESET di canvas
            if 300 <= event.x <= 500 and 480 <= event.y <= 530:
                self.reset_game()
        
        # Tombol PAUSE/RESUME in-game (pojok kanan atas)
        if self.is_playing or (not self.is_playing and not self.game_won and self.score > 0):
            if 720 <= event.x <= 780 and 10 <= event.y <= 40:
                if self.is_playing:
                    self.pause_game()
                else:
                    self.resume_game()
    
    def update_info_display(self):
        """Update info pesawat dan progress bar"""
        self.ship_scale_label.config(text=f"Ship Size: {self.player['scale']:.1f}x")
        self.ship_pos_label.config(text=f"Position: ({int(self.player['x'])}, {int(self.player['y'])})")
        self.score_label.config(text=f"Score: {self.score}")
        
        # Update progress bar
        progress = min(self.score / 500, 1.0)
        bar_width = int(276 * progress)
        
        self.progress_bar.delete('all')
        self.progress_bar.create_rectangle(0, 0, 276, 16, fill='#333333', outline='')
        
        if bar_width > 0:
            if progress < 0.5:
                color = '#ff6600'
            elif progress < 0.8:
                color = '#ffff00'
            else:
                color = '#00ff00'
            
            self.progress_bar.create_rectangle(0, 0, bar_width, 16, fill=color, outline='')
        
        percent = int(progress * 100)
        self.progress_bar.create_text(138, 8, text=f"{percent}%", 
                                      fill='#ffffff', font=('Arial', 9, 'bold'))
        
        self.progress_text.config(text=f"{self.score} / 500")
    
    def draw_line_dda(self, x0, y0, x1, y1, color='white'):
        dx = x1 - x0
        dy = y1 - y0
        steps = max(abs(dx), abs(dy))
        if steps == 0:
            return
        
        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x0, y0
        
        for _ in range(int(steps) + 1):
            self.canvas.create_rectangle(round(x), round(y), 
                                        round(x)+2, round(y)+2, 
                                        fill=color, outline=color)
            x += x_inc
            y += y_inc
    
    def draw_circle_midpoint(self, xc, yc, r, color='white', fill=False):
        if fill:
            self.canvas.create_oval(xc-r, yc-r, xc+r, yc+r, fill=color, outline=color)
            return
        
        x = 0
        y = r
        d = 1 - r
        
        def plot_circle_points(xc, yc, x, y):
            points = [
                (xc + x, yc + y), (xc - x, yc + y),
                (xc + x, yc - y), (xc - x, yc - y),
                (xc + y, yc + x), (xc - y, yc + x),
                (xc + y, yc - x), (xc - y, yc - x)
            ]
            for px, py in points:
                self.canvas.create_rectangle(px, py, px+2, py+2, fill=color, outline=color)
        
        plot_circle_points(xc, yc, x, y)
        
        while x < y:
            x += 1
            if d < 0:
                d = d + 2 * x + 1
            else:
                y -= 1
                d = d + 2 * (x - y) + 1
            plot_circle_points(xc, yc, x, y)
    
    def draw_polygon(self, vertices, color='white', fill=False):
        if len(vertices) < 3:
            return
        
        if fill:
            flat_coords = [coord for point in vertices for coord in point]
            self.canvas.create_polygon(flat_coords, fill=color, outline=color)
        else:
            for i in range(len(vertices)):
                x0, y0 = vertices[i]
                x1, y1 = vertices[(i + 1) % len(vertices)]
                self.draw_line_dda(x0, y0, x1, y1, color)
    
    def translate(self, vertices, tx, ty):
        return [(x + tx, y + ty) for x, y in vertices]
    
    def rotate(self, vertices, angle, cx=0, cy=0):
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        result = []
        for x, y in vertices:
            dx = x - cx
            dy = y - cy
            new_x = cx + dx * cos_a - dy * sin_a
            new_y = cy + dx * sin_a + dy * cos_a
            result.append((new_x, new_y))
        return result
    
    def scale(self, vertices, sx, sy, cx=0, cy=0):
        return [(cx + (x - cx) * sx, cy + (y - cy) * sy) for x, y in vertices]
    
    def reflect(self, vertices, axis='x', pos=0):
        if axis == 'x':
            return [(x, 2 * pos - y) for x, y in vertices]
        else:
            return [(2 * pos - x, y) for x, y in vertices]
    
    def draw_player(self, x, y, facing='right', scale_factor=1.0):
        ship = [(0, -20), (-15, 20), (0, 10), (15, 20)]
        ship = self.scale(ship, scale_factor, scale_factor, 0, 0)
        
        if facing == 'left':
            ship = self.reflect(ship, axis='y', pos=0)
            engine_offset = -15 * scale_factor
        else:
            engine_offset = 15 * scale_factor
        
        ship = self.translate(ship, x, y)
        self.draw_polygon(ship, '#00ff00', fill=True)
        
        engine_size = int(3 * scale_factor)
        self.draw_circle_midpoint(int(x), int(y + engine_offset), engine_size, '#ffff00', fill=True)
    
    def draw_enemy(self, x, y, rotation, spawn_side='center', scale_factor=1.0):
        enemy = [(0, -10), (-12, -5), (-8, 10), (8, 10), (12, -5)]
        enemy = self.scale(enemy, scale_factor, scale_factor, 0, 0)
        
        if spawn_side == 'left':
            enemy = self.reflect(enemy, axis='y', pos=0)
            color = '#ff6600'
            core_color = '#ff9966'
        else:
            color = '#ff0000'
            core_color = '#ff6666'
        
        enemy = self.rotate(enemy, rotation)
        enemy = self.translate(enemy, x, y)
        self.draw_polygon(enemy, color, fill=True)
        
        core_size = int(3 * scale_factor)
        self.draw_circle_midpoint(int(x), int(y), core_size, core_color, fill=True)
    
    def draw_bullet(self, x, y, scale_factor=1.0):
        size = int(3 * scale_factor)
        self.draw_circle_midpoint(int(x), int(y), size, '#ffff00', fill=True)
    
    def draw_powerup(self, x, y, powerup_type):
        pulse = 0.8 + 0.2 * math.sin(time.time() * 5)
        
        if powerup_type == 'scale_up':
            square = [(-8, -8), (8, -8), (8, 8), (-8, 8)]
            square = self.scale(square, pulse, pulse, 0, 0)
            square = self.translate(square, x, y)
            self.draw_polygon(square, '#00ffff', fill=True)
            self.canvas.create_text(x, y, text="↑", fill='#ffffff', font=('Arial', 14, 'bold'))
        
        elif powerup_type == 'scale_down':
            square = [(-8, -8), (8, -8), (8, 8), (-8, 8)]
            square = self.scale(square, pulse, pulse, 0, 0)
            square = self.translate(square, x, y)
            self.draw_polygon(square, '#ffff00', fill=True)
            self.canvas.create_text(x, y, text="↓", fill='#000000', font=('Arial', 14, 'bold'))
    
    def draw_button(self, x, y, width, height, text, color, hover=False):
        button_color = color if not hover else self.lighten_color(color)
        
        self.canvas.create_rectangle(x+3, y+3, x+width+3, y+height+3, fill='#000000', outline='')
        self.canvas.create_rectangle(x, y, x+width, y+height, fill=button_color, outline='#ffffff', width=2)
        self.canvas.create_text(x+width//2, y+height//2, text=text, fill='#ffffff', font=('Arial', 18, 'bold'))
    
    def draw_small_button(self, x, y, width, height, text, color):
        """Menggambar tombol kecil di canvas untuk in-game control"""
        self.canvas.create_rectangle(x+2, y+2, x+width+2, y+height+2, fill='#000000', outline='')
        self.canvas.create_rectangle(x, y, x+width, y+height, fill=color, outline='#ffffff', width=1)
        self.canvas.create_text(x+width//2, y+height//2, text=text, fill='#ffffff', font=('Arial', 10, 'bold'))
    
    def lighten_color(self, color):
        colors = {
            '#27ae60': '#2ecc71',
            '#e74c3c': '#e67e73'
        }
        return colors.get(color, color)
    
    def draw_start_screen(self):
        self.canvas.delete('all')
        
        for star in self.stars:
            self.draw_circle_midpoint(int(star['x']), int(star['y']), 
                                     int(star['size']), '#ffffff', fill=True)
        
        colors = ['#ff0000', '#ff6600', '#ffff00', '#00ff00', '#00ffff', '#0000ff', '#ff00ff']
        color_index = int(time.time() * 3) % len(colors)
        
        self.canvas.create_text(400, 180, text="SPACE DEFENDER", 
                               fill=colors[color_index], font=('Arial', 60, 'bold'))
        
        self.canvas.create_text(400, 250, text="Reach 500 points to WIN!", 
                               fill='#ffff00', font=('Arial', 18))
        
        pulse = 0.8 + 0.4 * math.sin(time.time() * 2)
        self.draw_player(400, 330, 'right', pulse)
        
        self.canvas.create_text(400, 395, text="← → : Move Ship  |  SPACE : Shoot  |  ↑ ↓ : Scale Ship", 
                               fill='#00ffff', font=('Arial', 13))
        
        self.draw_button(300, 420, 200, 50, "▶ START GAME", '#27ae60')
        
        blink = int(time.time() * 2) % 2
        if blink:
            self.canvas.create_text(400, 510, text="Click START button above or press ▶ button below", 
                                   fill='#00ff00', font=('Arial', 14))
        
        if not self.is_playing and not self.game_won:
            self.root.after(50, self.draw_start_screen)
    
    def draw_win_screen(self):
        self.canvas.delete('all')
        
        for star in self.stars:
            self.draw_circle_midpoint(int(star['x']), int(star['y']), 
                                     int(star['size']), '#ffffff', fill=True)
        
        colors = ['#ff0000', '#ff6600', '#ffff00', '#00ff00', '#00ffff', '#0000ff', '#ff00ff']
        for i in range(8):
            angle = i * 45 + (time.time() * 100) % 360
            rad = math.radians(angle)
            x = 400 + 150 * math.cos(rad)
            y = 180 + 150 * math.sin(rad)
            size = 10 + 5 * math.sin(time.time() * 5 + i)
            self.draw_circle_midpoint(int(x), int(y), int(size), colors[i % 7], fill=True)
        
        scale_text = 1.0 + 0.2 * math.sin(time.time() * 3)
        font_size = int(65 * scale_text)
        
        self.canvas.create_text(400, 180, text="YOU WIN!", 
                               fill='#ffff00', font=('Arial', font_size, 'bold'))
        
        self.canvas.create_text(400, 260, text="FINAL SCORE", 
                               fill='#00ffff', font=('Arial', 24, 'bold'))
        
        score_pulse = 1.0 + 0.1 * math.sin(time.time() * 4)
        score_size = int(50 * score_pulse)
        self.canvas.create_text(400, 320, text=str(self.final_score), 
                               fill='#ff00ff', font=('Arial', score_size, 'bold'))
        
        victory_scale = 1.5 + 0.3 * math.sin(time.time() * 2)
        self.draw_player(400, 400, 'right', victory_scale)
        
        self.canvas.create_text(400, 455, text="Congratulations, Commander!", 
                               fill='#ffffff', font=('Arial', 16))
        
        self.draw_button(300, 480, 200, 50, "↻ PLAY AGAIN", '#e74c3c')
        
        blink = int(time.time() * 2) % 2
        if blink:
            self.canvas.create_text(400, 550, text="Click PLAY AGAIN above or press ↻ button below", 
                                   fill='#ff00ff', font=('Arial', 13, 'bold'))
        
        if self.game_won:
            self.root.after(50, self.draw_win_screen)
    
    def scale_player(self, scale_change):
        if not self.is_playing:
            return
        
        new_scale = self.player['scale'] * scale_change
        self.player['scale'] = max(0.5, min(2.0, new_scale))
        self.update_info_display()
    
    def move_player(self, dx, direction):
        if not self.is_playing:
            return
        
        self.player['x'] = max(20, min(780, self.player['x'] + dx))
        self.player['facing'] = direction
        self.player['last_move'] = time.time()
        self.update_info_display()
    
    def shoot(self):
        if not self.is_playing:
            return
        now = time.time()
        if now - self.last_shot > 0.25:
            self.bullets.append({
                'x': self.player['x'], 
                'y': self.player['y'] - 20,
                'scale': self.player['scale']
            })
            self.last_shot = now
    
    def start_game(self):
        if not self.is_playing and not self.game_won:
            self.is_playing = True
            self.game_loop()
    
    def pause_game(self):
        self.is_playing = False
    
    def resume_game(self):
        if not self.game_won and self.score > 0:
            self.is_playing = True
            self.game_loop()
    
    def reset_game(self):
        self.is_playing = False
        self.game_won = False
        self.score = 0
        self.final_score = 0
        self.player = {'x': 400, 'y': 450, 'facing': 'right', 'scale': 1.0, 'last_move': 0}
        self.bullets = []
        self.enemies = []
        self.powerups = []
        self.update_info_display()
        self.canvas.delete('all')
        self.draw_start_screen()
    
    def game_loop(self):
        if not self.is_playing:
            return
        
        if self.score >= 500:
            self.is_playing = False
            self.game_won = True
            self.final_score = self.score
            self.draw_win_screen()
            return
        
        self.canvas.delete('all')
        
        for star in self.stars:
            self.draw_circle_midpoint(int(star['x']), int(star['y']), 
                                     int(star['size']), '#ffffff', fill=True)
            star['y'] += 0.5
            if star['y'] > 580:
                star['y'] = 0
                star['x'] = random.randint(0, 800)
        
        now = time.time()
        if now - self.last_powerup_spawn > 8:
            powerup_type = random.choice(['scale_up', 'scale_down'])
            self.powerups.append({
                'x': random.randint(50, 750),
                'y': -20,
                'type': powerup_type
            })
            self.last_powerup_spawn = now
        
        for powerup in self.powerups[:]:
            powerup['y'] += 2
            
            if powerup['y'] > 630:
                self.powerups.remove(powerup)
            else:
                self.draw_powerup(powerup['x'], powerup['y'], powerup['type'])
                
                dist = math.sqrt((powerup['x'] - self.player['x'])**2 + 
                               (powerup['y'] - self.player['y'])**2)
                if dist < 25:
                    if powerup['type'] == 'scale_up':
                        self.player['scale'] = min(2.0, self.player['scale'] * 1.3)
                    else:
                        for enemy in self.enemies:
                            enemy['scale'] = enemy.get('scale', 1.0) * 0.7
                    self.powerups.remove(powerup)
                    self.score += 5
                    self.update_info_display()
        
        if random.random() < 0.02:
            spawn_x = random.randint(20, 780)
            spawn_side = 'left' if spawn_x < 400 else 'center'
            
            self.enemies.append({
                'x': spawn_x,
                'y': -20,
                'rotation': 0,
                'spawn_side': spawn_side,
                'scale': 0.3,
                'target_scale': 1.0
            })
        
        for enemy in self.enemies[:]:
            enemy['y'] += 2
            enemy['rotation'] += 3
            
            if enemy['scale'] < enemy.get('target_scale', 1.0):
                enemy['scale'] += 0.02
            
            if enemy['y'] > 630:
                self.enemies.remove(enemy)
            else:
                self.draw_enemy(enemy['x'], enemy['y'], enemy['rotation'], 
                              enemy.get('spawn_side', 'center'), enemy['scale'])
        
        for bullet in self.bullets[:]:
            bullet['y'] -= 5
            
            if bullet['y'] < -10:
                self.bullets.remove(bullet)
            else:
                self.draw_bullet(bullet['x'], bullet['y'], bullet.get('scale', 1.0))
                
                for enemy in self.enemies[:]:
                    dist = math.sqrt((bullet['x'] - enemy['x'])**2 + 
                                   (bullet['y'] - enemy['y'])**2)
                    collision_radius = 15 * enemy.get('scale', 1.0)
                    
                    if dist < collision_radius:
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        bonus = 15 if enemy.get('spawn_side') == 'left' else 10
                        self.score += bonus
                        self.update_info_display()
                        break
        
        self.draw_player(self.player['x'], self.player['y'], 
                        self.player['facing'], self.player['scale'])
        
        # Draw tombol PAUSE kecil di pojok kanan atas saat bermain
        self.draw_small_button(720, 10, 60, 30, "⏸", '#f39c12')
        
        self.root.after(16, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceDefenderGame(root)
    root.mainloop()