# ITU AI/ML in 5G Challenge: Applying Machine Learning in Communication Networks
## Submission Details:

**Team:** Wireless Communications and Navigation (WCN) Lab, Dept. of Electrical Engineering, Indian Institute of Technology Jodhpur

**Team Members:**
1) Mr. Ankush Chaudhary, M. Tech 1st Year, Intelligent Communication Systems, Dept. of EE, IIT Jodhpur
2) Mr. Bheem Singh Akhawat, M. Tech 2nd Year, Intelligent Communication Systems, Dept. of EE, IIT Jodhpur
3) Ms. Aswathy P., Project Associate, WCN Lab, Dept. of EE, IIT Jodhpur
   
**Faculty Mentors:**
1) Dr. Sai Kiran M. P. R., Assistant Professor, Dept. of EE, IIT Jodpur
2) Dr. Arun Kumar Singh, Associate Professor, Dept. of EE, IIT Jodhpur

## File Descriptions:
In this project, we use [Open Air Interface - OAI](https://openairinterface.org/) 5G CN, RAN, and FlexRIC for deployment of O-RAN compliant 5G network. The below describes the usage of individual files:
1) [DataPreparation.m](https://github.com/mprsk/CQI-Prediction/blob/main/DataPreparation.m): A MATLAB script written for preparing an expect script that can automate varying channel parameters (noise power in this case) over telnet session in OAI RF Simulator periodically. This will help us in generating a CQI database ([CQI_DATASET](https://github.com/mprsk/CQI-Prediction/blob/main/CQI_DATASET)) that can be used for model training.
2) [channel_parameter_simulator.exp](https://github.com/mprsk/CQI-Prediction/blob/main/channel_parameter_simulator.exp): A sample expect script generated using [DataPreparation.m](https://github.com/mprsk/CQI-Prediction/blob/main/DataPreparation.m) where noise power is modifed every 100ms in the range of [-15 dB, -5 dB].
3) [CQI_DATASET](https://github.com/mprsk/CQI-Prediction/blob/main/CQI_DATASET): A sample CQI dataset (SQLite3 DB) generated using the [channel_parameter_simulator.exp](https://github.com/mprsk/CQI-Prediction/blob/main/channel_parameter_simulator.exp) script. The dataset is acquired using the xApp ([xapp_mac_stats_prediction.py](https://github.com/mprsk/CQI-Prediction/blob/main/xapp_mac_stats_prediction.py))
4) [xapp_mac_stats_prediction.py](https://github.com/mprsk/CQI-Prediction/blob/main/xapp_mac_stats_prediction.py): xAPP compatible with FlexRIC and OAI 5G Protocol Stack used for CQI dataset collection and real-time prediction. The ML model is baed on Bi-LSTM with SeLu activation units. The xApp simultaneously lodges the CQI data collected into SQLite3 DB and performs prediction. During validation of the model, the channel variations can be induced using a new expect script generated using [channel_parameter_simulator.exp](https://github.com/mprsk/CQI-Prediction/blob/main/channel_parameter_simulator.exp) and [DataPreparation.m](https://github.com/mprsk/CQI-Prediction/blob/main/DataPreparation.m)
5) 
