# Import mavutil
from pymavlink import mavutil



def ConnectToPixhawk():
    global master
    # Create the connection
    #master = mavutil.mavlink_connection("COM12") #Windows 10
    # master = mavutil.mavlink_connection("/dev/serial/by-id/usb-ArduPilot_Pixhawk1_2D0025001351383131383231-if00")
    #master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
    master = mavutil.mavlink_connection("/dev/serial/by-id/usb-ArduPilot_Pixhawk1_2D0025001351383131383231-if00")
    #master = mavutil.mavlink_connection("/dev/ttyAMA0", baud=57600)
    # Wait a heartbeat before sending commands
        #master = mavutil.mavlink_connection("/dev/serial/by-id/usb-ArduPilot_PH4-mini_3D001E001351383137383335-if00")	
    master.wait_heartbeat()
    return master

def changeFlightMode(flight_mode):
    if flight_mode not in master.mode_mapping():
        print('Unknown mode : {}'.format(flight_mode))
    else: 
        mode_id = master.mode_mapping()[flight_mode]
        master.mav.set_mode_send(master.target_system,mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,mode_id)
        print('Flight mode: {}'.format(flight_mode))            

connection_pixhawk_changer = True
masterReturn = None
def ConnectDisconnectPixhawk(stateBtn):
    global connection_pixhawk_changer, masterReturn
    if(connection_pixhawk_changer == True and stateBtn == True and masterReturn == None):
        connection_pixhawk_changer = False
        masterReturn = ConnectToPixhawk()
        return masterReturn
    elif(connection_pixhawk_changer == False and stateBtn == False ):
        connection_pixhawk_changer = True
        masterReturn = None
        return masterReturn
    else:
        return masterReturn

if __name__ == "__main__":
    try:
        #ConnectDisconnectPixhawk(False)
        while True:
            con = ConnectDisconnectPixhawk(True)

            if con != None:
                changeFlightMode('STABILIZE')
                print("connected")

    except Exception as e:
                print(e)
