var COMMON_URLS = {
    'cabinet': '{{ url_for('cabinet:main') }}',
    'cabinet_set_access_none': '{{ url_for('cabinet:set_access', access_type='none') }}',
    'cabinet_set_access_tor': '{{ url_for('cabinet:set_access', access_type='tor') }}' 
};
