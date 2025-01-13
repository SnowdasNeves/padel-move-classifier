import pandas as pd
import numpy as np
import tsfel
from sklearn.model_selection import train_test_split
# from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
# from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import joblib
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier


## Feature extraction
###############################################################################


def feature_extraction():
    # Load acc data file and extract features
    feature_filename = str(input("Choose file to extract features: "))
    df = pd.read_csv(feature_filename, delimiter=",")
    
    cfg = tsfel.get_features_by_domain()
    features_df = tsfel.time_series_features_extractor(cfg, df.iloc[:, 0:3].values, fs=25, window_size=77)
    
    # Labelling feature rows with movement name
    labels = ['N', 'B', 'S', 'L', 'J', 'R'] # Normal=N, Smash=S, Backhand=B
    reps_per_move = 20
    repeated_labels = np.repeat(labels, reps_per_move)
    
    features_df['Movement label'] = repeated_labels
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
    y = features_df['Movement label']
    
    
    # Train test split for kNN
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)
    
    # Standardize the features
    # scaler = StandardScaler()
    # X_train_scaled = scaler.fit_transform(X_train)
    # X_test_scaled = scaler.transform(X_test)
    
    
    # Cross validation for choosing k value
    # scores = []
    # k_values = [i for i in range(1, 31)]
    # for k in k_values:
    #     # kNN
    #     knn = KNeighborsClassifier(n_neighbors=k)
    #     score = cross_val_score(knn, X_train_scaled, y_train, cv=5)
    #     scores.append(np.mean(score))
    
    # k = np.argmax(scores) + 1
    # knn = KNeighborsClassifier(n_neighbors=3)
    # knn.fit(X_train_scaled, y_train)
    
    # y_pred_knn = knn.predict(X_test_scaled)
        
    # precision = precision_score(y_test, y_pred_knn, average='weighted')
    # recall = recall_score(y_test, y_pred_knn, average='weighted')
    # f1 = f1_score(y_test, y_pred_knn, average='weighted')
    # conf_matrix = confusion_matrix(y_test, y_pred_knn)
    
    # print('kNN')
    # print(f"Precision: {precision:.2f}")
    # print(f"Recall: {recall:.2f}")
    # print(f"F1-score: {f1:.2f}")
    # print("Confusion Matrix:")
    # print(conf_matrix, '\n')
    # # print(k)
    
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    
    y_pred_rf = rf.predict(X_test)
    
    precision = precision_score(y_test, y_pred_rf, average='weighted')
    recall = recall_score(y_test, y_pred_rf, average='weighted')
    f1 = f1_score(y_test, y_pred_rf, average='weighted')
    conf_matrix = confusion_matrix(y_test, y_pred_rf)
    
    print('RF')
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-score: {f1}")
    print("Confusion Matrix:")
    print(conf_matrix, '\n')
    
    return rf


features_df = feature_extraction()
rf = ml_algorithm(features_df)
joblib.dump(rf, 'Padel_RF_all.joblib')
