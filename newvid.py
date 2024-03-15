import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class VideoApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Video Processing App")

        self.video_source = None
        self.cap = None

        self.canvas = tk.Canvas(window, width=640, height=450)
        self.canvas.pack()

        self.btn_open = tk.Button(window, text="Open File", width=10, command=self.open_file)
        self.btn_open.pack(pady=10)

        self.btn_start = tk.Button(window, text="Start", width=10, command=self.start_video, state=tk.DISABLED)
        self.btn_start.pack(pady=5)

        self.btn_stop = tk.Button(window, text="Stop", width=10, command=self.stop_video, state=tk.DISABLED)
        self.btn_stop.pack()

        self.btn_save = tk.Button(window, text="Save Frame", width=10, command=self.save_frame, state=tk.DISABLED)
        self.btn_save.pack()

        self.threshold_slider = tk.Scale(window, from_=0, to=255, orient=tk.HORIZONTAL, label="Threshold",
                                         command=self.update_threshold, state=tk.DISABLED)
        self.threshold_slider.set(100)  # Initial threshold value
        self.threshold_slider.pack()

        self.is_playing = False
        self.update_video()

    def open_file(self):
        file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video Files", "*.mp4 *.avi")])
        if file_path:
            self.video_source = file_path
            self.cap = cv2.VideoCapture(self.video_source)
            self.btn_start.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.NORMAL)
            self.btn_save.config(state=tk.NORMAL)
            self.threshold_slider.config(state=tk.NORMAL)

    def update_video(self):
        if self.is_playing and self.cap is not None:
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

    def save_frame(self):
        ret, frame = self.cap.read()
        if ret:
            processed_frame = self.process_frame(frame)
            cv2.imwrite("processed_frame.jpg", processed_frame)
            print("Processed frame saved as 'processed_frame.jpg'")

    def update_threshold(self, value):
        # Threshold slider callback function
        pass  # Update processing parameters here if needed

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()
