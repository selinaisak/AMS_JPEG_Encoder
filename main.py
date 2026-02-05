import sys

from PIL import Image, UnidentifiedImageError
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from ChromaSubsampler import ChromaSubsampler
from ColorSpaceConverter import ColorSpaceConverter
from BlockSplitter import BlockSplitter
from LevelShifter import LevelShifter
from DiscreteCosineTransformer import DCT_2D, IDCT_2D
from Quantizer import Quantizer
from Helper import show_blocks, save_subsample_plot, get_images, save_image

# This is a basic JPEG encoder

SRC_IMAGE_DIR = Path('./pre_jpeg')
INTER_IMAGE_DIR = Path('./intermediate')
OUT_IMAGE_DIR = Path('./post_jpeg')

###### GENERAL STEPS OF A JPEG ENCODER ######
if __name__ == '__main__':
    # Use this for debugging/viewing purposes
    np.set_printoptions(threshold=sys.maxsize)

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
        img.save(INTER_IMAGE_DIR / "subsampling" / f"subsampled_{Path(image.filename).name}")
        save_subsample_plot(Y, Cb, Cr, Cb_up, Cr_up, INTER_IMAGE_DIR /  "subsampling" / f"sampled_{Path(image.filename).name}")


        # Block preparation/splitting (8x8)
        splitter = BlockSplitter(8)
        Y_blocks, Cb_blocks, Cr_blocks = splitter.split_all_channels(Y, Cb, Cr)
        print(Y_blocks.shape)
        print(Cb_blocks.shape)
        print(Cr_blocks.shape)
        show_blocks(Y_blocks[:10, :10], INTER_IMAGE_DIR / "blocking" / f"Y_{Path(image.filename).name}", "Y Blocks", 0, 255)
        show_blocks(Cb_blocks[:10, :10], INTER_IMAGE_DIR / "blocking" / f"Cb_{Path(image.filename).name}", "Cb Blocks", 0, 255)
        show_blocks(Cr_blocks[:10, :10], INTER_IMAGE_DIR / "blocking" / f"Cr_{Path(image.filename).name}", "Cr Blocks", 0, 255)

        # Shift pixel value range [0, 255] → [-128, 127] (for DCT)
        shifter = LevelShifter(128)
        Y_blocks, Cb_blocks, Cr_blocks = shifter.shift(Y_blocks, Cb_blocks, Cr_blocks)
        show_blocks(Y_blocks[:10, :10], INTER_IMAGE_DIR / "shifting" / f"Y_{Path(image.filename).name}", "Y Blocks Shifted", -128, 127)
        show_blocks(Cb_blocks[:10, :10], INTER_IMAGE_DIR / "shifting" / f"Cb_{Path(image.filename).name}", "Cb Blocks Shifted", -128, 127 )
        show_blocks(Cr_blocks[:10, :10], INTER_IMAGE_DIR / "shifting" / f"Cr_{Path(image.filename).name}", "Cr Blocks Shifted", -128, 127 )

        # Discrete Cosine Transform (DCT)
        Y_blocks, Cb_blocks, Cr_blocks = DCT_2D(Y_blocks, Cb_blocks, Cr_blocks)
        show_blocks(Y_blocks[:10, :10], INTER_IMAGE_DIR / "dct" / f"Y_{Path(image.filename).name}", "Y Blocks after DCT")
        show_blocks(Cb_blocks[:10, :10], INTER_IMAGE_DIR / "dct" / f"Cb_{Path(image.filename).name}", "Cb Blocks after DCT")
        show_blocks(Cr_blocks[:10, :10], INTER_IMAGE_DIR / "dct" / f"Cr_{Path(image.filename).name}", "Cr Blocks after DCT")

        # Inverse Discrete Cosine Transform (DCT) ONLY FOR VERIFICATION PURPOSES!!!
        I_Y_blocks, I_Cb_blocks, I_Cr_blocks = IDCT_2D(Y_blocks, Cb_blocks, Cr_blocks)
        show_blocks(I_Y_blocks[:10, :10], INTER_IMAGE_DIR / "idct" / f"Y_{Path(image.filename).name}",
                    "Y Blocks after IDCT", -128, 127)
        show_blocks(I_Cb_blocks[:10, :10], INTER_IMAGE_DIR / "idct" / f"Cb_{Path(image.filename).name}",
                    "Cb Blocks after IDCT", -128, 127)
        show_blocks(I_Cr_blocks[:10, :10], INTER_IMAGE_DIR / "idct" / f"Cr_{Path(image.filename).name}",
                    "Cr Blocks after IDCT", -128, 127)

        # Quantization (quantization table/matrix!)
        quantizer = Quantizer(50) # use base quality factor of 50
        Y_blocks, Cb_blocks, Cr_blocks = quantizer.quantize_blocks(Y_blocks, Cb_blocks, Cr_blocks)
        show_blocks(Y_blocks[:10, :10], INTER_IMAGE_DIR / "quantization" / f"Y_{Path(image.filename).name}",
                    "Y Blocks after Quantization")
        show_blocks(Cb_blocks[:10, :10], INTER_IMAGE_DIR / "quantization" / f"Cb_{Path(image.filename).name}",
                    "Cb Blocks after Quantization")
        show_blocks(Cr_blocks[:10, :10], INTER_IMAGE_DIR / "quantization" / f"Cr_{Path(image.filename).name}",
                    "Cr Blocks after Quantization")

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