import math

# =============================
# Bagian 1: Praktikum Koordinat
# =============================
x1 = float(input("Masukkan x1: "))
y1 = float(input("Masukkan y1: "))
x2 = float(input("Masukkan x2: "))
y2 = float(input("Masukkan y2: "))

# Hitung jarak antar titik
jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Tentukan kuadran titik pertama
if x1 > 0 and y1 > 0:
    kuadran = "Kuadran I"
elif x1 < 0 and y1 > 0:
    kuadran = "Kuadran II"
elif x1 < 0 and y1 < 0:
    kuadran = "Kuadran III"
elif x1 > 0 and y1 < 0:
    kuadran = "Kuadran IV"
elif x1 == 0 and y1 == 0:
    kuadran = "Titik pusat (0,0)"
elif x1 == 0:
    kuadran = "Sumbu Y"
else:
    kuadran = "Sumbu X"

# Tampilkan hasil
print("\n=== HASIL ===")
print(f"Titik pertama: ({x1}, {y1})")
print(f"Titik kedua  : ({x2}, {y2})")
print(f"Jarak antar titik: {jarak:.2f}")
print(f"Titik pertama berada di: {kuadran}")

# =============================
# Bagian 2: Simulasi Koordinat
# =============================
print("\n")

lebar = 10
tinggi = 5

# Posisi titik dari input x1, y1 (disesuaikan agar tetap di area grid)
x = int(x1)
y = int(y1 / 2)  # dibagi 2 biar tetap muat di tinggi 5 (penyesuaian sederhana)

for baris in range(tinggi, 0, -1):  # dari atas ke bawah
    for kolom in range(1, lebar + 1):  # dari kiri ke kanan
        if kolom == x and baris == y:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
