import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def get_path():
    path = input("Please enter the path to your log files (e.g.: C:\\Users\\<username>\\<path>\\<to>\\<files>): ")
    if not os.path.exists(path):
        print("That path does not exist.")
        path = get_path()
    return path

def get_gear():
    try:
        gears = int(input("Please enter the number of gears you would like to graph (must an integer >=1): "))
    except:
        print("Invalid entry")
        gears = get_gear()
    if gears < 1:
        print("Please enter a number > 1.")
        gears = get_gear()
    return gears

def make_graph(y_axis, path, gears):
    # Create dictionary to store plots for each gear
    plots = []
    for i in range(gears):
        plots.append([])

    fig = make_subplots(rows=gears, cols=1, subplot_titles=tuple([f"Gear {i}" for i in range(1, gears+1)]), x_title="Engine Speed (RPM)", y_title=y_axis)

    for filename in os.listdir(path):
        if filename.endswith(".csv"):
            filepath = os.path.join(path, filename)
            df = pd.read_csv(filepath)
            gear = 'Gear[-] [DME]' if 'Gear[-] [DME]' in df else 'Gear[-]'
            speed = 'Engine speed[1/min] [DME]' if 'Engine speed[1/min] [DME]' in df else 'Engine speed[1/min]'
            boost = y_axis if y_axis in df else 'Boost (Pre-Throttle)[psig] [DME]'
            for i in range(1, gears+1):
                try:
                    tmp = df[df[gear] == i]
                    if len(tmp) > 0:
                        plots[i-1].append(go.Scatter(x=list(tmp[speed]),
                                                        y=list(tmp[boost]),
                                                        mode='lines',
                                                        name=filename[43:-12],
                                                        showlegend=False))
                except Exception as e:
                    print(e)
    for i in range(1, gears+1):
        for x in range(len(plots[i-1])):
            fig.add_trace(plots[i-1][x], row=i, col=1)

        fig.update_layout(title=f"{y_axis} vs Engine Speed by Gear",
                         height=400*gears
                        )
    fig.write_html(f"{path}\\{y_axis}.html")
    
y_axes = ["Boost (Pre-Throttle)[psig]", "Boost pressure (Target)[psig]", "IAT[F]", "Ignition Cyl 1[deg]", "Ignition Timing 1[deg]", "Ignition Timing 2[deg]", "Ignition Timing 3[deg]", "Ignition Timing 4[deg]", "Knock detected[0-n]", "Lambda[AFR]"]
path = get_path()
gears = get_gear()
for i in y_axes:
    make_graph(i, path, gears)