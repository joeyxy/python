MongoDB Scanner
===============
* Author: Ettack  
* Email : ettack@gmail.com

**This projecgt is a scanner to find mongodb with remote connection enabled, which is the default setting, but risky as well.**

There are two version of scanners:

* mongoScan.py
* mongoScan_multiThreads.py

**_mongoScan.py_**  

    Single threads scanner, with instant state output and recoding IPs into a file.
    Usage: mongoScan.py [IpListFile] [OutputFile]

**_mongoScan\_MultiThreads.py_**  

    Multiple threads scanner, with time estimation. Only output success IPs.
    Usage: mongoScan_multiThreads.py [ThreadsNumber] [IpListFile]

* Parameters:
    * _IpListFile_  
    **Could be any text file that contains some ip addresses.**  
    <pre>
    There is no strict file format limit because I use regex to extract IPs.
    One of the best tools generating host list is nmap, here's how I used it:
        nmap -sL -oG -n ip.txt 192.168.1.1/16
        ----Generate a list from a range of IP, without scanning.
		nmap -p27017 -n --open -T4 -sT -oG ip.txt 192.168.1.1/24
        ----Find 27017(default port for mongoDB) opened IP
    </pre>

    * _ThreadsNumber_  
    **Decides the speed of the scan.**  
    <pre>
    Generally, larger threads number gives faster performance, but setting it too high may cause instablity.
    </pre>
