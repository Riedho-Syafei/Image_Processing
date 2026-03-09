import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


# -----------------------------
# Membuka citra dan mengkonversinya menjadi grayscale
# -----------------------------
img = Image.open("image.jpg").convert("L")
img_array = np.array(img)

height = img_array.shape[0]
width = img_array.shape[1]


# -----------------------------
# Hitung histogram secara manual
# -----------------------------
def compute_histogram(image):

    hist = [0] * 256

    for y in range(height):
        for x in range(width):

            pixel = image[y][x]
            hist[pixel] += 1

    return hist


# -----------------------------
# Mencari intensitas minimal dan maksimal secara manual
# -----------------------------
def find_min_max(image):

    min_val = 255
    max_val = 0

    for y in range(height):
        for x in range(width):

            pixel = image[y][x]

            if pixel < min_val:
                min_val = pixel

            if pixel > max_val:
                max_val = pixel

    return min_val, max_val


# -----------------------------
# Normalisasi histogram
# -----------------------------
def histogram_normalization(image):

    min_val, max_val = find_min_max(image)

    result = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):

            pixel = image[y][x]

            new_pixel = (pixel - min_val) / (max_val - min_val) * 255

            result[y][x] = int(new_pixel)

    return result


# -----------------------------
# Histogram Equalization
# -----------------------------
def histogram_equalization(image):

    hist = compute_histogram(image)

    total_pixels = height * width

    # PDF
    pdf = [0] * 256
    for i in range(256):
        pdf[i] = hist[i] / total_pixels


    # CDF
    cdf = [0] * 256
    cumulative = 0

    for i in range(256):
        cumulative += pdf[i]
        cdf[i] = cumulative


    # Mapping
    mapping = [0] * 256

    for i in range(256):
        mapping[i] = int(255 * cdf[i])


    # Apply mapping
    result = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):

            pixel = image[y][x]
            result[y][x] = mapping[pixel]

    return result


# -----------------------------
# Memproses citra
# -----------------------------
normalized = histogram_normalization(img_array)
equalized = histogram_equalization(img_array)


# -----------------------------
# Histograms
# -----------------------------
hist_before = compute_histogram(img_array)
hist_after_norm = compute_histogram(normalized)
hist_after_eq = compute_histogram(equalized)


# -----------------------------
# Menampilkan citra
# -----------------------------
plt.figure(figsize=(12,4))

plt.subplot(1,3,1)
plt.title("Original")
plt.imshow(img_array, cmap="gray")

plt.subplot(1,3,2)
plt.title("Setelah di Normalisasi")
plt.imshow(normalized, cmap="gray")

plt.subplot(1,3,3)
plt.title("Setelah di Equalisasi")
plt.imshow(equalized, cmap="gray")

plt.show()


# -----------------------------
# Menampilkan histogram
# -----------------------------
plt.figure(figsize=(12,4))

plt.subplot(1,3,1)
plt.title("Histogram sebelumnya")
plt.bar(range(256), hist_before)

plt.subplot(1,3,2)
plt.title("Setelah normalisasi")
plt.bar(range(256), hist_after_norm)

plt.subplot(1,3,3)
plt.title("Setelah equalisasi")
plt.bar(range(256), hist_after_eq)

plt.show()