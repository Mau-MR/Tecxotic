<?php
    $file_path = "../assets/config/AI1_config.json";
    $strJsonFileContents = file_get_contents($file_path);
    $array = json_decode($strJsonFileContents, true);
    echo(json_encode($array));
?>