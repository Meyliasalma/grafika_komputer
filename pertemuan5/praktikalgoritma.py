import turtle
import sys

# Setup layar - ukuran disesuaikan agar pas di layar
screen = turtle.Screen()
screen.title("Praktikum - Menggambar Garis, Lingkaran, dan Poligon")
screen.bgcolor("white")
screen.setup(width=1.0, height=1.0)  # Fullscreen mode

# Setup turtle untuk menggambar
t = turtle.Turtle()
t.speed(6)
t.pensize(2)

# Setup turtle untuk menulis teks
writer = turtle.Turtle()
writer.hideturtle()
writer.penup()
writer.speed(0)

def write_text(x, y, text, size=12, color="black"):
    """Fungsi untuk menulis teks"""
    writer.color(color)
    writer.goto(x, y)
    writer.write(text, align="center", font=("Arial", size, "bold"))

# ===== 1. ALGORITMA DDA UNTUK MENGGAMBAR GARIS =====
def dda_algorithm(x1, y1, x2, y2):
    """
    Algoritma DDA (Digital Differential Analyzer)
    untuk menggambar garis dari titik (x1,y1) ke (x2,y2)
    """
    print("\n=== ALGORITMA DDA ===")
    print(f"Menggambar garis dari ({x1},{y1}) ke ({x2},{y2})")
    
    # Hitung selisih
    dx = x2 - x1
    dy = y2 - y1
    
    print(f"dx = {dx}, dy = {dy}")
    
    # Tentukan jumlah langkah
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)
    
    print(f"Jumlah steps = {steps}")
    
    # Hitung increment
    if steps == 0:
        return
        
    x_increment = dx / steps
    y_increment = dy / steps
    
    print(f"x_increment = {x_increment:.2f}")
    print(f"y_increment = {y_increment:.2f}")
    
    # Mulai menggambar
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    
    x = x1
    y = y1
    
    # Gambar garis titik per titik
    for i in range(int(steps) + 1):
        t.goto(round(x), round(y))
        x += x_increment
        y += y_increment
    
    print("Garis selesai digambar!")
    t.penup()

# ===== 2. ALGORITMA MIDPOINT CIRCLE UNTUK MENGGAMBAR LINGKARAN =====
def midpoint_circle(xc, yc, r):
    """
    Algoritma Midpoint Circle
    untuk menggambar lingkaran dengan pusat (xc,yc) dan radius r
    """
    print("\n=== ALGORITMA MIDPOINT CIRCLE ===")
    print(f"Menggambar lingkaran dengan pusat ({xc},{yc}) dan radius {r}")
    
    def plot_8_points(xc, yc, x, y):
        """Plot 8 titik simetris pada lingkaran"""
        points = [
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x)
        ]
        return points
    
    # Inisialisasi
    x = 0
    y = r
    p = 1 - r  # Parameter keputusan awal
    
    print(f"Nilai awal: x={x}, y={y}, p={p}")
    
    # Kumpulkan semua titik terlebih dahulu
    all_points = []
    
    while x <= y:
        points = plot_8_points(xc, yc, x, y)
        all_points.extend(points)
        
        x += 1
        
        if p < 0:
            p = p + 2 * x + 1
        else:
            y -= 1
            p = p + 2 * (x - y) + 1
    
    # Gambar lingkaran dengan menghubungkan titik
    t.penup()
    t.goto(xc + r, yc)
    t.pendown()
    t.circle(r)
    
    print(f"Lingkaran selesai digambar!")
    print(f"Total iterasi: {x}")
    t.penup()

# ===== 3. ALGORITMA UNTUK MENGGAMBAR POLIGON =====
def draw_polygon(x, y, sides, length):
    """
    Algoritma untuk menggambar poligon beraturan
    x, y = koordinat awal
    sides = jumlah sisi
    length = panjang sisi
    """
    print("\n=== ALGORITMA POLIGON ===")
    print(f"Menggambar poligon {sides} sisi dengan panjang sisi {length}")
    
    # Hitung sudut eksterior
    angle = 360 / sides
    print(f"Sudut eksterior = 360° / {sides} = {angle}°")
    
    # Hitung sudut interior
    interior_angle = 180 - angle
    print(f"Sudut interior = 180° - {angle}° = {interior_angle}°")
    
    # Mulai menggambar
    t.penup()
    t.goto(x, y)
    t.pendown()
    
    # Gambar poligon
    for i in range(sides):
        t.forward(length)
        t.right(angle)
    
    print(f"Poligon {sides} sisi selesai digambar!")
    t.penup()

# ===== PROGRAM UTAMA =====
print("\n         Menggambar garis, lingkaran, dan poligon")
print("              Menggunakan Python + Turtle")
print("=" * 70)

# Judul Utama
write_text(0, 360, "PRAKTIKUM GRAFIKA KOMPUTER", 16, "navy")
write_text(0, 335, "Menggambar Garis, Lingkaran, dan Poligon", 13, "darkblue")

# ===== BAGIAN 1: MENGGAMBAR GARIS =====
write_text(-400, 270, "1. MENGGAMBAR GARIS", 14, "darkred")
write_text(-400, 250, "(Algoritma DDA)", 11, "black")

# Garis horizontal
t.color("red")
t.pensize(3)
dda_algorithm(-520, 200, -280, 200)
write_text(-400, 170, "Garis Horizontal", 10, "darkred")

# Garis vertikal
t.color("blue")
t.pensize(3)
dda_algorithm(-520, 130, -520, -20)
write_text(-520, -50, "Garis Vertikal", 10, "darkblue")

# Garis diagonal
t.color("green")
t.pensize(3)
dda_algorithm(-380, 130, -280, -20)
write_text(-330, -50, "Garis Diagonal", 10, "darkgreen")

# ===== BAGIAN 2: MENGGAMBAR LINGKARAN =====
write_text(0, 270, "2. MENGGAMBAR LINGKARAN", 14, "darkmagenta")
write_text(0, 250, "(Algoritma Midpoint Circle)", 11, "black")

# Lingkaran besar
t.color("purple")
t.pensize(3)
midpoint_circle(0, 80, 85)
write_text(0, -30, "Lingkaran Besar (r=90)", 10, "purple")

# Lingkaran sedang
t.color("orange")
t.pensize(2)
midpoint_circle(0, 80, 55)
write_text(0, -50, "Lingkaran Sedang (r=60)", 10, "darkorange")

# Lingkaran kecil
t.color("red")
t.pensize(2)
midpoint_circle(0, 80, 25)
write_text(0, -70, "Lingkaran Kecil (r=30)", 10, "darkred")

# ===== BAGIAN 3: MENGGAMBAR POLIGON =====
write_text(400, 270, "3. MENGGAMBAR POLIGON", 14, "darkgreen")
write_text(400, 250, "(Algoritma Poligon Beraturan)", 11, "black")

# Segitiga (3 sisi)
t.color("red")
t.pensize(3)
draw_polygon(300, 180, 3, 70)
write_text(340, 90, "Segitiga", 10, "darkred")
write_text(340, 75, "(3 sisi)", 9, "gray")

# Persegi (4 sisi)
t.color("blue")
t.pensize(3)
draw_polygon(440, 180, 4, 65)
write_text(502, 90, "Persegi", 10, "darkblue")
write_text(502, 75, "(4 sisi)", 9, "gray")

# Pentagon (5 sisi)
t.color("green")
t.pensize(3)
draw_polygon(310, 10, 5, 60)
write_text(360, -70, "Pentagon", 10, "darkgreen")
write_text(360, -85, "(5 sisi)", 9, "gray")

# Hexagon (6 sisi)
t.color("orange")
t.pensize(3)
draw_polygon(450, 10, 6, 55)
write_text(510, -70, "Hexagon", 10, "darkorange")
write_text(510, -85, "(6 sisi)", 9, "gray")

# Selesai
t.hideturtle()

# Analisis
print("\n" + "=" * 70)
print("                    ANALISIS PROSES MENGGAMBAR:")
print("=" * 70)
print("""
1. ALGORITMA DDA (Digital Differential Analyzer):
   - Input: Koordinat titik awal (x1,y1) dan titik akhir (x2,y2)
   - Proses:
     * Hitung dx = x2 - x1 dan dy = y2 - y1
     * Tentukan steps = max(|dx|, |dy|)
     * Hitung x_increment = dx/steps dan y_increment = dy/steps
     * Gambar titik dari (x1,y1) dengan increment sampai (x2,y2)
   - Hasil: 3 jenis garis (horizontal, vertikal, diagonal)

2. ALGORITMA MIDPOINT CIRCLE:
   - Input: Koordinat pusat (xc,yc) dan radius r
   - Proses:
     * Gunakan simetri 8-way untuk efisiensi
     * Mulai dari titik (0,r)
     * Gunakan decision parameter p untuk menentukan piksel berikutnya
     * Plot 8 titik simetris di setiap iterasi
   - Hasil: 3 lingkaran konsentris (besar, sedang, kecil)

3. ALGORITMA POLIGON BERATURAN:
   - Input: Koordinat awal (x,y), jumlah sisi, panjang sisi
   - Proses:
     * Hitung sudut eksterior = 360° / jumlah_sisi
     * Gambar dengan pola: maju → putar → maju → putar
     * Ulangi sebanyak jumlah sisi
   - Hasil: 4 poligon (Segitiga, Persegi, Pentagon, Hexagon)
""")

# Tunggu interaksi user
screen.mainloop()