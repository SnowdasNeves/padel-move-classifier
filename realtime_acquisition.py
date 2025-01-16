#!/usr/bin/env python3
import asyncio

# import logging
import uuid
from aioconsole import ainput
from bleak import BleakScanner, BleakClient
import csv
import joblib
import tsfel
import pandas as pd
import paho.mqtt.client as mqtt
import json

# Enable debug output
# logging.basicConfig(level=logging.DEBUG)

# BLE device and characteristics (must be matched to the .ino file)
DEVICE_NAME = ""
SERVICE_UUID = uuid.UUID("")
CHAR_UUID = uuid.UUID("")

# Creates csv to save data
CSV_FILE_NAME = "real_time_data.csv"

with open(CSV_FILE_NAME, mode="w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Accx", "Accy", "Accz"])


# BLE Comunication loop
sample_count = 0
iteration_count = 0


async def run(loop):
    print("Searching devices...")
    devices = await BleakScanner.discover()

    device = list(filter(lambda d: d.name == DEVICE_NAME, devices))
    if len(device) == 0:
        raise RuntimeError(f"Failed to find a device name '{DEVICE_NAME}'")

    address = device[0].address
    print(f"Connecting to the device... (address: {address})")
    flag = False
    while flag is False:
        try:
            async with BleakClient(address, loop=loop) as client:
                flag = True
                print("Done")
                print("Message from the device...")
                value = await client.read_gatt_char(CHAR_UUID)
                print(value.decode())

                print("Sending message to the device...")
                message = bytearray(b"RPI ready")
                await client.write_gatt_char(CHAR_UUID, message, True)

                # Receives the BLE data from the m5-stick
                def callback(sender, data):
                    global sample_count
                    global iteration_count
                    # timestamp = asyncio.get_event_loop().time()
                    acceleration = data.decode("utf-8")
                    values = acceleration.split(",")
                    float_values = [float(value.strip()) for value in values]
                    results = "{},{},{}".format(*float_values)

                    # Saves data in csv file
                    with open(CSV_FILE_NAME, mode="a", newline="") as csvfile_append:
                        csv_writer_append = csv.writer(csvfile_append)
                        csv_writer_append.writerow([results])

                    # Removes quotes
                    with open(CSV_FILE_NAME, mode="r", newline="") as csvfile:
                        lines = csvfile.readlines()
                        last_line = lines[-1].replace('"', "")

                    with open(CSV_FILE_NAME, mode="w", newline="") as csvfile:
                        csvfile.writelines(lines[:-1])
                        csvfile.write(last_line)

                    print(f"Received: {data}")

                    sample_count += 1

                    if sample_count == 77:
                        sample_count = 0

                        # Load acc data file and extract features
                        df = pd.read_csv(CSV_FILE_NAME, delimiter=",")
                        cfg = tsfel.get_features_by_domain()
                        features_df = tsfel.time_series_features_extractor(
                            cfg, df.iloc[:, 0:3].values, fs=25, window_size=77
                        )

                        selected_col = [
                            "0_Area under the curve",
                            "0_FFT mean coefficient_0",
                            "0_FFT mean coefficient_1",
                            "0_FFT mean coefficient_10",
                            "0_FFT mean coefficient_11",
                            "0_FFT mean coefficient_12",
                            "0_FFT mean coefficient_13",
                            "0_FFT mean coefficient_14",
                            "0_FFT mean coefficient_15",
                            "0_FFT mean coefficient_16",
                            "0_FFT mean coefficient_17",
                            "0_FFT mean coefficient_18",
                            "0_FFT mean coefficient_19",
                            "0_FFT mean coefficient_2",
                            "0_FFT mean coefficient_20",
                            "0_FFT mean coefficient_21",
                            "0_FFT mean coefficient_22",
                            "0_FFT mean coefficient_23",
                            "0_FFT mean coefficient_24",
                            "0_FFT mean coefficient_25",
                            "0_FFT mean coefficient_26",
                            "0_FFT mean coefficient_27",
                            "0_FFT mean coefficient_28",
                            "0_FFT mean coefficient_29",
                            "0_FFT mean coefficient_3",
                            "0_FFT mean coefficient_30",
                            "0_FFT mean coefficient_31",
                            "0_FFT mean coefficient_32",
                            "0_FFT mean coefficient_33",
                            "0_FFT mean coefficient_34",
                            "0_FFT mean coefficient_35",
                            "0_FFT mean coefficient_36",
                            "0_FFT mean coefficient_37",
                            "0_FFT mean coefficient_38",
                            "0_FFT mean coefficient_4",
                            "0_FFT mean coefficient_5",
                            "0_FFT mean coefficient_6",
                            "0_FFT mean coefficient_7",
                            "0_FFT mean coefficient_8",
                            "0_FFT mean coefficient_9",
                            "0_Mean absolute deviation",
                            "0_Spectral distance",
                            "0_Spectral variation",
                            "1_Area under the curve",
                            "1_FFT mean coefficient_0",
                            "1_FFT mean coefficient_1",
                            "1_FFT mean coefficient_10",
                            "1_FFT mean coefficient_11",
                            "1_FFT mean coefficient_12",
                            "1_FFT mean coefficient_13",
                            "1_FFT mean coefficient_14",
                            "1_FFT mean coefficient_15",
                            "1_FFT mean coefficient_16",
                            "1_FFT mean coefficient_17",
                            "1_FFT mean coefficient_18",
                            "1_FFT mean coefficient_19",
                            "1_FFT mean coefficient_2",
                            "1_FFT mean coefficient_20",
                            "1_FFT mean coefficient_21",
                            "1_FFT mean coefficient_22",
                            "1_FFT mean coefficient_23",
                            "1_FFT mean coefficient_24",
                            "1_FFT mean coefficient_25",
                            "1_FFT mean coefficient_26",
                            "1_FFT mean coefficient_27",
                            "1_FFT mean coefficient_28",
                            "1_FFT mean coefficient_29",
                            "1_FFT mean coefficient_3",
                            "1_FFT mean coefficient_30",
                            "1_FFT mean coefficient_31",
                            "1_FFT mean coefficient_32",
                            "1_FFT mean coefficient_33",
                            "1_FFT mean coefficient_34",
                            "1_FFT mean coefficient_35",
                            "1_FFT mean coefficient_36",
                            "1_FFT mean coefficient_37",
                            "1_FFT mean coefficient_38",
                            "1_FFT mean coefficient_4",
                            "1_FFT mean coefficient_5",
                            "1_FFT mean coefficient_6",
                            "1_FFT mean coefficient_7",
                            "1_FFT mean coefficient_8",
                            "1_FFT mean coefficient_9",
                            "1_Mean absolute deviation",
                            "1_Spectral distance",
                            "1_Spectral variation",
                            "2_Area under the curve",
                            "2_FFT mean coefficient_0",
                            "2_FFT mean coefficient_1",
                            "2_FFT mean coefficient_10",
                            "2_FFT mean coefficient_11",
                            "2_FFT mean coefficient_12",
                            "2_FFT mean coefficient_13",
                            "2_FFT mean coefficient_14",
                            "2_FFT mean coefficient_15",
                            "2_FFT mean coefficient_16",
                            "2_FFT mean coefficient_17",
                            "2_FFT mean coefficient_18",
                            "2_FFT mean coefficient_19",
                            "2_FFT mean coefficient_2",
                            "2_FFT mean coefficient_20",
                            "2_FFT mean coefficient_21",
                            "2_FFT mean coefficient_22",
                            "2_FFT mean coefficient_23",
                            "2_FFT mean coefficient_24",
                            "2_FFT mean coefficient_25",
                            "2_FFT mean coefficient_26",
                            "2_FFT mean coefficient_27",
                            "2_FFT mean coefficient_28",
                            "2_FFT mean coefficient_29",
                            "2_FFT mean coefficient_3",
                            "2_FFT mean coefficient_30",
                            "2_FFT mean coefficient_31",
                            "2_FFT mean coefficient_32",
                            "2_FFT mean coefficient_33",
                            "2_FFT mean coefficient_34",
                            "2_FFT mean coefficient_35",
                            "2_FFT mean coefficient_36",
                            "2_FFT mean coefficient_37",
                            "2_FFT mean coefficient_38",
                            "2_FFT mean coefficient_4",
                            "2_FFT mean coefficient_5",
                            "2_FFT mean coefficient_6",
                            "2_FFT mean coefficient_7",
                            "2_FFT mean coefficient_8",
                            "2_FFT mean coefficient_9",
                            "2_Mean absolute deviation",
                            "2_Spectral distance",
                            "2_Spectral variation",
                        ]

                        features_df = features_df[selected_col]

                        loaded_ml = joblib.load("Padel_RF.joblib")
                        prediction = loaded_ml.predict(features_df)

                        print(f"Prediction: {prediction}")

                        # Extracting y-axis data to send
                        start_row = iteration_count * 77 + 1
                        end_row = start_row + 76

                        acc_x = df["Accx"].iloc[start_row:end_row].values
                        acc_y = df["Accy"].iloc[start_row:end_row].values
                        acc_z = df["Accz"].iloc[start_row:end_row].values

                        # Open MQTT connection to broker
                        broker = "192.168.1.98"
                        client = mqtt.Client()
                        client.connect(broker, 1883, 60)

                        # Define the topic of publication
                        topic = "AAI/padel/data"

                        # Publised chosen msg
                        if prediction[-1] == "N":
                            msg = "Normal"
                        elif prediction[-1] == "S":
                            msg = "Smash"
                        elif prediction[-1] == "B":
                            msg = "Backhand"
                        elif prediction[-1] == "L":
                            msg = "Lob"
                        elif prediction[-1] == "J":
                            msg = "Bandeja"
                        elif prediction[-1] == "R":
                            msg = "Move unrecognized"

                        data_dict = {
                            "msg": msg,
                            "acc_x": acc_x.tolist(),
                            "acc_y": acc_y.tolist(),
                            "acc_z": acc_z.tolist(),
                        }

                        json_data = json.dumps(data_dict)

                        client.publish(topic, json_data)

                        # Ends MQTT connection
                        client.disconnect()

                        iteration_count += 1

                print("Subscribing to characteristic changes...")
                await client.start_notify(CHAR_UUID, callback)

                # print("Waiting 60 seconds to receive data from the device...")
                # await asyncio.sleep(60)

                # Waits for an input from user to end process
                result = await ainput("Press any key to exit")
                print("Disconnecting from device")
        except:
            print("Retrying ...")


# Start BLE comunications loop
loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
