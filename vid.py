import cv2
import tkinter as tk
from PIL import Image, ImageTk

class VideoApp:
    def __init__(self, window, video_source):
        self.window = window
        self.window.title("Video Processing App")

        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)

        # Adjust the window and canvas size
        self.window_width = 640  # Adjust as needed
        self.window_height = 480  # Adjust as needed
        self.canvas = tk.Canvas(window, width=self.window_width, height=self.window_height)
        self.canvas.pack()

        self.btn_start = tk.Button(window, text="Start", width=10, command=self.start_video)
        self.btn_start.pack(pady=10)

        self.btn_stop = tk.Button(window, text="Stop", width=10, command=self.stop_video)
        self.btn_stop.pack()

        self.threshold_slider = tk.Scale(window, from_=0, to=255, orient=tk.HORIZONTAL, label="Threshold",
                                         command=self.update_threshold)
        self.threshold_slider.set(100)  # Initial threshold value
        self.threshold_slider.pack()

        self.is_playing = False
        self.update_video()

    def update_video(self):
        if self.is_playing:
            ret, frame = self.cap.read()
            if ret:
                processed_frame = self.process_frame(frame)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(processed_frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update_video)

    def process_frame(self, frame):
        # Example image processing operation (convert frame to grayscale and apply threshold)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresholded_frame = cv2.threshold(gray_frame, self.threshold_slider.get(), 255, cv2.THRESH_BINARY)
        return thresholded_frame

    def start_video(self):
        self.is_playing = True

    def stop_video(self):
        self.is_playing = False

    def update_threshold(self, value):
        # Threshold slider callback function
        pass  # Update processing parameters here if needed

if __name__ == "__main__":
    # Specify the video file path
    video_file = "WhatsApp Video 2024-03-15 at 20.36.10_fa170f82.mp4"

    root = tk.Tk()
    app = VideoApp(root, video_file)

    # Adjust the window size
    root.geometry(f"{app.window_width}x{app.window_height}")

    root.mainloop()
