<?php 
    require "Connection.php";
    $result=null;
    if($pdo!=null){
        error_log("Connection is not null");
        $parameters = [];
        $auxParam = array_keys($_GET);
        $idVal = -1;
        for($i = 0; $i < sizeof($auxParam); $i++){
            if($auxParam[$i] != 'id'){
                $temp = $auxParam[$i]."=".$_GET[$auxParam[$i]];
                array_push($parameters,$temp);
            }else{
                $idVal = $_GET[$auxParam[$i]];
            }
        }
        $parameters = implode(",", $parameters);
        $sql = "UPDATE ArP_message SET ". $parameters . " WHERE id=". $idVal;
        $stmt = $pdo->prepare($sql);
        if($stmt->execute()){
            $result = "Update Success";
        }
        else{
            $result = "Update Error";
        }
    }
    else{
        $result = "Connection Error";
    }
    echo json_encode($result);
?>
