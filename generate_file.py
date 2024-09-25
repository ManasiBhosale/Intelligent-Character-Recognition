#!C:\Users\manas\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe
#!/usr/bin/env python

import sys
import json
import os
from fpdf import FPDF
import cv2


def generate_text_file(filename,  boxes):
    content = ""
    for box in boxes:
        content += f"{box[4]} at position ({box[0]}, {box[1]}) size ({box[2]}, {box[3]})\n"
    with open(filename, 'w') as file:
        file.write(content)
    return filename
    
    
"""  
    
def generate_text_file(image_filename, output_file, boxes):

    # Read the image to get its dimensions
    image = cv2.imread(image_filename)
    if image is None:
        raise ValueError(f"Image file {image_filename} not found or cannot be opened.")
    _, width = image.shape[:2]
    
    # Normalize the box coordinates
    #normalized_boxes = normalize_positions(boxes)
    normalized_boxes = (boxes)
    
    # Initialize a grid with empty spaces
    max_width = width
    grid = [' ' * max_width for _ in range(1)]  # single row grid for horizontal placement
    
    # Process each box
    for box in normalized_boxes:
        left, _, _, _, digit = box
        # Ensure digit fits within grid boundaries
        if 0 <= left < max_width:
            # Create a list from the string to manipulate specific characters
            row = list(grid[0])
            if left < len(row):  # Ensure we don't go out of bounds
                row[left] = str(digit)
            grid[0] = ''.join(row)
    
    # Write content to the file
    with open(output_file, 'w') as file:
        file.write(grid[0])
    
    return output_file

    
"""

def generate_pdf_file(filename, boxes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 14)
    for box in boxes:
        pdf.set_xy(box[0] / 8, box[1] / 8)  # Adjust scaling as needed
        pdf.cell(box[2], box[3], str(box[4]))
    pdf.output(filename)
    return filename
    
    
def normalize_positions(boxes):
    if not boxes:
        return []
    
    # Extract the coordinates of the first digit
    first_digit = boxes[0]
    first_left = first_digit[0]
    first_top = first_digit[1]
    
    # Normalize the positions
    normalized_boxes = []
    for box in boxes:
        normalized_box = [
            box[0] - first_left,  # left
            box[1] - first_top,    # top
            box[2],              # width
            box[3],             # height
            box[4]               # digit
        ]
        normalized_boxes.append(normalized_box)
    
    return normalized_boxes
   

def generate_hocr_file(output_file, boxes, lines):
    """
    Generate an HOCR file with digits and their positions.

    Args:
        output_file (str): The path to the output HOCR file.
        boxes (list of lists): Each box contains [left, top, width, height, digit].
        lines (list of lists): Each line contains [top, bottom] coordinates.
    """
    hocr_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
 <head>
  <title></title>
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
  <meta name='ocr-system' content='custom'/>
  <meta name='ocr-capabilities' content='ocr_page ocr_carea ocr_par ocr_line ocrx_word ocrp_wconf'/>
 </head>
 
 <body>
  <div class='ocr_page' id='page_1' title='image "image.png"; bbox 0 0 1000 1000; ppageno 0'>
   <div class='ocr_carea' id='block_1_1' title="bbox 0 0 1000 1000">
    <p class='ocr_par' id='par_1_1' lang='eng' title="bbox 0 0 1000 1000">
"""

    for line_id, (line_top, line_bottom) in enumerate(lines, start=1):
        line_boxes = [box for box in boxes if line_top <= box[1] < line_bottom]
        if line_boxes:
            line_left = min(box[0] for box in line_boxes)
            line_right = max(box[0] + box[2] for box in line_boxes)
            line_bbox = f"{line_left} {line_top} {line_right} {line_bottom}"
            hocr_content += f"""     <span class='ocr_line' id='line_1_{line_id}' title="bbox {line_bbox}; baseline 0 0">
"""

            for word_id, box in enumerate(line_boxes, start=1):
                left, top, width, height, digit = box
                word_bbox = f"{left} {top} {left + width} {top + height}"
                hocr_content += f"""      <span class='ocrx_word' id='word_1_{line_id}_{word_id}' title='bbox {word_bbox}; x_wconf 100'>{digit}</span>
"""
            hocr_content += "     </span>\n"

    hocr_content += """    </p>
   </div>
  </div>
 </body>
</html>
"""

    with open(output_file, 'w') as file:
        file.write(hocr_content)

    return output_file   
    

def main():
    if len(sys.argv) != 5:
        print("Usage: python generate_file.py <input_image> <output_format> <boxes>")
        sys.exit(1)
    
    #print("hi1")
    
    input_image = sys.argv[1]
    output_format = sys.argv[2]
    boxes = json.loads(sys.argv[3])
    lines = json.loads(sys.argv[4])
    
    #print(input_image)
    #print(output_format)
    #print(boxes)
    #print("lines", lines)
    
    output_dir = 'C:\\Users\\manas\\Downloads\\'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    base_name = os.path.splitext(os.path.basename(input_image))[0]
    if output_format == 'text':
        output_file = os.path.join(output_dir, f"{base_name}.txt")
        generate_text_file(output_file, boxes)
    elif output_format == 'pdf':
        output_file = os.path.join(output_dir, f"{base_name}.pdf")
        generate_pdf_file(output_file, boxes)
        
    elif output_format == 'hocr':
        output_file = os.path.join(output_dir, f"{base_name}.hocr")
#         output_file = 'output.hocr'
        generate_hocr_file(output_file, boxes, lines)
    else:
        print("Invalid output format")
        sys.exit(1)
    
    print(output_file)

if __name__ == "__main__":
    #print("hi")
    main()
