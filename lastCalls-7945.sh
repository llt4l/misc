#!/bin/bash

# This script utilises log files found in the web interface of a Cisco 7945 IP Phone
# For this script to work, the phone must have Web Access enabled. The script only works 
# on Cisco 7940 Series Phones, but can be tweaked to work with others as well.
# Written by t4

mkdir lastcallstmp 2>/dev/null

# Credit for the below function goes to jjmarc (https://gist.github.com/jjarmoc/1299906)
echo "function itoa
{
#returns the dotted-decimal ascii form of an IP arg passed in integer format
echo -n $(($(($(($((${1}/256))/256))/256))%256)).
echo -n $(($(($((${1}/256))/256))%256)).
echo -n $(($((${1}/256))%256)).
echo $((${1}%256))
}" > lastcallstmp/itoa

source ./lastcallstmp/itoa
echo -n "" > lastcallstmp/tmp;
echo -n "" > lastcallstmp/tmp2;
echo -n "" > lastcallstmp/tmp3;

if [[ $1 != "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" ]]; then hostname=$1; fi
if [ -z "$hostname" ]; then echo "unknown user"; exit 1; fi

echo "---------------------------------------------------------"
echo "Subject's hostname: $hostname"

model=$(timeout 5 wget -q -O- "http://$hostname" | grep "Model Number</B></TD><td width=20></TD><TD><B>[A-Za-z0-9\-]*" -o | cut -d">" -f7)

echo "Subject's phone model: $model"

wget -q -O- "http://$hostname/CGI/Java/Serviceability?adapter=device.statistics.consolelog" | grep -o "/FS/cache/log[0-9]*.log" | sort | uniq > lastcallstmp/tmp

for i in $(cat lastcallstmp/tmp); do
	wget -q -O- "http://$hostname/$i" >> blah;
	wget -q -O- "http://$hostname/$i" | grep Remote | grep host|  cut -d"(" -f2 | cut -d"," -f1 | cut -d" " -f2 >> lastcallstmp/tmp2;
done

for i in $(cat lastcallstmp/tmp2); do
	echo $((16#$i)) >> lastcallstmp/tmp3;
done;

for i in $(cat lastcallstmp/tmp3);
	do echo"";
	echo -n "Call made to: ";
	itoa $i | tr '\n' ',';
	echo -n " which belongs to: ";
	grep -i $(host $(itoa $i) | cut -d" " -f5 | cut -d"." -f1) u2phones | cut -d"," -f2 | head -n 1| tr '\n' ' ';
	echo - Extension: $(wget -q -O- "http://$( itoa $i)/" | grep -o -P "Phone DN.{0,40}" | rev | cut -d">" -f1 | rev | cut -d"<" -f1);
done;

echo "";

remote=$(wget  -q -O- "http://$hostname/CGI/Java/Serviceability?adapter=device.statistics.streaming.0" | grep -o "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*" | head -n 1)

echo "Last call made to: $remote ($(wget -q -O- 'http://$remote/' | grep -o -P 'Phone DN.{0,40}' | rev | cut -d'>' -f1 | rev | cut -d'<' -f1))";
echo "--------------------------------------------------------";
rm -r lastcallstmp/
