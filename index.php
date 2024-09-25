<!--

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Image</title>
</head>
<body>

<form action="process_image.php" method="post" enctype="multipart/form-data">
    <center><input type="file" name="image" accept="image/*" required>
    <button type="submit">Submit</button></center>

</form>

</body>
</html>
-->

<!--
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Image</title>
</head>
<body>

<form action="process_image.php" method="post" enctype="multipart/form-data">
    <center>
        <input type="file" name="image" accept="image/*" required>
        
        <div>
            <label for="shadow">Shadow?</label>
            <input type="checkbox" name="shadow" id="shadow" value="True">
        </div>
        
        <div>
            <label for="noise">Noise?</label>
            <input type="checkbox" name="noise" id="noise" value="True">
        </div>
        
        <div>
            <label for="skew_correction">Skew Correction?</label>
            <input type="checkbox" name="skew_correction" id="skew_correction" value="True">
        </div>
        
        <div>
            <label for="lined_paper">Lined Paper?</label>
            <input type="checkbox" name="lined_paper" id= "lined_paper" value="True">
        </div>
        
        <div>
            <label for="skeletonize">Skeletonize?</label>
            <input type="checkbox" name="skeletonize" id="skeletonize" value="True">
        </div>
        
        <button type="submit">Submit</button>
    </center>
</form>

</body>
</html>
-->



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Image</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
        
            background-image: url('https://images.saymedia-content.com/.image/t_share/MTkyOTkyMzE2OTQ3MjQ0MjUz/website-background-templates.jpg'); /* URL to your background image */
            background-size: cover;
            
            background-position: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            color: white; /* Change text color to contrast with background */
        }
        h1 {
            margin-bottom: 20px;
            font-size: 32px;
            color: #333;
            font-family: Verdana, sans-serif;
            background-image: linear-gradient(to right top, #67aaf2, #00bbf6, #00c7da, #00cda3, #43cd5b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        form {
            background-color: rgba(255, 255, 255, 0.9); /* Slight transparency for better visibility on background */
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            text-align: center;
            width: 100%;
            max-width: 500px;
        }
        input[type="file"] {
            display: none;
        }
        .custom-file-upload {
            display: inline-block;
            cursor: pointer;
            padding: 10px 20px;
            border: 2px solid #007bff;
            border-radius: 5px;
            background-color: #007bff;
            color: white;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .custom-file-upload:hover {
            background-color: #0056b3;
        }
        .custom-file-upload i {
            margin-right: 8px;
        }
        label {
            display: block;
            margin: 10px 0;
            font-size: 16px;
            color: #333;
            text-align: left;
            padding-left: 170px;
        }
        input[type="checkbox"] {
            margin-right: 10px;
        }
        button[type="submit"] {
            padding: 10px 20px;
            font-size: 18px;
            color: white;
            background-color: #28a745;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button[type="submit"]:hover {
            background-color: #218838;
        }
        .loading-indicator {
            display: none;
            margin-top: 20px;
            font-size: 16px;
            color: #555;
        }
        .file-name {
            margin-top: 10px;
            font-size: 16px;
            color: #333;
        }
    </style>
    <!-- Font Awesome CDN Link -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body>

<h1>Intelligent Character Recognition</h1>

<form action="process_image.php" method="post" enctype="multipart/form-data" onsubmit="showLoadingIndicator()">
    <label for="image" class="custom-file-upload">
        <i class="fa fa-upload"></i> Choose Image
    </label>
    <input type="file" name="image" id="image" accept="image/*" required onchange="displayFileName()">

    <div class="file-name" id="fileName">No file chosen</div><br>

    <div>
        <label for="shadow">
            <input type="checkbox" name="shadow" id="shadow" value="True">
            Shadow?
        </label>
    </div>

    <div>
        <label for="noise">
            <input type="checkbox" name="noise" id="noise" value="True">
            Noise?
        </label>
    </div>

    <div>
        <label for="skew_correction">
            <input type="checkbox" name="skew_correction" id="skew_correction" value="True">
            Skew Correction?
        </label>
    </div>

    <div>
        <label for="lined_paper">
            <input type="checkbox" name="lined_paper" id="lined_paper" value="True">
            Lined Paper?
        </label>
    </div>

    <div>
        <label for="skeletonize">
            <input type="checkbox" name="skeletonize" id="skeletonize" value="True">
            Skeletonize?
        </label>
    </div>

    <button type="submit">Submit</button>
    <div class="loading-indicator" id="loadingIndicator">Processing...</div>
</form>

<script>
    function showLoadingIndicator() {
        document.getElementById('loadingIndicator').style.display = 'block';
    }

    function displayFileName() {
        const fileInput = document.getElementById('image');
        const fileNameDisplay = document.getElementById('fileName');
        
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = fileInput.files[0].name;
        } else {
            fileNameDisplay.textContent = 'No file chosen';
        }
    }
</script>

</body>
</html>



