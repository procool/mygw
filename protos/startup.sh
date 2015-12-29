#! /bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

if [ "x$1"="xstart" ]; then
	echo "Restarting PF..."
	/sbin/pfctl -f /etc/pf.conf
	echo "Running mygw project startup scripts..."
	@SCRIPTS@/pfctl_ipdb_reinit.py;
fi


