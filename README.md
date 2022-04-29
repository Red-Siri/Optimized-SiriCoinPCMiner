# Deprecated SiriCoinPCMiner
Why deprecated? Simply because there's a [better one](https://github.com/alberiolima/siriCoin) out there made by @alberiolima

Optimized Siri-Coin PC miner reaching 300 KH/s or more!  

# Setup  

## Windows:  
Go over to releases and download the exe, it's as fast as the python script ;)  

## Linux:  

You have two options:  

a) Download the pre-compiled binary (Slower)  
then run chmod +x SiriCoinPCMiner  
To run: ./SiriCoinPCMiner  

b) Install python 3 and run it using the script (faster)  

```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9
pip3 install -r requirements.txt
python3 SiriCoinPCMiner.py
```

Happy mining! Feel free to fork and submit issues!

