# -*- coding: utf-8 -*-
"""
Submitting Entity: IIT Jodhpur, Rajasthan, India

- This file is used for training the Bidirectional-LSTM based AI model for predicting CQI for a UE in every frame considering the past CQI data (of 400 frames)
- We consider a training dataset collected from Open Air Interface RF Simulator with CQI values varying in the range [0,15]
- The  training data is present in the SQLITE 3 DB with file name "CQI_DATASET"


Credits: 
--------
The references for the data preprocessing and Bi-LSTM architecture used in this model include the following:
- Author: Ilias Chatzistefanidis
  1) ML-based Traffic Steering for Heterogeneous Ultra-dense beyond-5G Networks (https://ieeexplore.ieee.org/abstract/document/10118923)
  2) Which ML Model to Choose? Experimental Evaluation for a Beyond-5G Traffic Steering Case (https://ieeexplore.ieee.org/abstract/document/10279485) 
 
We have made necessary modifications to the model configuration and for training with our in-house collected dataset.

"""



# Include essential libraries

import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from joblib import dump, load
from random import random
from random import randint
from numpy import array
from numpy import zeros
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import TimeDistributed
import datetime
from keras.layers import Dropout
from keras.layers import TimeDistributed
from keras.layers import Activation
from keras.layers import RepeatVector
from keras.layers import Bidirectional
from keras.layers import GRU

from numpy import array
from numpy import hstack
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Conv1D
from keras.layers import MaxPooling1D
import sqlite3



## Load the training data from the DB CQI_DATASET

con = sqlite3.connect("CQI_DATASET")
cur = con.cursor()
res = cur.execute("SELECT wb_cqi FROM MAC_UE")
df = np.array(res.fetchall())




# Using approximately 60k samples for training and 10k samples for testing
# Initial 240 samples were ignored considering the simulator settling time and time taken for initializing channel simulator
df_train = df[240:60000]
df_test = df[60001:70000]



## Plot the CQI training data from the dataset
# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(y=list(df.reshape(-1))))

# Set title
fig.update_layout(
    title_text="Time series with range slider and selectors"
)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
        ),
        rangeslider=dict(
            visible=True
        )
    )
)

fig.show()

### Data Pre-Processing - Normalize data by rescaling them to the range [0,1] for efficient training.

# Using the MinMaxScaler
values = df_train
values = values.reshape((len(values), 1))

scaler = MinMaxScaler(feature_range=(0, 1))
scaler = scaler.fit(values)

print('Min: %f, Max: %f' % (scaler.data_min_, scaler.data_max_))

# normalize the dataset
normalized = scaler.transform(values)

# Save the scaler to use during integration with xAPP
dump(scaler, 'scaler_training.bin', compress=True)

"""
Supervised Learning Structure
=============================

We use a sliding window mechanism to prepare the data for training and testing (to feed as input to the model)

Parameters used are $L$ = 400, $p$ = 1, $m$ = 2

This prepares the input as normalized CQI values corresponding to past 400 frames (for example frame numbers 0 to 399) and label comprises of normalized CQI value of the next frame (corresponding to frame 400)
In the next instance, we slide the window so that input comprises of normalized CQI values corresponding to frame numbers 1 to 400, and the label comprises normalized CQI value of the 401-th frame.

To split the data in this format for training and testing, we use the preprocessing function developed by the following author:

- Author: Ilias Chatzistefanidis
  1) ML-based Traffic Steering for Heterogeneous Ultra-dense beyond-5G Networks (https://ieeexplore.ieee.org/abstract/document/10118923)
  2) Which ML Model to Choose? Experimental Evaluation for a Beyond-5G Traffic Steering Case (https://ieeexplore.ieee.org/abstract/document/10279485) 


"""

def split_sequence(sequence, n_steps, pred_steps, mean_batch):
    """
    This function applies a filtering technique to reduce the data volume and
    then applies the sliding window technique to create a supervised learning structure.

    Regarding the filtering, the algorithm filters the sequence by calculating the average
    value of every m values. E.g. the average of every 5 values. In this way, the sequence's
    size is reduced maintaing the data patterns.

    Regarding the sliding window, the algorithm calculates input windows X_i and the respective
    y_i labels to be fed into the model. Each input window is slided by one value to the future
    to create multiple samples for the model. Each X has length L. Each y is the label and
    represent the forecasting of the model. Each y is a single value that represents the average
    of multiple values. The number of these value that are used to calculate each y is p.
    Importantly, these values of the y label are locating after the respective X values to
    represent the future.

    Params:

    - sequence: input sequence
    - n_steps (L): input window time-steps/length   (length of X)
          The number of values that will be used to form the input window of the model
    - pred_steps (p): number of time-steps used for output/label(y)
          The number of values that will be used to calculate an average value (mean).
          This average value will be the y label.
            e.g. if pred_steps equals 5, the mean of 5 values will be the y label
    - mean_batch (m): filtering window length
          The number of values that will be used by the filtering window

    An example for better understanding is the following:

    Assume the normalized inputs:
    sequence = [0.93, 0.93, 0.80, 0.80, 0.67, 0.67, 0.60, 0.60, 0.50, 0.50, 0.40, 0.40]
    n_steps = 3
    pred_steps = 2
    mean_batch = 2

    Then the filtered sequence after applying the filtering with mean_batch = 2 is:
    filtered_seq = [0.93, 0.80, 0.67, 0.60, 0.50, 0.40]

    Then samples are created using the sliding window with n_steps = 3, pred_steps = 2.

    X_1 = [0.93, 0.80, 0.67]
    and y_1 = the average of 0.60 and 0.50.
    Hence, y_1 = [0.55]

    Then, we slide by on value and
    X_2 = [0.80, 0.67, 0.60] and y_2 = [0.45] (mean of 0.50 and 0.40)
    """
    new_sequence = []

    ### Filtering
    temp_sum = 0
    # iterate through sequence
    for i,item in enumerate(sequence,start=1):
        temp_sum+=item
        # for every m values calculate the mean value and
        # append it in the new sequence
        if i%mean_batch == 0:
            mean_temp = temp_sum/mean_batch
            temp_sum=0
            new_sequence.append(mean_temp)

    # work with the new filtered sequence
    sequence = new_sequence

    # adjust the params to the new sequence
    n_steps = int(n_steps/mean_batch)
    #pred_steps = int(pred_steps/mean_batch)
    pred_steps = int(pred_steps)

    ### Sliding window technique
    X, y = list(), list()
    # iterate through sequence
    for i in range(len(sequence)):
        # for each iteration (i),
        # find the end of this pattern (X_i)
        end_ix = i + n_steps

        # check if X_i is beyond the sequence
        if end_ix > len(sequence)-1:
            break
        # check if values for y_i go beyond the sequence
        pred_ix = end_ix + pred_steps
        if pred_ix > len(sequence)-1:
            break

        # compute the y label (mean of p values after X_i)
        mean_pred = np.mean(sequence[end_ix:pred_ix])

        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], mean_pred

        # store sample
        X.append(seq_x)
        y.append(seq_y)

    return np.array(X), np.array(y)

"""Now that we defined the function, lets use it on our normalized data"""

# define input sequence
raw_seq = normalized
# choose a number of input time steps
n_steps = 400
# choose a number of prediction steps to calculate each label
pred_steps = 1
# choose filtering window
mean_batch = 1


# split into samples
X_train, y_train = split_sequence(raw_seq, n_steps, pred_steps, mean_batch)

"""Print X, y shapes"""

print(X_train.shape)
print(y_train.shape)

"""
Now, reshape samples appropriately for the model
"""

n_features = 1
X_train = X_train.reshape((X_train.shape[0],  X_train.shape[1],  1   ))

print(X_train.shape)
print(y_train.shape)
print(X_train)

"""## Bi-LSTM model

We use a Bi-LSTM model which has 1 input layer of size. 1 hidden layer, and 1 dense output layer
Activation function used is Scaled Exponential Linear Unit (selu)
Error function: Mean Square Error
Optimizer: Adam

"""

# define model
model = keras.Sequential()
model.add(Bidirectional(LSTM(25, activation='selu',return_sequences=True), input_shape=(int(n_steps/mean_batch), n_features)    ))
model.add(Bidirectional(LSTM(25, activation='selu') ))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
model.summary()

# train model and calculate training time
a = datetime.datetime.now()
model.fit(X_train, y_train,  epochs=15, verbose=1, batch_size=2**6)
b = datetime.datetime.now()
diff = b-a
diff_secs = diff.total_seconds()
print("Training Time:", round(diff_secs,1),"seconds.")

# Save the model to use in the xApp
model.save('trained_model.keras')

"""## Validation Data

Now we use unseen CQI data (excluded from training set) to validate model.

"""

val_df = df_test

"""Plot CQI data to observe the traffic patterns."""

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(y=list(val_df.reshape(-1))))

# Set title
fig.update_layout(
    title_text="Time series with range slider and selectors"
)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
        ),
        rangeslider=dict(
            visible=True
        )
    )
)

fig.show()

"""### Data Pre-processing

Follow the same pre-processing with the training data.
"""

# prepare data for normalization
values = np.array(val_df)
values = values.reshape((len(values), 1))

# normalize the dataset and print the first 5 rows
normalized_test = scaler.transform(values)
print(normalized_test)

"""### Supervised Learning Structure

Use the function developed above to structure appropriately the validation data.
"""

# define input sequence
raw_seq = normalized_test
# choose a number of time steps
n_steps = 400
# choose a number of prediction steps
pred_steps = 1
# mean_batch
mean_batch = 1


# split into samples
X_test, y_test = split_sequence(raw_seq, n_steps, pred_steps, mean_batch)


"""### Forecasting

Use the pre-trained model to make forecasting on the validation data.
"""

# init 2 sets for predictions and real values (labels)
all_preds_test = []
all_real_test = []

# iterate through the validation samples
for i in range(X_test.shape[0]):
    # print progress
    if i%100==0:
        print(i,'/',X_test.shape[0])

    # define model's input window
    x_input = X_test[i]

    # reshape appropriately
    x_input = x_input.reshape((1, int(n_steps/mean_batch), n_features))
    # predict
    yhat = model.predict(x_input, verbose=0)

    # inverse transform of the normalized scale back to the original scale of
    # CQI data [0,15]
    y_pred = yhat
    y_real = y_test[i]
    y_pred_inversed = np.rint(scaler.inverse_transform(y_pred))
    y_real_inversed = scaler.inverse_transform(np.array(y_real).reshape(-1,1))

    # store predictions and real values (labels)
    all_preds_test.append(y_pred_inversed)
    all_real_test.append(y_real_inversed)

"""### Evaluation

Plot the CQI forecasting compared with the real values.
"""

# reshape appropriately

all_preds_test = np.array(all_preds_test).reshape(-1)
all_real_test = np.array(all_real_test).reshape(-1)
print(np.mean(np.abs(all_preds_test-all_real_test)))

# plot
plt.figure(figsize=[10,5])
plt.plot(all_preds_test[0:2000],'orange',label="yhat")
plt.plot(all_real_test[0:2000],'blue',label="y")
plt.ylim([0,16])
plt.legend()

"""Calculate Mean Absolute Error (MAE) between the forecasting and the real values."""

print("Accuracy: ", np.count_nonzero(all_preds_test==all_real_test)/len(all_preds_test))

print("MAE:", round(mean_absolute_error(all_preds_test, all_real_test),2))

"""Calculate Mean Squared Error (MSE) between the forecasting and the real values."""

print("MSE:", round(mean_squared_error(all_preds_test, all_real_test),2))
