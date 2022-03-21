arm_disarm_changer = False


def Move(master, roll, pitch, yaw, thrust, buttons):
	master.mav.manual_control_send(master.target_system,
                pitch,   # -1000 to 1000
                roll,    # -1000 to 1000
                thrust,  # 0 to 1000  ==  500 means neutral throttle
                yaw,     # -1000 to 1000
                buttons)



def Arm_Disarm(master, stateBtn):
	global arm_disarm_changer
	if(arm_disarm_changer == True and stateBtn == True):
		master.arducopter_arm()
		arm_disarm_changer = False
	elif(arm_disarm_changer == False and stateBtn == False):
		master.arducopter_disarm()
		arm_disarm_changer = True


def ChangeFlightMode(master, mode):
	if(master.flightmode != mode):
		mode_id = master.mode_mapping()[mode]
		master.set_mode(mode_id)
