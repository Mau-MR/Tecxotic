<?php
    $file_path = "../assets/config/config.json";
    $strJsonFileContents = file_get_contents($file_path);
    $stored_configuration = json_decode($strJsonFileContents, true);
    // print_r($stored_configuration);
    // echo(  count($_GET) );
    foreach ($_GET as $key => $value)
    {
        $stored_configuration[$key] = $value;
    }
    $myJSON = json_encode($stored_configuration,JSON_NUMERIC_CHECK);
    // echo("<br>");
    // echo("<br>");
    // echo("<br>");
    // print_r($myJSON);
    file_put_contents($file_path, $myJSON);
    echo("success");
?>