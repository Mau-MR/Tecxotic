<?php 
    $servername = "127.0.0.1";
    $username = "root";
    $password = "root";
    $dbname = "TecXoticControllerV2";

    try {
        $pdo = new PDO('mysql:host='.$servername.';dbname='.$dbname, $username, $password);

        // set the PDO error mode to exception
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    }
    catch(PDOException $e)
    {
        $pdo = null;
    }     
?>
