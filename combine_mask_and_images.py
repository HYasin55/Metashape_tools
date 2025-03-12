"""
Combining the mask with image and saving to as new file
H. Yasin Ozturk - March 2025
"""

import Metashape, os
import numpy as np

def get_directory_only(full_path, image_name):
    """
    Extracts the directory path from a full file path, ensuring the image_name is part of the filename.

    Args:
        full_path (str): The full path to the file.
        image_name (str): The name of the image to check in the file path.

    Returns:
        str: The directory path if image_name is in the filename, otherwise returns the full path.
    """
    directory = os.path.dirname(full_path)
    if image_name in os.path.basename(full_path):
        return directory
    return full_path

def combine_mask_and_images (metashape_image, metashape_mask):
    """
    Combines an image with its corresponding mask by applying the mask to the image.

    Args:
        metashape_image (Metashape.Image): The image to which the mask will be applied.
        metashape_mask (Metashape.Mask): The mask to apply to the image.

    Returns:
        Metashape.Image: The resulting image after applying the mask.
    """
    image_array = np.fromstring(metashape_image.tostring(), dtype=np.uint8)
    mask_image = metashape_mask.image()
    mask_array = np.fromstring(mask_image.tostring(), dtype=np.uint8)
    mask_array_rgb = np.repeat(mask_array, 3)
    image_array[mask_array_rgb ==0] = 0

    masked_image = Metashape.Image.fromstring(image_array, metashape_image.width, metashape_image.height, 'RGB', datatype='U8')
    return masked_image

def save_and_get_new_path_masked_image(masked_image, original_name, original_path):
    """
    Saves the masked image to a new directory and returns the new file path.

    Args:
        masked_image (Metashape.Image): The masked image to save.
        original_name (str): The name of the original image.
        original_path (str): The full path to the original image.

    Returns:
        str: The path to the saved masked image.
    """
    directory = get_directory_only(original_path, original_name)
    new_folder = directory + "/images_combined_with_masks"
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    new_directory = new_folder + '/masked_' + original_name + '.jpg'
    masked_image.save(new_directory)
    return new_directory

doc = Metashape.app.document
chunk = doc.chunk

camera_index = []
camera_labels = []
camera_path = []

for index, camera in enumerate(chunk.cameras):
    if camera.enabled:
        camera_index.append(index)
        camera_labels.append(camera.label)
        camera_path.append(camera.photo.path)

INDEX = 0 

camera = chunk.cameras[INDEX]
image = camera.image()
mask = camera.mask

masked_image = combine_mask_and_images(image, mask)

image_directory = save_and_get_new_path_masked_image(masked_image, camera_labels[INDEX], camera_path[INDEX])
print(image_directory)