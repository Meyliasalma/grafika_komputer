import tkinter as tk
import math

class Room3D:
    def __init__(self, root):
        self.root = root   
        self.root.title("First Person View - Kelas & Lab (Lighting + Shadow)")
        self.root.configure(bg='#1a1a2e')
        
        self.w, self.h = 1400, 800
        self.canvas = tk.Canvas(root, width=self.w, height=self.h, bg='#e8e8e8', highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.cam_x, self.cam_y, self.cam_z = 0, -100, 250
        self.cam_yaw, self.cam_pitch = 0, 0
        self.time, self.show_grid, self.light_on, self.fov = 0, True, True, 90
        self.mouse_sensitivity, self.mouse_down = 0.003, False
        self.last_mouse_x, self.last_mouse_y = 0, 0
        
        # REFLEKSI LANTAI (Floor Mirror Effect)
        self.floor_reflection = True
        
        # LIGHTING SYSTEM
        self.light_intensity = 1.0  # 0.0 - 1.0
        self.light_pulse = True  # Animasi pulse cahaya
        self.light_sources = [
            {'pos': [0, -300, 0], 'color': [255, 220, 180], 'intensity': 1.0, 'range': 800},  # Lampu kelas
            {'pos': [650, -300, 0], 'color': [180, 200, 255], 'intensity': 0.9, 'range': 700}  # Lampu lab
        ]
        
        # SHADOW SYSTEM
        self.show_shadows = True
        self.shadow_light_pos = [0, -350, 0]  # Posisi cahaya untuk bayangan
        
        self.create_controls()
        self.build_rooms()
        self.animate()
    
    def create_controls(self):
        bs = {'font': ('Arial', 9, 'bold'), 'padx': 8, 'pady': 4, 'relief': tk.FLAT, 'cursor': 'hand2'}
        
        f1 = tk.Frame(self.root, bg='#1a1a2e')
        f1.pack(pady=3)
        tk.Label(f1, text="FIRST PERSON - 2 RUANGAN:", bg='#1a1a2e', fg='#06ffa5', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(f1, text="🔄 RESET", command=self.reset, bg='#e63946', fg='white', **bs).pack(side=tk.LEFT, padx=2)
        tk.Button(f1, text="🎬 Grid", command=self.toggle_grid, bg='#9d4edd', fg='white', **bs).pack(side=tk.LEFT, padx=2)
        tk.Button(f1, text="💡 Lampu", command=self.toggle_light, bg='#ffd60a', fg='#000', **bs).pack(side=tk.LEFT, padx=2)
        tk.Button(f1, text="🌟 Pulse", command=self.toggle_pulse, bg='#fb8500', fg='white', **bs).pack(side=tk.LEFT, padx=2)
        tk.Button(f1, text="👤 Shadow", command=self.toggle_shadow, bg='#023047', fg='white', **bs).pack(side=tk.LEFT, padx=2)
        
        f2 = tk.Frame(self.root, bg='#1a1a2e')
        f2.pack(pady=3)
        tk.Label(f2, text="GERAKAN:", bg='#1a1a2e', fg='#2a9d8f', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(f2, text="⬆️ W", command=lambda: self.move_forward(30), bg='#2a9d8f', fg='white', **bs).pack(side=tk.LEFT)
        tk.Button(f2, text="⬇️ S", command=lambda: self.move_forward(-30), bg='#2a9d8f', fg='white', **bs).pack(side=tk.LEFT)
        tk.Button(f2, text="⬅️ A", command=lambda: self.move_strafe(-30), bg='#2a9d8f', fg='white', **bs).pack(side=tk.LEFT)
        tk.Button(f2, text="➡️ D", command=lambda: self.move_strafe(30), bg='#2a9d8f', fg='white', **bs).pack(side=tk.LEFT)
        
        # REFLEKSI LANTAI
        f3 = tk.Frame(self.root, bg='#1a1a2e')
        f3.pack(pady=3)
        tk.Label(f3, text="EFEK VISUAL:", bg='#1a1a2e', fg='#ff006e', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(f3, text="🪞 Refleksi (M)", command=self.toggle_floor_reflection, bg='#ff006e', fg='white', **bs).pack(side=tk.LEFT, padx=2)
        
        # LIGHT INTENSITY SLIDER
        f4 = tk.Frame(self.root, bg='#1a1a2e')
        f4.pack(pady=3)
        tk.Label(f4, text="☀️ INTENSITAS CAHAYA:", bg='#1a1a2e', fg='#ffd60a', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        self.intensity_slider = tk.Scale(f4, from_=0, to=100, orient=tk.HORIZONTAL, 
                                        command=self.update_intensity, bg='#1a1a2e', fg='#ffd60a',
                                        highlightthickness=0, length=200, troughcolor='#333')
        self.intensity_slider.set(100)
        self.intensity_slider.pack(side=tk.LEFT, padx=5)
        
        self.root.bind('w', lambda e: self.move_forward(30))
        self.root.bind('s', lambda e: self.move_forward(-30))
        self.root.bind('a', lambda e: self.move_strafe(-30))
        self.root.bind('d', lambda e: self.move_strafe(30))
        self.root.bind('<Left>', lambda e: self.look_horizontal(-0.15))
        self.root.bind('<Right>', lambda e: self.look_horizontal(0.15))
        self.root.bind('<Up>', lambda e: self.look_vertical(-0.1))
        self.root.bind('<Down>', lambda e: self.look_vertical(0.1))
        self.root.bind('r', lambda e: self.reset())
        self.root.bind('g', lambda e: self.toggle_grid())
        self.root.bind('l', lambda e: self.toggle_light())
        self.root.bind('m', lambda e: self.toggle_floor_reflection())
        self.root.bind('p', lambda e: self.toggle_pulse())
        self.root.bind('h', lambda e: self.toggle_shadow())
        
        self.canvas.bind('<Button-1>', self.mouse_press)
        self.canvas.bind('<B1-Motion>', self.mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_release)
    
    def update_intensity(self, val):
        self.light_intensity = float(val) / 100.0
    
    def toggle_pulse(self):
        self.light_pulse = not self.light_pulse
    
    def toggle_shadow(self):
        self.show_shadows = not self.show_shadows
    
    def mouse_press(self, e):
        self.mouse_down = True
        self.last_mouse_x, self.last_mouse_y = e.x, e.y
    
    def mouse_drag(self, e):
        if self.mouse_down:
            self.cam_yaw += (e.x - self.last_mouse_x) * self.mouse_sensitivity
            self.cam_pitch += (e.y - self.last_mouse_y) * self.mouse_sensitivity
            self.cam_pitch = max(-1.5, min(1.5, self.cam_pitch))
            self.last_mouse_x, self.last_mouse_y = e.x, e.y
    
    def mouse_release(self, e):
        self.mouse_down = False
    
    def check_collision(self, new_x, new_z):
        """Cek apakah posisi baru menabrak tembok"""
        margin = 30  # Jarak minimal dari tembok
        
        # Batas Ruang Kelas
        if new_x < -400 + margin:  # Tembok kiri kelas
            return False
        if new_z < -400 + margin:  # Tembok belakang kelas
            return False
        if new_z > 400 - margin:  # Tembok depan kelas
            return False
        
        # Batas Ruang Lab
        if new_x > 900 - margin:  # Tembok kanan lab
            return False
        
        # Tembok pembatas antara kelas dan lab (dengan pintu)
        if 395 < new_x < 405:  # Di area dinding pembatas
            # Cek apakah di area pintu (Z antara -100 dan 100, Y antara -250 dan 0)
            if not (-100 < new_z < 100):  # Di luar area pintu
                return False
        
        return True
    
    def move_forward(self, d):
        new_x = self.cam_x + d * math.sin(self.cam_yaw)
        new_z = self.cam_z - d * math.cos(self.cam_yaw)
        
        if self.check_collision(new_x, new_z):
            self.cam_x = new_x
            self.cam_z = new_z
    
    def move_strafe(self, d):
        new_x = self.cam_x + d * math.cos(self.cam_yaw)
        new_z = self.cam_z + d * math.sin(self.cam_yaw)
        
        if self.check_collision(new_x, new_z):
            self.cam_x = new_x
            self.cam_z = new_z
    
    def look_horizontal(self, a):
        self.cam_yaw += a
    
    def look_vertical(self, a):
        self.cam_pitch += a
        self.cam_pitch = max(-1.5, min(1.5, self.cam_pitch))
    
    def build_rooms(self):
        self.objs = []
        
        # KELAS - Lantai & Dinding
        self.objs.append({'v': [[-400,0,-400], [400,0,-400], [400,0,400], [-400,0,400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#a0a0a0'], 'p': [0,0,0], 'n': 'Lantai', 'cast_shadow': False})
        self.objs.append({'v': [[-400,0,-400], [400,0,-400], [400,-350,-400], [-400,-350,-400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#e0e0e0'], 'p': [0,0,0], 'n': 'Dinding', 'cast_shadow': False})
        self.objs.append({'v': [[-400,0,-400], [-400,0,400], [-400,-350,400], [-400,-350,-400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#e0e0e0'], 'p': [0,0,0], 'n': 'Dinding', 'cast_shadow': False})
        self.objs.append({'v': [[-400,0,400], [400,0,400], [400,-350,400], [-400,-350,400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#e0e0e0'], 'p': [0,0,0], 'n': 'Dinding', 'cast_shadow': False})
        self.objs.append({'v': [[-400,-350,-400], [400,-350,-400], [400,-350,400], [-400,-350,400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#c8c8c8'], 'p': [0,0,0], 'n': 'Atap', 'cast_shadow': False})
        
        # Dinding Kanan dengan Pintu (diperbaiki - pintu di lantai)
        self.objs.append({'v': [[400,0,-400], [400,0,-100], [400,-100,-100], [400,-100,-400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#e0e0e0'], 'p': [0,0,0], 'n': 'Dinding', 'cast_shadow': False})
        self.objs.append({'v': [[400,-250,-400], [400,-250,100], [400,-350,100], [400,-350,-400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#e0e0e0'], 'p': [0,0,0], 'n': 'Dinding', 'cast_shadow': False})
        self.objs.append({'v': [[400,0,100], [400,0,400], [400,-350,400], [400,-350,100]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#e0e0e0'], 'p': [0,0,0], 'n': 'Dinding', 'cast_shadow': False})
        
        # Frame Pintu (kayu coklat) - DARI LANTAI (Y=0)
        self.objs.append({'v': [[395,0,-105], [405,0,-105], [405,-250,-105], [395,-250,-105], [395,0,-100], [405,0,-100], [405,-250,-100], [395,-250,-100]], 'e': [], 'f': [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#8b4513'], 'p': [0,0,0], 'n': 'Frame Pintu Kiri', 'cast_shadow': True})
        self.objs.append({'v': [[395,0,100], [405,0,100], [405,-250,100], [395,-250,100], [395,0,105], [405,0,105], [405,-250,105], [395,-250,105]], 'e': [], 'f': [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#8b4513'], 'p': [0,0,0], 'n': 'Frame Pintu Kanan', 'cast_shadow': True})
        self.objs.append({'v': [[395,-250,-100], [405,-250,-100], [405,-250,100], [395,-250,100], [395,-260,-100], [405,-260,-100], [405,-260,100], [395,-260,100]], 'e': [], 'f': [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#8b4513'], 'p': [0,0,0], 'n': 'Frame Pintu Atas', 'cast_shadow': True})
        
        # Daun Pintu (kayu dengan panel) - DARI LANTAI
        self.objs.append({'v': [[398,-5,-95], [398,-5,0], [398,-245,0], [398,-245,-95], [402,-5,-95], [402,-5,0], [402,-245,0], [402,-245,-95]], 'e': [], 'f': [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#6b3410'], 'p': [0,0,0], 'n': 'Daun Pintu', 'cast_shadow': True})
        
        # Gagang Pintu (kuningan)
        self.objs.append({'v': [[400,-120,-5], [407,-120,-5], [407,-135,-5], [400,-135,-5], [400,-120,5], [407,-120,5], [407,-135,5], [400,-135,5]], 'e': [], 'f': [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#FFD700'], 'p': [0,0,0], 'n': 'Gagang Pintu', 'cast_shadow': True})
        
        # Papan & Meja Guru
        self.objs.append({'v': [[-200,-150,0], [200,-150,0], [200,-270,0], [-200,-270,0], [-200,-150,10], [200,-150,10], [200,-270,10], [-200,-270,10]], 'e': [], 'f': [[0,1,2,3], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#2d4a2e'], 'p': [0,0,-380], 'n': 'Papan', 'cast_shadow': True})
        self.objs.append({'v': [[-120,-80,-60], [120,-80,-60], [120,-80,60], [-120,-80,60], [-120,-90,-60], [120,-90,-60], [120,-90,60], [-120,-90,60]], 'e': [], 'f': [[0,1,2,3], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#8b4513'], 'p': [0,0,-250], 'n': 'Meja', 'cast_shadow': True})
        
        # Jendela Kelas - Dinding Kiri (2 jendela vertikal - tidak dekat papan tulis)
        for i in range(2):
            jz = 100 + i*200  # Posisi di tengah dan depan saja (tidak di belakang dekat papan)
            self.objs.append({'v': [[-5,-150,-60], [5,-150,-60], [5,-280,-60], [-5,-280,-60], [-5,-150,60], [5,-150,60], [5,-280,60], [-5,-280,60]], 'e': [], 'f': [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#654321'], 'p': [-395,0,jz], 'n': 'Frame Jendela Kiri', 'cast_shadow': True})
            # Kaca jendela dengan efek sinar matahari
            self.objs.append({'v': [[0,-155,-55], [0,-155,55], [0,-275,55], [0,-275,-55]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#E0F6FF'], 'p': [-395,0,jz], 'n': 'Kaca Jendela Kiri', 'cast_shadow': False, 'transparent': True, 'glow': True})
        
        # Kursi yang lebih realistis (sandaran di Z positif)
        for r in range(3):
            for c in range(3):
                cx, cz = -180 + c*180, 50 + r*100
                sw, sd, sh = 35, 35, 10  # width, depth, seat height
                
                # Warna kursi bervariasi (biru, hijau, merah)
                chair_colors = ['#4a90e2', '#2ecc71', '#e74c3c']
                chair_col = chair_colors[(r + c) % 3]
                
                # 1. Tempat duduk (seat)
                self.objs.append({'v': [
                    [-sw,-40,-sd], [sw,-40,-sd], [sw,-40,sd], [-sw,-40,sd],
                    [-sw,-50,-sd], [sw,-50,-sd], [sw,-50,sd], [-sw,-50,sd]
                ], 'e': [], 'f': [
                    [0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]
                ], 'c': [chair_col], 'p': [cx,0,cz], 'n': 'Kursi Duduk', 'cast_shadow': True})
                
                # 2. Sandaran (backrest) - lebih lebar dan tinggi
                self.objs.append({'v': [
                    [-sw,-50,sd-8], [sw,-50,sd-8], [sw,-130,sd-8], [-sw,-130,sd-8],
                    [-sw,-50,sd+8], [sw,-50,sd+8], [sw,-130,sd+8], [-sw,-130,sd+8]
                ], 'e': [], 'f': [
                    [0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]
                ], 'c': [chair_col], 'p': [cx,0,cz], 'n': 'Kursi Sandaran', 'cast_shadow': True})
                
                # 3. Kaki kursi (4 kaki)
                leg_w = 4
                leg_positions = [
                    [-sw+8, -sd+8], [sw-8, -sd+8], [-sw+8, sd-8], [sw-8, sd-8]
                ]
                for lx, lz in leg_positions:
                    self.objs.append({'v': [
                        [lx-leg_w,0,lz-leg_w], [lx+leg_w,0,lz-leg_w], [lx+leg_w,0,lz+leg_w], [lx-leg_w,0,lz+leg_w],
                        [lx-leg_w,-50,lz-leg_w], [lx+leg_w,-50,lz-leg_w], [lx+leg_w,-50,lz+leg_w], [lx-leg_w,-50,lz+leg_w]
                    ], 'e': [], 'f': [
                        [0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]
                    ], 'c': ['#2c3e50'], 'p': [cx,0,cz], 'n': 'Kaki Kursi', 'cast_shadow': True})
                
                # 4. Penyangga sandaran (support poles) - 2 tiang
                pole_w = 3
                for pole_x in [-sw+10, sw-10]:
                    self.objs.append({'v': [
                        [pole_x-pole_w,-50,sd-6], [pole_x+pole_w,-50,sd-6], [pole_x+pole_w,-50,sd], [pole_x-pole_w,-50,sd],
                        [pole_x-pole_w,-130,sd-6], [pole_x+pole_w,-130,sd-6], [pole_x+pole_w,-130,sd], [pole_x-pole_w,-130,sd]
                    ], 'e': [], 'f': [
                        [0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]
                    ], 'c': ['#34495e'], 'p': [cx,0,cz], 'n': 'Penyangga Kursi', 'cast_shadow': True})
                
                # 5. Bantalan kursi (cushion detail)
                cushion_inset = 5
                self.objs.append({'v': [
                    [-sw+cushion_inset,-39,-sd+cushion_inset], [sw-cushion_inset,-39,-sd+cushion_inset], 
                    [sw-cushion_inset,-39,sd-cushion_inset], [-sw+cushion_inset,-39,sd-cushion_inset]
                ], 'e': [], 'f': [[0,1,2,3]], 'c': [self.lighten_color(chair_col, 1.2)], 'p': [cx,0,cz], 'n': 'Bantalan Kursi', 'cast_shadow': False})
        
        # LAB - Lantai & Dinding
        self.objs.append({'v': [[400,0,-400], [900,0,-400], [900,0,400], [400,0,400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#909090'], 'p': [0,0,0], 'n': 'Lantai Lab', 'cast_shadow': False})
        self.objs.append({'v': [[400,0,-400], [900,0,-400], [900,-350,-400], [400,-350,-400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#d0d0e0'], 'p': [0,0,0], 'n': 'Dinding Lab', 'cast_shadow': False})
        self.objs.append({'v': [[900,0,-400], [900,0,400], [900,-350,400], [900,-350,-400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#d0d0e0'], 'p': [0,0,0], 'n': 'Dinding Lab', 'cast_shadow': False})
        self.objs.append({'v': [[400,0,400], [900,0,400], [900,-350,400], [400,-350,400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#d0d0e0'], 'p': [0,0,0], 'n': 'Dinding Lab', 'cast_shadow': False})
        self.objs.append({'v': [[400,-350,-400], [900,-350,-400], [900,-350,400], [400,-350,400]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#b8b8c8'], 'p': [0,0,0], 'n': 'Atap Lab', 'cast_shadow': False})
        
        # Meja Lab & Komputer
        for i in range(3):
            lz = -200 + i*200
            self.objs.append({'v': [[-100,-80,-40], [100,-80,-40], [100,-80,40], [-100,-80,40], [-100,-90,-40], [100,-90,-40], [100,-90,40], [-100,-90,40]], 'e': [], 'f': [[0,1,2,3], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#505050'], 'p': [650,0,lz], 'n': 'Meja Lab', 'cast_shadow': True})
            self.objs.append({'v': [[-30,-90,-5], [30,-90,-5], [30,-130,-5], [-30,-130,-5], [-30,-90,5], [30,-90,5], [30,-130,5], [-30,-130,5]], 'e': [], 'f': [[0,1,2,3], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#1a1a1a'], 'p': [650,0,lz], 'n': 'PC', 'cast_shadow': True})
        
        # Lemari Lab
        self.objs.append({'v': [[-60,0,-40], [60,0,-40], [60,-200,-40], [-60,-200,-40], [-60,0,40], [60,0,40], [60,-200,40], [-60,-200,40]], 'e': [], 'f': [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#6b4423'], 'p': [850,0,-350], 'n': 'Lemari', 'cast_shadow': True})
        
        # Jendela Lab (lebih besar, kaca transparan dengan efek cahaya)
        # Jendela lab 1
        self.objs.append({'v': [[-80,-130,-5], [-80,-130,5], [-80,-300,5], [-80,-300,-5], [80,-130,-5], [80,-130,5], [80,-300,5], [80,-300,-5]], 'e': [], 'f': [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#654321'], 'p': [650,0,395], 'n': 'Frame Jendela Lab', 'cast_shadow': True})
        # Kaca jendela lab 1 (transparan dengan cahaya)
        self.objs.append({'v': [[-75,-135,0], [75,-135,0], [75,-295,0], [-75,-295,0]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#E0F6FF'], 'p': [650,0,395], 'n': 'Kaca Jendela Lab', 'cast_shadow': False, 'transparent': True, 'glow': True})
        
        # Jendela lab 2 (di dinding samping)
        self.objs.append({'v': [[-5,-130,-80], [5,-130,-80], [5,-300,-80], [-5,-300,-80], [-5,-130,80], [5,-130,80], [5,-300,80], [-5,-300,80]], 'e': [], 'f': [[0,1,2,3], [4,5,6,7], [0,1,5,4], [1,2,6,5], [2,3,7,6], [3,0,4,7]], 'c': ['#654321'], 'p': [895,0,0], 'n': 'Frame Jendela Lab', 'cast_shadow': True})
        # Kaca jendela lab 2
        self.objs.append({'v': [[0,-135,-75], [0,-135,75], [0,-295,75], [0,-295,-75]], 'e': [], 'f': [[0,1,2,3]], 'c': ['#E0F6FF'], 'p': [895,0,0], 'n': 'Kaca Jendela Lab', 'cast_shadow': False, 'transparent': True, 'glow': True})
    
    def reset(self):
        self.cam_x, self.cam_y, self.cam_z = 0, -100, 250
        self.cam_yaw, self.cam_pitch = 0, 0
        self.floor_reflection = True
        self.light_intensity = 1.0
        self.intensity_slider.set(100)
    
    def toggle_grid(self):
        self.show_grid = not self.show_grid
    
    def toggle_light(self):
        self.light_on = not self.light_on
    
    def toggle_floor_reflection(self):
        self.floor_reflection = not self.floor_reflection
    
    def calculate_lighting(self, world_pos, base_color):
        """Hitung lighting berdasarkan jarak ke sumber cahaya"""
        if not self.light_on:
            return self.darken_color(base_color, 0.2)
        
        total_r, total_g, total_b = 0, 0, 0
        
        # Pulse effect
        pulse_factor = 1.0
        if self.light_pulse:
            pulse_factor = 0.85 + 0.15 * math.sin(self.time * 0.05)
        
        for light in self.light_sources:
            # Hitung jarak ke cahaya
            dx = world_pos[0] - light['pos'][0]
            dy = world_pos[1] - light['pos'][1]
            dz = world_pos[2] - light['pos'][2]
            dist = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            # Attenuation (falloff)
            attenuation = max(0, 1.0 - (dist / light['range']))
            attenuation = attenuation * attenuation  # Quadratic falloff
            
            # Apply light color and intensity
            intensity = light['intensity'] * attenuation * self.light_intensity * pulse_factor
            total_r += light['color'][0] * intensity
            total_g += light['color'][1] * intensity
            total_b += light['color'][2] * intensity
        
        # Ambient light
        ambient = 0.15 * self.light_intensity
        total_r += 255 * ambient
        total_g += 255 * ambient
        total_b += 255 * ambient
        
        # Apply to base color
        try:
            base_r = int(base_color[1:3], 16)
            base_g = int(base_color[3:5], 16)
            base_b = int(base_color[5:7], 16)
            
            final_r = min(255, int(base_r * total_r / 255))
            final_g = min(255, int(base_g * total_g / 255))
            final_b = min(255, int(base_b * total_b / 255))
            
            return '#{:02x}{:02x}{:02x}'.format(final_r, final_g, final_b)
        except:
            return base_color
    
    def lighten_color(self, col, factor):
        """Terangkan warna dengan faktor tertentu untuk efek bantalan"""
        try:
            r = min(255, int(int(col[1:3], 16) * factor))
            g = min(255, int(int(col[3:5], 16) * factor))
            b = min(255, int(int(col[5:7], 16) * factor))
            return '#{:02x}{:02x}{:02x}'.format(r, g, b)
        except:
            return col
    
    def darken_color(self, col, factor):
        """Gelapkan warna dengan faktor tertentu"""
        try:
            r = int(int(col[1:3], 16) * factor)
            g = int(int(col[3:5], 16) * factor)
            b = int(int(col[5:7], 16) * factor)
            return '#{:02x}{:02x}{:02x}'.format(r, g, b)
        except:
            return col
    
    def transform_camera(self, verts, pos):
        res = []
        for v in verts:
            x, y, z = v[0] + pos[0] - self.cam_x, v[1] + pos[1] - self.cam_y, v[2] + pos[2] - self.cam_z
            cos_y, sin_y = math.cos(-self.cam_yaw), math.sin(-self.cam_yaw)
            x, z = x*cos_y - z*sin_y, x*sin_y + z*cos_y
            cos_x, sin_x = math.cos(-self.cam_pitch), math.sin(-self.cam_pitch)
            y, z = y*cos_x - z*sin_x, y*sin_x + z*cos_x
            res.append([x, y, z])
        return res
    
    def transform_camera_reflection(self, verts, pos):
        res = []
        for v in verts:
            x, y, z = v[0] + pos[0] - self.cam_x, v[1] + pos[1] - self.cam_y, v[2] + pos[2] - self.cam_z
            y = -y
            cos_y, sin_y = math.cos(-self.cam_yaw), math.sin(-self.cam_yaw)
            x, z = x*cos_y - z*sin_y, x*sin_y + z*cos_y
            cos_x, sin_x = math.cos(-self.cam_pitch), math.sin(-self.cam_pitch)
            y, z = y*cos_x - z*sin_x, y*sin_x + z*cos_x
            res.append([x, y, z])
        return res
    
    def project(self, verts):
        res = []
        fov_factor = 1.0 / math.tan(math.radians(self.fov / 2))
        for v in verts:
            if v[2] <= 0.1:
                res.append([self.w//2, self.h//2, -1000])
            else:
                scale = fov_factor * 500 / v[2]
                res.append([v[0]*scale + self.w//2, v[1]*scale + self.h//2, v[2]])
        return res
    
    def draw_shadow(self, c, obj):
        """Gambar bayangan objek di lantai"""
        if not obj.get('cast_shadow', False):
            return
        
        shadow_verts = []
        for v in obj['v']:
            # Project vertex ke lantai (y=0)
            wx = v[0] + obj['p'][0]
            wy = v[1] + obj['p'][1]
            wz = v[2] + obj['p'][2]
            
            # Shadow projection dari light source
            lx, ly, lz = self.shadow_light_pos
            
            if ly - wy != 0:
                t = -wy / (ly - wy)
                shadow_x = wx + t * (lx - wx)
                shadow_z = wz + t * (lz - wz)
                shadow_verts.append([shadow_x, 1, shadow_z])  # Sedikit di atas lantai
            else:
                shadow_verts.append([wx, 1, wz])
        
        if not shadow_verts:
            return
        
        tv = self.transform_camera(shadow_verts, [0, 0, 0])
        pv = self.project(tv)
        
        for f in obj['f']:
            if all(v < len(pv) and pv[v][2] > 0 for v in f):
                coords = [coord for v in f for coord in [pv[v][0], pv[v][1]]]
                if len(coords) >= 6:
                    try:
                        c.create_polygon(coords, fill='#000000', outline='', stipple='gray50')
                    except:
                        pass
    
    def draw_obj(self, c, obj):
        tv = self.transform_camera(obj['v'], obj['p'])
        pv = self.project(tv)
        fz = [(sum(pv[v][2] for v in f)/len(f), i) for i, f in enumerate(obj['f']) if all(v < len(pv) and pv[v][2] > 0 for v in f)]
        fz.sort(reverse=True)
        
        for z, i in fz:
            f = obj['f'][i]
            
            # Hitung posisi world center dari face
            world_center = [0, 0, 0]
            for v_idx in f:
                world_center[0] += obj['v'][v_idx][0] + obj['p'][0]
                world_center[1] += obj['v'][v_idx][1] + obj['p'][1]
                world_center[2] += obj['v'][v_idx][2] + obj['p'][2]
            world_center = [x / len(f) for x in world_center]
            
            # Apply lighting
            base_col = obj['c'][i % len(obj['c'])]
            col = self.calculate_lighting(world_center, base_col)
            
            coords = [coord for v in f for coord in [pv[v][0], pv[v][1]]]
            if len(coords) >= 6:
                try:
                    # Cek apakah objek transparan (kaca jendela)
                    if obj.get('transparent', False):
                        # Kaca dengan efek cahaya matahari (glow effect)
                        if obj.get('glow', False) and self.light_on:
                            # Efek cahaya terang dari jendela
                            glow_intensity = 0.7 + 0.3 * math.sin(self.time * 0.02)
                            glow_col = '#{:02x}{:02x}{:02x}'.format(
                                min(255, int(224 * glow_intensity)),
                                min(255, int(246 * glow_intensity)),
                                255
                            )
                            c.create_polygon(coords, fill=glow_col, outline='#FFFFFF', width=1, stipple='gray12')
                        else:
                            c.create_polygon(coords, fill=col, outline='#4682B4', width=2, stipple='gray50')
                    else:
                        c.create_polygon(coords, fill=col, outline='#2a2a2a', width=1)
                except:
                    pass
    
    def draw_obj_reflection(self, c, obj):
        tv = self.transform_camera_reflection(obj['v'], obj['p'])
        pv = self.project(tv)
        fz = [(sum(pv[v][2] for v in f)/len(f), i) for i, f in enumerate(obj['f']) if all(v < len(pv) and pv[v][2] > 0 for v in f)]
        fz.sort(reverse=True)
        
        for z, i in fz:
            f = obj['f'][i]
            col = obj['c'][i % len(obj['c'])]
            
            try:
                r = max(0, int(int(col[1:3], 16) * 0.15))
                g = max(0, int(int(col[3:5], 16) * 0.15))
                b = max(0, int(int(col[5:7], 16) * 0.15))
                ref_col = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            except:
                ref_col = '#222222'
            
            coords = [coord for v in f for coord in [pv[v][0], pv[v][1]]]
            if len(coords) >= 6:
                try:
                    c.create_polygon(coords, fill=ref_col, outline='', stipple='gray25')
                except:
                    pass
    
    def draw_grid(self, c):
        gv = []
        for i in range(-400, 901, 100):
            gv.extend([[-400,0,i], [900,0,i], [i,0,-400], [i,0,400]])
        tv = self.transform_camera(gv, [0,0,0])
        pv = self.project(tv)
        for i in range(0, len(pv), 2):
            if i+1 < len(pv) and pv[i][2] > 0 and pv[i+1][2] > 0:
                try:
                    c.create_line(pv[i][0], pv[i][1], pv[i+1][0], pv[i+1][1], fill='#ccc', width=1, dash=(2,2))
                except:
                    pass
    
    def get_room(self):
        return "🎓 RUANG KELAS" if self.cam_x < 400 else "🔬 LABORATORIUM"
    
    def animate(self):
        self.canvas.delete('all')
        self.time += 1
        
        # Dynamic background based on light
        if self.light_on:
            bg_brightness = int(200 + 32 * self.light_intensity)
            bg_color = '#{:02x}{:02x}{:02x}'.format(bg_brightness, bg_brightness, bg_brightness)
        else:
            bg_color = '#4a4a4a'
        self.canvas.config(bg=bg_color)
        
        if self.show_grid:
            self.draw_grid(self.canvas)
        
        oz = []
        for obj in self.objs:
            tv = self.transform_camera(obj['v'], obj['p'])
            valid_z = [v[2] for v in tv if v[2] > 0]
            if valid_z:
                oz.append((sum(valid_z)/len(valid_z), obj))
        oz.sort(reverse=True, key=lambda x: x[0])
        
        # Gambar bayangan terlebih dahulu
        if self.show_shadows and self.light_on:
            for _, obj in oz:
                self.draw_shadow(self.canvas, obj)
        
        # Gambar refleksi
        if self.floor_reflection:
            for _, obj in oz:
                if 'Lantai' not in obj['n']:
                    self.draw_obj_reflection(self.canvas, obj)
        
        # Gambar objek asli
        for _, obj in oz:
            self.draw_obj(self.canvas, obj)
        
        # UI
        room = self.get_room()
        col = '#06ffa5' if room == "🎓 RUANG KELAS" else '#ff006e'
        
        self.canvas.create_rectangle(10, 10, 420, 180, fill='#fff', outline=col, width=3)
        self.canvas.create_text(20, 30, anchor='w', text=f"LOKASI: {room}", fill=col, font=('Arial', 14, 'bold'))
        self.canvas.create_text(20, 60, anchor='w', text=f"Pos: ({self.cam_x:.0f}, {self.cam_y:.0f}, {self.cam_z:.0f})", fill='#2a9d8f', font=('Arial', 10))
        self.canvas.create_text(20, 85, anchor='w', text=f"Yaw={math.degrees(self.cam_yaw):.0f}° Pitch={math.degrees(self.cam_pitch):.0f}°", fill='#e76f51', font=('Arial', 10))
        
        # LIGHTING INFO
        light_status = "ON ☀️" if self.light_on else "OFF 🌙"
        pulse_status = "ON 🌟" if self.light_pulse else "OFF"
        shadow_status = "ON 👤" if self.show_shadows else "OFF"
        
        self.canvas.create_text(20, 115, anchor='w', text="💡 SISTEM LIGHTING:", fill='#ffd60a', font=('Arial', 10, 'bold'))
        self.canvas.create_text(30, 140, anchor='w', text=f"Lampu: {light_status} | Intensitas: {int(self.light_intensity*100)}%", fill='#fb8500', font=('Arial', 9))
        
        # REFLEKSI & SHADOW INFO (Simplified)
        ref_status = "ON 🪞" if self.floor_reflection else "OFF"
        self.canvas.create_text(30, 160, anchor='w', text=f"Pulse: {pulse_status} | Shadow: {shadow_status} | Refleksi: {ref_status}", fill='#023047', font=('Arial', 9))
        
        # Instruksi
        self.canvas.create_rectangle(10, self.h - 110, 580, self.h - 10, fill='#fff', outline='#06ffa5', width=2)
        self.canvas.create_text(20, self.h - 95, anchor='w', text="⌨️ WASD=Gerak | Arrow=Lihat | Mouse Drag=Look", fill='#888', font=('Arial', 8))
        self.canvas.create_text(20, self.h - 75, anchor='w', text="🚪 Jalan ke KANAN (D) untuk masuk LABORATORIUM!", fill='#ff6b00', font=('Arial', 9, 'bold'))
        self.canvas.create_text(20, self.h - 55, anchor='w', text="💡 L=Lampu | P=Pulse | H=Shadow | M=Refleksi | G=Grid | R=Reset", fill='#ffd60a', font=('Arial', 9, 'bold'))
        self.canvas.create_text(20, self.h - 35, anchor='w', text="☀️ Gunakan slider untuk kontrol intensitas cahaya!", fill='#06ffa5', font=('Arial', 9, 'bold'))
        self.canvas.create_text(20, self.h - 15, anchor='w', text="🪟 Perhatikan cahaya matahari masuk dari jendela!", fill='#ff006e', font=('Arial', 8, 'bold'))
        
        self.root.after(30, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = Room3D(root)
    root.mainloop()