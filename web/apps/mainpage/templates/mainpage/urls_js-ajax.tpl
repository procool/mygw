var COMMON_URLS = {
    'cabinet_set_access_none': '{{ url_for('cabinet:set_access', access_type='none') }}',
    'cabinet_set_access_tor': '{{ url_for('cabinet:set_access', access_type='tor') }}',
    'admin': '{{ url_for('admin:main') }}',
    'login': '{{ url_for('admin:login') }}',
    'login_test': '{{ url_for('admin:login_test') }}',
    'logout': '{{ url_for('admin:logout') }}',
    'cabinet': '{{ url_for('cabinet:main') }}'
};
