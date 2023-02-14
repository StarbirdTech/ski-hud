import cv2 as cv
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import time


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the camera)
        self.vid = cv2.VideoCapture(self.video_source)

        # Get the video source properties
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)
        self.frame_width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.frame_width, height=self.frame_height)
        self.canvas.pack()

        # Create a label to display information about the video source
        self.info_label = tk.Label(window, text="Video source: {}\nFPS: {:.2f}\nFrame width: {}\nFrame height: {}".format(
            self.video_source, self.fps, self.frame_width, self.frame_height))
        self.info_label.pack(side="right")

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = int(1000/(self.fps+1))
        self.start_time = time.time()
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            orb = cv.ORB_create()
            kp, des = orb.detectAndCompute(gray, None)
            kpImage = cv.drawKeypoints(frame, kp, None, color=(0, 255, 0))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(kpImage))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
        self.window.after(self.delay, self.update)


# Create a window and pass it to the Application object
App(tk.Tk(), "Tkinter and OpenCV")
