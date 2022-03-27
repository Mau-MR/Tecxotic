<?php 
    $filename = "../variables/agent1.json";
    $to_save = Array (
        "first_low" => intval($_GET['first_value_low']),
        "first_high" => intval($_GET['first_value_high']),
        "second_low" => intval($_GET['second_value_low']),
        "second_high" => intval($_GET['second_value_high']),
        "third_low" => intval($_GET['third_value_low']),
        "third_high" => intval($_GET['third_value_high']),
        "size_min" => intval($_GET['size_value_min']),
        "size_max" => intval($_GET['size_value_max']),
        "percentage_min" => intval($_GET['percentage_value_min']),
        "percentage_max" => intval($_GET['percentage_value_max'])
    );

    $content = json_encode($to_save);
    file_put_contents($filename, $content);
    echo($content);

?>
