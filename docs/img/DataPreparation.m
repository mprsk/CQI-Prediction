clc;
clear all;
close all;

N = 50000; % Number of data points
interval = 0.1; % In seconds
r = [-15, -5]; % Range of noise power in dB

fileID = fopen('channel_parameter_simulator.exp','w');
fprintf(fileID,'#!/usr/bin/expect -f\n');
fprintf(fileID,'\n\n# Developed by Wireless Communications and Navigation Lab, IIT Jodhpur (Author: Kiran M. P. R. S.)\n');
fprintf(fileID,'# Automated expect script generated for channel parameter variation using MATLAB\n');
fprintf(fileID,'# This script continuously varies the DL noise power in the range [-15 dB, -5 dB] thus inducing CQI variations\n');
fprintf(fileID,'# This is used for CQI training dataset generation later used for Bi-LSTM model training\n\n\n');

% To change the channel parameters in DL (at UE)
fprintf(fileID,'spawn telnet 127.0.0.1 9091\n');

fprintf(fileID, 'send "\\r\"\n');
fprintf(fileID,'expect "softmodem_5Gue"\n');

fprintf(fileID,'send "channelmod modify 0 noise_power_dB -50\\r"\n');
fprintf(fileID,'sleep %0.2f\n', interval);

% Generate sample data
for i=1:N
    noise_power_dB = randi(r);
    fprintf(fileID,'send "channelmod modify 0 noise_power_dB %d\\r"\n',noise_power_dB);
    if(mod(i,1000)==0)
        fprintf(fileID,'puts "Progress: %d/%d (%0.2f %%)"\n', i,N,i*100/N);
    end
    fprintf(fileID,'sleep %0.2f\n', interval);

end

