# sensor_mapping.py
import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple
import os

# Given data
sensor_angles = [30, 37.5, 52.5, 60, 60, 52.5, 37.5, 30]
cumulative_angles = [0] + [sum(sensor_angles[:i+1]) for i in range(len(sensor_angles))]

# Define the LUT
LUT = namedtuple('LUT', ['reading', 'distance'])
lut_data = [
    LUT(10, 7),
    LUT(67.19, 7),
    LUT(104.09, 6),
    LUT(120.0, 5),
    LUT(158.03, 4),
    LUT(234.93, 3),
    LUT(383.84, 2),
    LUT(601.46, 1.5),
    LUT(1465.63, 1),
    LUT(2133.33, 0.5),
    LUT(4095.00, 0)
]

def get_distance_from_reading(reading):
    for i in range(len(lut_data) - 1):
        # If the reading is within the range of two consecutive LUT entries
        if lut_data[i].reading <= reading <= lut_data[i+1].reading:
            # Linear interpolation
            slope = (lut_data[i+1].distance - lut_data[i].distance) / (lut_data[i+1].reading - lut_data[i].reading)
            return lut_data[i].distance + slope * (reading - lut_data[i].reading)
    # If the reading is not in the range of the LUT
    if reading > lut_data[-1].reading:
        return 0
    if reading < lut_data[0].reading:
        return lut_data[0].distance
    
def draw_sector(ax, start_angle, end_angle, distance):  # Added ax as the first parameter
    if distance == 7:
        return  # Skip plotting for 7cm values
    
    theta = np.linspace(np.radians(start_angle), np.radians(end_angle), 100)
    
    max_distance = max([lut.distance for lut in lut_data])
    r = np.linspace(distance, max_distance, 100)  # Adjusted r range
    
    X, Y = np.meshgrid(r, theta)
    X = X.flatten()
    Y = Y.flatten()
    
    x = X * np.sin(Y)
    y = X * np.cos(Y)
    
    colors = plt.cm.Reds((max_distance - X.flatten()) / max_distance)    
    ax.scatter(x, y, color=colors, s=2)  # s is the size of the points

def read_sensor_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    sensor_data = [line.strip().split(':') for line in lines]
    sensor_data = [int(value) for _, value in sensor_data]
    return [sensor_data[i:i+8] for i in range(0, len(sensor_data), 8)]

def save_plot(sensor_distances, output_folder, dataset_num):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')

    for i in range(len(sensor_angles)):
        draw_sector(ax, cumulative_angles[i], cumulative_angles[i+1], sensor_distances[i])
        mid_angle = (cumulative_angles[i] + cumulative_angles[i+1]) / 2
        x_text = 8 * np.sin(np.radians(mid_angle))
        y_text = 8 * np.cos(np.radians(mid_angle))
        
        # Change text color to red if distance is below 2.7 cm
        text_color = 'red' if sensor_distances[i] < 2.7 else 'black'
        
        # Check if the distance is 7cm, and display "7+" if it is
        if sensor_distances[i] == 7:
            ax.text(x_text, y_text, f'{i} (7+cm)', fontsize=9, ha='center', color=text_color)
        else:
            ax.text(x_text, y_text, f'{i} ({sensor_distances[i]:.1f}cm)', fontsize=9, ha='center', color=text_color)

    # Draw robot representation
    robot_radius = 0.2  # Adjust as needed
    robot_circle = plt.Circle((0, 0), robot_radius, color='blue', fill=True)
    ax.add_patch(robot_circle)

    # Draw direction arrow
    arrow_length = 0.4  # Adjust as needed
    ax.arrow(0, 0, 0, arrow_length, head_width=0.35, head_length=0.35, fc='blue', ec='blue')

    plt.title('Gradient Environment Indicator - Dataset {}'.format(dataset_num))
    plt.xlabel('X Distance (cm)')
    plt.ylabel('Y Distance (cm)')
    plt.grid(True)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    plt.savefig(os.path.join(output_folder, 'plot_dataset_{}.png'.format(dataset_num)))
    plt.close()

def main():
    sensor_readings_file = r"D:\Drive D Documents\Mafaz\Academic\School\University\Sheffield University\MSc\Robotics\Modules\Foundation of Robotics\epuck2\epuck_mapper_6\webots_data_reduced.txt"
    output_folder = r"D:\Drive D Documents\Mafaz\Academic\School\University\Sheffield University\MSc\Robotics\Modules\Foundation of Robotics\epuck2\epuck_mapper_6\graphs3"
    
    all_sensor_readings = read_sensor_data(sensor_readings_file)
    for i, sensor_readings in enumerate(all_sensor_readings):
        sensor_distances = [get_distance_from_reading(reading) for reading in sensor_readings]
        save_plot(sensor_distances, output_folder, i + 1)

def run_sensor_mapping(input_file, output_folder):
    all_sensor_readings = read_sensor_data(input_file)
    for i, sensor_readings in enumerate(all_sensor_readings):
        sensor_distances = [get_distance_from_reading(reading) for reading in sensor_readings]
        save_plot(sensor_distances, output_folder, i + 1)

if __name__ == '__main__':
    input_file = r"D:\Drive D Documents\Mafaz\Academic\School\University\Sheffield University\MSc\Robotics\Modules\Foundation of Robotics\epuck2\epuck2_mapper_manual2\In Lab\task1_2.txt"
    output_folder = r"D:\Drive D Documents\Mafaz\Academic\School\University\Sheffield University\MSc\Robotics\Modules\Foundation of Robotics\epuck2\epuck2_mapper_manual2\graphs_new2"
    run_sensor_mapping(input_file, output_folder)