# Padel Move Classifier

This repository provides a real-time machine learning classifier for padel moves, utilizing accelerometer data from an M5StickCPlus device. The system employs a Random Forest algorithm to predict padel moves and presents the data through a Streamlit web application.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Project Structure

The repository consists of the following key files:

- **`accelerometer_data_readings.ino`**: Arduino code for the M5StickCPlus to read accelerometer data and transmit it via MQTT.
- **`model_training.py`**: Python script to train the Random Forest classifier using collected accelerometer data.
- **`realtime_acquisition.py`**: Python script to receive accelerometer data in real-time from the M5StickCPlus and make predictions using the trained model.
- **`streamlit_webpage.py`**: Streamlit application to visualize real-time predictions and provide user instructions.
- **`requirements.txt`**: List of Python dependencies required to run the project.

## Installation

To set up the project, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/SnowdasNeves/padel-move-classifier.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd padel-move-classifier
   ```

3. **Install the required Python dependencies:**

   Ensure you have Python installed on your system. Then, install the dependencies using:

   ```bash
   pip install -r requirements.txt
   ```

4. **Upload the Arduino code to the M5StickCPlus:**

   - Open the `accelerometer_data_readings.ino` file located in the repository.
   - Use the Arduino IDE to upload this code to your M5StickCPlus device.
   - Ensure all necessary Arduino libraries are installed.

## Usage

1. **Start the Streamlit web application:**

   In the terminal, run:

   ```bash
   streamlit run streamlit_webpage.py
   ```

   This will launch the web application where you can monitor and visualize the padel move predictions.

2. **Run the real-time data acquisition script:**

   Open another terminal window and execute:

   ```bash
   python realtime_acquisition.py
   ```

   This script handles the reception and evaluation of data from the M5StickCPlus device. Ensure that the MQTT broker ID and topic names are consistently set in both `streamlit_webpage.py` and `realtime_acquisition.py`.

3. **Perform padel moves:**

   With the M5StickCPlus device properly set up and the system running, press the 'B' button on the device to start data acquisition. You have 2 seconds to perform a padel move. The system will analyze the accelerometer data and display the predicted move on the Streamlit web application.

## Contributing

Contributions to enhance the functionality or performance of this project are welcome. Please fork the repository and submit a pull request with your proposed changes.
