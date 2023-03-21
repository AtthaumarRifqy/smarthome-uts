import msvcrt
# from client import create_client

# host_ip = "192.168.118.173"
# port = 1883

# # create_client(sub_topic, value, changed, host, port)
# topic = ""
# status = ""

# client_all = create_client("smarthome/+/status", topic, status, host_ip, port)

# client_all.start_loop()

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

curr_ac_status = "Off"
curr_light_status = "Off"

# def sendOrder(order):
#     topic = ''
#     loadc= ''
    
#     if order == b'1':
#         topic = "smarthome/light"
#         load = f"{not curr_light_status}, "
#     elif order == b'2':
#         topic = "smarthome/ac"
#         load = f"{not curr_ac_status}, "
#     elif (order == b'3') or (order == b'4'):
#         topic = "smarthome/all"
#         if (order == b'3'):
#             load = "on, "
#         else:
#             load = "off, "
#     else:
#         return None

#     client_all.publish()

def toggle(text):
    match text:
        case "On": return "Off"
        case "Off": return "On"
        case _: return None 

print(" Light         AC")
status_str = f"[ { curr_light_status } ]      [ { curr_ac_status } ]"
print(f"{ status_str }")
print("Toggle Light (1) / AC (2) or Turn All On (3) / Off (4)?")
# current_menu = ''
# print(current_menu)
while True:
    
    if msvcrt.kbhit():
        # order = msvcrt.getch()
        # current_menu+="Would you like to set a timer? (y/n)"
        # print(LINE_UP, end=LINE_CLEAR)
        # print(current_menu)

        # if msvcrt.getch() == b'n':
        #     sendOrder(order, 0)
        #     current_menu=''
        # elif msvcrt.getch() == b'y':
        #     temp = int(input("Input amount: "))
        #     sendOrder(order, temp)
        #     current_menu=''

        if msvcrt.getch() == b'1':
            curr_light_status = toggle(curr_light_status)
        elif msvcrt.getch() == b'2':
            curr_ac_status = toggle(curr_ac_status)
        elif msvcrt.getch() == b'3':
            curr_ac_status = "On"
            curr_light_status = "On"
        elif msvcrt.getch() == b'4':
            curr_ac_status = "Off"
            curr_light_status = "Off"
        
        print(LINE_UP + LINE_UP, end=LINE_CLEAR)
        status_str = f"[ { curr_light_status } ]      [ { curr_ac_status } ]"
        print(f"{ status_str }")
        print("Toggle Light (1) / AC (2) or Turn All On (3) / Off (4)?")