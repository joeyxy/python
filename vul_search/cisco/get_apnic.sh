#!/usr/bin/env bash
FILE=`pwd`/ip_apnic
TMP=/dev/shm/ip.tmp
CNC_FILE=`pwd`/CNC
CTC_FILE=`pwd`/CTC
rm -f $FILE
wget http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest -O $FILE

grep 'apnic|CN|ipv4|' $FILE | cut -f 4,5 -d'|'|sed -e 's/|/ /g' | while read ip cnt
do
       echo $ip:$cnt
       mask=$(cat &lt;&lt; EOF | bc | tail -1

pow=32;
define log2(x) {
if (x&lt;=1) return (pow);
pow--;
return(log2(x/2));
}

log2($cnt)
EOF
)

whois $ip@whois.apnic.net &gt; $TMP.tmp
sed -n '/^inetnum/,/source/p' $TMP.tmp | awk '(/mnt-/ || /netname/)' &gt;  $TMP
NETNAME=`grep ^netname $TMP | sed -e 's/.*:      \(.*\)/\1/g' | sed -e 's/-.*//g'|sed 's: ::g'`

egrep -qi "(CNC|UNICOM|WASU|NBIP|CERNET|CHINAGBN|CHINACOMM|FibrLINK|BGCTVNET|DXTNET|CRTC)" $TMP
  if [ $? = 0 ];then
      echo $ip/$mask &gt;&gt; $CNC_FILE
    else
      egrep -qi "(CHINATELECOM|CHINANET)" $TMP
      if [ $? = 0 ];then
        echo $ip/$mask &gt;&gt; $CTC_FILE
      else
         sed -n '/^route/,/source/p' $TMP.tmp | awk '(/mnt-/ || /netname/)' &gt;  $TMP
         egrep -qi "(CNC|UNICOM|WASU|NBIP|CERNET|CHINAGBN|CHINACOMM|FibrLINK|BGCTVNET|DXTNET|CRTC)" $TMP
         if [ $? = 0 ];then
           echo $ip/$mask &gt;&gt; $CNC_FILE
         else
           egrep -qi "(CHINATELECOM|CHINANET)" $TMP
           if [ $? = 0 ];then
             echo $ip/$mask &gt;&gt; $CTC_FILE
           else
             echo "$ip/$mask $NETNAME" &gt;&gt; `pwd`/OTHER
           fi
         fi
      fi
    fi
done

rm -rf $TMP $TMP.tmp
