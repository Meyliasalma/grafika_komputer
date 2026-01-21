import pygame
import math
import random

pygame.init()

WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BlockCraft 3D - Mini Minecraft")
clock = pygame.time.Clock()

class Block:
    def __init__(self, x, y, z, block_type):
        self.x = x
        self.y = y
        self.z = z
        self.block_type = block_type
        self.size = 1
        
    def get_vertices(self):
        s = self.size / 2
        return [
            [self.x - s, self.y - s, self.z - s],
            [self.x + s, self.y - s, self.z - s],
            [self.x + s, self.y + s, self.z - s],
            [self.x - s, self.y + s, self.z - s],
            [self.x - s, self.y - s, self.z + s],
            [self.x + s, self.y - s, self.z + s],
            [self.x + s, self.y + s, self.z + s],
            [self.x - s, self.y + s, self.z + s]
        ]
    
    def get_faces(self):
        return [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [2, 3, 7, 6],
            [0, 3, 7, 4],
            [1, 2, 6, 5]
        ]
    
    def get_colors(self):
        colors = {
            'grass': [(80, 180, 80), (60, 160, 60), (50, 140, 50), (100, 200, 100), (70, 170, 70), (90, 190, 90)],
            'dirt': [(139, 90, 43), (120, 80, 40), (100, 70, 35), (150, 100, 50), (130, 85, 42), (110, 75, 38)],
            'stone': [(128, 128, 128), (110, 110, 110), (100, 100, 100), (140, 140, 140), (120, 120, 120), (105, 105, 105)],
            'wood': [(139, 90, 0), (120, 80, 0), (100, 70, 0), (150, 100, 10), (130, 85, 5), (110, 75, 0)],
            'sand': [(238, 214, 175), (220, 200, 160), (210, 190, 150), (245, 220, 180), (230, 210, 170), (225, 205, 165)],
            'water': [(64, 164, 223), (50, 150, 210), (40, 140, 200), (70, 170, 230), (60, 160, 220), (55, 155, 215)],
            'leaf': [(34, 139, 34), (30, 120, 30), (25, 110, 25), (40, 150, 40), (35, 130, 35), (32, 125, 32)],
            'plank': [(205, 133, 63), (190, 120, 55), (180, 110, 50), (215, 140, 70), (200, 125, 60), (195, 118, 58)],
            'brick': [(178, 34, 34), (160, 30, 30), (150, 25, 25), (190, 40, 40), (170, 32, 32), (165, 28, 28)],
            'glass': [(173, 216, 230), (150, 200, 220), (140, 190, 210), (180, 220, 235), (160, 210, 225), (155, 205, 218)]
        }
        return colors.get(self.block_type, [(255, 0, 255)] * 6)

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 8
        self.z = -20
        self.angle_x = 0.3
        self.angle_y = 0
        self.fov = 500
        self.reflect_x = False
        self.reflect_y = False
        
    def rotate_point(self, point):
        px, py, pz = point[0] - self.x, point[1] - self.y, point[2] - self.z
        
        if self.reflect_x:
            px = -px
        
        if self.reflect_y:
            py = -py
        
        y = py * math.cos(self.angle_x) - pz * math.sin(self.angle_x)
        z = py * math.sin(self.angle_x) + pz * math.cos(self.angle_x)
        py, pz = y, z
        
        x = px * math.cos(self.angle_y) + pz * math.sin(self.angle_y)
        z = -px * math.sin(self.angle_y) + pz * math.cos(self.angle_y)
        px, pz = x, z
        
        return [px, py, pz]
    
    def project(self, point):
        rotated = self.rotate_point(point)
        if rotated[2] <= 0.1:
            return None
        
        factor = self.fov / rotated[2]
        x = rotated[0] * factor + WIDTH / 2
        y = -rotated[1] * factor + HEIGHT / 2
        return [x, y, rotated[2]]

def get_face_normal(vertices, face):
    v1 = [vertices[face[1]][i] - vertices[face[0]][i] for i in range(3)]
    v2 = [vertices[face[2]][i] - vertices[face[0]][i] for i in range(3)]
    
    normal = [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]
    
    length = math.sqrt(sum(n * n for n in normal))
    if length > 0:
        normal = [n / length for n in normal]
    
    return normal

def calculate_lighting(face_normal, light_dir):
    dot = (face_normal[0] * light_dir[0] + 
           face_normal[1] * light_dir[1] + 
           face_normal[2] * light_dir[2])
    brightness = max(0.3, min(1.0, dot * 0.7 + 0.3))
    return brightness

def build_house(world, x_start, z_start, y_base):
    for x in range(x_start, x_start + 5):
        for z in range(z_start, z_start + 5):
            world[(x, y_base, z)] = Block(x, y_base, z, 'plank')
    
    for y in range(y_base + 1, y_base + 4):
        for x in range(x_start, x_start + 5):
            for z in range(z_start, z_start + 5):
                if x == x_start or x == x_start + 4 or z == z_start or z == z_start + 4:
                    if not (x == x_start + 2 and z == z_start and y == y_base + 1):
                        world[(x, y, z)] = Block(x, y, z, 'brick')
    
    world[(x_start, y_base + 2, z_start + 2)] = Block(x_start, y_base + 2, z_start + 2, 'glass')
    world[(x_start + 4, y_base + 2, z_start + 2)] = Block(x_start + 4, y_base + 2, z_start + 2, 'glass')

def build_tower(world, x_start, z_start, y_base):
    for x in range(x_start - 1, x_start + 2):
        for z in range(z_start - 1, z_start + 2):
            world[(x, y_base, z)] = Block(x, y_base, z, 'stone')
    
    for y in range(y_base + 1, y_base + 8):
        for x in range(x_start - 1, x_start + 2):
            for z in range(z_start - 1, z_start + 2):
                if x == x_start - 1 or x == x_start + 1 or z == z_start - 1 or z == z_start + 1:
                    world[(x, y, z)] = Block(x, y, z, 'brick')

def build_pyramid(world, x_start, z_start, y_base):
    size = 4
    for level in range(size):
        y = y_base + level
        for x in range(x_start - (size - level - 1), x_start + (size - level)):
            for z in range(z_start - (size - level - 1), z_start + (size - level)):
                world[(x, y, z)] = Block(x, y, z, 'sand')

def generate_world():
    world = {}
    
    for x in range(-20, 21):
        for z in range(-20, 21):
            height = int(3 + math.sin(x * 0.3) * math.cos(z * 0.3))
            
            for y in range(height):
                if y == height - 1:
                    world[(x, y, z)] = Block(x, y, z, 'grass')
                elif y >= height - 2:
                    world[(x, y, z)] = Block(x, y, z, 'dirt')
                else:
                    world[(x, y, z)] = Block(x, y, z, 'stone')
    
    build_house(world, -15, -15, 4)
    build_house(world, 10, -15, 4)
    build_tower(world, -15, 10, 3)
    build_tower(world, 15, 10, 3)
    build_pyramid(world, -5, -5, 3)
    build_pyramid(world, 12, 12, 3)
    build_house(world, -15, 0, 4)
    build_house(world, 10, 5, 4)
    
    for _ in range(8):
        tx = random.randint(-18, 18)
        tz = random.randint(-18, 18)
        
        skip = False
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                if (tx + dx, 4, tz + dz) in world and world[(tx + dx, 4, tz + dz)].block_type != 'grass':
                    skip = True
                    break
            if skip:
                break
        
        if skip:
            continue
            
        for ty in range(4, 7):
            world[(tx, ty, tz)] = Block(tx, ty, tz, 'wood')
        
        for lx in range(tx - 1, tx + 2):
            for lz in range(tz - 1, tz + 2):
                for ly in range(6, 8):
                    if (lx, ly, lz) not in world:
                        world[(lx, ly, lz)] = Block(lx, ly, lz, 'leaf')
    
    return world

camera = Camera()
world = generate_world()
selected_block_type = 'grass'
block_types = ['grass', 'dirt', 'stone', 'wood', 'sand', 'plank', 'leaf', 'brick', 'glass']
selected_index = 0
light_dir = [0.5, -0.7, 0.5]
length = math.sqrt(sum(d * d for d in light_dir))
light_dir = [d / length for d in light_dir]

show_help = True
destroy_mode = False
mirror_mode = False

running = True
font_small = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 36)

mouse_down_left = False
mouse_down_right = False
destroy_timer = 0

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_down_left = True
            elif event.button == 3:
                mouse_down_right = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down_left = False
            elif event.button == 3:
                mouse_down_right = False
        elif event.type == pygame.MOUSEMOTION:
            mx, my = pygame.mouse.get_pos()
            center_x, center_y = WIDTH // 2, HEIGHT // 2
            
            dx = mx - center_x
            dy = my - center_y
            
            camera.angle_y += dx * 0.003
            camera.angle_x += dy * 0.003
            camera.angle_x = max(-math.pi / 2 + 0.1, min(math.pi / 2 - 0.1, camera.angle_x))
            
            pygame.mouse.set_pos(center_x, center_y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_e:
                selected_index = (selected_index + 1) % len(block_types)
                selected_block_type = block_types[selected_index]
            elif event.key == pygame.K_q:
                selected_index = (selected_index - 1) % len(block_types)
                selected_block_type = block_types[selected_index]
            elif event.key == pygame.K_h:
                forward_x = math.sin(camera.angle_y)
                forward_y = math.sin(camera.angle_x)
                forward_z = math.cos(camera.angle_y) * math.cos(camera.angle_x)
                
                for dist in range(1, 12):
                    check_x = camera.x + forward_x * dist
                    check_y = camera.y + forward_y * dist
                    check_z = camera.z + forward_z * dist
                    
                    bx, by, bz = round(check_x), round(check_y), round(check_z)
                    
                    if (bx, by, bz) in world:
                        del world[(bx, by, bz)]
                        if mirror_mode and (-bx, by, bz) in world:
                            del world[(-bx, by, bz)]
                        break
            elif event.key == pygame.K_t:
                forward_x = math.sin(camera.angle_y)
                forward_y = math.sin(camera.angle_x)
                forward_z = math.cos(camera.angle_y) * math.cos(camera.angle_x)
                
                for dist in range(1, 12):
                    check_x = camera.x + forward_x * dist
                    check_y = camera.y + forward_y * dist
                    check_z = camera.z + forward_z * dist
                    
                    bx, by, bz = round(check_x), round(check_y), round(check_z)
                    
                    if (bx, by, bz) in world:
                        prev_dist = dist - 0.5
                        place_x = camera.x + forward_x * prev_dist
                        place_y = camera.y + forward_y * prev_dist
                        place_z = camera.z + forward_z * prev_dist
                        
                        pbx, pby, pbz = round(place_x), round(place_y), round(place_z)
                        
                        if (pbx, pby, pbz) not in world:
                            world[(pbx, pby, pbz)] = Block(pbx, pby, pbz, selected_block_type)
                            if mirror_mode and (-pbx, pby, pbz) not in world:
                                world[(-pbx, pby, pbz)] = Block(-pbx, pby, pbz, selected_block_type)
                        break
            elif event.key == pygame.K_x:
                destroy_mode = not destroy_mode
            elif event.key == pygame.K_r:
                world = generate_world()
            elif event.key == pygame.K_f:
                camera.reflect_x = not camera.reflect_x
            elif event.key == pygame.K_v:
                camera.reflect_y = not camera.reflect_y
            elif event.key == pygame.K_m:
                mirror_mode = not mirror_mode
            elif event.key == pygame.K_p:
                show_help = not show_help
    
    if mouse_down_left:
        destroy_timer += 1
        if destroy_timer > 8:
            destroy_timer = 0
            
            forward_x = math.sin(camera.angle_y)
            forward_y = math.sin(camera.angle_x)
            forward_z = math.cos(camera.angle_y) * math.cos(camera.angle_x)
            
            for dist in range(1, 12):
                check_x = camera.x + forward_x * dist
                check_y = camera.y + forward_y * dist
                check_z = camera.z + forward_z * dist
                
                bx, by, bz = round(check_x), round(check_y), round(check_z)
                
                if (bx, by, bz) in world:
                    del world[(bx, by, bz)]
                    if mirror_mode and (-bx, by, bz) in world:
                        del world[(-bx, by, bz)]
                    break
    else:
        destroy_timer = 0
    
    if mouse_down_right:
        mouse_down_right = False
        
        forward_x = math.sin(camera.angle_y)
        forward_y = math.sin(camera.angle_x)
        forward_z = math.cos(camera.angle_y) * math.cos(camera.angle_x)
        
        for dist in range(1, 12):
            check_x = camera.x + forward_x * dist
            check_y = camera.y + forward_y * dist
            check_z = camera.z + forward_z * dist
            
            bx, by, bz = round(check_x), round(check_y), round(check_z)
            
            if (bx, by, bz) in world:
                prev_dist = dist - 0.5
                place_x = camera.x + forward_x * prev_dist
                place_y = camera.y + forward_y * prev_dist
                place_z = camera.z + forward_z * prev_dist
                
                pbx, pby, pbz = round(place_x), round(place_y), round(place_z)
                
                if (pbx, pby, pbz) not in world:
                    world[(pbx, pby, pbz)] = Block(pbx, pby, pbz, selected_block_type)
                    if mirror_mode and (-pbx, pby, pbz) not in world:
                        world[(-pbx, pby, pbz)] = Block(-pbx, pby, pbz, selected_block_type)
                break
    
    if destroy_mode and not mouse_down_left:
        forward_x = math.sin(camera.angle_y)
        forward_y = math.sin(camera.angle_x)
        forward_z = math.cos(camera.angle_y) * math.cos(camera.angle_x)
        
        for dist in range(1, 12):
            check_x = camera.x + forward_x * dist
            check_y = camera.y + forward_y * dist
            check_z = camera.z + forward_z * dist
            
            bx, by, bz = round(check_x), round(check_y), round(check_z)
            
            if (bx, by, bz) in world:
                del world[(bx, by, bz)]
                if mirror_mode and (-bx, by, bz) in world:
                    del world[(-bx, by, bz)]
                break
    
    keys = pygame.key.get_pressed()
    move_speed = 0.4
    
    if keys[pygame.K_SPACE]:
        move_speed = 0.7
    
    forward_x = math.sin(camera.angle_y)
    forward_z = math.cos(camera.angle_y)
    right_x = math.cos(camera.angle_y)
    right_z = -math.sin(camera.angle_y)
    
    if keys[pygame.K_w]:
        camera.x += forward_x * move_speed
        camera.z += forward_z * move_speed
    if keys[pygame.K_s]:
        camera.x -= forward_x * move_speed
        camera.z -= forward_z * move_speed
    if keys[pygame.K_a]:
        camera.x -= right_x * move_speed
        camera.z -= right_z * move_speed
    if keys[pygame.K_d]:
        camera.x += right_x * move_speed
        camera.z += right_z * move_speed
    if keys[pygame.K_LSHIFT]:
        camera.y -= move_speed
    if keys[pygame.K_LCTRL]:
        camera.y += move_speed
    
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (34, 139, 34), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    
    faces_to_draw = []
    render_distance = 25
    
    for block in world.values():
        dx = block.x - camera.x
        dy = block.y - camera.y
        dz = block.z - camera.z
        dist = dx*dx + dy*dy + dz*dz
        
        if dist > render_distance * render_distance:
            continue
            
        vertices = block.get_vertices()
        faces = block.get_faces()
        colors = block.get_colors()
        
        for i, face in enumerate(faces):
            projected = []
            for vertex_idx in face:
                proj = camera.project(vertices[vertex_idx])
                if proj is None:
                    break
                projected.append(proj)
            
            if len(projected) == 4:
                center_z = sum(p[2] for p in projected) / 4
                normal = get_face_normal(vertices, face)
                brightness = calculate_lighting(normal, light_dir)
                color = tuple(int(c * brightness) for c in colors[i])
                faces_to_draw.append((center_z, projected, color))
    
    faces_to_draw.sort(reverse=True, key=lambda x: x[0])
    
    for z, projected, color in faces_to_draw:
        points = [(p[0], p[1]) for p in projected]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, (0, 0, 0), points, 1)
    
    crosshair_size = 20
    cx, cy = WIDTH // 2, HEIGHT // 2
    crosshair_color = (255, 0, 0) if destroy_mode else (0, 255, 0) if mouse_down_left else (255, 255, 255)
    pygame.draw.line(screen, crosshair_color, (cx - crosshair_size, cy), (cx + crosshair_size, cy), 3)
    pygame.draw.line(screen, crosshair_color, (cx, cy - crosshair_size), (cx, cy + crosshair_size), 3)
    pygame.draw.circle(screen, crosshair_color, (cx, cy), 4, 2)
    
    sample_block = Block(0, 0, 0, selected_block_type)
    sample_colors = sample_block.get_colors()
    inventory_x = 20
    inventory_y = HEIGHT - 80
    pygame.draw.rect(screen, sample_colors[0], (inventory_x, inventory_y, 50, 50))
    pygame.draw.rect(screen, (255, 255, 255), (inventory_x, inventory_y, 50, 50), 2)
    
    block_name = font_small.render(selected_block_type.upper(), True, (255, 255, 255))
    screen.blit(block_name, (inventory_x + 60, inventory_y + 15))
    
    status_y = 60
    if mouse_down_left:
        bg = pygame.Surface((400, 30))
        bg.set_alpha(200)
        bg.fill((0, 150, 0))
        screen.blit(bg, (15, status_y))
        txt = font_large.render("MENGHANCURKAN!", True, (255, 255, 255))
        screen.blit(txt, (20, status_y + 2))
        status_y += 35
    
    if camera.reflect_x:
        bg = pygame.Surface((300, 28))
        bg.set_alpha(180)
        bg.fill((128, 128, 0))
        screen.blit(bg, (15, status_y))
        txt = font_small.render("FLIP HORIZONTAL AKTIF", True, (255, 255, 0))
        screen.blit(txt, (20, status_y + 3))
        status_y += 32
    
    if camera.reflect_y:
        bg = pygame.Surface((300, 28))
        bg.set_alpha(180)
        bg.fill((128, 128, 0))
        screen.blit(bg, (15, status_y))
        txt = font_small.render("FLIP VERTICAL AKTIF", True, (255, 255, 0))
        screen.blit(txt, (20, status_y + 3))
        status_y += 32
    
    if mirror_mode:
        bg = pygame.Surface((300, 28))
        bg.set_alpha(180)
        bg.fill((0, 100, 100))
        screen.blit(bg, (15, status_y))
        txt = font_small.render("MIRROR BUILD AKTIF", True, (0, 255, 255))
        screen.blit(txt, (20, status_y + 3))
        status_y += 32
    
    if destroy_mode:
        bg = pygame.Surface((300, 28))
        bg.set_alpha(180)
        bg.fill((100, 0, 0))
        screen.blit(bg, (15, status_y))
        txt = font_small.render("AUTO-DESTROY AKTIF", True, (255, 0, 0))
        screen.blit(txt, (20, status_y + 3))
    
    if show_help:
        help_bg = pygame.Surface((280, 300))
        help_bg.set_alpha(200)
        help_bg.fill((0, 0, 0))
        screen.blit(help_bg, (WIDTH - 300, 20))
        
        help_texts = [
            ("BLOCKCRAFT 3D", (255, 255, 0)),
            ("", (255, 255, 255)),
            ("GERAKAN:", (0, 255, 255)),
            ("WASD: Jalan", (255, 255, 255)),
            ("SPACE: Lari", (255, 255, 255)),
            ("Shift: Turun", (255, 255, 255)),
            ("Ctrl: Naik", (255, 255, 255)),
            ("", (255, 255, 255)),
            ("REFLEKSI:", (0, 255, 255)),
            ("F: Flip Horizontal", (255, 255, 255)),
            ("V: Flip Vertical", (255, 255, 255)),
            ("M: Mirror Build", (255, 255, 255)),
            ("", (255, 255, 255)),
            ("LAINNYA:", (0, 255, 255)),
            ("Q/E: Ganti Balok", (255, 255, 255)),
            ("R: Reset Dunia", (255, 255, 255)),
            ("P: Hide Help", (255, 255, 255)),
            ("", (255, 255, 255)),
            (f"Balok: {len(world)}", (200, 200, 200))
        ]
        
        y_off = 30
        for text, color in help_texts:
            if text:
                surf = font_small.render(text, True, color)
                screen.blit(surf, (WIDTH - 290, y_off))
            y_off += 22
    
    title = font_large.render("BLOCKCRAFT 3D", True, (255, 255, 255))
    screen.blit(title, (20, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
