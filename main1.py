import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import tkinter as tk
from datetime import datetime
from tkinter import Entry, Label, Button, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main application window
root = tk.Tk()
root.title("Home Page")
root.geometry("800x600")  # Set a custom window size (adjust as needed)

# Create a label for the title
title_label = tk.Label(root, text="WEATHER PREDICTION", font=("Arial", 24))
title_label.pack(pady=20)

# Function for the first button
def button1_action():
    # Load your dataset
    df = pd.read_csv('seattle-weather.csv')

    # Extract date-related features
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year

    # Define features and target
    X = df[['day_of_week', 'month', 'year']]
    y_weather = df['weather']

    # Split the data into training and test sets
    X_train, X_test, y_weather_train, y_weather_test = train_test_split(X, y_weather, test_size=0.2, random_state=42)

    # Create and train a random forest classifier for weather category
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_weather_train)

    # Function to predict weather and display the graph
    def predict_weather():
        date_str = date_entry.get()
        date = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date.weekday()
        month = date.month
        year = date.year

        # Make predictions for the input date
        prediction_weather = rf.predict([[day_of_week, month, year]])
        # Update the result label
        result_label.config(text=f"The predicted weather on {date.date()} is: {prediction_weather[0]}")

        # Display the graph for the input date
        display_weather_graph(date)

    # Function to display the weather graph for a specific date
    def display_weather_graph(date):
        # Create a list of dates for the x-axis
        dates = pd.date_range(start=date, end=date + pd.Timedelta(days=6), freq='D')

        # Make predictions for the input dates
        X_week = pd.DataFrame({'day_of_week': dates.weekday, 'month': dates.month, 'year': dates.year})
        predictions_weather = rf.predict(X_week)

        # Create a new window for the graph
        graph_window = tk.Tk()
        graph_window.geometry("800x600")  # Set the graph window size (adjust as needed)
        graph_window.title('Seattle Weather Predictions for the Next Week')

        # Create a Figure with a specific size
        fig, ax = plt.subplots(figsize=(8, 6))  # Adjust the size as needed

        ax.plot(dates, predictions_weather, label='Weather Category')
        ax.set_xlabel('Date')
        ax.set_ylabel('Weather Category')
        ax.set_title('Seattle Weather Predictions for the Next Week')
        ax.legend()

        # Embed the plot into the Tkinter window and center it
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas_widget.configure(yscrollcommand=canvas.yaxis.set)

        # Start the GUI main loop for the graph window
        graph_window.mainloop()

    # Create the GUI window for weather prediction
    prediction_window = tk.Tk()
    prediction_window.geometry("400x200")  # Set a custom window size
    prediction_window.title("Weather Prediction")

    # Create a label and entry field for date input
    date_label = tk.Label(prediction_window, text="Enter the date (YYYY-MM-DD):", font=("Arial", 16))
    date_label.pack(pady=10)

    date_entry = tk.Entry(prediction_window, font=("Arial", 16))
    date_entry.pack()

    # Create a button to trigger the prediction
    predict_button = tk.Button(prediction_window, text="Predict Weather", command=predict_weather, font=("Arial", 16))
    predict_button.pack(pady=10)

    # Create a label to display the result
    result_label = tk.Label(prediction_window, text="", font=("Arial", 16))
    result_label.pack()

    # Start the GUI main loop for the weather prediction window
    prediction_window.mainloop()

# Create the first button
button1 = tk.Button(root, text="PREC BY DATE", command=button1_action, font=("Arial", 20))
button1.pack(pady=20)

# Function for the second button
def button2_action():
    # Function to predict weather based on user input and display the graph
    def predict_weather():
        temp_max = float(entry_temp_max.get())
        temp_min = float(entry_temp_min.get())
        precipitation = float(entry_precipitation.get())
        wind_kmh = float(entry_wind.get())
        wind = wind_kmh / 3.6

        # Predict the weather value for the input values
        prediction = rf.predict([[temp_max, temp_min, precipitation, wind]])

        predicted_weather_label.config(text=f"The predicted weather is: {prediction[0]}")

        # Display the graph for the predicted weather category
        display_weather_graph(prediction[0])

    # Function to display the weather graph for a specific category
    def display_weather_graph(category):
        weather_data = df[df['weather'] == category]

        # Create a new window for the graph
        graph_window = tk.Toplevel(root)
        graph_window.title(f"Weather Data for {category}")

        # Create a Figure and a set of subplots
        fig, ax = plt.subplots(figsize=(8, 6))

        ax.plot(weather_data['date'], weather_data['temp_max'], label='Max Temp')
        ax.plot(weather_data['date'], weather_data['temp_min'], label='Min Temp')
        ax.plot(weather_data['date'], weather_data['precipitation'], label='Precipitation')
        ax.plot(weather_data['date'], weather_data['wind'], label='Wind')
        ax.set_xlabel('Date')
        ax.set_ylabel('Values')
        ax.set_title(f'Weather Data for {category}')
        ax.legend()

        # Embed the plot into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

    # Load the CSV file into a Pandas DataFrame
    df = pd.read_csv('seattle-weather.csv')

    # Prepare the data
    X = df[['temp_max', 'temp_min', 'precipitation', 'wind']]
    y = df['weather']

    # Train a random forest classifier on the data
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)

    # Create the Tkinter GUI window
    input_window = tk.Tk()
    input_window.title("Weather Prediction")
    input_window.state('zoomed')  # Maximize the window

    # Create a Frame to hold the input elements
    input_frame = Frame(input_window)
    input_frame.pack(pady=20)

    # Labels and entry fields for user input
    label_temp_max = Label(input_frame, text="Enter maximum temperature:", font=("Arial", 16))
    label_temp_min = Label(input_frame, text="Enter minimum temperature:", font=("Arial", 16))
    label_precipitation = Label(input_frame, text="Enter precipitation:", font=("Arial", 16))
    label_wind = Label(input_frame, text="Enter wind speed (km/h):", font=("Arial", 16))

    entry_temp_max = Entry(input_frame, font=("Arial", 16))
    entry_temp_min = Entry(input_frame, font=("Arial", 16))
    entry_precipitation = Entry(input_frame, font=("Arial", 16))
    entry_wind = Entry(input_frame, font=("Arial", 16))

    # Layout for input elements
    label_temp_max.grid(row=0, column=0, sticky='e')
    label_temp_min.grid(row=1, column=0, sticky='e')
    label_precipitation.grid(row=2, column=0, sticky='e')
    label_wind.grid(row=3, column=0, sticky='e')

    entry_temp_max.grid(row=0, column=1)
    entry_temp_min.grid(row=1, column=1)
    entry_precipitation.grid(row=2, column=1)
    entry_wind.grid(row=3, column=1)

    # Create a Frame to hold the predict button and predicted label
    button_frame = Frame(input_window)
    button_frame.pack(pady=20)

    predict_button = Button(button_frame, text="Predict Weather", command=predict_weather, font=("Arial", 16))
    predicted_weather_label = Label(button_frame, text="", font=("Arial", 18))

    # Layout for predict button and predicted label
    predict_button.grid(row=0, column=0, padx=10)
    predicted_weather_label.grid(row=0, column=1)

    # Start the GUI main loop for the input window
    input_window.mainloop()

# Create the second button
button2 = tk.Button(root, text="PREDICT BY VALUES", command=button2_action, font=("Arial", 20))
button2.pack(pady=20)

# Start the main window's GUI main loop
root.mainloop()
