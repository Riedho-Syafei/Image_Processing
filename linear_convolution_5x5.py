"""
Program Konvolusi Citra menggunakan Linear Filter (Kernel Rataan 5x5)
Tanpa library OpenCV maupun library pemrosesan citra lainnya.
Hanya menggunakan Pillow untuk membaca/menyimpan file gambar.
"""

from PIL import Image


def buat_kernel_rataan(ukuran=5):
    """
    Membuat kernel rataan (mean filter) berukuran ukuran x ukuran.
    Setiap elemen bernilai 1/(ukuran*ukuran).
    """
    nilai = 1.0 / (ukuran * ukuran)
    return [[nilai] * ukuran for _ in range(ukuran)]


def konvolusi_2d(piksel, kernel, lebar, tinggi):
    """
    Melakukan operasi konvolusi 2D secara manual pada satu channel.

    Parameters:
        piksel  : list 2D (tinggi x lebar) nilai piksel satu channel
        kernel  : list 2D kernel filter
        lebar   : lebar gambar (jumlah kolom)
        tinggi  : tinggi gambar (jumlah baris)

    Returns:
        hasil   : list 2D hasil konvolusi
    """
    k = len(kernel)          # ukuran kernel (misal 5)
    pad = k // 2             # jumlah padding (misal 2 untuk kernel 5x5)

    # Inisialisasi matriks output dengan nol
    hasil = [[0.0] * lebar for _ in range(tinggi)]

    for y in range(tinggi):
        for x in range(lebar):
            akumulasi = 0.0
            for ky in range(k):
                for kx in range(k):
                    # Koordinat piksel sumber dengan zero-padding
                    py = y + ky - pad
                    px = x + kx - pad
                    # Abaikan koordinat di luar batas (zero-padding)
                    if 0 <= py < tinggi and 0 <= px < lebar:
                        akumulasi += piksel[py][px] * kernel[ky][kx]
            # Klem nilai antara 0-255 dan simpan
            hasil[y][x] = max(0, min(255, round(akumulasi)))

    return hasil


def terapkan_filter_rataan(path_masukan, path_keluaran, ukuran_kernel=5):
    """
    Membaca gambar, menerapkan mean filter 5x5, dan menyimpan hasilnya.

    Parameters:
        path_masukan   : path file gambar input
        path_keluaran  : path file gambar output
        ukuran_kernel  : ukuran kernel rataan (default 5)
    """
    # ── Baca gambar ──────────────────────────────────────────────────────────
    gambar = Image.open(path_masukan).convert("RGB")
    lebar, tinggi = gambar.size
    print(f"Gambar dimuat: {path_masukan} ({lebar}x{tinggi} piksel)")

    # ── Buat kernel rataan ───────────────────────────────────────────────────
    kernel = buat_kernel_rataan(ukuran_kernel)
    print(f"Kernel rataan {ukuran_kernel}x{ukuran_kernel} dibuat "
          f"(setiap elemen = {kernel[0][0]:.4f})")

    # ── Pisahkan channel R, G, B ─────────────────────────────────────────────
    piksel_r = [[0] * lebar for _ in range(tinggi)]
    piksel_g = [[0] * lebar for _ in range(tinggi)]
    piksel_b = [[0] * lebar for _ in range(tinggi)]

    for y in range(tinggi):
        for x in range(lebar):
            r, g, b = gambar.getpixel((x, y))
            piksel_r[y][x] = r
            piksel_g[y][x] = g
            piksel_b[y][x] = b

    # ── Konvolusi per channel ─────────────────────────────────────────────────
    print("Menjalankan konvolusi... (mohon tunggu)")
    hasil_r = konvolusi_2d(piksel_r, kernel, lebar, tinggi)
    hasil_g = konvolusi_2d(piksel_g, kernel, lebar, tinggi)
    hasil_b = konvolusi_2d(piksel_b, kernel, lebar, tinggi)

    # ── Gabungkan kembali channel dan simpan ──────────────────────────────────
    gambar_hasil = Image.new("RGB", (lebar, tinggi))
    for y in range(tinggi):
        for x in range(lebar):
            gambar_hasil.putpixel(
                (x, y),
                (hasil_r[y][x], hasil_g[y][x], hasil_b[y][x])
            )

    gambar_hasil.save(path_keluaran)
    print(f"Gambar hasil disimpan: {path_keluaran}")


# ─────────────────────────────────────────────────────────────────────────────
# Titik masuk program
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    INPUT_PATH  = "image.jpg"
    OUTPUT_PATH = "output.jpg"   # Nama file hasil

    terapkan_filter_rataan(INPUT_PATH, OUTPUT_PATH, ukuran_kernel=5)