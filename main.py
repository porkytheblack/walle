import serial
import time

from detection import process_webcam_input

bluetooth_port = '/dev/tty.HC-05'
baud_rate = 9600


# def main():
#     try:
#         with serial.Serial(bluetooth_port, baud_rate) as ser:
#             time.sleep(2)
#             command = 'Hello World\n'
#             ser.write(command.encode())
#             print(f"Sent : {command.strip()}")
#     except serial.SerialException as e:
#         print(f"Error : {e}")



if __name__ == '__main__':
    # main()
    process_webcam_input()