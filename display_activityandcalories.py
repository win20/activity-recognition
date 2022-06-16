import sys

from calculate_bpm import calculate_bpm
import tensorflow as tf
import numpy as np
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import glob
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder


def get_frames(df, frame_size, hop_size):
    N_FEATURES = 3  # x, y, z

    frames = []
    for i in range(0, len(df) - frame_size, hop_size):
        x = df['x'].values[i: i + frame_size]
        y = df['y'].values[i: i + frame_size]
        z = df['z'].values[i: i + frame_size]

        frames.append([x, y, z])

    # Convert to np array
    frames = np.asarray(frames).reshape(-1, frame_size, N_FEATURES)

    return frames

def process_input(file_path):
    data = pd.read_csv(file_path, header=None)
    columns = ['activity', 'x', 'y', 'z']
    data.columns = columns

    data['x'] = data['x'].astype('float')
    data['y'] = data['y'].astype('float')
    data['z'] = data['z'].astype('float')
    X = data[['x', 'y', 'z']]

    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    scaled_X = pd.DataFrame(data=X, columns=['x', 'y', 'z'])

    Fs = 20
    frame_size = Fs * 4  # 4 seconds, 80 samples
    hop_size = Fs * 2

    X = get_frames(scaled_X, frame_size, hop_size)
    X = X.reshape(X.shape[0], X.shape[1], 3, 1)

    labels = pd.read_csv("C:\\Users\\winba\\Desktop\\UbiqFinal\\data\\labels.txt", header=None, index_col=None)
    flat_labels = [item for sublist in labels.values for item in sublist]
    return X, flat_labels


def make_prediction(X, labels):
    print('Activity recognition started...')
    model = tf.keras.models.load_model('"C:\\Users\\winba\\Desktop\\UbiqFinal\\saved_model"')
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    predictions = probability_model.predict(X)
    prediction_indices = []
    for item in predictions:
        prediction_indices.append(np.argmax(item))

    counter = 0
    max_num = prediction_indices[0]
    for item in prediction_indices:
        current_frequency = prediction_indices.count(item)
        if current_frequency > counter:
            counter = current_frequency
            max_num = item

    prediction_out = labels[max_num]
    print('Done: Activity = ' + prediction_out)
    return prediction_out


def calculate_calories_burned(gender, duration, bpm, weight, age):
    calories_burned = 0
    if gender == 0:
        calories_burned = duration * (0.6309 * bpm + 0.1988 * weight + 0.2017 * age - 55.0969) / 4.184
    else:
        calories_burned = duration * (0.4472 * bpm - 0.1263 * weight + 0.074 * age - 20.4022) / 4.184

    return int(round(calories_burned, 0))


def is_user_input_float(user_input):
    try:
        val = float(user_input)
    except ValueError:
        print('Please enter a valid number')
        return False
    return True

def is_user_input_int(user_input):
    try:
        val = int(user_input)
    except ValueError:
        print('Please enter a valid number')
        return False
    return True


def main():
    # Get bpm
    # vid_path = sys.argv[1]
    # bpm = calculate_bpm(vid_path)

    data, labels = process_input("C:\\Users\\winba\\Desktop\\UbiqFinal\\data\\test_data\\23,04,22,07,23,44,Jogging,accelerometer.txt")
    pred = make_prediction(data, labels)


    # accel_path = 'data/sensors/23,04,22,09,12,22,Stair climber,accelerometer.txt'
    # gyro_path = 'data/sensors/23,04,22,09,12,22,Stair climber,gyroscope.txt'

    # accel_path = sys.argv[2]
    # gyro_path = sys.argv[3]
    # data, labels = get_input_data(accel_path, gyro_path)
    #
    # pred = make_prediction(data, labels)

    # calories = 0
    # display_questions = True
    # while display_questions:
    #     gender = input("Enter your gender (0 = male; 1 = female):  ").rstrip()
    #     if gender != '0' and gender != '1':
    #         print('Please enter a valid number')
    #         continue
    #
    #     duration = input('Exercise duration in minutes:  ')
    #     while not is_user_input_float(duration):
    #         duration = input('Exercise duration in minutes:  ')
    #
    #     weight = input('Weight in kg:  ')
    #     while not is_user_input_float(weight):
    #         weight = input('Weight in kg:  ')
    #
    #     age = input('Age:  ')
    #     while not is_user_input_int(age):
    #         age = input('Age:  ')
    #
    #     gender = int(gender)
    #     duration = float(duration)
    #     weight = float(weight)
    #     age = float(age)
    #     calories = calculate_calories_burned(gender, duration, 100, weight, age)
    #     break
    #
    #
    # print(calories)


if __name__ == '__main__':
    # bpm = calculate_bpm('finger-tip-2.mp4')
    # print(bpm)
    # model = tf.keras.models.load_model('ml_model')
    # # print(model.summary())
    # accel_path = 'data/sensors/23,04,22,09,12,22,Stair climber,accelerometer.txt'
    # gyro_path = 'data/sensors/23,04,22,09,12,22,Stair climber,gyroscope.txt'
    #
    # data, labels = get_input_data(accel_path, gyro_path)
    #
    # pred = make_prediction(data, labels)

    # calories = calculate_calories_burned(1, 2, 100, 55, 22)
    # print(calories)
    main()