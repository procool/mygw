#! /bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

if [ "x$1"="xstart" ]; then
	pfctl -f /etc/pf.conf
	/projects/mygw/scripts/pfctl_ipdb_reinit.py;
fi


