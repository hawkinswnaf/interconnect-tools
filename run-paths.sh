#!/bin/bash
months='01 04'
sites='lax01-38.98 dfw01-38.107 sea01-38.102'

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
connection_spec.server_ip as sip,
connection_spec.client_ip as cip,
GROUP_CONCAT(paris_traceroute_hop.dest_ip, "#")
from 
m_lab.2014_MONTH
where
project = 3
AND LEFT(connection_spec.server_ip,SERVERIPLEN) = "SERVERIP"
AND (include(input/comcast.input))
group by test_id, sip, cip
END`
		query=`sed -e s/MONTH/$month/g -e s/SERVERIPLEN/$iplen/g -e s/SERVERIP/$ip/g <<< $sql`
		bq query --format csv  $query | tee output/output-$site-$month-paths.txt
	done
done
