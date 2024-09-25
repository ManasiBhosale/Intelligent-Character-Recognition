
<html lang="en">
<head>
<title>Upload Image</title>
</head>

<?php
// upload.php
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['image'])) {
    $target_dir = "uploads/";
    $target_file = $target_dir . basename($_FILES["image"]["name"]);
    $imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

    // Check if image file is an actual image or fake image
    $check = getimagesize($_FILES["image"]["tmp_name"]);
    if ($check !== false) {
        // Move uploaded file to target directory
        if (move_uploaded_file($_FILES["image"]["tmp_name"], $target_file)) {
            // Get the checkbox values
            $shadow = isset($_POST['shadow']) ? 'True' : 'False';
            $noise = isset($_POST['noise']) ? 'True' : 'False';
            $skew = isset($_POST['skew_correction']) ? 'True' : 'False';
            $lined = isset($_POST['lined_paper']) ? 'True' : 'False';
            $skeletonize = isset($_POST['skeletonize']) ? 'True' : 'False';

            //echo "noise" .$noise;
            //echo "skew" .$skew;
            //echo "lined" .$lined;
            // Redirect to the next page with the checkbox values as query parameters
            header("Location: index.php?input_image=" . $target_file . "&output_image=" . $target_file . "&shadow=" . $shadow . "&noise=" . $noise . "&skew=" . $skew . "&lined=" . $lined . "&skeletonize=" . $skeletonize);
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    } else {
        echo "File is not an image.";
    }
} else {
    echo "No file uploaded.";
}
?>
</html>
