import cv2

import lib
import time
from pySerialTransfer import pySerialTransfer as txfer

if __name__ == '__main__':
    link = None
    vid = None
    try:
        link = txfer.SerialTransfer(lib.getSerialPort("Arduino"))

        link.open()
        time.sleep(5)  # allow some time for the Arduino to completely reset

        vid = cv2.VideoCapture(0)
        if not vid.isOpened():
            print("Cannot open camera")
            exit()

        while (True):
            sendSize = 0

            sendSize = link.tx_obj([0,1,3,4,5,6,7,8,9], start_pos=sendSize)
            link.send(sendSize)

            while not link.available():
                if link.status < 0:
                    if link.status == txfer.CRC_ERROR:
                        print('ERROR: CRC_ERROR')
                    elif link.status == txfer.PAYLOAD_ERROR:
                        print('ERROR: PAYLOAD_ERROR')
                    elif link.status == txfer.STOP_BYTE_ERROR:
                        print('ERROR: STOP_BYTE_ERROR')
                    else:
                        print('ERROR: {}'.format(link.status))
            
            rec_list_ = link.rx_obj(obj_type=type(sendSize), obj_byte_size=sendSize, list_format='i')

            print('SENT: {}'.format(sendSize))
            print('RCVD: {}'.format(rec_list_))
            print(' ')

    except KeyboardInterrupt:
        if link is not None:
            link.close()
        if vid is not None:
            vid.release()
        cv2.destroyAllWindows()

    except:
        import traceback
        traceback.print_exc()

        if link is not None:
            link.close()
        if vid is not None:
            vid.release()
        cv2.destroyAllWindows()
