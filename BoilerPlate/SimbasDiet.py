import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd


def radar_plot(ax, angles, values, color, label):
    angles = np.append(angles, angles[0])  
    values = np.append(values, values[0])
    ax.plot(angles, values, color=color, linewidth=2, label=label)
    ax.fill(angles, values, color=color, alpha=0.25)

def show_plot():
    animal1 = animal_var1.get()
    animal2 = animal_var2.get()

    # Macronutrient percentages for each animal
    percents = {
        "Meerkat": [55, 25, 15],
        "Warthog": [45, 35, 15],
        "Ungulates": [60, 30, 7.5],
        "Mealworms": [55, 35, 7.5],
        "Crickets": [65, 17.5, 10]
    }

    # Calculate the kcal density for each animal based on its macronutrient content
    kcal_density = {}
    for animal in percents.keys():
        kcal_density[animal] = sum([percent/100 * conversion_factors[i] for i, percent in enumerate(percents[animal])])

    data = {animal: np.multiply(percents[animal], conversion_factors) for animal in percents.keys()}

    max_value = max([max(data[animal]) for animal in data.keys()])
    rticks = np.linspace(0, max_value, 5)

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [1, 1.5]})
    ax1 = plt.subplot(1, 2, 1, polar=True)

    radar_plot(ax1, angles, data[animal1], "blue", animal1)
    radar_plot(ax1, angles, data[animal2], "red", animal2)
    ax1.set_thetagrids(np.degrees(angles), labels)
    ax1.set_rlabel_position(22.5)
    ax1.set_rticks(rticks)
    ax1.set_rlim(0, max_value)
    ax1.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
    ax1.set_title("Macronutrient Composition")

    # Calculate the daily kcal requirement for each age group
    age_groups = [0, 3, 12, 24, 36] # in months
    daily_kcal_requirement = [240, 280, 400, 430, 440] # in kcal
    animal1_kcal_density = kcal_density[animal1]
    animal2_kcal_density = kcal_density[animal2]
    daily_kg1 = np.array([round((d / (animal1_kcal_density / 1000)), 2) for d in daily_kcal_requirement])
    daily_kg2 = np.array([round((d / (animal2_kcal_density / 1000)), 2) for d in daily_kcal_requirement])

    # Calculate the daily kg requirement for each age group
    daily_kg1 = np.array([round((d / (animal1_kcal_density / 1000)), 2) for d in daily_kcal_requirement])
    daily_kg2 = np.array([round((d / (animal2_kcal_density / 1000)), 2) for d in daily_kcal_requirement])

    df = pd.DataFrame({
        'Age (Months)': np.tile(age_groups, 2),
        'Daily Consumption (kg)': np.concatenate((daily_kg1, daily_kg2)),
        'Diet': np.repeat([animal_var1.get(), animal_var2.get()], len(age_groups))
    })
    
    # Plot the line graph
    sns.lineplot(data=df, x='Age (Months)', y='Daily Consumption (kg)', hue='Diet', ax=ax2)
    ax2.set_title('Daily Kg Needs')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=20, columnspan=2)



root = tk.Tk()
root.title("Animal Radar Plot & Lion Weight Comparison")

conversion_factors = np.array([4, 9, 4])
labels = [    f"Protein ({conversion_factors[0]} kcal/g)",    f"Fat ({conversion_factors[1]} kcal/g)",    f"Carbohydrates ({conversion_factors[2]} kcal/g)",]

animal_var1 = tk.StringVar(root)
animal_var1.set("Meerkat")  # Set the default value
animal_var2 = tk.StringVar(root)
animal_var2.set("Warthog")  # Set the default value
animal_options = ["Meerkat", "Warthog", "Ungulates", "Mealworms", "Crickets"]

animal_dropdown1 = ttk.Combobox(root, textvariable=animal_var1, values=animal_options)
animal_dropdown1.grid(row=0, column=0, padx=20, pady=20)
animal_dropdown2 = ttk.Combobox(root, textvariable=animal_var2, values=animal_options)
animal_dropdown2.grid(row=0, column=1, padx=20, pady=20)

# Add a button to generate the plot
plot_button = tk.Button(root, text="Show Plot", command=show_plot)
plot_button.grid(row=0, column=2, padx=20, pady=20)

# Run the Tkinter event loop
root.mainloop()