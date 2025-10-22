x = int(input("memasukkan nilai x: "))

if x > 0:
    print ("titik di kanan layar.")
elif x < 0:
    print ("titik di kiri layar.")
else:
    print ("titik di tengah.")
    
print ("menampilkan  5 titik:")
for i in range (1, 6):
    print (f"titik ke-{i}")