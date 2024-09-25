
<?php
session_start();

$result_message = ''; // Initialize the result message variable

if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['output_format'])) {
    $input_image = $_POST['input_image'];
    $boxes = json_decode($_POST['boxes'], true);
    $output_format = $_POST['output_format'];
    $line_coords = $_SESSION['line_coords'];
    $escaped_boxes = escapeshellarg(json_encode($boxes));
    $escaped_line_coords = escapeshellarg(json_encode($line_coords));

    // Command to execute the Python script
    $command = escapeshellcmd("python3 generate_file.py $input_image $output_format $escaped_boxes $escaped_line_coords");
    $output = shell_exec($command);

    // Assuming the Python script will return the file path
    $output = trim($output); // Removing any trailing new lines or spaces

    // Set the result message with copy functionality
    $result_message = "
        <div class='result'>
            <p>Output file created:</p>
            <div class='result-content'>
                <a href='$output' download>$output</a>
                <span class='copy-icon' data-clipboard-text='$output' title='Copy to clipboard'>
                    <i class='fa fa-copy'></i>
                </span>
            </div>
        </div>
    ";
}

$input_image = isset($_POST['input_image']) ? $_POST['input_image'] : '';
$boxes = isset($_POST['boxes']) ? $_POST['boxes'] : '';
$output_format = isset($_POST['output_format']) ? $_POST['output_format'] : '';

display_form($input_image, $boxes, $output_format, $result_message);

function display_form($input_image, $boxes, $selected_format, $result_message) {
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Select Output Format</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                min-height: 100vh;

      background-image: url('https://images.saymedia-content.com/.image/t_share/MTkyOTkyMzE2OTQ3MjQ0MjUz/website-background-templates.jpg'); /* URL to your background image */
            background-size: cover;
    
            }

            .nav-bar {
                background: #007BFF;
                padding: 10px;
                color: #fff;
                text-align: center;
                font-size: 1.2em;
            }

            .nav-bar a {
                color: #fff;
                text-decoration: none;
                font-weight: bold;
            }

            .container {
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 500px;
                margin: auto;
                text-align: center;
                position: relative;
            }

            h1 {
                font-size: 1.5em;
                margin-bottom: 20px;
                color: #333;
            }

            label {
                display: block;
                margin-bottom: 10px;
                color: #555;
            }

            select {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 1em;
                margin-bottom: 20px;
            }

            button {
                display: block;
                width: 100%;
                padding: 10px;
                background-color: #007BFF;
                border: none;
                color: #fff;
                font-size: 1em;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.3s;
            }

            button:hover {
                background-color: #0056b3;
            }

            .result {
                margin-top: 30px;
                color: #333;
                text-align: left;
            }

            .result p {
                margin: 0 0 10px;
                font-weight: bold;
            }

            .result-content {
                display: flex;
                align-items: center;
                justify-content: space-between;
                border: 1px solid #ddd;
                padding: 10px;
                border-radius: 4px;
                background-color: #f9f9f9;
            }

            .result-content a {
                color: #007BFF;
                text-decoration: none;
                flex: 1;
                word-wrap: break-word;
            }

            .result-content a:hover {
                text-decoration: underline;
            }

            .copy-icon {
                margin-left: 15px;
                color: #007BFF;
                cursor: pointer;
                transition: color 0.3s;
            }

            .copy-icon:hover {
                color: #0056b3;
            }

            .spinner {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                display: none;
                font-size: 2em;
                color: #007BFF;
            }

            .spinner.show {
                display: block;
            }
        </style>
    </head>
    <body>
        <div class="nav-bar">
            <a href="index.php">Back to Home</a>
        </div>
        <div class="container">
            <h1>Save your Results!</h1>
            <form id="form" action="submit_digits.php" method="post">
                <input type="hidden" name="input_image" value="<?= htmlspecialchars($input_image) ?>">
                <input type="hidden" name="boxes" value="<?= htmlspecialchars($boxes) ?>">
                
                <label for="output_format">Select output format:</label>
                <select name="output_format" id="output_format">
                    <option value="text" <?= $selected_format == 'text' ? 'selected' : '' ?>>Text</option>
                    <option value="pdf" <?= $selected_format == 'pdf' ? 'selected' : '' ?>>PDF</option>
                    <option value="hocr" <?= $selected_format == 'hocr' ? 'selected' : '' ?>>HOCR</option>
                </select>
                
                <button type="submit">Generate Output</button>
            </form>
            
            <?= $result_message ?>

            <!-- Spinner for processing indicator -->
            <div id="spinner" class="spinner">
                <i class="fa fa-spinner fa-spin"></i>
            </div>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.8/clipboard.min.js"></script>
        <script>
            // Initialize Clipboard.js
            new ClipboardJS('.copy-icon');

            // Optional: Add feedback for copy action
            document.querySelectorAll('.copy-icon').forEach(item => {
                item.addEventListener('click', () => {
                    alert('File location copied to clipboard!');
                });
            });

            // Show spinner when form is submitted
            document.getElementById('form').addEventListener('submit', function() {
                document.getElementById('spinner').classList.add('show');
            });
        </script>
    </body>
    </html>
    <?php
}
?>





