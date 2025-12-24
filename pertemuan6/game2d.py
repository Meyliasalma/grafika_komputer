import pygame
import math
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 800, 600
FPS = 60

# Warna
SKY_BLUE = (135, 206, 235)
CLOUD_WHITE = (255, 255, 255)
GRASS_GREEN = (107, 142, 35)
DIRT_BROWN = (139, 69, 19)
PLAYER_BLUE = (74, 144, 226)
SKIN_COLOR = (255, 212, 163)
GOLD = (255, 215, 0)
RED = (255, 68, 68)
BLACK = (0, 0, 0)

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Praktikum Transformasi 2D - Game Platformer")
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.facing_right = True
        self.rotation = 0  # Rotasi untuk efek dash
        self.is_dashing = False
        self.dash_cooldown = 0
        self.scale = 1.0  # Scaling
        self.target_scale = 1.0
        self.anim_frame = 0
        self.is_attacking = False
        self.attack_frame = 0
        self.sword_swing_angle = 0
        self.projectiles = []
        
    def move(self, keys):
        # Translasi horizontal menggunakan panah kiri dan kanan
        # dx = 20 sesuai soal
        dx = 20
        
        if keys[pygame.K_RIGHT]:  # Panah Kanan
            self.velocity_x = dx
            self.facing_right = True
        elif keys[pygame.K_LEFT]:  # Panah Kiri
            self.velocity_x = -dx
            self.facing_right = False
        else:
            self.velocity_x *= 0.8
            
        # Jump menggunakan panah atas (dy = 0 saat di tanah, dy berubah saat lompat)
        if keys[pygame.K_UP] and not self.is_jumping:
            self.velocity_y = -12
            self.is_jumping = True
            
        # Dash menggunakan huruf D - Rotasi 30 derajat dan serangan
        if keys[pygame.K_d] and not self.is_dashing and self.dash_cooldown == 0:
            self.is_dashing = True
            self.is_attacking = True
            self.attack_frame = 0
            self.dash_cooldown = 60
            self.velocity_x = (1 if self.facing_right else -1) * 15
            # Rotasi 30 derajat sesuai soal
            self.rotation = (1 if self.facing_right else -1) * math.radians(30)
        
        # Tembak projectile dengan huruf S
        if keys[pygame.K_s] and len(self.projectiles) < 3:
            self.shoot_projectile()
        
        # Scale up dengan huruf W
        if keys[pygame.K_w]:
            self.target_scale = min(self.target_scale + 0.05, 5.0)
        
        # Scale down dengan panah bawah
        if keys[pygame.K_DOWN]:
            self.target_scale = max(self.target_scale - 0.05, 0.5)
            
    def update(self):
        # Gravity
        self.velocity_y += 0.5
        
        # Update posisi (Translasi dengan dx=20, dy=0 di tanah)
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Ground collision
        ground_y = HEIGHT - 150
        if self.y >= ground_y - self.height:
            self.y = ground_y - self.height
            self.velocity_y = 0  # dy = 0 saat di tanah
            self.is_jumping = False
            
        # Screen boundaries
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
            
        # Dash cooldown
        if self.is_dashing:
            self.dash_cooldown -= 1
            self.attack_frame += 1
            # Animasi ayunan pedang (0 sampai 120 derajat)
            self.sword_swing_angle = min(self.attack_frame * 6, 120)
            
            if self.dash_cooldown <= 40:
                self.is_dashing = False
                self.is_attacking = False
                self.sword_swing_angle = 0
                self.rotation *= 0.9
                if abs(self.rotation) < 0.01:
                    self.rotation = 0
        elif self.dash_cooldown > 0:
            self.dash_cooldown -= 1
            
        # Smooth scaling (1.5x sesuai soal)
        self.scale += (self.target_scale - self.scale) * 0.1
        
        # Animation frame
        self.anim_frame += 1
    
    def shoot_projectile(self):
        global projectiles_fired
        # Buat projectile baru
        proj_x = self.x + (self.width if self.facing_right else 0)
        proj_y = self.y + self.height // 2
        direction = 1 if self.facing_right else -1
        self.projectiles.append(Projectile(proj_x, proj_y, direction))
        projectiles_fired += 1
        
    def update_projectiles(self):
        # Update semua projectile
        for proj in self.projectiles[:]:
            proj.update()
            if not proj.active:
                self.projectiles.remove(proj)
        
    def collect_item(self):
        # Scaling 1.5x saat ambil item sesuai soal
        self.target_scale = min(self.target_scale * 1.5, 3.0)
        
    def draw(self, surface, mirror=False):
        # Hitung posisi tengah untuk rotasi
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        if mirror:
            center_y = HEIGHT - center_y
        
        # Buat surface untuk karakter
        char_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
        char_rect = char_surface.get_rect(center=(40, 40))
        
        # Animasi lengan
        arm_swing = math.sin(self.anim_frame * 0.2) * 10
        
        # Gambar karakter relatif ke pusat
        # Body
        body_rect = pygame.Rect(25, 25, 30, 35)
        pygame.draw.rect(char_surface, PLAYER_BLUE, body_rect)
        
        # Head
        pygame.draw.circle(char_surface, SKIN_COLOR, (40, 20), 12)
        
        # Eyes
        eye_offset = 4 if self.facing_right else -4
        pygame.draw.circle(char_surface, BLACK, (40 - eye_offset, 18), 2)
        pygame.draw.circle(char_surface, BLACK, (40 + eye_offset, 18), 2)
        
        # Legs
        pygame.draw.rect(char_surface, (46, 92, 138), (28, 60, 8, 15))
        pygame.draw.rect(char_surface, (46, 92, 138), (44, 60, 8, 15))
        
        # Arms
        pygame.draw.rect(char_surface, (46, 92, 138), (22, 35 + arm_swing, 6, 20))
        pygame.draw.rect(char_surface, (46, 92, 138), (52, 35 - arm_swing, 6, 20))
        
        # Pedang - selalu terlihat
        sword_base_x = 55 if self.facing_right else 10
        sword_base_y = 30
        
        if self.is_attacking:
            # Animasi ayunan pedang dengan efek slash
            swing_angle = math.radians(self.sword_swing_angle)
            
            # Hitung posisi pedang saat mengayun
            sword_length = 35
            pivot_x = 55 if self.facing_right else 25
            pivot_y = 28
            
            # Rotasi pedang
            angle = -60 + self.sword_swing_angle if self.facing_right else -60 - self.sword_swing_angle
            angle_rad = math.radians(angle)
            
            end_x = pivot_x + sword_length * math.cos(angle_rad)
            end_y = pivot_y + sword_length * math.sin(angle_rad)
            
            # Gambar efek slash (beberapa garis untuk efek motion blur)
            for i in range(5):
                alpha_val = 255 - (i * 50)
                trail_angle = angle_rad - (i * 0.15 if self.facing_right else -i * 0.15)
                trail_x = pivot_x + sword_length * math.cos(trail_angle)
                trail_y = pivot_y + sword_length * math.sin(trail_angle)
                
                # Buat surface untuk trail dengan alpha
                trail_surf = pygame.Surface((80, 80), pygame.SRCALPHA)
                pygame.draw.line(trail_surf, (200, 200, 255, alpha_val), (pivot_x, pivot_y), (trail_x, trail_y), 4)
                char_surface.blit(trail_surf, (0, 0))
            
            # Gambar blade (pedang utama)
            pygame.draw.line(char_surface, (220, 220, 220), (pivot_x, pivot_y), (end_x, end_y), 5)
            pygame.draw.line(char_surface, (255, 255, 255), (pivot_x, pivot_y), (end_x, end_y), 3)
            
            # Handle pedang
            handle_x = pivot_x - 8 * math.cos(angle_rad)
            handle_y = pivot_y - 8 * math.sin(angle_rad)
            pygame.draw.line(char_surface, (139, 69, 19), (pivot_x, pivot_y), (handle_x, handle_y), 6)
            
            # Guard (pelindung tangan)
            guard_angle = angle_rad + math.pi / 2
            guard_len = 6
            guard_x1 = pivot_x + guard_len * math.cos(guard_angle)
            guard_y1 = pivot_y + guard_len * math.sin(guard_angle)
            guard_x2 = pivot_x - guard_len * math.cos(guard_angle)
            guard_y2 = pivot_y - guard_len * math.sin(guard_angle)
            pygame.draw.line(char_surface, (218, 165, 32), (guard_x1, guard_y1), (guard_x2, guard_y2), 4)
            
        else:
            # Pedang idle di pinggang
            if self.facing_right:
                # Blade
                pygame.draw.line(char_surface, (192, 192, 192), (sword_base_x, sword_base_y), (sword_base_x + 30, sword_base_y), 4)
                pygame.draw.line(char_surface, (255, 255, 255), (sword_base_x, sword_base_y), (sword_base_x + 30, sword_base_y), 2)
                # Handle
                pygame.draw.rect(char_surface, (139, 69, 19), (sword_base_x - 8, sword_base_y - 3, 10, 6))
                # Guard
                pygame.draw.rect(char_surface, (218, 165, 32), (sword_base_x - 2, sword_base_y - 5, 4, 10))
            else:
                # Blade (untuk arah kiri)
                pygame.draw.line(char_surface, (192, 192, 192), (sword_base_x, sword_base_y), (sword_base_x - 30, sword_base_y), 4)
                pygame.draw.line(char_surface, (255, 255, 255), (sword_base_x, sword_base_y), (sword_base_x - 30, sword_base_y), 2)
                # Handle
                pygame.draw.rect(char_surface, (139, 69, 19), (sword_base_x - 2, sword_base_y - 3, 10, 6))
                # Guard
                pygame.draw.rect(char_surface, (218, 165, 32), (sword_base_x - 2, sword_base_y - 5, 4, 10))
        
        # Flip jika menghadap kiri
        if not self.facing_right:
            char_surface = pygame.transform.flip(char_surface, True, False)
            
        # Rotasi 30 derajat
        if self.rotation != 0:
            char_surface = pygame.transform.rotate(char_surface, math.degrees(-self.rotation))
            
        # Scaling 1.5x
        if self.scale != 1.0:
            new_size = (int(80 * self.scale), int(80 * self.scale))
            char_surface = pygame.transform.scale(char_surface, new_size)
            
        # Flip vertikal untuk mirror mode (refleksi horizontal)
        if mirror:
            char_surface = pygame.transform.flip(char_surface, False, True)
            char_surface.set_alpha(150)
            
        # Draw ke screen
        char_rect = char_surface.get_rect(center=(center_x, center_y))
        surface.blit(char_surface, char_rect)

class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 8
        self.size = 8
        self.active = True
        self.trail = []
        
    def update(self):
        # Simpan posisi untuk trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)
        
        # Gerak projectile
        self.x += self.speed * self.direction
        
        # Hapus jika keluar layar
        if self.x < 0 or self.x > WIDTH:
            self.active = False
    
    def draw(self, surface):
        # Gambar trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(150 * (i / len(self.trail)))
            size = self.size - (len(self.trail) - i) * 1
            pygame.draw.circle(surface, (255, 200, 100), (int(tx), int(ty)), max(1, size))
        
        # Gambar projectile utama (bola api)
        pygame.draw.circle(surface, (255, 150, 0), (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(surface, (255, 220, 100), (int(self.x), int(self.y)), self.size - 3)
        
        # Efek sparkle
        for i in range(3):
            angle = (self.x * 10 + i * 120) % 360
            spark_x = self.x + math.cos(math.radians(angle)) * (self.size + 2)
            spark_y = self.y + math.sin(math.radians(angle)) * (self.size + 2)
            pygame.draw.circle(surface, (255, 255, 200), (int(spark_x), int(spark_y)), 2)

class HitEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lifetime = 20
        self.particles = []
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            self.particles.append({
                'x': x,
                'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.randint(2, 5)
            })
    
    def update(self):
        self.lifetime -= 1
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.3  # Gravity
            p['vx'] *= 0.95
    
    def draw(self, surface):
        alpha = int(255 * (self.lifetime / 20))
        for p in self.particles:
            color = (255, 100, 100, alpha)
            pygame.draw.circle(surface, color[:3], (int(p['x']), int(p['y'])), p['size'])
    
    def is_alive(self):
        return self.lifetime > 0

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 40
        self.velocity_x = 2
        self.velocity_y = 0
        self.facing_right = True
        self.anim_frame = 0
        self.alive = True
        self.hp = 3
        self.hit_cooldown = 0
        
    def update(self, player):
        if not self.alive:
            return
            
        # AI sederhana - bergerak ke arah player
        if player.x > self.x + 100:
            self.velocity_x = 2
            self.facing_right = True
        elif player.x < self.x - 100:
            self.velocity_x = -2
            self.facing_right = False
        else:
            self.velocity_x *= 0.8
            
        # Gravity
        self.velocity_y += 0.5
        
        # Update posisi
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Ground collision
        ground_y = HEIGHT - 150
        if self.y >= ground_y - self.height:
            self.y = ground_y - self.height
            self.velocity_y = 0
            
        # Screen boundaries
        if self.x < 0:
            self.x = 0
            self.velocity_x *= -1
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
            self.velocity_x *= -1
            
        # Update cooldown
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
            
        self.anim_frame += 1
        
    def take_damage(self):
        if self.hit_cooldown == 0:
            self.hp -= 1
            self.hit_cooldown = 30
            if self.hp <= 0:
                self.alive = False
                return True
        return False
        
    def draw(self, surface):
        if not self.alive:
            return
            
        # Buat surface untuk enemy
        enemy_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
        
        # Flash merah saat kena hit
        if self.hit_cooldown > 0 and self.hit_cooldown % 4 < 2:
            body_color = (255, 100, 100)
        else:
            body_color = (200, 50, 50)
        
        # Animasi lengan
        arm_swing = math.sin(self.anim_frame * 0.15) * 8
        
        # Body (merah untuk musuh)
        pygame.draw.rect(enemy_surface, body_color, (25, 25, 30, 35))
        
        # Head (lebih gelap)
        pygame.draw.circle(enemy_surface, (150, 100, 100), (40, 20), 12)
        
        # Eyes (mata merah)
        eye_offset = 4 if self.facing_right else -4
        pygame.draw.circle(enemy_surface, (255, 0, 0), (40 - eye_offset, 18), 3)
        pygame.draw.circle(enemy_surface, (255, 0, 0), (40 + eye_offset, 18), 3)
        
        # Legs
        pygame.draw.rect(enemy_surface, (120, 30, 30), (28, 60, 8, 15))
        pygame.draw.rect(enemy_surface, (120, 30, 30), (44, 60, 8, 15))
        
        # Arms
        pygame.draw.rect(enemy_surface, (120, 30, 30), (22, 35 + arm_swing, 6, 20))
        pygame.draw.rect(enemy_surface, (120, 30, 30), (52, 35 - arm_swing, 6, 20))
        
        # Flip jika menghadap kiri
        if not self.facing_right:
            enemy_surface = pygame.transform.flip(enemy_surface, True, False)
        
        # Draw ke screen
        enemy_rect = enemy_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(enemy_surface, enemy_rect)
        
        # HP bar
        bar_width = 40
        bar_height = 5
        bar_x = self.x + self.width // 2 - bar_width // 2
        bar_y = self.y - 15
        
        # Background bar
        pygame.draw.rect(surface, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # HP bar
        hp_width = int(bar_width * (self.hp / 3))
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, hp_width, bar_height))

class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.rotation = 0
        
    def update(self):
        self.rotation += 3
        
    def draw(self, surface):
        if not self.collected:
            # Buat surface untuk item
            item_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            
            # Gift box
            pygame.draw.rect(item_surface, GOLD, (5, 5, 20, 20))
            
            # Ribbon
            pygame.draw.rect(item_surface, RED, (13, 5, 4, 20))
            pygame.draw.rect(item_surface, RED, (5, 13, 20, 4))
            
            # Bow
            pygame.draw.circle(item_surface, RED, (7, 5), 4)
            pygame.draw.circle(item_surface, RED, (23, 5), 4)
            
            # Rotasi item
            rotated = pygame.transform.rotate(item_surface, self.rotation)
            rect = rotated.get_rect(center=(self.x, self.y))
            surface.blit(rotated, rect)

class Cloud:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(50, 150)
        self.speed = random.uniform(0.3, 0.8)
        self.size = random.randint(40, 70)
        
    def update(self):
        self.x += self.speed
        if self.x > WIDTH + self.size:
            self.x = -self.size
            
    def draw(self, surface):
        pygame.draw.circle(surface, CLOUD_WHITE, (int(self.x), int(self.y)), self.size // 2)
        pygame.draw.circle(surface, CLOUD_WHITE, (int(self.x + self.size * 0.4), int(self.y)), self.size // 3)
        pygame.draw.circle(surface, CLOUD_WHITE, (int(self.x - self.size * 0.4), int(self.y)), self.size // 3)
        pygame.draw.circle(surface, CLOUD_WHITE, (int(self.x), int(self.y - self.size * 0.3)), self.size // 2)

def draw_background(surface):
    # Sky gradient
    for i in range(HEIGHT):
        color_value = int(135 + (i / HEIGHT) * 40)
        pygame.draw.line(surface, (color_value, 206, 235), (0, i), (WIDTH, i))

def draw_ground(surface):
    ground_y = HEIGHT - 150
    # Grass
    pygame.draw.rect(surface, GRASS_GREEN, (0, ground_y, WIDTH, 30))
    # Dirt
    pygame.draw.rect(surface, DIRT_BROWN, (0, ground_y + 30, WIDTH, HEIGHT - ground_y - 30))
    # Grass blades
    for i in range(0, WIDTH, 10):
        pygame.draw.rect(surface, (85, 139, 47), (i, ground_y - 5, 3, 8))

def main():
    global projectiles_fired
    
    player = Player(50, 100)
    
    # Buat items
    items = []
    for i in range(5):
        items.append(Item(150 + i * 150, 200 + random.randint(0, 150)))
    
    # Buat clouds
    clouds = [Cloud() for _ in range(6)]
    
    # Buat enemies
    enemies = []
    for i in range(3):
        enemies.append(Enemy(300 + i * 200, 100))
    
    # Efek hit
    hit_effects = []
    
    # Score system
    score = 0
    kills = 0
    items_collected = 0
    projectiles_fired = 0
    
    mirror_mode = False
    running = True
    
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    while running:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Huruf M = Mirror Mode
                    mirror_mode = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    mirror_mode = False
        
        # Get keys
        keys = pygame.key.get_pressed()
        
        # Update
        player.move(keys)
        player.update()
        player.update_projectiles()
        
        for cloud in clouds:
            cloud.update()
        
        # Update enemies
        for enemy in enemies:
            enemy.update(player)
            
            # Check collision dengan player dash/attack
            if player.is_attacking and enemy.alive:
                dx = player.x - enemy.x
                dy = player.y - enemy.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < 50:  # Jangkauan pedang lebih jauh
                    if enemy.take_damage():
                        kills += 1
                        score += 10
                    # Tambah efek hit
                    hit_effects.append(HitEffect(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
            
            # Check collision dengan projectile
            for proj in player.projectiles[:]:
                if enemy.alive:
                    dx = proj.x - (enemy.x + enemy.width // 2)
                    dy = proj.y - (enemy.y + enemy.height // 2)
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance < 20:
                        proj.active = False
                        if enemy.take_damage():
                            kills += 1
                            score += 10
                        hit_effects.append(HitEffect(enemy.x + enemy.width // 2, enemy.y + enemy.height // 2))
            
            # Check collision dengan player (player kena damage)
            if enemy.alive and not player.is_dashing:
                dx = player.x - enemy.x
                dy = player.y - enemy.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < 35:
                    # Player terpental
                    knockback = 10
                    if player.x > enemy.x:
                        player.x += knockback
                    else:
                        player.x -= knockback
        
        # Update hit effects
        hit_effects = [effect for effect in hit_effects if effect.is_alive()]
        for effect in hit_effects:
            effect.update()
            
        for item in items:
            item.update()
            # Collision detection
            if not item.collected:
                dx = player.x - item.x
                dy = player.y - item.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance < 40:
                    item.collected = True
                    player.collect_item()
                    items_collected += 1
                    score += 5
        
        # Draw
        draw_background(screen)
        
        for cloud in clouds:
            cloud.draw(screen)
            
        draw_ground(screen)
        
        for item in items:
            item.draw(screen)
        
        # Draw projectiles
        for proj in player.projectiles:
            proj.draw(screen)
        
        # Draw enemies
        for enemy in enemies:
            enemy.draw(screen)
        
        # Draw hit effects
        for effect in hit_effects:
            effect.draw(screen)
        
        # Draw player normal
        player.draw(screen)
        
        # Mirror world effect (refleksi horizontal sesuai soal)
        if mirror_mode:
            player.draw(screen, mirror=True)
            for enemy in enemies:
                if enemy.alive:
                    # Draw mirrored enemy
                    temp_y = enemy.y
                    enemy.y = HEIGHT - enemy.y - enemy.height
                    enemy.draw(screen)
                    enemy.y = temp_y
            # Mirror line
            pygame.draw.line(screen, (100, 150, 255), (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 3)
        
        # UI
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        kills_text = small_font.render(f"Kills: {kills}/3", True, BLACK)
        screen.blit(kills_text, (10, 50))
        
        kills_text = small_font.render(f"Kills: {kills}/3", True, BLACK)
        screen.blit(kills_text, (10, 50))
        
        scale_text = small_font.render(f"Scale: {player.scale:.1f}x", True, BLACK)
        screen.blit(scale_text, (10, 75))
        
        if player.dash_cooldown > 0:
            dash_text = small_font.render(f"Dash: {player.dash_cooldown // 60 + 1}s", True, BLACK)
        else:
            dash_text = small_font.render("Dash: Ready!", True, (0, 255, 0))
        screen.blit(dash_text, (10, 160))
        
        # Transformasi info
        transform_text = small_font.render(f"Translasi: dx=20, dy={int(player.velocity_y)} | Rotasi: {int(math.degrees(player.rotation))}°", True, BLACK)
        screen.blit(transform_text, (10, 185))
        
        # Controls
        control_text = small_font.render("← → ↑ ↓ : Gerak | D=Pedang | S=Tembak | W=Besar | M=Mirror", True, BLACK)
        screen.blit(control_text, (10, HEIGHT - 30))
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()