import tkinter as tk
import re

OPERATOR = ("+", "-", "×", "÷")

# Ekspresi disimpan dalam format mentah (desimal pakai ".", tanpa pemisah ribuan)
# Layar menampilkan versi yang sudah diformat (ribuan "." dan desimal ",")
ekspresi = "0"


# ---------- Fungsi format ----------
def format_angka(teks):
    """Ubah semua angka dalam teks menjadi format Indonesia: 1234567.5 -> 1.234.567,5"""
    def ubah(m):
        bulat = f"{int(m.group(1)):,}".replace(",", ".")
        if m.group(2) is not None:  # ada titik desimal
            return bulat + "," + m.group(3)
        return bulat
    return re.sub(r"(\d+)(\.(\d*))?", ubah, teks)


def perbarui_layar():
    entry_layar.delete(0, tk.END)
    if ekspresi == "Error":
        entry_layar.insert(tk.END, "Error")
    else:
        entry_layar.insert(tk.END, format_angka(ekspresi))


# ---------- Fungsi ----------
def tambah_ke_layar(nilai):
    global ekspresi
    current = ekspresi
    if current == "Error":
        current = "0"

    segmen_terakhir = current
    for op in OPERATOR:
        segmen_terakhir = segmen_terakhir.rsplit(op, 1)[-1]

    if nilai in OPERATOR:
        if current == "0":
            return  # abaikan jika belum ada angka
        if current[-1] in OPERATOR:
            current = current[:-1] + nilai  # ganti operator terakhir
        else:
            current += nilai
    elif nilai == ".":
        if "." in segmen_terakhir:
            return  # cegah titik desimal ganda dalam angka yang sama
        if current == "0":
            current = "0."
        elif current[-1] in OPERATOR:
            current += "0."
        else:
            current += "."
    else:
        if current == "0":
            current = nilai
        elif segmen_terakhir == "0":
            current = current[:-1] + nilai  # hindari angka berawalan nol (mis. 05)
        else:
            current += nilai

    ekspresi = current
    perbarui_layar()


def hapus():
    global ekspresi
    ekspresi = "0"
    perbarui_layar()


def hapus_satu():
    global ekspresi
    if ekspresi == "Error" or len(ekspresi) <= 1:
        ekspresi = "0"
    else:
        ekspresi = ekspresi[:-1]
    perbarui_layar()


def hitung():
    global ekspresi
    try:
        ekspresi_python = ekspresi.replace("×", "*").replace("÷", "/")
        hasil = eval(ekspresi_python)
        if hasil == int(hasil):
            hasil = int(hasil)
            ekspresi = str(hasil)
        else:
            # hindari notasi ilmiah & error pembulatan (mis. 0.1+0.2)
            ekspresi = f"{hasil:.10f}".rstrip("0").rstrip(".")
    except Exception:
        ekspresi = "Error"
    perbarui_layar()


# ---------- Tampilan (GUI) ----------
window = tk.Tk()
window.title("Kalkulator Sederhana")
window.geometry("300x420")
window.resizable(False, False)
window.configure(bg="#1e1e1e")

entry_layar = tk.Entry(
    window, font=("Segoe UI", 24), justify="right",
    bd=0, bg="#2b2b2b", fg="white", insertbackground="white"
)
entry_layar.insert(tk.END, "0")
entry_layar.pack(fill="x", padx=10, pady=20, ipady=15)

frame_tombol = tk.Frame(window, bg="#1e1e1e")
frame_tombol.pack(expand=True, fill="both", padx=10)

# Konfigurasi tombol
tombol_style = {"font": ("Segoe UI", 16, "bold"), "bd": 0}

def buat_tombol(teks, baris, kolom, bg="#333333", fg="white", command=None, colspan=1, rowspan=1):
    btn = tk.Button(
        frame_tombol, text=teks, bg=bg, fg=fg,
        activebackground="#555555", activeforeground="white",
        command=command, **tombol_style
    )
    btn.grid(row=baris, column=kolom, columnspan=colspan, rowspan=rowspan, sticky="nsew", padx=4, pady=4)

for i in range(4):
    frame_tombol.grid_columnconfigure(i, weight=1)
for i in range(5):
    frame_tombol.grid_rowconfigure(i, weight=1)

# Baris 0: C, ⌫, ÷, ×
buat_tombol("C", 0, 0, bg="#F44336", command=hapus)
buat_tombol("⌫", 0, 1, bg="#F44336", command=hapus_satu)
buat_tombol("÷", 0, 2, bg="#FF9800", command=lambda: tambah_ke_layar("÷"))
buat_tombol("×", 0, 3, bg="#FF9800", command=lambda: tambah_ke_layar("×"))

# Baris 1: 7 8 9 -
buat_tombol("7", 1, 0, command=lambda: tambah_ke_layar("7"))
buat_tombol("8", 1, 1, command=lambda: tambah_ke_layar("8"))
buat_tombol("9", 1, 2, command=lambda: tambah_ke_layar("9"))
buat_tombol("-", 1, 3, bg="#FF9800", command=lambda: tambah_ke_layar("-"))

# Baris 2: 4 5 6 +
buat_tombol("4", 2, 0, command=lambda: tambah_ke_layar("4"))
buat_tombol("5", 2, 1, command=lambda: tambah_ke_layar("5"))
buat_tombol("6", 2, 2, command=lambda: tambah_ke_layar("6"))
buat_tombol("+", 2, 3, bg="#FF9800", command=lambda: tambah_ke_layar("+"))

# Baris 3: 1 2 3 = (= memanjang ke bawah, baris 3-4)
buat_tombol("1", 3, 0, command=lambda: tambah_ke_layar("1"))
buat_tombol("2", 3, 1, command=lambda: tambah_ke_layar("2"))
buat_tombol("3", 3, 2, command=lambda: tambah_ke_layar("3"))
buat_tombol("=", 3, 3, bg="#4CAF50", command=hitung, rowspan=2)

# Baris 4: 0 ,
buat_tombol("0", 4, 0, colspan=2, command=lambda: tambah_ke_layar("0"))
buat_tombol(",", 4, 2, command=lambda: tambah_ke_layar("."))

window.mainloop()