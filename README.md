# ITU AI/ML in 5G Challenge: Applying Machine Learning in Communication Networks
## Submission Details:

**Team:** Wireless Communications and Navigation (WCN) Lab, Dept. of Electrical Engineering, Indian Institute of Technology Jodhpur

**Team Members:**
1) Mr. Ankush Chaudhary, M. Tech 1st Year, Intelligent Communication Systems, Dept. of EE, IIT Jodhpur
2) Ms. Aswathy P., Project Associate, WCN Lab, Dept. of EE, IIT Jodhpur
   
**Faculty Mentors:**
1) Dr. Sai Kiran M. P. R., Assistant Professor, Dept. of EE, IIT Jodpur
2) Dr. Arun Kumar Singh, Associate Professor, Dept. of EE, IIT Jodhpur
   
## Report Submitted
To access the detailed report or input document submitted: [Input Document for Hackathon](https://github.com/mprsk/CQI-Prediction/blob/main/docs/INPUT%20DOCUMENT%20-%20IITJ%20-%20A%20Real%20Time%20CQI%20Prediction%20Framework%20for%20Proactive%20Resource%20Scheduling%20in%205G%20Enabled%20Drones%20Using%20%20AI.pdf)

For accessing the PPT Slides: [PPT Submitted for Hackathon](https://github.com/mprsk/CQI-Prediction/blob/main/docs/PPT-IITJ-A%20Real-time%20CQI%20Prediction%20Framework%20for%20Proactive%20Resource%20Scheduling%20in%205G%20Enabled%20Drones%20Using%20%20AI.pdf)

## File Descriptions:
In this project, we use [Open Air Interface - OAI](https://openairinterface.org/) 5G CN, RAN, and FlexRIC for deployment of O-RAN compliant 5G network. The below describes the usage of individual files:
1) [DataPreparation.m](https://github.com/mprsk/CQI-Prediction/blob/main/DataPreparation.m): A MATLAB script written for preparing an expect script that can automate varying channel parameters (noise power in this case) over telnet session in OAI RF Simulator periodically. This will help us in generating a CQI database ([CQI_DATASET](https://github.com/mprsk/CQI-Prediction/blob/main/CQI_DATASET)) that can be used for model training.
2) [channel_parameter_simulator.exp](https://github.com/mprsk/CQI-Prediction/blob/main/channel_parameter_simulator.exp): A sample expect script generated using [DataPreparation.m](https://github.com/mprsk/CQI-Prediction/blob/main/DataPreparation.m) where noise power is modified every 100ms in the range of [-15 dB, -5 dB].
3) [channel_parameter_simulator_validation.exp](https://github.com/mprsk/CQI-Prediction/blob/main/channel_parameter_simulator_validation.exp): Another expect script generated using [DataPreparation.m](https://github.com/mprsk/CQI-Prediction/blob/main/DataPreparation.m) where noise power is modified every 100ms in the range of [-15 dB, -5 dB] used for validation. This is created for testing the developed AI model performance with unseen data during training.
4) [CQI_DATASET](https://github.com/mprsk/CQI-Prediction/blob/main/CQI_DATASET): A sample CQI dataset (SQLite3 DB) generated using the [channel_parameter_simulator.exp](https://github.com/mprsk/CQI-Prediction/blob/main/channel_parameter_simulator.exp) script. The dataset is acquired using the xApp ([xapp_mac_stats_prediction.py](https://github.com/mprsk/CQI-Prediction/blob/main/xapp_mac_stats_prediction.py))
5) [xapp_mac_stats_prediction.py](https://github.com/mprsk/CQI-Prediction/blob/main/xapp_mac_stats_prediction.py): xAPP compatible with FlexRIC and OAI 5G Protocol Stack used for CQI dataset collection and real-time prediction. The ML model is based on Bi-LSTM with SeLu activation units. The xApp simultaneously lodges the CQI data collected into SQLite3 DB and performs prediction. During validation of the model, the channel variations can be induced using a new expect script generated using [channel_parameter_simulator.exp](https://github.com/mprsk/CQI-Prediction/blob/main/channel_parameter_simulator.exp) and [DataPreparation.m](https://github.com/mprsk/CQI-Prediction/blob/main/DataPreparation.m)
6) [CQI_PREDICTION_OAI.py](https://github.com/mprsk/CQI-Prediction/blob/main/CQI_PREDICTION_OAI.py): Bi-LSTM model with SELU activation units developed for prediction of CQI in Python 3. The model takes the input of CQI values for the past 400 frames and predicts the CQI value of the upcoming frame.
7) [trained_model.keras](https://github.com/mprsk/CQI-Prediction/blob/main/trained_model.keras): The trained model saved using Keras libraries and can be used for prediction or validation. This is used in the xApp ([xapp_mac_stats_prediction.py](https://github.com/mprsk/CQI-Prediction/blob/main/xapp_mac_stats_prediction.py)) for validation of the model and prediction of CQI
8) [scaler_training.bin](https://github.com/mprsk/CQI-Prediction/blob/main/scaler_training.bin): MinMaxScaler used during training. This is required for prediction in xApp ([xapp_mac_stats_prediction.py](https://github.com/mprsk/CQI-Prediction/blob/main/xapp_mac_stats_prediction.py))
9) [gnb.sa.band78.fr1.106PRB.2x2.usrpn300.conf](https://github.com/mprsk/CQI-Prediction/blob/main/gnb.sa.band78.fr1.106PRB.2x2.usrpn300.conf): OAI gNB configuration file for supporting 2x2 MIMO with 40 MHz bandwidth, 30 KHz SCS, and TDD configuration
10) [ue.conf](https://github.com/mprsk/CQI-Prediction/blob/main/ue.conf): OAI UE configuration file for supporting 2x2 MIMO
11) [channelmod_rfsimu.conf](https://github.com/mprsk/CQI-Prediction/blob/main/channelmod_rfsimu.conf): Channel model configuration for OAI RF Simulator

## Deployment Steps:
1) [Setup OAI 5G CN, RAN, and FlexRIC](https://github.com/mprsk/CQI-Prediction/blob/main/docs/OAI%20Setup.md)
2) [Data Collection Setup](https://github.com/mprsk/CQI-Prediction/blob/main/docs/Data%20Collection%20Setup.md)
3) [Performing Prediction Using xApp](https://github.com/mprsk/CQI-Prediction/blob/main/docs/Performing%20prediction%20using%20xApp.md)
