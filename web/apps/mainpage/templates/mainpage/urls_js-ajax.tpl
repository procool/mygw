var COMMON_URLS = {
    'cabinet_set_access_none': '{{ url_for('cabinet:set_access', access_type='none') }}',
    'cabinet_set_access_tor': '{{ url_for('cabinet:set_access', access_type='tor') }}',
    'cabinet': '{{ url_for('cabinet:main') }}',
    'login': '{{ url_for('admin:login') }}',
    'login_test': '{{ url_for('admin:login_test') }}',
    'logout': '{{ url_for('admin:logout') }}',
    'admin': '{{ url_for('admin:main') }}',
    'admin_status': '{{ url_for('admin:status') }}',
    'admin_sys_reboot': '{{ url_for('admin:system_shutdown', command='reboot') }}',
    'admin_sys_poweroff': '{{ url_for('admin:system_shutdown', command='poweroff') }}',
    'underconstruction': '{{ url_for('mainpage:underconstruction') }}'
};
