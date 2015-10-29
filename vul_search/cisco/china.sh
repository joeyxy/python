#!/usr/bin/env python 
#Get ip China
#by polly
#get the newest delegated-apnic-latest
grep 'apnic|CN|ipv4' delegated-apnic-latest | cut -f 4,5 -d '|' | tr '|' ' ' | while read ip cnt
do
	mask=$(bc <<END | tail -1
	pow=32;
	define log2(x) {
	if (x<=1) return (pow);
		pow--;
		return(log2(x/2));
	}
	log2($cnt);
	END
	)
	echo $ip/$mask';'>>chinaip.txt
done
