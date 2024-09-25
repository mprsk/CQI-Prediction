After starting OAI CN, RAN, and FlexRIC using the guide [Setup OAI 5G CN, RAN, and FlexRIC](https://github.com/mprsk/CQI-Prediction/blob/main/docs/OAI%20Setup.md), follow the below steps for setting up data collection.

### Vary channel parameters in the DL
Run the expect script ([channel_parameter_simulator.exp](https://github.com/mprsk/CQI-Prediction/blob/main/channel_parameter_simulator.exp)) generated using the MATLAB script ([DataPreparation.m](https://github.com/mprsk/CQI-Prediction/blob/main/DataPreparation.m))

The output should like the following
![Channel simulator](https://github.com/mprsk/CQI-Prediction/blob/main/docs/img/ChannelSimulator.png)

While this is running, on the UE logs, you can observe the change in CQI values as below
![UE logs with cannel simulator](https://github.com/mprsk/CQI-Prediction/blob/main/UE%20CQI%20Logs.png)

### Setting up of xApp
Run the xApp [xapp_mac_stats_prediction.py](https://github.com/mprsk/CQI-Prediction/blob/main/xapp_mac_stats_prediction.py). It shows the DB name and location where the data collection is performed. The same is shown in below figure.
![xApp data collection](https://github.com/mprsk/CQI-Prediction/blob/main/xApp%20DB%20location.png)



