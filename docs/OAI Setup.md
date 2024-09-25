The following tutorial has been originally developed at: [OAIC 2024 Workshop - OAI, FLexRIC Documentation](https://openaicellular.github.io/oaic/OAIC-2024-Workshop-oai-flexric-documentation.html)
### Install Dependencies
```
sudo apt install git vim tree net-tools libsctp-dev python3.8 cmake-curses-gui libpcre2-dev python-dev build-essential cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libtool autoconf python3-pip curl bison flex iperf
```
### Install Swig 4.1
```
git clone https://github.com/swig/swig.git
cd swig
git checkout release-4.1
./autogen.sh
./configure --prefix=/usr/
make -j8
sudo make install
```
### Check GCC Version (gcc-10, gcc-12, or gcc-13)

```
gcc --version
```
> [!WARNING]
> If you see that you have gcc 11, follow the steps given [here](https://linuxconfig.org/how-to-switch-between-multiple-gcc-and-g-compiler-versions-on-ubuntu-20-04-lts-focal-fossa) to switch to a different version

### Install Docker Compose for deploying OAI 5G CN

```
sudo apt install -y putty ca-certificates gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt install -y docker-buildx-plugin docker-compose-plugin
```
### Check the version of Docker Compose
```
sudo docker compose --version
```

### Setup OAI 5G Core Network
```
wget -O ~/oai-cn5g.zip https://gitlab.eurecom.fr/oai/openairinterface5g/-/archive/develop/openairinterface5g-develop.zip?path=doc/tutorial_resources/oai-cn5g
unzip ~/oai-cn5g.zip
mv ~/openairinterface5g-develop-doc-tutorial_resources-oai-cn5g/doc/tutorial_resources/oai-cn5g ~/oai-cn5g
rm -r ~/openairinterface5g-develop-doc-tutorial_resources-oai-cn5g ~/oai-cn5g.zip
cd ~/oai-cn5g
sudo docker compose pull
sudo docker compose up -d
```
After execution of all the above commands, check if all the CN containers are deployed using the below command
```
sudo docker ps -a
```
The result should be as shown below
![5G CN containers health status](https://github.com/mprsk/CQI-Prediction/blob/main/docs/OAI%205GCN.png)


### Setup OAI Radio Access Network and UE
Clone the OAI 5G RAN repository and checkout the oaic_workshop_2024_v1 branch. This has the FlexRIC repo cloned into OAI already. Alternatively, one can follow the steps provided by OAI in this [guide](https://gitlab.eurecom.fr/oai/openairinterface5g)
```
git clone https://github.com/openaicellular/openairinterface5G.git ~/oai
cd ~/oai
git checkout oaic_workshop_2024_v1
cd ~/oai/cmake_targets/
./build_oai -I -w SIMU --gNB --nrUE --build-e2 --ninja
```

### Setup FlexRIC
This is required for running the xapp

Clone the OAI 5G RAN repository and checkout the beabdd07 commit.
```
git clone https://github.com/openaicellular/flexric.git ~/flexric
cd ~/flexric
git checkout beabdd07
```
Copy the xApp [xapp_mac_stats_prediction.py](https://github.com/mprsk/CQI-Prediction/blob/main/xapp_mac_stats_prediction.py) into the following folders

```
flexric/examples/xApp/python3
flexric/build/examples/xApp/python3
```

Build the flexRIC module.

```
mkdir build
cd build
cmake ../
```

Install the FlexRIC libraries and xApps
```
make -j`nproc`
sudo make install
```
### Start the gNB and UE softmodems
To start the gNB
```
cd ~/oai/cmake_targets/ran_build/build
sudo ./nr-softmodem -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb.sa.band78.fr1.106PRB.2x2.usrpn300.conf --gNBs.[0].min_rxtxtime 6 --rfsim --sa --rfsimulator.options chanmod --telnetsrv --channelmod.modellist modellist_rfsimu_1
```
To start the UE
```
cd ~/oai/cmake_targets/ran_build/build
sudo ./nr-uesoftmodem -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf -r 106 --numerology 1 --band 78 -C 3319680000 --rfsim --sa --rfsimulator.serveraddr 127.0.0.1 --ue-nb-ant-rx 2 --ue-nb-ant-tx 2 --rfsimulator.options chanmod --telnetsrv --telnetsrv.listenport 9091
```
