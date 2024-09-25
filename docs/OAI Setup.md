The following tutorial has been originally developed at: [OAIC 2024 Workshop - OAI, FLexRIC Documentation](https://openaicellular.github.io/oaic/OAIC-2024-Workshop-oai-flexric-documentation.html)
# Install Dependencies
```
sudo apt install git vim tree net-tools libsctp-dev python3.8 cmake-curses-gui libpcre2-dev python-dev build-essential cmake libfftw3-dev libmbedtls-dev libboost-program-options-dev libconfig++-dev libtool autoconf python3-pip curl bison flex iperf
```
# Install Swig 4.1
```
git clone https://github.com/swig/swig.git
cd swig
git checkout release-4.1
./autogen.sh
./configure --prefix=/usr/
make -j8
sudo make install
```
# Check GCC Version (gcc-10, gcc-12, or gcc-13)

```
gcc --version
```
[!WARNING]
If you see that you have gcc 11, follow the steps given [here](https://linuxconfig.org/how-to-switch-between-multiple-gcc-and-g-compiler-versions-on-ubuntu-20-04-lts-focal-fossa) to switch to a different version

