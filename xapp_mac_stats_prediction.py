import xapp_sdk as ric
import time
import os
import pdb
import numpy as np
import tensorflow as tf
import sys
from tensorflow import keras
from tensorflow.keras.models import Model
from sklearn.preprocessing import MinMaxScaler
from joblib import dump, load


####################
#### MAC INDICATION CALLBACK & AI MODEL FOR CQI PREDICTION
####################

#  MACCallback class is defined and derived from C++ class mac_cb
#  Whenever the RIC indication message is received, this callback function is called
#  Once we receive the CQI update, we use the recent CQI data corresponding to 400 frames and make prediction for the next frame CQI

class MACCallback(ric.mac_cb):
    # Variables required for preparing input data. Trained model is already saved
    prev_frame = 0
    ready = 0
    input = np.empty(400)
    model = Model()
    scaler = MinMaxScaler(feature_range=(0, 1))
    pred_CQI = 0
    pred_count = 0;
    accuracy = 0;
    mae = 0;
    mse = 0;
    t = time.time()
    pred_log = '';
    # Define Python class 'constructor'
    def __init__(self):

        # Call C++ base class constructor
        ric.mac_cb.__init__(self)

        # Load the trained model for real-time prediction
        self.model = tf.keras.models.load_model('trained_model.keras')
        self.model.summary()

        # Load the scaler used during the training (MinMaxScaler)
        self.scaler = load('scaler_training.bin')
        print('Min: %f, Max: %f' % (self.scaler.data_min_, self.scaler.data_max_))

    # Override C++ method: virtual void handle(swig_mac_ind_msg_t a) = 0;
    def handle(self, ind):
        # Print swig_mac_ind_msg_t
        if len(ind.ue_stats) > 0:
           if (ind.ue_stats[0].frame != self.prev_frame):

              # Wait until the input buffer is filled. Our input for prediction is recent CQI values for 400 frames
              if (self.ready < 400):
                 self.input[self.ready] = ind.ue_stats[0].wb_cqi
                 self.ready = self.ready + 1

              # Once the input is ready, predict the CQI value of upcoming frame everytime
              else:
                 # Perform left shift to inser the recent CQI at the end of the input
                 self.input[0:398] = self.input[1:399]
                 self.input[399] = ind.ue_stats[0].wb_cqi
                 try:
                    self.pred_log = self.pred_log + '['+str(self.prev_frame) + ',' + str(int(self.input[-1])).rjust(2, '0') + ',' + str(int(self.pred_CQI)).rjust(2, '0') + '],   '
                    if(self.pred_count%10==0): 
                       self.pred_log = self.pred_log + '\n'
                    if(self.pred_count>0):
                       if(self.input[-1]==self.pred_CQI):
                          self.accuracy = self.accuracy+1
                       error = np.abs(self.input[-1]-self.pred_CQI)
                       self.mae = self.mae+ error
                       self.mse = self.mse + error**2

#                    print('Frame: ' + str(self.prev_frame) + ', Real CQI: '+ str(self.input[-1]) + ', Predicted CQI: ' + str(self.pred_CQI))
                       if(self.pred_count%100==0):
                          error_mae = round(self.mae.item()/self.pred_count,2)
                          error_mse = round(self.mse.item()/self.pred_count,2)
                          acc = round(self.accuracy*100/self.pred_count,2)
                          print(self.pred_log)
                          print('Stats Summary (100 frames) - Time Elapsed: '+ str(round(time.time()-self.t,2)) + ' Sec, MAE: ' + str(error_mae) + ' (CQI), MSE: ', str(error_mse) + ' (CQI^2)')

#                         To print accuracy enable the below line and comment the aboe line
#                          print('Time Elapsed: '+ str(round(time.time()-self.t,2)) + ' Sec, Frame: ' + str(self.prev_frame) + ', Accuracy: '+ str(acc) + '%, MAE: ' + str(error_mae) + ', MSE: ', str(error_mse))

                          print('------------------------------------------------------------------------------------')
                          self.pred_log = '\n\nFrame Level Predictions [Frame Number, Actual CQI, Predicted CQI]\n\n'
                    
                    self.prev_frame = ind.ue_stats[0].frame

                    # Scale the input using the MinMaxScaler fitted during the training procedure. Scales from [0,15] -> [0,1]
                    normalized_in = self.scaler.transform(self.input.reshape(len(self.input),1))


                    # Make the prediction and do inverse of scaling to get the CQI mapping of [0,15] from scaled prediction [0,1]
                    self.pred_CQI =  np.rint(self.scaler.inverse_transform(self.model.predict(normalized_in.reshape((1, 400, 1)), verbose=0))) 
                    if(self.pred_CQI>15): self.pred_CQI = 15
                    self.pred_count = self.pred_count + 1
                 except Exception as e: print(e)

####################
####  GENERAL CONFIGURATION
####################

# Initialize the RIC
ric.init()

# Check the connected nodes (gNB in this case)
conn = ric.conn_e2_nodes()
assert(len(conn) > 0)

# Print the E2 nodes information , if any
for i in range(0, len(conn)):
    print("Global E2 Node [" + str(i) + "]: PLMN MCC = " + str(conn[i].id.plmn.mcc))
    print("Global E2 Node [" + str(i) + "]: PLMN MNC = " + str(conn[i].id.plmn.mnc))

####################
#### CONFIGURING MAC INDICATION CALLBACK FOR MONITORING AND PREDICTION
####################

# Configure the MAC SM indications with 10 ms intervals (corresponding to every frame) along with callback config
mac_hndlr = []
for i in range(0, len(conn)):
    mac_cb = MACCallback()
    hndlr = ric.report_mac_sm(conn[i].id, ric.Interval_ms_10, mac_cb)
    mac_hndlr.append(hndlr)     
    time.sleep(1)


# Define the xApp execution time (100s in this case)
time.sleep(100)

# Remove the handler created for MAC and free resources
for i in range(0, len(mac_hndlr)):
    ric.rm_report_mac_sm(mac_hndlr[i])


# Stop the xApp. Avoid deadlock. ToDo revise architecture 
while ric.try_stop == 0:
    time.sleep(1)

print("xApp executed successfully")
