# Praktikum Representasi Gambar (Vektor)
# Menampilkan garis vektor dari titik (0,0) ke (5,3)

x1, y1 = 0, 0
x2, y2 = 5, 3

print("=== REPRESENTASI VEKTOR ===")
print(f"Titik awal : ({x1}, {y1})")
print(f"Titik akhir: ({x2}, {y2})")

# Hitung arah dan panjang vektor
dx = x2 - x1
dy = y2 - y1

print(f"Arah vektor  : Δx = {dx}, Δy = {dy}")
panjang = (dx**2 + dy**2) ** 0.5
print(f"Panjang vektor: {panjang:.2f}")

# Simulasi tampilan vektor dalam grid 6x4
print("\n=== GRID VEKTOR ===")
for y in range(3, -1, -1):  # dari atas ke bawah
    for x in range(0, 6):
        # titik awal
        if x == x1 and y == y1:
            print("A", end=" ")  # Titik awal
        # titik akhir
        elif x == x2 and y == y2:
            print("B", end=" ")  # Titik akhir
        # garis di antara keduanya (perkiraan sederhana)
        elif y == round((dy/dx) * x):
            print("-", end=" ")
        else:
            print(".", end=" ")
    print()
