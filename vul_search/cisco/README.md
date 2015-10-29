1.get new ip from apnic
 ./getnew.sh 

2.output the crid format ip
./process_ip.py newip_2015-1029-1441.txt 

3.get the port 80 open ip address
sudo /usr/local/Cellar/zmap/1.2.1/sbin/zmap -w ip.txt -p 80 -o 80.txt

4.poc scan 80 open ip.

5.test the target.