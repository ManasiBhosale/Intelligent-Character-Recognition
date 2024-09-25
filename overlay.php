<?php
session_start();

$target_dir = "uploads/";
$file_name = $target_dir . basename($_GET['input_image']);

if (isset($_SESSION['original_image_coords']) && isset($_SESSION['relative_to_lines_coords']) && isset($_SESSION['line_coords'])) {
    $original_image_coords = $_SESSION['original_image_coords'];
    $relative_to_lines_coords = $_SESSION['relative_to_lines_coords'];
    $line_coords = $_SESSION['line_coords'];
    $relative_to_lines_coords_list = $_SESSION['relative_to_lines_coords_list'];
    
    $escaped_file_name = escapeshellarg($file_name);
    $escaped_line_coords = escapeshellarg(json_encode($line_coords ));
    
    $json_relative_to_lines_coords_list = json_encode($relative_to_lines_coords_list);
    file_put_contents('debug_json_relative_to_lines_coords.json', $json_relative_to_lines_coords_list);
    $escaped_relative_to_lines_coords = escapeshellarg($json_relative_to_lines_coords_list);
    
    $command = "python3 cut_image.py $escaped_file_name $escaped_line_coords $escaped_relative_to_lines_coords";
    $output = shell_exec($command);
    file_put_contents('output_log.txt', $output);
    $rows = json_decode($output, true);
} else {
    echo "Line or character coordinates not found in session.";
    $rows = [];
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Digits</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f7f7f7;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;

      background-image: url('https://images.saymedia-content.com/.image/t_share/MTkyOTkyMzE2OTQ3MjQ0MjUz/website-background-templates.jpg'); /* URL to your background image */
            background-size: cover;
    
        }
        .line-results {
            width: 100%;
            max-width: 1200px;
        }
        .line {
            margin-bottom: 50px; /* Increased space between each line result */
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%;
            margin-bottom: 10px; /* Increased space between input and output */
        }
        .image-strip {
            max-width: 90%;
            height: 30px; /* Previously auto */
            max-height: 200px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .editable-box {
            position: absolute;
            border: 2px solid #007bff;
            background-color: rgba(255, 255, 255, 0.8);
            padding: 5px;
            font-size: 30px;
            border-radius: 5px;
        }
        .editable-box input {
            border: none;
            background: transparent;
            font-size: 30px;
            width: 100%;
            height: 100%;
            text-align: center;
        }
        .editable-box input:focus {
            outline: none;
        }
        .output-container {
            position: relative;
            display: inline-block;
            width: auto;
            margin-top: 10px; /* Increased margin between input image and its output */
        }
        .output-container .editable-box {
            position: relative;
            display: inline-block;
            margin: 0 5px; /* Increased space between output boxes */
        }
        form {
            margin-top: 0 px; /* Space between output section and the submit button */
            text-align: center; /* Center the submit button */
        }
        button[type="submit"] {
            padding: 10px 30px;
            font-size: 18px;
            color: white;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

<!-- Display Line Results -->
<div class="line-results">
    <?php foreach ($rows as $index => $row): ?>
        <div class="line">
            <!-- Input Image Row -->
            <div class="container">
                <h3>Input Row <?= $index + 1 ?></h3>
                <img class="image-strip" src="data:image/png;base64,<?= htmlspecialchars($row) ?>" alt="Input Row Image">
            </div>
            <!-- Output Row -->
            <div class="container">
                <h3>Output Row <?= $index + 1 ?></h3>
                <div class="output-container" id="outputRow<?= $index ?>">
                    <!-- This will be populated by JavaScript -->
                </div>
            </div>
        </div>
    <?php endforeach; ?>
</div>

<!-- Submit Updated Digits -->
<form action="submit_digits.php" method="post">
    <input type="hidden" name="input_image" value="<?= htmlspecialchars($_GET['input_image']) ?>">
    <input type="hidden" name="boxes" id="boxesInput">
    <button type="submit">Submit Updated Digits</button>
</form>

<script>
    var original_image_coords = <?php echo json_encode($original_image_coords); ?>;
    var relative_to_lines_coords = <?php echo json_encode($relative_to_lines_coords); ?>;
    var line_coords = <?php echo json_encode($line_coords); ?>;
    var boxes = [];

    function createEditableBoxes(lineIndex, container) {
        var rowCharCoords = relative_to_lines_coords[lineIndex] || [];

        rowCharCoords.forEach(function(box) {
            var boxDiv = document.createElement('div');
            boxDiv.className = 'editable-box';
            boxDiv.style.width = (box.width + 10) + 'px';
            boxDiv.style.height = (box.height + 10) + 'px';
            boxDiv.innerHTML = '<input type="text" value="' + box.digit + '">';
            container.appendChild(boxDiv);
            boxes.push(box);
        });
    }

    function createLineResults() {
        line_coords.forEach(function(line, index) {
            var outputContainer = document.getElementById('outputRow' + index);
            createEditableBoxes(index, outputContainer);
        });
    }

    function collectBoxData() {
        var boxData = [];
        var inputs = document.querySelectorAll('.editable-box input');
        inputs.forEach(function(input, index) {
            var box = boxes[index];
            if (box) {
                var digit = parseInt(input.value, 10);
                if (!isNaN(digit)) {
                    boxData.push([
                        Math.round(box.left),
                        Math.round(box.top),
                        Math.round(box.width),
                        Math.round(box.height),
                        digit
                    ]);
                }
            }
        });
        document.getElementById('boxesInput').value = JSON.stringify(boxData);
    }

    document.querySelector('form').addEventListener('submit', function(event) {
        collectBoxData();
    });

    window.onload = function() {
        createLineResults();
    };
</script>

</body>
</html>
