#!C:\Users\manas\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe
#!/usr/bin/env python

import numpy as np
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from PIL import Image
from skimage import io, color, morphology
import cv2
import numpy as np
import matplotlib.pyplot as plt
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import load_model
from skimage import io, color, morphology
import json
from keras.models import model_from_json
import sys




def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_shadows(image):
    rgb_planes = cv2.split(image)
    result_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(norm_img)
    result = cv2.merge(result_planes)
    return result

def binarize_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return binary

def remove_noise(binary_image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    cleaned = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel, iterations=1)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel, iterations=1)
    return cleaned
    
def remove_lines(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (image.shape[1] // 30, 1))
    lines = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=2)
    cleaned = image - lines
    return cleaned
    
def correct_skew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return corrected

def skeletonize(image):
   # Convert to boolean
    binary_bool = image > 0
    skeleton = morphology.skeletonize(binary_bool)
    # Convert back to uint8
    skeleton_uint8 = (skeleton * 255).astype(np.uint8)
    return skeleton_uint8

def final_noise_filter(binary_image):
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_image, connectivity=8)
    sizes = stats[1:, -1]
    filtered = np.zeros((labels.shape), np.uint8)
    for i in range(1, num_labels):
        if sizes[i - 1] >= 100:
            filtered[labels == i] = 255
    return filtered
"""
def preprocess_image(binary_image, noise_removal_flag=False, skew_correction_flag=False, remove_lines_flag=False, skeletonization_flag=False):
    images = []
    images.append(("Original", image))
    
    
    
    no_shadows = remove_shadows(image)  # Pass the original image instead of the grayscale one
    images.append(("No Shadows", no_shadows))
    
    binary = binarize_image(no_shadows)
    images.append(("Binarized", binary))
    
    cleaned = (binary)
    images.append(("Noise Removed", cleaned))
    
    if remove_lines_flag:
        line_removed = remove_lines(cleaned)
        images.append(("Lines Removed", line_removed))
    else:
        line_removed = cleaned
    
    
    skew_corrected = correct_skew(line_removed)
    images.append(("Skew Corrected", skew_corrected))



    if skeletonization_flag==True:
        final_image = skeletonize(skew_corrected)
        images.append(("Skeletonized", final_image))
    else:
        final_image = line_removed
    
    final_cleaned = final_noise_filter(final_image)
    images.append(("Final Noise Filtered", final_cleaned))
#     plt.imshow(final_cleaned)
    return final_cleaned,images
"""


def preprocess_image(image, remove_shadows_flag=False, noise_removal_flag=False, skew_correction_flag=False, remove_lines_flag=False, skeletonization_flag=False):
    images = []
    images.append(("Original", image))
    
    if remove_shadows_flag:
        no_shadows = remove_shadows(image)  # Pass the original image instead of the grayscale one
        images.append(("No Shadows", no_shadows))
    else:
        no_shadows = image
    
    binary = binarize_image(no_shadows)
    images.append(("Binarized", binary))
    
    if noise_removal_flag:
        cleaned = remove_noise(binary)
        images.append(("Noise Removed", cleaned))
    else:
        cleaned = binary
    
    if remove_lines_flag:
        line_removed = remove_lines(cleaned)
        images.append(("Lines Removed", line_removed))
    else:
        line_removed = cleaned
    
    if skew_correction_flag:
        skew_corrected = correct_skew(line_removed)
        images.append(("Skew Corrected", skew_corrected))
    else:
        skew_corrected = line_removed
    
    if skeletonization_flag:
        skeleton_image = skeletonize(skew_corrected)
        images.append(("Skeletonized", final_image))
    else:
        skeleton_image = skew_corrected
        
    if remove_shadows_flag or noise_removal_flag or remove_lines_flag:
        final_image = final_noise_filter(skeleton_image)
        images.append(("Final Noise Filtered", final_image))
    else:
        final_image= skeleton_image
        
    #final_image=final_noise_filter(final_image)
    
    return final_image




def line_segmentation(binary_image):
    horizontal_sum = np.sum(binary_image, axis=1)
    lines = []
    start_idx = None
    for i in range(len(horizontal_sum)):
        if horizontal_sum[i] > 0 and start_idx is None:
            start_idx = i
        elif horizontal_sum[i] == 0 and start_idx is not None:
            lines.append((start_idx, i))
            start_idx = None
    if start_idx is not None:
        lines.append((start_idx, len(horizontal_sum)))
    return lines

def word_segmentation(binary_image, line_coords, max_gap_between_digits):
    words = []
    
    for (start, end) in line_coords:
        line_image = binary_image[start:end, :]
        vertical_sum = np.sum(line_image, axis=0)
        
        in_word = False
        word_start = None
        for j in range(len(vertical_sum)):
            if vertical_sum[j] > 0 and not in_word:
                in_word = True
                word_start = j
            elif vertical_sum[j] == 0 and in_word:
                if j - word_start > max_gap_between_digits:
                    words.append((start, end, word_start, j))
                    in_word = False
        
        # If the line ends while inside a word, add the current word
        if in_word:
            words.append((start, end, word_start, len(vertical_sum)))
    
    return words

def character_segmentation(binary_image, word_coords):
    characters = []
    
    for (line_start, line_end, word_start, word_end) in word_coords:
        word_image = binary_image[line_start:line_end, word_start:word_end]
        vertical_sum = np.sum(word_image, axis=0)
        
        char_start = None
        for k in range(len(vertical_sum)):
            if vertical_sum[k] > 0 and char_start is None:
                char_start = k
            elif vertical_sum[k] == 0 and char_start is not None:
                characters.append((line_start, line_end, word_start + char_start, word_start + k))
                char_start = None
        
        if char_start is not None:
            characters.append((line_start, line_end, word_start + char_start, word_end))
    
    return characters



#-------------------------

def word_segmentation_line(line_image, max_gap_between_digits=100):
    vertical_sum = np.sum(line_image, axis=0)
    words = []
    
    in_word = False
    word_start = None
    for j in range(len(vertical_sum)):
        if vertical_sum[j] > 0 and not in_word:
            in_word = True
            word_start = j
        elif vertical_sum[j] == 0 and in_word:
            if j - word_start > max_gap_between_digits:
                words.append((0, line_image.shape[0], word_start, j))
                in_word = False
    
    if in_word:
        words.append((0, line_image.shape[0], word_start, len(vertical_sum)))
    
    return words

def character_segmentation_line(line_image, word_coords):
    characters = []
    
    for (line_start, line_end, word_start, word_end) in word_coords:
        word_image = line_image[line_start:line_end, word_start:word_end]
        vertical_sum = np.sum(word_image, axis=0)
        
        char_start = None
        for k in range(len(vertical_sum)):
            if vertical_sum[k] > 0 and char_start is None:
                char_start = k
            elif vertical_sum[k] == 0 and char_start is not None:
                characters.append((0, line_end - line_start, word_start + char_start, word_start + k))
                char_start = None
        
        if char_start is not None:
            characters.append((0, line_end - line_start, word_start + char_start, word_end))
    
    return characters
#-------------------------
'''
def crop_and_resize_characters(image, char_coords_per_line, target_size=(28, 28), padding=3):
    char_images = []
    target_height, target_width = target_size
    
    for characters in char_coords_per_line:
        for (_, _, c_start, c_end) in characters:
            char_image = image[:, c_start:c_end]

            # Calculate the current size of the character image
            current_height, current_width = char_image.shape

            if current_height > target_height or current_width > target_width:
                # Resize the image to fit within the target size while maintaining aspect ratio
                scaling_factor = min(target_height / current_height, target_width / current_width)
                new_size = (int(current_width * scaling_factor), int(current_height * scaling_factor))
                char_image_resized = cv2.resize(char_image, new_size, interpolation=cv2.INTER_AREA)

                # Calculate the padding needed to reach the target size
                pad_top = (target_height - new_size[1]) // 2
                pad_bottom = target_height - new_size[1] - pad_top
                pad_left = (target_width - new_size[0]) // 2
                pad_right = target_width - new_size[0] - pad_left
            else:
                # Calculate the padding needed to reach the target size
                pad_top = (target_height - current_height) // 2
                pad_bottom = target_height - current_height - pad_top
                pad_left = (target_width - current_width) // 2
                pad_right = target_width - current_width - pad_left

            # Add padding to the original image
            char_image_resized = char_image

            # Add the calculated padding
            char_image_resized = cv2.copyMakeBorder(char_image_resized, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

            char_images.append(char_image_resized)
    
    return char_images
'''



def crop_and_resize_characters(image, char_coords_per_line, target_size=(28, 28), padding=3):
    char_images = []
    target_height, target_width = target_size
    k=[]
    v=[]
    for characters in char_coords_per_line:
        for (_, _, c_start, c_end) in characters:
            char_image = image[:, c_start:c_end]

            # Calculate the current size of the character image
            current_height, current_width = char_image.shape
            v.append(char_image.shape)
#             print("original size (h,w)",char_image.shape)
            if current_height > target_height or current_width > target_width:
                # Resize the image to fit within the target size while maintaining aspect ratio
                scaling_factor = min(target_height / current_height, target_width / current_width)
                new_size = (int(current_width * scaling_factor), int(current_height * scaling_factor))
                char_image = cv2.resize(char_image, new_size, interpolation=cv2.INTER_AREA)
#                 print("new_size (h,w)",new_size)
                # Calculate the padding needed to reach the target size
                pad_top = (target_height - new_size[1]) // 2
                pad_bottom = target_height - new_size[1] - pad_top
                pad_left = (target_width - new_size[0]) // 2
                pad_right = target_width - new_size[0] - pad_left
                
#                 print("larger")
                
            else:
                # Calculate the padding needed to reach the target size
                pad_top = (target_height - current_height) // 2
                pad_bottom = target_height - current_height - pad_top
                pad_left = (target_width - current_width) // 2
                pad_right = target_width - current_width - pad_left
#                 print("smaller")
            # Add padding to the original image
#             char_image_resized = char_image

            # Add the calculated padding
            char_image_resized = cv2.copyMakeBorder(char_image, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

            char_images.append(char_image_resized)
#             print("top", pad_top,"bottom",pad_bottom,"left",pad_left,"right",pad_right)
#             print("final size",char_image_resized.shape)
            k.append(char_image_resized.shape)
#     print("original size",v)
#     print("final size",k)
    
    return char_images



def predict_characters(char_images, model):
    # Normalize and reshape the character images
    char_images = np.array(char_images).reshape((-1, 28, 28, 1)).astype('float32') / 255.0
    
    # Get predictions from the model
    predictions = model.predict(char_images,verbose= 0)
    
    # Get the predicted digits using argmax
    predicted_digits = np.argmax(predictions, axis=1)
    
    # Create a list to store the predicted digits and their max values
    predicted_with_confidence = []
    
    # Iterate over the predictions and predicted digits
    for digit, prediction in zip(predicted_digits, predictions):
        max_value = np.max(prediction)
        predicted_with_confidence.append([digit, max_value])
#         print(f"Predicted digit: {digit}, Confidence: {max_value}")
    
    return predicted_digits, predicted_with_confidence


def plot_segmentations(image, lines, word_coords_per_line, char_coords_per_line):
    fig, axs = plt.subplots(len(lines), 1, figsize=(15, 3 * len(lines)))
    
    if len(lines) == 1:
        axs = [axs]
    
    for idx, (start, end) in enumerate(lines):
        strip = image[start:end, :]
        line_image = cv2.cvtColor(strip, cv2.COLOR_GRAY2BGR)
        
        for (_, _, w_start, w_end) in word_coords_per_line[idx]:
            cv2.rectangle(line_image, (w_start, 0), (w_end, end - start), (255, 0, 0), 2)
        
        for (_, _, c_start, c_end) in char_coords_per_line[idx]:
            cv2.rectangle(line_image, (c_start, 0), (c_end, end - start), (0, 0, 255), 2)
        
        axs[idx].imshow(line_image)
        axs[idx].set_title(f"Line {idx + 1}")
        axs[idx].axis('off')
    
    plt.show()


def plot_char_images_per_line(char_images_per_line):
    for line_idx, char_images in enumerate(char_images_per_line):
        num_images = len(char_images)
        num_cols = 10
        num_rows = (num_images // num_cols) + (1 if num_images % num_cols != 0 else 0)

        plt.figure(figsize=(15, 3 * num_rows))
        for i in range(num_images):
            plt.subplot(num_rows, num_cols, i + 1)
            plt.imshow(char_images[i], cmap='gray')
            plt.axis('off')
        plt.suptitle(f"Line {line_idx + 1}")
        plt.show()    

        
def plot_char_images_with_predictions(char_images, preds):
    num_images = len(char_images)

    plt.figure(figsize=(2, 2 * num_images))
    for i in range(num_images):
        # Plot character image
        plt.subplot(num_images, 2, 2 * i + 1)
        plt.imshow(char_images[i], cmap='gray')
        plt.axis('off')
        
        # Plot predicted digit
        plt.subplot(num_images, 2, 2 * i + 2)
        plt.text(1, 0.5, str(preds[i]), fontsize=12, ha='center', va='center')
        plt.axis('off')
        
    plt.show()        
        
        

def segment_image(image):
    #image = cv2.imread(image_path)
    #binary_image = binarize_image(image)
    #image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    #binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)[1]
    
    
    
    line_coords = line_segmentation(image)
    word_coords = word_segmentation(image, line_coords, max_gap_between_digits=100)
    char_coords = character_segmentation(image, word_coords)

    return line_coords, word_coords, char_coords

def segment_image_relative_to_lines(image):
    # Load and process the image
#     image_path = r"C:\Users\manas\UoM\Project\Code\Raw Testing\stacked_image_0_invert.png"

    #image = cv2.imread(image_path)
    #binary_image = binarize_image(image)
    #image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    #binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)[1]

    
    
    # Segment lines
    line_coords = line_segmentation(image)

    # Segment words and characters per line
    word_coords_per_line = []
    char_coords_per_line = []
    for (start, end) in line_coords:
        strip = image[start:end, :]
        words = word_segmentation_line(strip)
        word_coords_per_line.append(words)

        chars = character_segmentation_line(strip, words)
        char_coords_per_line.append(chars)
        
    return line_coords, word_coords_per_line, char_coords_per_line


def calculate_original_image_coords(predicted_digits, coords):
    original_results = []
    char_index = 0  # Index to track character position in original_image char_coords
    original_char_coords = coords['original_image']['char_coords']

    for digits in predicted_digits:
#         print("digits:",digits)
        for digit in digits:
            if char_index >= len(original_char_coords):
                raise IndexError("Character index out of range for original_image coordinates.")
                
            # For original_image, get the combined character coordinates
            orig_char_coords = original_char_coords[char_index]
            orig_char_start, orig_char_end = orig_char_coords[2], orig_char_coords[3]
            orig_left = orig_char_start
            orig_top = orig_char_coords[0]
            orig_width = orig_char_end - orig_char_start
            orig_height = orig_char_coords[1] - orig_char_coords[0]

            original_results.append({
                "left": orig_left,
                "top": orig_top,
                "width": orig_width,
                "height": orig_height,
                "digit": str(digit)
            })

            char_index += 1

    return original_results

def calculate_relative_to_lines_coords(predicted_digits, coords):
    relative_results_per_line = []
    relative_results_per_line_list=[]
    relative_line_coords = coords['relative_to_lines']['line_coords']
    relative_char_coords = coords['relative_to_lines']['char_coords']

    for line_num, digits in enumerate(predicted_digits):
        if line_num >= len(relative_char_coords):
            raise IndexError("Line number out of range for relative_to_lines coordinates.")
        
        line_start, line_end = relative_line_coords[line_num]
        line_results = []
        line_results_list=[]
        
        for char_index, digit in enumerate(digits):
            if char_index >= len(relative_char_coords[line_num]):
                raise IndexError("Character index out of range for relative_to_lines coordinates.")
                
            # Get the relative character coordinates
            rel_char_coords = relative_char_coords[line_num][char_index]
            char_start, char_end = rel_char_coords[2], rel_char_coords[3]
            left = char_start
            top = line_start
            width = char_end - char_start
            height = line_end - line_start

            line_results.append({
                "left": left,
                "top": top,
                "width": width,
                "height": height,
                "digit": str(digit)
            })
            
            
            line_results_list.append([left,top,width,height])

        relative_results_per_line.append(line_results)
        relative_results_per_line_list.append(line_results_list)
        
    return relative_results_per_line, relative_results_per_line_list



if __name__ == "__main__":
    image_path = sys.argv[1]
    options_json = (sys.argv[2])
    #print("options_json",options_json)
    options_json = options_json.replace("[", "")
    options_json = options_json.replace("]", "")
    options_json=options_json.split(",")

    #for i in options_json:
    #  print(i)
    remove_shadows_flag= eval(options_json[0])
    noise_removal_flag=eval(options_json[1])
    skew_correction_flag=eval(options_json[2])
    remove_lines_flag=eval(options_json[3])
    skeletonization_flag=eval(options_json[4])
    #print("hi")
    #print("flag", (noise_removal_flag))
    image = cv2.imread(image_path)
    binary_image = binarize_image(image)
    
    final_image = preprocess_image(image, remove_shadows_flag, noise_removal_flag, skew_correction_flag, remove_lines_flag, skeletonization_flag)
    
    #print((p))
    
    # Get coordinates relative to the original image
    line_coords, word_coords_per_line, char_coords_per_line = segment_image(final_image)

    # Get coordinates relative to each line/row
    rel_line_coords, rel_word_coords_per_line, rel_char_coords_per_line = segment_image_relative_to_lines(final_image)
    
    
    # Plot segmentations
    #plot_segmentations(binary_image, rel_line_coords, rel_word_coords_per_line, rel_char_coords_per_line)

    # Crop and resize characters per line
    char_images_per_line = []
    for (start, end), char_coords in zip(rel_line_coords, rel_char_coords_per_line):
        strip = final_image[start:end, :]
        char_images = crop_and_resize_characters(strip, [char_coords], target_size=(28, 28))
        char_images_per_line.append(char_images)
        
    # Plot character images per line
    #plot_char_images_per_line(char_images_per_line)
    
    
    coordinates = {
        "original_image": {
            "line_coords": line_coords,
            "word_coords": word_coords_per_line,
            "char_coords": char_coords_per_line
        },
        "relative_to_lines": {
            "line_coords": rel_line_coords,
            "word_coords": rel_word_coords_per_line,
            "char_coords": rel_char_coords_per_line
        }
    }
      #print(output)     
    
    # load json and create model
    json_file = open(r'C:\Users\manas\UoM\Project\Code\Model\model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights(r"C:\Users\manas\UoM\Project\Code\Model\model.h5")    
    
    all_predictions = []
    # Predict characters
    for i in char_images_per_line:
        predicted_digits, preds = predict_characters(i, model)
        all_predictions.append(list(predicted_digits))
         #print("Predicted Digits: ", predicted_digits)
         #print(preds)
         #plot_char_images_with_predictions(i, predicted_digits)    
    

    original_results = calculate_original_image_coords(all_predictions, coordinates)

    relative_results_per_line, relative_results_per_line_list = calculate_relative_to_lines_coords(all_predictions, coordinates)


    results = {
        "original_image": (original_results),
        "relative_to_lines": (relative_results_per_line),
        "line_coords":(line_coords),
        "relative_results_per_line_list": (relative_results_per_line_list)
    }
    #print("results",results, "\njson results", json.dumps(results))
    
    print(json.dumps(results))    
