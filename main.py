from PIL import Image, UnidentifiedImageError
from pathlib import Path
# This is a basic JPEG encoder

SRC_IMAGE_DIR = Path('./pre_jpeg')

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.

def get_images():
    images = []
    for filename in SRC_IMAGE_DIR.iterdir():
        # skip iteration if it is not a 'regular' file
        if not filename.is_file():
            continue
        # else treat as image
        try:
            # check if image --> only then append to list
            with Image.open(filename) as image:
                image.verify()
                print(f"opened image {image.filename}")
                images.append(image)

        # print error if not image or other problem
        except (UnidentifiedImageError, FileNotFoundError) as e:
            print(e)
    return images

###### GENERAL STEPS OF A JPEG ENCODER ######
if __name__ == '__main__':
    images = get_images()


    # Color space conversion RGB --> YCbCr
    # Chroma subsampling (4:2:0)
    # Block preparation/splitting (8x8)
    # Shift pixel value range [0, 255] → [-128, 127] (for DCT)
    # Direct Cosine Transform (DCT)
    # Quantization (quantization table/matrix!)
    # Zigzag scan/ordering
    # Differential encoding (DC)
    # Run-length Encoding (AC)
    # Huffman Encoding (Huffman tables!)
    # Frame builder --> construct/display JPEG encoded image!


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
