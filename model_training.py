import pandas as pd
import numpy as np
import tsfel
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import joblib
from sklearn.ensemble import RandomForestClassifier


## Feature extraction
###############################################################################


def feature_extraction():
    # Load acc data file and extract features
    feature_filename = str(input("Choose file to extract features: "))
    df = pd.read_csv(feature_filename, delimiter=",")

    cfg = tsfel.get_features_by_domain()
    features_df = tsfel.time_series_features_extractor(
        cfg, df.iloc[:, 0:3].values, fs=25, window_size=77
    )

    # Labelling feature rows with movement name
    labels = ["N", "B", "S", "L", "J", "R"]  # Normal=N, Smash=S, Backhand=B
    reps_per_move = 20
    repeated_labels = np.repeat(labels, reps_per_move)

    features_df["Movement label"] = repeated_labels
    # print(features_df)

    # Write to csv to use in Orange
    # feature_file = str(input("Choose feature file name: "))

    # try:
    #     existing_data = pd.read_csv(feature_file)
    #     updated_data = pd.concat([existing_data, features_df], ignore_index=True)
    # except FileNotFoundError:
    #     updated_data = features_df

    # features_df.to_csv(feature_file, index=False)

    return features_df


## Start of ML algorithm
###############################################################################


def ml_algorithm(features_df):
    # Separate features and target variable
    X = features_df.iloc[:, :-1]
    y = features_df["Movement label"]

    # Train test split for kNN
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    # Standardize the features
    # scaler = StandardScaler()
    # X_train_scaled = scaler.fit_transform(X_train)
    # X_test_scaled = scaler.transform(X_test)

    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)

    y_pred_rf = rf.predict(X_test)

    precision = precision_score(y_test, y_pred_rf, average="weighted")
    recall = recall_score(y_test, y_pred_rf, average="weighted")
    f1 = f1_score(y_test, y_pred_rf, average="weighted")
    conf_matrix = confusion_matrix(y_test, y_pred_rf)

    print("RF")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-score: {f1}")
    print("Confusion Matrix:")
    print(conf_matrix, "\n")

    return rf


features = feature_extraction()
trained_rf_model = ml_algorithm(features)
joblib.dump(trained_rf_model, "Padel_RF_all.joblib")
