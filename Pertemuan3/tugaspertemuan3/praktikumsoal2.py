# Ukuran layar 10x5
lebar = 10
tinggi = 5

# Titik yang akan ditampilkan
x = 3
y = 2

# Cetak tampilan koordinat
print("=== SIMULASI KOORDINAT ===")

for baris in range(tinggi, 0, -1):  
    for kolom in range(1, lebar + 1):  
        if kolom == x and baris == y:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
