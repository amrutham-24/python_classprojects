import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class ObjectDetectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection System")
        self.root.geometry("1050x700")
        self.root.configure(bg="#1E1E2E")
        
        # Style configuration for ttk widgets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TScale", background="#313244", troughcolor="#181825", slidercolor="#89B4FA", bordercolor="#313244")
        
        self.original_image = None
        self.processed_image = None
        self.display_image = None
        
        # Transformations
        self.scale_factor = tk.DoubleVar(value=1.0)
        self.angle = tk.DoubleVar(value=0.0)
        
        # -------- TITLE --------
        title_frame = tk.Frame(root, bg="#1E1E2E")
        title_frame.pack(fill="x", pady=(20, 10))
        
        title = tk.Label(title_frame, text="Vision", font=("Segoe UI", 28, "bold"), bg="#1E1E2E", fg="#89B4FA")
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Interactive Object & Color Detection", font=("Segoe UI", 12), bg="#1E1E2E", fg="#A6ADC8")
        subtitle.pack()

        # -------- MAIN CONTENT --------
        self.main_frame = tk.Frame(root, bg="#1E1E2E")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel for buttons
        self.control_panel = tk.Frame(self.main_frame, bg="#313244", bd=0, relief="flat", padx=20, pady=10)
        self.control_panel.pack(side="left", fill="y", padx=(0, 20))
        
        # Right panel for image
        self.image_frame = tk.Frame(self.main_frame, bg="#181825", bd=0, relief="flat")
        self.image_frame.pack(side="right", fill="both", expand=True)
        self.image_frame.grid_propagate(False) # Prevent window from expanding when image scales up
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)
        
        self.panel = tk.Label(self.image_frame, bg="#181825", text="No Image Uploaded\nUpload an image to start", fg="#585B70", font=("Segoe UI", 16))
        self.panel.grid(row=0, column=0, sticky="nsew")

        # -------- CONTROLS --------
        lbl_controls = tk.Label(self.control_panel, text="Controls", font=("Segoe UI", 16, "bold"), bg="#313244", fg="#CDD6F4")
        lbl_controls.pack(pady=(0, 15))

        # Upload & Reset Buttons
        upload_frame = tk.Frame(self.control_panel, bg="#313244")
        upload_frame.pack(fill="x", pady=8)
        
        # "➕ Upload New Image" with an icon
        self.create_button("➕ Upload New Image", self.upload_image, "#A6E3A1", "#11111B", parent=upload_frame).pack(fill="x")
        self.create_button("↺ Reset Image & Sliders", self.reset_image, "#94E2D5", "#11111B").pack(fill="x", pady=(0, 15))
        
        # Detection Buttons
        self.create_button("Detect Shapes", self.detect_shapes, "#89B4FA", "#11111B").pack(fill="x", pady=8)
        self.create_button("Detect Colors", self.detect_color, "#F38BA8", "#11111B").pack(fill="x", pady=8)
        
        # Sliders Frame
        slider_frame = tk.Frame(self.control_panel, bg="#313244")
        slider_frame.pack(fill="x", pady=20)
        
        # Rotation Slider
        self.lbl_angle = tk.Label(slider_frame, text="Rotation Angle: 0°", font=("Segoe UI", 10), bg="#313244", fg="#A6ADC8")
        self.lbl_angle.pack(anchor="w")
        ttk.Scale(slider_frame, from_=0, to=360, variable=self.angle, command=self.apply_transformations).pack(fill="x", pady=(0, 10))
        
        # Scale Slider
        self.lbl_scale = tk.Label(slider_frame, text="Scale Factor: 1.0 (100%)", font=("Segoe UI", 10), bg="#313244", fg="#A6ADC8")
        self.lbl_scale.pack(anchor="w")
        ttk.Scale(slider_frame, from_=0.0, to=2.0, variable=self.scale_factor, command=self.apply_transformations).pack(fill="x")

        # Trace variables to update numbers live
        self.angle.trace_add("write", lambda *args: self.lbl_angle.config(text=f"Rotation Angle: {int(self.angle.get())}°"))
        self.scale_factor.trace_add("write", lambda *args: self.lbl_scale.config(text=f"Scale Factor: {self.scale_factor.get():.1f} ({int(self.scale_factor.get()*100)}%)"))

        # -------- FOOTER --------
        tk.Label(root, text="Developed with OpenCV & Tkinter", font=("Segoe UI", 10), bg="#1E1E2E", fg="#585B70").pack(side="bottom", pady=10)
        
    def create_button(self, text, command, bg_color, fg_color, parent=None):
        if parent is None:
            parent = self.control_panel
        def on_enter(e):
            e.widget['background'] = '#FFFFFF'
        def on_leave(e):
            e.widget['background'] = bg_color

        btn = tk.Button(parent, text=text, command=command,
                        font=("Segoe UI", 11, "bold"), bg=bg_color, fg=fg_color,
                        activebackground="#FFFFFF", activeforeground=fg_color,
                        bd=0, padx=15, pady=8, cursor="hand2", relief="flat")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def display(self, img, scale_factor=1.0):
        if img is None:
            return
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        
        self.root.update_idletasks()
        frame_width = self.image_frame.winfo_width()
        frame_height = self.image_frame.winfo_height()
        
        if frame_width < 100: frame_width = 700
        if frame_height < 100: frame_height = 500
        
        # Calculate fit ratio for 1.0 scale
        orig_w, orig_h = img_pil.size
        fit_ratio = min((frame_width - 20) / max(1, orig_w), (frame_height - 20) / max(1, orig_h))
        if fit_ratio > 1.0:
            fit_ratio = 1.0 # Don't stretch small images by default at 1.0 scale
            
        base_w = int(orig_w * fit_ratio)
        base_h = int(orig_h * fit_ratio)
        
        # Apply user scale factor
        final_w = int(base_w * scale_factor)
        final_h = int(base_h * scale_factor)
        
        if final_w > 0 and final_h > 0:
            img_pil = img_pil.resize((final_w, final_h), Image.Resampling.LANCZOS)
        
        imgtk = ImageTk.PhotoImage(img_pil)
        self.panel.config(image=imgtk, text="")
        self.panel.image = imgtk

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if path:
            self.original_image = cv2.imread(path)
            self.processed_image = self.original_image.copy()
            self.reset_transformations()
            self.apply_transformations()
            
    def reset_transformations(self):
        self.scale_factor.set(1.0)
        self.angle.set(0.0)

    def reset_image(self):
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.reset_transformations()
            self.apply_transformations()

    def detect_shapes(self):
        if self.original_image is None:
            return
            
        img = self.original_image.copy()
        
        # Improve edge detection for light colors (like yellow) on light backgrounds
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        s_channel = hsv[:, :, 1]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Combine edges from grayscale and saturation to catch all colors
        blur_gray = cv2.GaussianBlur(gray, (5, 5), 0)
        blur_s = cv2.GaussianBlur(s_channel, (5, 5), 0)
        
        edges_gray = cv2.Canny(blur_gray, 50, 150)
        edges_s = cv2.Canny(blur_s, 20, 100) # Lower threshold for saturation to catch faint colors
        
        # Combine both edges to ensure nothing is missed
        edges = cv2.bitwise_or(edges_gray, edges_s)
        
        # Morphological closing to connect broken edges
        kernel = np.ones((5,5), np.uint8)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Extract true background by masking out all detected objects
        bg_mask = np.ones(gray.shape, dtype=np.uint8) * 255
        for cnt in contours:
            if cv2.contourArea(cnt) > 100:
                cv2.drawContours(bg_mask, [cnt], -1, 0, -1)
                
        bg_brightness = cv2.mean(gray, mask=bg_mask)[0]
        
        # If bright background, use black outline with white text, else white outline with black text
        if bg_brightness > 127:
            box_color = (0, 0, 0)      # Black bounding box on light BG
            text_color = (255, 255, 255) # White text
        else:
            box_color = (255, 255, 255) # White bounding box on dark BG
            text_color = (0, 0, 0)       # Black text

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                peri = cv2.arcLength(cnt, True)
                # Slightly looser tolerance to catch triangles more reliably
                approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                
                sides = len(approx)
                shape = "Polygon"
                if sides == 3:
                    shape = "Triangle"
                elif sides == 4:
                    rect = cv2.minAreaRect(cnt)
                    rect_w, rect_h = rect[1]
                    if rect_h > 0 and rect_w > 0:
                        ratio = rect_w / float(rect_h)
                        shape = "Square" if 0.85 <= ratio <= 1.15 else "Rectangle"
                    else:
                        shape = "Rectangle"
                elif sides == 5:
                    shape = "Pentagon"
                elif sides == 6:
                    shape = "Hexagon"
                elif sides > 6:
                    # check circularity to distinguish from circle
                    circularity = 4 * np.pi * (area / (peri * peri))
                    if circularity > 0.85:
                        shape = "Circle"
                    else:
                        shape = f"Polygon ({sides})"

                # Draw smooth circle or exact polygon contour
                if shape == "Circle":
                    (cx, cy), radius = cv2.minEnclosingCircle(cnt)
                    cv2.circle(img, (int(cx), int(cy)), int(radius), box_color, 3)
                else:
                    cv2.drawContours(img, [approx], -1, box_color, 3)
                
                (text_width, text_height), _ = cv2.getTextSize(shape, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                cv2.rectangle(img, (x, y - text_height - 10), (x + text_width + 10, y), box_color, -1)
                
                cv2.putText(img, shape, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)

        self.processed_image = img
        self.apply_transformations()

    def detect_color(self):
        if self.original_image is None:
            return
            
        img = self.original_image.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Define color ranges: Red, Orange, Yellow, Green, Blue, Violet
        colors = {
            "Red": [
                [np.array([0, 100, 100]), np.array([10, 255, 255])],
                [np.array([170, 100, 100]), np.array([180, 255, 255])]
            ],
            "Orange": [[np.array([11, 100, 100]), np.array([25, 255, 255])]],
            "Yellow": [[np.array([26, 100, 100]), np.array([35, 255, 255])]],
            "Green": [[np.array([36, 50, 50]), np.array([85, 255, 255])]],
            "Blue": [[np.array([86, 100, 0]), np.array([130, 255, 255])]],
            "Violet": [[np.array([131, 100, 50]), np.array([169, 255, 255])]]
        }
        
        # Gather all color masks combined to find the global background brightness
        mask_all = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for c_name, ranges in colors.items():
            for lower, upper in ranges:
                mask_all |= cv2.inRange(hsv, lower, upper)
                
        contours_all, _ = cv2.findContours(mask_all, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Mask out colored objects to measure real background
        bg_mask = np.ones(gray.shape, dtype=np.uint8) * 255
        for cnt in contours_all:
            if cv2.contourArea(cnt) > 500:
                cv2.drawContours(bg_mask, [cnt], -1, 0, -1)
                
        bg_brightness = cv2.mean(gray, mask=bg_mask)[0]
        
        # Black boundary for bright backgrounds, White boundary for dark backgrounds
        if bg_brightness > 127:
            box_color = (0, 0, 0)
            text_color = (255, 255, 255)
        else:
            box_color = (255, 255, 255)
            text_color = (0, 0, 0)

        for c_name, ranges in colors.items():
            mask = None
            for lower, upper in ranges:
                if mask is None:
                    mask = cv2.inRange(hsv, lower, upper)
                else:
                    mask |= cv2.inRange(hsv, lower, upper)
                    
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 500:
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
                    x, y, w, h = cv2.boundingRect(approx)
                    
                    sides = len(approx)
                    is_circle = False
                    if sides > 6:
                        circularity = 4 * np.pi * (area / (peri * peri))
                        if circularity > 0.85:
                            is_circle = True
                            
                    if is_circle:
                        (cx, cy), radius = cv2.minEnclosingCircle(cnt)
                        cv2.circle(img, (int(cx), int(cy)), int(radius), box_color, 3)
                    else:
                        cv2.drawContours(img, [approx], -1, box_color, 3)
                    
                    (text_width, text_height), _ = cv2.getTextSize(c_name, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                    cv2.rectangle(img, (x, y - text_height - 10), (x + text_width + 10, y), box_color, -1)
                    
                    cv2.putText(img, c_name, (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)

        self.processed_image = img
        self.apply_transformations()

    def apply_transformations(self, *args):
        if self.processed_image is None:
            return

        img = self.processed_image.copy()
        scale = self.scale_factor.get()
        angle = self.angle.get()

        # 1. We no longer physical scale the image array since display() handles zooming properly
        # This preserves the original resolution when rotating and zooming in
        
        # 2. Rotate
        if angle != 0.0:
            h, w = img.shape[:2]
            center = (w / 2, h / 2)
            matrix = cv2.getRotationMatrix2D(center, -angle, 1.0) # Negative angle for counter-clockwise
            
            # Canvas bounds to contain whole image
            abs_cos = abs(matrix[0, 0])
            abs_sin = abs(matrix[0, 1])
            bound_w = int(h * abs_sin + w * abs_cos)
            bound_h = int(h * abs_cos + w * abs_sin)
            
            matrix[0, 2] += bound_w / 2 - center[0]
            matrix[1, 2] += bound_h / 2 - center[1]
            
            img = cv2.warpAffine(img, matrix, (bound_w, bound_h), borderValue=(37, 24, 24))

        self.display_image = img
        self.display(self.display_image, scale_factor=scale)

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectDetectionGUI(root)
    root.mainloop()
