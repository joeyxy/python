#!/usr/bin/env bash
#get the new ip list from apnic,then get the cn ipv4 list.

date=`date +%Y-%m%d-%H%M`

rm -rf delegated-apnic-latest

wget http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest

cat delegated-apnic-latest  |grep 'CN|ipv4' | awk -F"|" '{print $4,$5}' > newip_$date.txt
