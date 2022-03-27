<?php 
    $filename = "../variables/throttlePID.json";
    $to_save = Array (
        "p" => intval($_GET['p']),
        "i" => intval($_GET['i']),
        "d" => intval($_GET['d'])
    );

    $content = json_encode($to_save);
    echo($content);
    file_put_contents($filename, $content);

?>
