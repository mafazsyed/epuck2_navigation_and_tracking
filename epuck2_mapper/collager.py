import os
from moviepy.editor import ImageSequenceClip
import re

# Define the parameters
folder_path = r"path\to\input\folder" # Change this to your folder's path
output_video = routput_video = r"path\to\putput\folder.mp4"
fps = 10  # 1 image per second

# Function to sort filenames based on numerical order
def sort_files(file):
    numbers = re.findall(r'\d+', file)
    if numbers:
        return int(numbers[0])
    return file

# Fetch all image paths in the folder (assuming they're all .png for simplicity)
image_files = os.listdir(folder_path)
sorted_image_files = sorted(image_files, key=sort_files)
image_paths = [os.path.join(folder_path, img) for img in sorted_image_files if img.endswith('.png')]

# Create video from images
clip = ImageSequenceClip(image_paths, fps=fps)
clip.write_videofile(output_video, fps=fps)

print(f"Video saved as {output_video}")