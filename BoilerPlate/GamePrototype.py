#vectorgame.py
import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path
import tkinter as tk
from tkinter import simpledialog
valid_spaces_file = Path("valid_spaces.json")
valid_spaces_file.touch(exist_ok=True)
valid_loops_file = Path("valid_loops.json")
valid_loops_file.touch(exist_ok=True)
clicks_file = Path("clicks.json")
clicks_file.touch(exist_ok=True)
def get_surrounding_triangles(triangle_vertices):
    midpoints = np.zeros((3, 2))
    for i in range(3):
        midpoints[i] = (triangle_vertices[i] + triangle_vertices[(i + 1) % 3]) / 2
    surrounding_triangles = np.zeros((4, 3, 2))
    for i in range(3):
        surrounding_triangles[i] = np.vstack((triangle_vertices[i], midpoints[i], midpoints[(i - 1) % 3]))
    surrounding_triangles[3] = midpoints
    return surrounding_triangles
def plot_triangle(ax, triangle_vertices):
    theta = np.arctan2(triangle_vertices[:, 1], triangle_vertices[:, 0])
    r = np.sqrt(triangle_vertices[:, 0]**2 + triangle_vertices[:, 1]**2)
    ax.plot(np.append(theta, theta[0]), np.append(r, r[0]), 'k-')
    ax.fill(theta, r, alpha=0.3)
    # save r theta pairs to JSON file
    with open('valid_spaces.json', 'a') as f:
        for i in range(3):
            json.dump({'r': r[i], 'theta': theta[i]}, f)
            f.write('\n')
    # Save polar coordinates of each vertex to JSON file
    with open('valid_loops.json', 'a') as f:
        vertices = [{'r': r[i], 'theta': theta[i]} for i in range(3)]
        json.dump({'vertices': vertices}, f)
        f.write('\n')
def plot_tessellation(ax):
    r = 1
    theta = np.linspace(0, 2 * np.pi, 4)[:-1] + np.pi / 6
    vertices = np.zeros((3, 2))
    vertices[:, 0] = r * np.cos(theta)
    vertices[:, 1] = r * np.sin(theta)
    depth = 3
    triangles_to_plot = [vertices]
    all_vertices = []  # keep track of all vertices generated
    for _ in range(depth):
        new_triangles = []
        for triangle in triangles_to_plot:
            new_triangles.extend(get_surrounding_triangles(triangle))
            all_vertices.extend(triangle.tolist())
        triangles_to_plot = new_triangles
    for triangle in triangles_to_plot:
        plot_triangle(ax, triangle)
def load_valid_spaces():
    vertices = []
    with open('valid_spaces.json', 'r') as f:
        for line in f:
            vertex = json.loads(line)
            vertices.append((vertex['r'], vertex['theta']))
    return vertices
def load_valid_loops():
    loops = []
    with open('valid_loops.json', 'r') as f:
        for line in f:
            loop = json.loads(line)
            loops.append(loop['vertices'])
    return loops
def load_clicks():
    with open('clicks.json', 'r') as f:
        clicks = [json.loads(line) for line in f]
    return clicks
def find_nearest_valid_space(r, theta, valid_spaces):
    min_distance = float('inf')
    nearest_vertex = None
    for vertex in valid_spaces:
        vertex_r, vertex_theta = vertex
        delta_theta = vertex_theta - theta
        if delta_theta > np.pi:
            delta_theta -= 2 * np.pi
        elif delta_theta < -np.pi:
            delta_theta += 2 * np.pi
        distance = np.sqrt((r - vertex_r)**2 + delta_theta**2)
        if distance < min_distance:
            min_distance = distance
            nearest_vertex = vertex
    return nearest_vertex
def load_points():
    points = []
    with open('clicks.json', 'r') as f:
        for line in f:
            point = json.loads(line)
            points.append((point['address'][0], point['address'][1]))
    return points
def load_valid_loops2():
    with open('valid_loops.json', 'r') as f:
        valid_loops = [json.loads(line) for line in f]
    return valid_loops
def count_unique_vectors(filename):
    with open(filename, 'r') as f:
        unique_vectors = set()
        for line in f:
            vector = json.loads(line)
            unique_vectors.add((vector['r'], vector['theta']))
    return len(unique_vectors)
def popup_message(message):
    root = tk.Tk()
    root.withdraw()
    simpledialog.messagebox.showinfo(title="Game Over", message=message)
def reset_clicks_file():
    with open('clicks.json', 'w') as f:
        pass
def check_end_game(num_clicks, unique_vectors_count, high_score):
    if num_clicks >= unique_vectors_count:
        red_score, blue_score = calculate_scores(get_loop_colors(find_formed_loops(load_clicks(), load_valid_loops2()), load_clicks()))
        winner = ''
        if high_score:
            if red_score > blue_score:
                winner = 'Red'
            elif blue_score > red_score:
                winner = 'Blue'
            else:
                winner = 'Tie'
        else:
            if red_score < blue_score:
                winner = 'Red'
            elif blue_score < red_score:
                winner = 'Blue'
            else:
                winner = 'Tie'
        popup_message(f"{winner} has won the game!")
        reset_clicks_file()
def is_valid_loop(points, valid_loops):
    for loop in valid_loops:
        loop_points = set((point['r'], point['theta']) for point in loop['vertices'])
        if set(tuple(point) for point in points) == loop_points:
            return True
    return False
def find_formed_loops(clicks, valid_loops):
    formed_loops = []
    click_points = [click['address'] for click in clicks]
    for i in range(len(click_points)):
        for j in range(i + 1, len(click_points)):
            for k in range(j + 1, len(click_points)):
                points = [click_points[i], click_points[j], click_points[k]]
                if is_valid_loop(points, valid_loops):
                    formed_loops.append(points)
    return formed_loops
def vector_color(r, theta, clicks):
    for click in clicks:
        click_r, click_theta = click['address']
        if click_r == r and click_theta == theta:
            return click['color']
    return None
def get_loop_colors(formed_loops, clicks):
    loop_colors = []
    for loop in formed_loops:
        colors = [vector_color(r, theta, clicks) for r, theta in loop]
        loop_colors.append("".join(colors))
    return loop_colors
def calculate_scores(loop_colors):
    red_score = 0
    blue_score = 0
    for color_pattern in loop_colors:
        if color_pattern == 'redredred':
            red_score -= 1
            blue_score += 1
        elif color_pattern == 'blueblueblue':
            red_score += 1
            blue_score -= 1
        elif color_pattern in ('redbluered', 'blueredred'):
            red_score += 1
        elif color_pattern in ('redblueblue', 'blueredblue'):
            blue_score += 1
        elif color_pattern == 'bluebluered':
            red_score += 2
        elif color_pattern == 'redredblue':
            blue_score += 2
    return red_score, blue_score
def truncate_vector(vector):
    r, theta = vector
    return (round(r, 3), round(theta, 3))
def plot_scoring_loops(loop_colors, formed_loops):
    data = []
    red_running_score = 0
    blue_running_score = 0
    
    for i, loop in enumerate(formed_loops):
        truncated_loop = [truncate_vector(vector) for vector in loop]
        red_score, blue_score = calculate_scores([loop_colors[i]])
        red_running_score += red_score
        blue_running_score += blue_score
        running_scores = f"{red_running_score}:{blue_running_score}"
        data.append([truncated_loop, loop_colors[i], running_scores])
    
    # Create the table
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=data, colLabels=['Loop', 'Colors', 'Running Scores'], cellLoc='center', loc='center')
    
    # Set font size and scale table
    for key, cell in the_table.get_celld().items():
        if key[0] == 0:
            cell.set_text_props(fontweight='bold')
    
    # Adjust column widths to fit content
    for i in range(len(data[0])):
        the_table.auto_set_column_width(i)
    
    # Display the table
    plt.show()
def on_click(event):
    if event.inaxes in [ax1, ax2]:
        # Load clicks and determine game state
        clicks = load_clicks()
        red_clicks = sum(1 for click in clicks if click['color'] == 'red')
        blue_clicks = sum(1 for click in clicks if click['color'] == 'blue')
        if red_clicks == blue_clicks:
            valid_turn = True
        else:
            last_click = clicks[-1]
            valid_turn = (last_click['color'] == 'red' and event.inaxes == ax2) or (last_click['color'] == 'blue' and event.inaxes == ax1)
        if valid_turn:
            r, theta = event.ydata, event.xdata
            valid_spaces = load_valid_spaces()
            nearest_space = find_nearest_valid_space(r, theta, valid_spaces)
            color = 'red' if event.inaxes == ax1 else 'blue'
            ax1.plot(nearest_space[1], nearest_space[0], marker='o', markersize=5, color=color)
            ax2.plot(nearest_space[1], nearest_space[0], marker='o', markersize=5, color=color)
            fig.canvas.draw()
            # Save click information to JSON file
            with open('clicks.json', 'a') as f:
                json.dump({'color': color, 'address': nearest_space}, f)
                f.write('\n')
            # Calculate and display scores
            clicks = load_clicks()
            valid_loops = load_valid_loops2()
            formed_loops = find_formed_loops(clicks, valid_loops)
            loop_colors = get_loop_colors(formed_loops, clicks)
            red_score, blue_score = calculate_scores(loop_colors)
            print(f"Red: {red_score}, Blue: {blue_score}")
            check_end_game(len(load_clicks()), count_unique_vectors('valid_spaces.json'), high_score)
root = tk.Tk()
root.withdraw()
high_score = simpledialog.messagebox.askyesno("Game Mode", "Do you want to play for high scores? (No for low scores)")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), subplot_kw={'projection': 'polar'})
plot_tessellation(ax1)
plot_tessellation(ax2)
ax1.set_title('Triforce Tessellation 1')
ax2.set_title('Triforce Tessellation 2')
fig.canvas.mpl_connect('button_press_event', on_click)
plt.show()
