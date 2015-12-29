include conf/local.mk

.DEFAULT_GOAL := help

WEB		?= ${ROOT}/web
DAEMONS		?= ${ROOT}/daemons
SCRIPTS		?= ${ROOT}/scripts
CRONSC		?= ${SCRIPTS}/cron
GLOBALS		?= ${ROOT}/globals
APPS		?= ${WEB}/apps
PROTOS		?= ${ROOT}/protos
CONFIG		?= ${ROOT}/conf
LOGS		?= ${ROOT}/logs
TEMPLATES	?= ${WEB}/templates
ASSETS		?= ${WEB}/assets
HTTPD_USER	?= ${OWNER}
HTTPD_GROUP	?= ${OWNER_GROUP}
HTTPD_LOGS	?= ${ROOT}/logs
MAKE		?= make


NETWORK_INT := $(shell python globals/utils/get_net_data.py ${ADDR_INT} net)
NETMASK_INT := $(shell python globals/utils/get_net_data.py ${ADDR_INT} mask)
BROADCAST_INT := $(shell python globals/utils/get_net_data.py ${ADDR_INT} broadcast)
IP_INT := $(shell python globals/utils/get_net_data.py ${ADDR_INT} addr)
CIDR_INT := $(shell python globals/utils/get_net_data.py ${ADDR_INT} cidr)
NET_INT = ${IP_INT}/${CIDR_INT}

IFCONFIG_INT    ?= inet ${IP_INT} netmask ${NETMASK_INT}

help:
	@echo '\
	Avalible targets:\
	*	init		- Build configs based on conf/local.mk;\
	*	configs		- Link configs to system directories;\
		\
		\
	Targets marked by "*" need superuser privileges!\
	'

configs: configs-freebsd

configs-freebsd: init
	@mkdir -p /usr/local/etc/supervisor
	@ln -sf ${CONFIG}/supervisor.conf /usr/local/etc/supervisor/mygw.conf
	@mkdir -p /usr/local/etc/nginx/sites-enabled
	@ln -sf ${CONFIG}/nginx.conf /usr/local/etc/nginx/sites-enabled/mygw.conf
	@ln -sf ${SCRIPTS}/startup.sh /usr/local/etc/rc.d/z_mygw_startup.sh
	@cp ${CONFIG}/dhcpd.conf /usr/local/etc/dhcpd.conf
	@cp ${CONFIG}/named.conf /usr/local/etc/namedb/named.conf
	@cp ${CONFIG}/rc.conf /etc/rc.conf
	@cp ${CONFIG}/pf.conf /etc/pf.conf
	@cp ${PROTOS}/fingerprints /etc/fingerprints
	@cp ${PROTOS}/sysctl.conf /etc/sysctl.conf
	@cp ${CONFIG}/resolv.conf /etc/resolv.conf
	@cp ${CONFIG}/privoxy.conf /usr/local/etc/privoxy/config
	@cp ${CONFIG}/torrc /usr/local/etc/tor/torrc
	@cp ${CONFIG}/hosts /etc/hosts
	@cp ${PROTOS}/sshd_config /etc/ssh/sshd_config
	@ln -sf ${CONFIG}/haproxy.conf /usr/local/etc/haproxy.conf
#	@cp ${CONFIG}/squid.conf /usr/local/etc/squid/squid.conf





init: build_protos
	${call build_exec, ${PROTOS}/start.py, ${APPS}/start.py}
	${call build_exec, ${PROTOS}/startup.sh, ${SCRIPTS}/startup.sh}
#	${call build_exec}

compat_links:
#	ln -s ${PROJECTLIBS}/dbsrc/* ${PROJECTLIBS}/${DB_TABLEPREFIX}db/ >/dev/null 2>&1; "

build_protos: make_dirs compat_links 
	${call build, ${PROTOS}/haproxy.conf, ${CONFIG}/haproxy.conf}
	${call build, ${PROTOS}/supervisor.conf, ${CONFIG}/supervisor.conf}
	${call build, ${PROTOS}/dhcpd.conf, ${CONFIG}/dhcpd.conf}
	${call build, ${PROTOS}/named.conf, ${CONFIG}/named.conf}
	${call build, ${PROTOS}/nginx.conf, ${CONFIG}/nginx.conf}
	${call build, ${PROTOS}/settings.py, ${WEB}/settings/local.py}
	${call build, ${PROTOS}/global_settings.py, ${GLOBALS}/global_settings/local.py}
	${call build, ${PROTOS}/py_path.py, ${APPS}/py_path.py}
	${call build, ${PROTOS}/py_path.py, ${CRONSC}/py_path.py}
	${call build, ${PROTOS}/py_path.py, ${DAEMONS}/py_path.py}
	${call build, ${PROTOS}/py_path.py, ${GLOBALS}/models/py_path.py}
	${call build, ${PROTOS}/py_path.py, ${GLOBALS}/alembic/py_path.py}
	${call build, ${PROTOS}/resolv.conf, ${CONFIG}/resolv.conf}
	${call build, ${PROTOS}/rc.conf, ${CONFIG}/rc.conf}
	${call build, ${PROTOS}/pf.conf, ${CONFIG}/pf.conf}
	${call build, ${PROTOS}/privoxy.conf, ${CONFIG}/privoxy.conf}
	${call build, ${PROTOS}/squid.conf, ${CONFIG}/squid.conf}
	${call build, ${PROTOS}/torrc, ${CONFIG}/torrc}
	${call build, ${PROTOS}/hosts, ${CONFIG}/hosts}
	${call build, ${PROTOS}/resolv.conf, ${CONFIG}/resolv.conf}

make_dirs:
	@mkdir -p ${PROTOS} 2>/dev/null
	@mkdir -p ${CONFIG} 2>/dev/null
	@mkdir -p ${LOGS} 2>/dev/null
	@mkdir -p ${ASSETS} 2>/dev/null
	@mkdir -p ${DAEMONS} 2>/dev/null
	@mkdir -p ${GLOBALS} 2>/dev/null
	@mkdir -p ${GLOBALS}/global_settings 2>/dev/null
	@mkdir -p ${CRONSC} 2>/dev/null
	@chown -R ${OWNER} ${ROOT}
	@chgrp -R ${HTTPD_GROUP} ${ASSETS} 
	@chown -R ${HTTPD_USER}:${HTTPD_GROUP} ${LOGS} 



define build_exec
	${call build, ${1}, ${2}} && chmod a+x ${2}
endef


define build
	@sed \
		-e 's%@ROOT@%${ROOT}%g' \
		-e 's%@WEB@%${WEB}%g' \
		-e 's%@APPS@%${APPS}%g' \
		-e 's%@GLOBALS@%${GLOBALS}%g' \
		-e 's%@HOSTNAME@%${HOSTNAME}%g' \
		-e 's%@DOMAIN@%${DOMAIN}%g' \
		-e 's%@DEFAULTROUTER@%${DEFAULTROUTER}%g' \
		-e 's%@IF_EXT@%${IF_EXT}%g' \
		-e 's%@IFCONFIG_EXT@%${IFCONFIG_EXT}%g' \
		-e 's%@IP_EXT@%${IP_EXT}%g' \
		-e 's%@DNS1@%${DNS1}%g' \
		-e 's%@IF_INT@%${IF_INT}%g' \
		-e 's%@IFCONFIG_INT@%${IFCONFIG_INT}%g' \
		-e 's%@IP_INT@%${IP_INT}%g' \
		-e 's%@NET_INT@%${NET_INT}%g' \
		-e 's%@NETMASK_INT@%${NETMASK_INT}%g' \
		-e 's%@NETWORK_INT@%${NETWORK_INT}%g' \
		-e 's%@CIDR_INT@%${CIDR_INT}%g' \
		-e 's%@BROADCAST_INT@%${BROADCAST_INT}%g' \
		-e 's%@DHCP_RANGE@%${DHCP_RANGE}%g' \
		-e 's%@CONFIG@%${CONFIG}%g' \
		-e 's%@PROTOS@%${PROTOS}%g' \
		-e 's%@CRONSC@%${CRONSC}%g' \
		-e 's%@DAEMONS@%${DAEMONS}%g' \
		-e 's%@SCRIPTS@%${SCRIPTS}%g' \
		-e 's%@LOGS@%${LOGS}%g' \
		-e 's%@TEMPLATES@%${TEMPLATES}%g' \
		-e 's%@ASSETS@%${ASSETS}%g' \
		-e 's%@ROOTCOOKIE@%${ROOTCOOKIE}%g' \
		-e 's%@HTTPD_USER@%${HTTPD_USER}%g' \
		-e 's%@HTTPD_HOST@%${HTTPD_HOST}%g' \
		-e 's%@HTTPD_LOGS@%${HTTPD_LOGS}%g' \
		-e 's%@TIMEDIFF_TZ@%${TIMEDIFF_TZ}%g' \
		-e 's%@OWNER@%${OWNER}%g' \
		-e 's%@DB_TYPE_IDENT@%${DB_TYPE_IDENT}%g' \
		-e 's%@DB_USER@%${DB_USER}%g' \
		-e 's%@DB_PASS@%${DB_PASS}%g' \
		-e 's%@DB_HOST@%${DB_HOST}%g' \
		-e 's%@DB_PORT@%${DB_PORT}%g' \
		-e 's%@DB_NAME@%${DB_NAME}%g' \
		-e 's%@DB_SOCKET@%${DB_SOCKET}%g' \
		-e 's%@MAKE@%${MAKE}%g' \
	< ${1} > ${2}
endef
