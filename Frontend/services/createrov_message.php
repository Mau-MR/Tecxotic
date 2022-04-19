<?php 
    require "Connection.php";
    $bindings = [];
    $result=null;
    if($pdo!=null){
        error_log("Connection is not null");

        $parameters = ['arm_disarm', 'connect_pixhawk', 'pitch_camera', 'yaw_camera', 'throttle', 'roll', 'pitch', 'yaw', 'activate_agent1', 'activate_agent2', 'activate_agent3', 'miniROV_direction', 'reel_direction', 'kp_throttle', 'ki_throttle', 'kd_throttle', 'kp_roll', 'ki_roll', 'kd_roll', 'kp_pitch', 'ki_pitch', 'kd_pitch', 'kp_yaw', 'ki_yaw', 'kd_yaw'];

        for($i = 0; $i < sizeof($parameters); $i++){
            if(!isset($_GET[$parameters[$i]])){
                $result = "Parameter ".$parameters[$i]." missing";
                break;
            }
            else{
                $bindings[] = $_GET[$parameters[$i]];
            }
        }
        if($result==null){
            $sql = 'INSERT INTO ROV_message( time, arm_disarm, connect_pixhawk, pitch_camera, yaw_camera, throttle, roll, pitch, yaw, activate_agent1, activate_agent2, activate_agent3, miniROV_direction, reel_direction, kp_throttle, ki_throttle, kd_throttle, kp_roll, ki_roll, kd_roll, kp_pitch, ki_pitch, kd_pitch, kp_yaw, ki_yaw, kd_yaw) VALUES 
                (CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)';
                
            $stmt = $pdo->prepare($sql);
            if($stmt->execute($bindings)){
                $result = "Insertion Success";
            }
            else{
                $result = "Insertion Error";
            }
        }
    }
    else{
        $result = "Connection Error";
    }
    echo json_encode($result);
?>
