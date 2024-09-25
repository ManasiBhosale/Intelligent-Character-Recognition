

<html lang="en">
<head>
<title>Upload Image</title>
</head>

<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['image'])) {
    $target_dir = "uploads/";
    if (!is_dir($target_dir)) {
        mkdir($target_dir, 0777, true);
    }
    $target_file = $target_dir . basename($_FILES["image"]["name"]);
    $imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

    // Check if image file is a actual image or fake image
    $check = getimagesize($_FILES["image"]["tmp_name"]);
    if ($check !== false) {
        // Move uploaded file to target directory
        if (move_uploaded_file($_FILES["image"]["tmp_name"], $target_file)) {
            // Prepare checkbox values
            $shadow = isset($_POST['shadow']) ? 'True' : 'False';
            $noise = isset($_POST['noise']) ? 'True' : 'False';
            $skew_correction = isset($_POST['skew_correction']) ? 'True' : 'False';
            $lined_paper = isset($_POST['lined_paper']) ? 'True' : 'False';
            $skeletonize = isset($_POST['skeletonize']) ? 'True' : 'False';

            // Redirect to display page with input image path and checkbox values
            $query_string = http_build_query([
                'input_image' => $target_file,
                'shadow' => $shadow,
                'noise' => $noise,
                'skew_correction' => $skew_correction,
                'lined_paper' => $lined_paper,
                'skeletonize' => $skeletonize,
            ]);
            header("Location: display_image1.php?$query_string");
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
