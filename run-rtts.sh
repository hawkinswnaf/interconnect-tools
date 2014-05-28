#!/bin/bash
months='03'
sites='dfw01-38.107'

if [ ! -d output ]; then
	mkdir output
fi

for siteconfig in $sites; do
	site=${siteconfig%%-*}
	ip=${siteconfig##*-}
	iplen=${#ip}

	echo $site
	echo $ip
	echo $iplen

	for month in $months; do
		sql=`m4 << END
select 
HOUR(SEC_TO_TIMESTAMP(log_time)) as time,
AVG(paris_traceroute_hop.rtt) as rtt
from 
m_lab.2014_MONTH
where
project = 3
AND LEFT(connection_spec.server_ip,SERVERIPLEN) = "SERVERIP"
AND (include(input/cogent.hops.src.input))
AND (include(input/comcast.hops.dest.input))
group by time
order by time
END`
		query=`sed -e s/MONTH/$month/g -e s/SERVERIPLEN/$iplen/g -e s/SERVERIP/$ip/g <<< $sql`
		bq query --format csv  $query | tee output/output-$site-$month-rtts.txt
	done
done
