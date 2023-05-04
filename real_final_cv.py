import cv2
from tkinter import ttk
from PIL import Image, ImageTk
import PIL.Image

# Import required Libraries
from tkinter import *

import customtkinter as ctk

import numpy as np
import mediapipe as mp

from PIL import Image as Img
from PIL import ImageTk
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class WebcamApp:
    def __init__(self, window):
        self.window = window
        self.window.title("AI-Webcam-gym")
        self.window.iconbitmap('gym2.ico')
        self.counter = 0 
        self.stage = None
        self.counter1 = 0 
        self.stage1 = None

        # Create main frame with title and subtitle
        main_frame = ttk.Frame(self.window, padding=20, style="Main.TFrame")
        main_frame.pack(fill=BOTH, expand=True)

        title = ttk.Label(main_frame, text="Webcam Gym", font=("Helvetica", 18, "bold"), style="Title.TLabel")
        title.pack()
        
        title1 = ttk.Label(main_frame, text="Position your body 8 feet away from the webcam.", font=("Helvetica", 8, "bold"), style="Subtitle.TLabel")
        title1.pack()


        # Create button to open webcam
        self.btn = ttk.Button(main_frame, text="Open Webcam", command=self.open_webcam, style="Button.TButton")
        self.btn.pack(pady=10)
        
        # Create button to release webcam
        self.btn = ttk.Button(main_frame, text="release Webcam", command=self.close_webcam, style="Button.TButton")
        self.btn.pack(pady=10)

        # Create label to display video feed
        self.label = ttk.Label(main_frame, style="Video.TLabel")
        self.label.pack(fill=BOTH, expand=True)

        # Initialize video capture variables
        self.video_capture = None
        self.video_width = None
        self.video_height = None

    def open_webcam(self):
        self.video_capture = cv2.VideoCapture(0)
        self.video_width = int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.update_frame()
    
    ##################################
    def close_webcam(self):
        self.video_capture.release()
        self.video_capture.destroyAllWindows()
        
        
    def calculate_angle(self,a,b,c):
        self.a = np.array(a) # First
        self.b = np.array(b) # Mid
        self.c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle 

    def update_frame(self):
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            cv2image= cv2.cvtColor(self.video_capture.read()[1],cv2.COLOR_BGR2RGB)
            
            cv2image.flags.writeable = False
            
            # Make detection
            results = pose.process(cv2image)

            # Recolor back to BGR
            cv2image.flags.writeable = True
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                
                # Get coordinates
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                
                shoulder2 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow2 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrist2 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                
                
                
                # Calculate angle
                angle = self.calculate_angle(shoulder, elbow, wrist)
                
                # Calculate angle2
                angle2 = self.calculate_angle(shoulder2, elbow2, wrist2)
                
                # Visualize angle
                cv2.putText(cv2image, str(angle), 
                               tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                
                
                # Visualize angle2
                cv2.putText(cv2image, str(angle2), 
                               tuple(np.multiply(elbow2, [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                    )
                # Curl counter logic
                if angle > 160:
                    self.stage = "down"
                if angle < 30 and self.stage =='down':
                    self.stage="up"
                    self.counter +=1
                    print(self.counter)
                    
            
                if angle2 > 160:
                    self.stage1 = "down"
                if angle2 < 30 and self.stage1 =='down':
                    self.stage1="up"
                    self.counter1 +=1
                    print(self.counter1)
                   
                           
            except:
                pass
            
            # Render curl counter
            # Setup status box
            cv2.rectangle(cv2image, (0,0), (225,73), (245,117,16), -1)
            
            # Rep data
            cv2.putText(cv2image, 'Left', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(cv2image, str(self.counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(cv2image, 'Sholder', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(cv2image, self.stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            
            # Render detections
            mp_drawing.draw_landmarks(cv2image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )      
            
            
            ##########################################500,700,16
            cv2.rectangle(cv2image, (700,70), (370,0), (245,117,16), -1)
            
            cv2.putText(cv2image, 'Right', (495,12),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (10,7,0), 1, cv2.LINE_AA)
            cv2.putText(cv2image, str(self.counter1),(430,60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(cv2image, 'Sholder', (545,12),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(cv2image, self.stage1,(480,60),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            img = Img.fromarray(cv2image)
            # Convert image to PhotoImage
            imgtk = ImageTk.PhotoImage(image = img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
            # Repeat after an interval to capture continiously
            self.label.after(20, self.update_frame)
       
 
            
        

if __name__ == '__main__':
    window = Tk()
    window.geometry("685x700")
    window.configure(bg="black")

    # Create custom styles for widgets
    style = ttk.Style()

    # Main frame style
    style.configure("Main.TFrame", background="black")

    # Title label style
    style.configure("Title.TLabel", foreground="black",padding=4)

    # Subtitle label style
    style.configure("Subtitle.TLabel", foreground="#757575",padding=3)

    # Button style
    style.configure("Button.TButton", foreground="black", background="black")

    # Video feed label style
    style.configure("Video.TLabel", background="grey")

    # Add image to GUI
    img = ImageTk.PhotoImage(PIL.Image.open("3131.jpg"))
    img_label = ttk.Label(window, image=img, padding=10)
    img_label.pack(side=TOP)

    app = WebcamApp(window)
    
    window.mainloop()
