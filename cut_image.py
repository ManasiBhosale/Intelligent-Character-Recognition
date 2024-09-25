#!C:\Users\manas\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\python.exe
#!/usr/bin/env python



from PIL import Image, ImageDraw
import json
import base64
import io
import sys

def cut_image_into_rows(image_path, line_coords, box_coords):
    image = Image.open(image_path)
    rows = []

    for idx, coords in enumerate(line_coords):
        top, bottom = coords
        cropped_image = image.crop((0, top, image.width, bottom))
        
        # Draw boundary boxes on the cropped image
        draw = ImageDraw.Draw(cropped_image)
        for box in box_coords[idx]:
            """
            left = box['left']
            top = box['top']
            width = box['width']
            height = box['height']
            """
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            #draw.rectangle([left, top, left + width, top + height], outline="red", width=7)
            draw.rectangle([left -3, 0, left + width + 3, top + height], outline="red", width=1)
        # Convert the image to base64
        buffered = io.BytesIO()
        cropped_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        rows.append(img_str)
    #print("rows",rows)
    return rows

if __name__ == "__main__":
    image_path = sys.argv[1]
    #line_coords = [[254, 276], [280, 302], [307, 326]]
    #box_coords = [[{"left": 132, "top": 254, "width": 9, "height": 22, "digit": "6"}, {"left": 153, "top": 254, "width": 19, "height": 22, "digit": "0"}, {"left": 326, "top": 254, "width": 16, "height": 22, "digit": "0"}, {"left": 353, "top": 254, "width": 13, "height": 22, "digit": "5"}, {"left": 379, "top": 254, "width": 14, "height": 22, "digit": "8"}, {"left": 406, "top": 254, "width": 14, "height": 22, "digit": "5"}, {"left": 432, "top": 254, "width": 11, "height": 22, "digit": "7"}, {"left": 459, "top": 254, "width": 10, "height": 22, "digit": "9"}, {"left": 483, "top": 254, "width": 17, "height": 22, "digit": "6"}, {"left": 513, "top": 254, "width": 6, "height": 22, "digit": "1"}, {"left": 538, "top": 254, "width": 13, "height": 22, "digit": "6"}, {"left": 559, "top": 254, "width": 16, "height": 22, "digit": "7"}], [{"left": 91, "top": 280, "width": 11, "height": 22, "digit": "9"}, {"left": 115, "top": 280, "width": 15, "height": 22, "digit": "7"}, {"left": 142, "top": 280, "width": 15, "height": 22, "digit": "5"}, {"left": 169, "top": 280, "width": 12, "height": 22, "digit": "8"}, {"left": 198, "top": 280, "width": 9, "height": 22, "digit": "6"}, {"left": 446, "top": 280, "width": 14, "height": 22, "digit": "4"}], [{"left": 450, "top": 307, "width": 4, "height": 19, "digit": "1"}]]
    
    
    #line_coords = json.loads(sys.argv[2])
    #box_coords = json.loads(sys.argv[3])
    #box_coords=sys.argv[3]
    #print("box_coords",box_coords)
    
    #print("hi1")
    try:
      line_coords = json.loads(sys.argv[2])
      box_coords = json.loads(sys.argv[3])
      #print("hi try")
    except json.JSONDecodeError as e:
      #print("hi except")
      print(f"JSON decode error: {e}")
      sys.exit(1)

   
    # Print received arguments for debugging
    #print(f"Image path: {image_path}")
    #print(f"Line coords: {line_coords}")
    #print(f"Line coords: {isinstance(box_coords, str)}")
    #print(f"Box coords: {box_coords}")
    
    
    rows = cut_image_into_rows(image_path, line_coords, box_coords)
    print(json.dumps(rows))
