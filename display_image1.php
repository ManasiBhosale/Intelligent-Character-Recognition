<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Display Image</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;

      background-image: url('https://images.saymedia-content.com/.image/t_share/MTkyOTkyMzE2OTQ3MjQ0MjUz/website-background-templates.jpg'); /* URL to your background image */
            background-size: cover;
    
        }

        .container {
            display: flex;
            justify-content: center;
            width: 100%;
            max-width: 1200px;
            margin-bottom: 50px; /* Space between content and the overlay button */
        }
        .image-container, .output-container {
            width: 50%;
            position: relative;
            padding: 10px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .image-container img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
            border-radius: 8px;
        }
        .editable-box {
            position: absolute;
            border: 2px solid red;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 1px;
            font-size: 16px;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        .overlay-button-container {
            text-align: center;
            margin-top: 50px; /* Space between image containers and button */
        }
        .overlay-button-container button {
            padding: 10px 30px;
            font-size: 18px;
            color: white;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .overlay-button-container button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

<!-- Container for Image and Output -->
<div class="container">
    <!-- Input Image Display -->
    <div class="image-container">
        <?php if (isset($_GET['input_image'])): ?>
            <img src="<?= htmlspecialchars($_GET['input_image']) ?>" alt="Input Image" id="inputImage">
        <?php endif; ?>
    </div>
    <!-- Output Display -->
    <div class="output-container" id="outputContainer">
        <!-- Boundary Boxes will be added here -->
    </div>
</div>

<!-- Overlay Button in the Center -->
<div class="overlay-button-container">
    <?php if (isset($_GET['input_image'])): ?>
        <form action="overlay.php" method="get">
            <input type="hidden" name="input_image" value="<?= htmlspecialchars($_GET['input_image']) ?>">
            <input type="hidden" name="noise" value="<?= htmlspecialchars($_GET['noise']) ?>">
            <input type="hidden" name="skew_correction" value="<?= htmlspecialchars($_GET['skew_correction']) ?>">
            <input type="hidden" name="lined_paper" value="<?= htmlspecialchars($_GET['lined_paper']) ?>">
            <input type="hidden" name="skeletonize" value="<?= htmlspecialchars($_GET['skeletonize']) ?>">
            <button type="submit">Overlay</button>
        </form>
    <?php endif; ?>
</div>

<?php
session_start();

$target_dir = "uploads/";
$file_name = $target_dir . basename($_GET['input_image']);

// Collect checkbox values
$shadow = isset($_GET['shadow']) ? $_GET['shadow'] : 'False';
$noise = isset($_GET['noise']) ? $_GET['noise'] : 'False';
$skew_correction = isset($_GET['skew_correction']) ? $_GET['skew_correction'] : 'False';
$lined_paper = isset($_GET['lined_paper']) ? $_GET['lined_paper'] : 'False';
$skeletonize = isset($_GET['skeletonize']) ? $_GET['skeletonize'] : 'False';

//echo [$shadow , $noise, $skew_correction, $lined_paper, $skeletonize];

$command = escapeshellcmd("python3 main3.py " . escapeshellarg($file_name) . " " . escapeshellarg(json_encode([$shadow , $noise, $skew_correction, $lined_paper, $skeletonize])));
$output = shell_exec($command);

$result = json_decode($output, true);

if ($result !== null) {
    $_SESSION['original_image_coords'] = $result['original_image'];
    $_SESSION['relative_to_lines_coords'] = $result['relative_to_lines'];
    $_SESSION['line_coords'] = $result['line_coords'];
    $_SESSION['relative_to_lines_coords_list'] = $result['relative_results_per_line_list'];
} else {
    file_put_contents('error_log.txt', $output, FILE_APPEND);

    // Output the error to the browser
    echo "Error: Could not decode JSON. Raw output: " . htmlspecialchars($output);
}
?>

<script>
    // Placeholder data for boundary boxes and digits
    var boxes = <?php echo json_encode($_SESSION['original_image_coords']); ?>;

    function createBoxes() {
        var container = document.getElementById('outputContainer');
        boxes.forEach(function(box) {
            var boxDiv = document.createElement('div');
            boxDiv.className = 'editable-box';
            boxDiv.style.left = box.left + 'px';
            boxDiv.style.top = box.top + 'px';
            boxDiv.style.width = box.width + 'px';
            boxDiv.style.height = box.height + 'px';
            boxDiv.innerHTML = box.digit;
            boxDiv.contentEditable = true;
            container.appendChild(boxDiv);
        });
    }

    createBoxes();
</script>

</body>
</html>
