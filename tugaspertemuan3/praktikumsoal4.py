# === PRAKTIKUM REPRESENTASI GAMBAR - RASTER ===

lebar = 10
tinggi = 10

x = 4
y = 6

print("=== REPRESENTASI RASTER ===")
for baris in range(tinggi, 0, -1):  # dari atas ke bawah
    for kolom in range(1, lebar + 1):  # dari kiri ke kanan
        if kolom == x and baris == y:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
