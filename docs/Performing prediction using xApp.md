### Performing prediction using the trained model

Once the model training is completed, the two files that are created include
1) Trained model for use in xApp for prediction: [trained_model.keras](https://github.com/mprsk/CQI-Prediction/blob/main/trained_model.keras)
2) MinMaxScalre used during training which can be used in xApp during prediction: [scaler_training.bin](https://github.com/mprsk/CQI-Prediction/blob/main/scaler_training.bin)

### Loading the trained model into the xApp for the prediction
The xApp  [xapp_mac_stats_prediction.py](https://github.com/mprsk/CQI-Prediction/blob/main/xapp_mac_stats_prediction.py) which is used for the data collection also has the prediction integrated. The below class ```MACCallback``` shows the integration of the prediction model. Especially, note that in the definition of ```__init__(self)```, we load the saved model and the scaler described above:

```
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


```
