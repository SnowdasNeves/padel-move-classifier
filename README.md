# Padel Move Classifier

This repository contains a machine learning real time classifier for padel moves using the Random Forest algorithm and an M5StickCPlus for accelerometer data acquisition.

The program was created to use a Raspberry Pi receiving and evaluating the data and then send the prediction to a streamlit webpage via an MQTT broker.

## Installation and usage

1. Clone the repository:

   ```sh
   git clone https://github.com/SnowdasNeves/padel-move-classifier.git
   ```

2. Navigate to the project directory:

   ```sh
   cd padel-move-classifier
   ```

3. Install the required dependencies from `requirements.txt`.

4. Upload `accelerometer_data_readings.ino` to an M5StickCPlus (don't forget to install the required Arduino libraries).

5. Run `streamlit_webpage.py` with the following code and consult the About page to learn how to proceed.

   ```sh
   streamlit run streamlit_webpage.py
   ```

6. Run `realtime_acquisition` simultaneously to receive and evaluate the data coming from the M5StickCPlus (broker id and topic name must be selected in the files listed in 5 and 6).
