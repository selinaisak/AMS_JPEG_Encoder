import sys

from PIL import Image, UnidentifiedImageError
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from ChromaSubsampler import ChromaSubsampler
from ColorSpaceConverter import ColorSpaceConverter
from BlockSplitter import BlockSplitter

# This is a basic JPEG encoder

SRC_IMAGE_DIR = Path('./pre_jpeg')
INTER_IMAGE_DIR = Path('./intermediate')
OUT_IMAGE_DIR = Path('./post_jpeg')


def show_blocks(blocks, output_file, title):
    n_v, n_h, b_h, b_w = blocks.shape
    fig, axes = plt.subplots(n_v, n_h, figsize=(n_h, n_v))

    for i in range(n_v):
        for j in range(n_h):
            # Use vmin/vmax to scale all blocks across 0-255 (lowest value of all --> map
            # to 0, highest value of all -> map to white, everything else in relation!
            # IF THIS IS OMITTED: The 0-255 scale will be applied for EACH BLOCK -->
            # contrast seems extremely high, as 0/255 is assigned to the lowest/highest value
            # PER BLOCK!
            axes[i, j].imshow(blocks[i, j], cmap="gray", vmin=0, vmax=255)
            axes[i, j].axis("off")

    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Saved blocking preview to '{output_file}'")


def save_subsample_plot(Y, Cb, Cr, Cb_up, Cr_up, output_file):
    """
    Saves a matplotlib figure showing Y, subsampled Cb/Cr, upsampled Cb/Cr
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    axes[0, 0].imshow(Y, cmap="gray")
    axes[0, 0].set_title("Y (Luma)")
    axes[0, 0].axis("off")

    axes[0, 1].imshow(Cb, cmap="gray")
    axes[0, 1].set_title("Cb (Subsampled)")
    axes[0, 1].axis("off")

    axes[0, 2].imshow(Cr, cmap="gray")
    axes[0, 2].set_title("Cr (Subsampled)")
    axes[0, 2].axis("off")

    axes[1, 0].imshow(Y, cmap="gray")
    axes[1, 0].set_title("Y (Luma)")
    axes[1, 0].axis("off")

    axes[1, 1].imshow(Cb_up, cmap="gray")
    axes[1, 1].set_title("Cb (Upsampled)")
    axes[1, 1].axis("off")

    axes[1, 2].imshow(Cr_up, cmap="gray")
    axes[1, 2].set_title("Cr (Upsampled)")
    axes[1, 2].axis("off")

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Saved subsampling preview to '{output_file}'")

# Fetch all images for JPEG encoding
def get_images():
    images = []
    for filename in SRC_IMAGE_DIR.iterdir():
        # Skip iteration if it is not a 'regular' file
        if not filename.is_file():
            continue
        # Else treat as image
        try:
            # Check if image --> only then append to list
            with Image.open(filename) as image:
                image.verify()
                print(f"opened image {image.filename}")
                images.append(Image.open(filename) )

        # Print error if not image or other problem
        except (UnidentifiedImageError, FileNotFoundError) as e:
            print(e)
    return images

# Save the resulting image at path
def save_image(image: Image.Image, path: Path):
    image.save(path)


###### GENERAL STEPS OF A JPEG ENCODER ######
if __name__ == '__main__':
    # Fetch all images
    images = get_images()

    for image in images:
        # Color space conversion RGB --> YCbCr
        converter = ColorSpaceConverter('RGB', 'YCbCr')
        converted = converter.convert(image)
        # Check whether color space conversion worked
        print(converted.mode)

        # Chroma subsampling (4:2:0)
        subsampler = ChromaSubsampler(converted,4,2,0)
        Y, Cb, Cr = subsampler.subsample()

        # Test subsampling effect via upsampling
        Y_up, Cb_up, Cr_up = subsampler.upsample(Y, Cb, Cr)
        #print("Y :", Y_up.shape)
        #print("Cb:", Cb_up.shape)
        #print("Cr:", Cr_up.shape)
        img = Image.merge(
            "YCbCr",
            (
                Image.fromarray(Y_up),
                Image.fromarray(Cb_up),
                Image.fromarray(Cr_up),
            ),
        )
        back_converter = ColorSpaceConverter('YCbCr', 'RGB')
        img = back_converter.convert(img)
        img.save(INTER_IMAGE_DIR / f"subsampled_{Path(image.filename).name}")
        #save_subsample_plot(Y, Cb, Cr, Cb_up, Cr_up, INTER_IMAGE_DIR / f"sampled_{Path(image.filename).name}")


        # Block preparation/splitting (8x8)
        splitter = BlockSplitter(8)
        np.set_printoptions(threshold=sys.maxsize)
        Y_blocks, Cb_blocks, Cr_blocks = splitter.split_all_channels(Y, Cb, Cr)
        print(Y_blocks.shape)
        print(Cb_blocks.shape)
        print(Cr_blocks.shape)
        show_blocks(Y_blocks[:10, :10], INTER_IMAGE_DIR / f"blocked_Y_{Path(image.filename).name}", "Y Blocks")
        show_blocks(Cb_blocks[:10, :10], INTER_IMAGE_DIR / f"blocked_Cb_{Path(image.filename).name}", "Cb Blocks")
        show_blocks(Cr_blocks[:10, :10], INTER_IMAGE_DIR / f"blocked_Cr_{Path(image.filename).name}", "Cr Blocks")




        # Shift pixel value range [0, 255] → [-128, 127] (for DCT)
        # Direct Cosine Transform (DCT)
        # Quantization (quantization table/matrix!)
        # Zigzag scan/ordering
        # Differential encoding (DC)
        # Run-length Encoding (AC)
        # Huffman Encoding (Huffman tables!)
        # Frame builder --> construct/display JPEG encoded image!

        # Save image to output directory --> add appropriate extension (.jpeg)
        # --> also reuse original file name (get it via Path)
        out_path = (OUT_IMAGE_DIR / Path(image.filename).name).with_suffix(".jpg")
        save_image(converted, out_path)

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/