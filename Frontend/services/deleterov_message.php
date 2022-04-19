<?php 
    require "Connection.php";
    $bindings = [];
    $result=null;
    if($pdo!=null){
        error_log("Connection is not null");
        $parameters = [];
        $auxParam = array_keys($_GET);
        foreach ($auxParam as $val){
            array_push($parameters,$val);
        }
        $parameters = implode(",", $parameters);
        foreach ($auxParam as $val){
            $bindings[] = $_GET[$val];
        }
        $bindings = implode(",", $bindings);
        $sql = "DELETE FROM ROV_message WHERE (" . $parameters . ") = (" . $bindings . ")";
        $stmt = $pdo->prepare($sql);
        if($stmt->execute()){
            $result = "Deletion Success";
        }
        else{
            $result = "Deletion Error";
        }
    }
    else{
        $result = "Connection Error";
    }
    echo json_encode($result);
?>
