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




