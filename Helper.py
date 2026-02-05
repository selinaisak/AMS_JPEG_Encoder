from matplotlib import pyplot as plt
from PIL import Image, UnidentifiedImageError
from pathlib import Path

#
# This file only contains auxiliary functions --> prevent cluttering main method!
# It is mainly used for loading/displaying/saving purposes
#

# Fetch all images for JPEG encoding
def get_images(src_dir: Path):
    images = []
    for filename in src_dir.iterdir():
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

# Saves a matplotlib figure showing Y, subsampled Cb/Cr, upsampled Cb/Cr
def save_subsample_plot(Y, Cb, Cr, Cb_up, Cr_up, output_file):
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))

    axes[0, 0].imshow(Y, cmap="gray", vmin=0, vmax=255)
    axes[0, 0].set_title("Y (Luma)")
    axes[0, 0].axis("off")

    axes[0, 1].imshow(Cb, cmap="gray", vmin=0, vmax=255)
    axes[0, 1].set_title("Cb (Subsampled)")
    axes[0, 1].axis("off")

    axes[0, 2].imshow(Cr, cmap="gray", vmin=0, vmax=255)
    axes[0, 2].set_title("Cr (Subsampled)")
    axes[0, 2].axis("off")

    axes[1, 0].imshow(Y, cmap="gray", vmin=0, vmax=255)
    axes[1, 0].set_title("Y (Luma)")
    axes[1, 0].axis("off")

    axes[1, 1].imshow(Cb_up, cmap="gray", vmin=0, vmax=255)
    axes[1, 1].set_title("Cb (Upsampled)")
    axes[1, 1].axis("off")

    axes[1, 2].imshow(Cr_up, cmap="gray", vmin=0, vmax=255)
    axes[1, 2].set_title("Cr (Upsampled)")
    axes[1, 2].axis("off")

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Saved subsampling preview to '{output_file}'")

# Saves (a portion of) blocks and displays them in a figure
def show_blocks(blocks, output_file, min, max, title):
    num_vertical, num_horizontal, block_height, block_width = blocks.shape
    fig, axes = plt.subplots(num_vertical, num_horizontal, figsize=(num_horizontal, num_vertical))

    for i in range(num_vertical):
        for j in range(num_horizontal):
            # Use vmin/vmax to scale all blocks across min-max (0,255 before shift, -128,127 after level shift)
            # (lowest value of all --> map to black, highest value of all -> map to white), everything else in relation!
            # IF THIS IS OMITTED: The min-max scale will be applied for EACH BLOCK -->
            # contrast seems extremely high, as min/max is assigned to the lowest/highest value
            # PER BLOCK!
            axes[i, j].imshow(blocks[i, j], cmap="gray", vmin=min, vmax=max)
            axes[i, j].axis("off")

    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Saved blocking preview to '{output_file}'")