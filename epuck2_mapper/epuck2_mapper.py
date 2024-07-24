import tkinter as tk
from tkinter import filedialog
import sensor_mapping
import sensor_mapping_old
from moviepy.editor import ImageSequenceClip
import re
import os
from tkinter import filedialog, messagebox

class SensorMappingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("epuck2 IR Mapper")
        self.geometry("500x375")

        self.create_widgets()

    def create_widgets(self):
        self.heading_label = tk.Label(self, text="epuck2 Gradient Environment Mapping - Team 2N", font=("Calibri", 14, "bold"))
        self.heading_label.pack(pady=10)

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(pady=5)

        self.input_label = tk.Label(self.input_frame, text="Input Sensor Readings")
        self.input_label.pack(side="left")

        self.input_entry = tk.Entry(self.input_frame, width=40)
        self.input_entry.pack(side="left", padx=5)

        self.browse_button = tk.Button(self.input_frame, text="Browse", command=self.browse_input)
        self.browse_button.pack(side="right")

        self.output_frame = tk.Frame(self)
        self.output_frame.pack(pady=5)

        self.output_label = tk.Label(self.output_frame, text="Output Plots Folder:")
        self.output_label.pack(side="left")

        self.output_entry = tk.Entry(self.output_frame, width=40)
        self.output_entry.pack(side="left", padx=5)

        self.browse_button = tk.Button(self.output_frame, text="Browse", command=self.browse_output)
        self.browse_button.pack(side="right")

        self.run_button = tk.Button(self, text="Generate Plots", command=self.run_sensor_mapping)
        self.run_button.pack(pady=10)

        self.mapping_method_frame = tk.Frame(self)
        self.mapping_method_frame.pack(pady=5)

        self.mapping_method_label = tk.Label(self.mapping_method_frame, text="Select Mapping Method:")
        self.mapping_method_label.pack(side="left")

        self.mapping_method_var = tk.StringVar(value="Environment Indicator")
        self.mapping_method_dropdown = tk.OptionMenu(self.mapping_method_frame, self.mapping_method_var, "Environment Indicator", "Heatmap")
        self.mapping_method_dropdown.pack(side="left", padx=5)
        
        self.image_folder_frame = tk.Frame(self)
        self.image_folder_frame.pack(pady=5)

        self.image_folder_label = tk.Label(self.image_folder_frame, text="Plots Folder:")
        self.image_folder_label.pack(side="left")

        self.image_folder_entry = tk.Entry(self.image_folder_frame, width=40)
        self.image_folder_entry.pack(side="left", padx=5)

        self.browse_image_folder_button = tk.Button(self.image_folder_frame, text="Browse", command=self.browse_image_folder)
        self.browse_image_folder_button.pack(side="right")

        self.output_video_frame = tk.Frame(self)
        self.output_video_frame.pack(pady=5)

        self.output_video_label = tk.Label(self.output_video_frame, text="Output Video Path:")
        self.output_video_label.pack(side="left")

        self.output_video_entry = tk.Entry(self.output_video_frame, width=40)
        self.output_video_entry.pack(side="left", padx=5)

        self.browse_output_video_button = tk.Button(self.output_video_frame, text="Browse", command=self.browse_output_video)
        self.browse_output_video_button.pack(side="right")

        self.fps_frame = tk.Frame(self)
        self.fps_frame.pack(pady=5)

        self.fps_label = tk.Label(self.fps_frame, text="Frames Per Second:")
        self.fps_label.pack(side="left")

        self.fps_entry = tk.Entry(self.fps_frame, width=5)
        self.fps_entry.pack(side="left", padx=5)

        self.create_video_button = tk.Button(self, text="Create Video", command=self.create_video)
        self.create_video_button.pack(pady=10)


    def browse_input(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, filepath)

    def browse_output(self):
        folderpath = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, folderpath)

    def run_sensor_mapping(self):
        input_file = self.input_entry.get()
        output_folder = self.output_entry.get()
        mapping_method = self.mapping_method_var.get()
        
        try:
            if mapping_method == "Environment Indicator":
                sensor_mapping.run_sensor_mapping(input_file, output_folder)
            elif mapping_method == "Heatmap":
                sensor_mapping_old.run_sensor_mapping(input_file, output_folder)  # Corrected function call
                
            messagebox.showinfo("Success", "Plots have been generated and saved to {}".format(output_folder))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def browse_image_folder(self):
        folderpath = filedialog.askdirectory()
        self.image_folder_entry.delete(0, tk.END)
        self.image_folder_entry.insert(0, folderpath)

    def browse_output_video(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        self.output_video_entry.delete(0, tk.END)
        self.output_video_entry.insert(0, filepath)

    def sort_files(self, file):
        numbers = re.findall(r'\d+', file)
        if numbers:
            return int(numbers[0])
        return file

    def create_video(self):
        image_folder = self.image_folder_entry.get()
        output_video = self.output_video_entry.get()
        try:
            fps = float(self.fps_entry.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid number for FPS.")
            return
        
        image_files = os.listdir(image_folder)
        sorted_image_files = sorted(image_files, key=self.sort_files)
        image_paths = [os.path.join(image_folder, img) for img in sorted_image_files if img.endswith('.png')]
        
        clip = ImageSequenceClip(image_paths, fps=fps)
        clip.write_videofile(output_video, fps=fps)
        
        tk.messagebox.showinfo("Success", f"Video saved as {output_video}")

app = SensorMappingApp()
app.mainloop()