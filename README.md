# Intelligent-Character-Recognition

This project is an Optical Character Recognition (OCR) system that focuses on recognizing and processing number sequences from uploaded images. The system allows users to upload images containing number sequences, processes them through image preprocessing, segmentation, and classification, and outputs the recognized number sequences in various formats (TEXT, PDF, HOCR).

## Table of Contents

- [Overview](#overview)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [Outputs](#outputs)

---

## Overview

The OCR system is designed to:
1. Take an image input from a user (typically containing number sequences).
2. Process the image to extract number sequences.
3. Provide machine-readable outputs in different formats, including plain text, PDF, and HOCR.

The system is built using a combination of PHP for front-end and backend interaction and Python for image processing and classification.

## Folder Structure

```plaintext
root/
│   cut_image.py
│   display_image1.php
│   generate_file.py
│   index.php
│   main3.py
│   overlay.php
│   process_image.php
│   submit_digits.php
│   upload.php
│
└───Samples/
        Image1.png
        Image1_to_HOCR.hocr
        Image1_to_PDF.pdf
        Image1_to_TEXT.txt
```

### Key Folders:
- **Samples/**: Contains a sample image (`Image1.png`) and the output of the OCR system in various formats such as `TEXT`, `PDF`, and `HOCR`.

---

## Installation

### Prerequisites

- **XAMPP**: Required to run the PHP files on a local server. Ensure you have XAMPP installed and running (Apache server and MySQL).
- **Python 3.x**: For running Python scripts.
- **PHP 7.x+**: Needed to run the PHP scripts.

### Steps

1. **Clone the Repository**: 
    ```bash
    git clone <repository-url>
    ```

2. **Set up XAMPP**:
   - Install and run XAMPP.
   - Place the project folder inside the `htdocs` directory of your XAMPP installation.
   - Start the Apache server.

3. **Install Python Dependencies**:
    - Install the required Python libraries by running:
    ```bash
    pip install -r requirements.txt
    ```

4. **Access the Application**:
   - Open a browser and navigate to `http://localhost/<your_project_folder>`.

---

## Usage

1. **Upload an Image**:
    - Open `index.php` in the browser.
    - Upload an image containing a number sequence.

2. **Processing**:
    - The image is processed through several steps: image preprocessing, segmentation, and classification.

3. **Output**:
    - View the original and processed image through `display_image1.php`.
    - Compare the input strip with the output strip using `overlay.php`.
    - The recognized text is generated into different formats (TEXT, PDF, HOCR) for further use.

---

## File Descriptions

- **index.php**: The front-end upload form for users to submit images for OCR processing.
- **upload.php**: Handles the file upload and stores the uploaded image for further processing.
- **process_image.php**: Handles the core image processing tasks by invoking the Python scripts for OCR.
- **display_image1.php**: Displays the original image along with the machine-readable text.
- **overlay.php**: Displays both the input and output strips for comparison and also allows the user to correct any misclassified digits.
- **submit_digits.php**: Supports the submission of the recognized digits.
- **main3.py**: Python script responsible for image preprocessing, segmentation, and classification.
- **cut_image.py**: Slices the input image into row strips for better segment visualization.
- **generate_file.py**: Converts the recognized text into various formats such as TEXT, PDF, and HOCR.

---

## Outputs

The system generates the following outputs:
- **Plain Text (`.txt`)**: The recognized number sequences in plain text format.
- **PDF (`.pdf`)**: A PDF file containing the recognized number sequences.
- **HOCR (`.hocr`)**: An HOCR file with the recognized text, useful for further machine reading or integration with other OCR tools.


---

### requirements.txt

```
opencv-python==4.5.3.56
numpy==1.21.2
pytesseract==0.3.7
Pillow==8.3.1
pdf2image==1.16.0
fpdf==1.7.2
```

### Additional Requirements

- **XAMPP**: Required for running the PHP files in a local environment. Install XAMPP and configure it to run the PHP scripts on `localhost`.
