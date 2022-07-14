# Optimized Siricoin PC Miner
Optimized Siricoin PC miner reaching 800 KH/s or more!  
![image](https://user-images.githubusercontent.com/75716744/179065743-5f3c027a-fcd1-47c7-b01c-86b3f188f9c1.png)



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

**Extra step on ARM:**  
You have to run  
```
pip3 uninstall sha3
pip3 install pysha3
```
before starting the miner!


Happy mining! Feel free to fork and submit issues!

