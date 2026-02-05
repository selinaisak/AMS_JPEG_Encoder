import sys

from PIL import Image, UnidentifiedImageError
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from ChromaSubsampler import ChromaSubsampler
from ColorSpaceConverter import ColorSpaceConverter
from BlockSplitter import BlockSplitter
from Helper import show_blocks, save_subsample_plot, get_images, save_image

# This is a basic JPEG encoder

SRC_IMAGE_DIR = Path('./pre_jpeg')
INTER_IMAGE_DIR = Path('./intermediate')
OUT_IMAGE_DIR = Path('./post_jpeg')

###### GENERAL STEPS OF A JPEG ENCODER ######
if __name__ == '__main__':
    # Fetch all images
    images = get_images(SRC_IMAGE_DIR)

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
        save_subsample_plot(Y, Cb, Cr, Cb_up, Cr_up, INTER_IMAGE_DIR / f"sampled_{Path(image.filename).name}")


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