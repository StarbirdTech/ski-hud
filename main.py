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
            if objects := lib.getObjects(vid, debug=True):
                print("left: {}".format(objects[0]))
                print("right: {}".format(objects[1]))

                payload = link.tx_obj([y for x in objects[0] for y in x])
                link.send(payload)

                time.sleep(0.01)
            else:
                print("none")

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
