<!DOCTYPE html>
<html>
<head>
    <title>myECAD Project</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}/css/index.css">
    <link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}/css/normalize.css">
    <link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}/css/common.css">
    <link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}/css/tabs.css">


    <script type="text/javascript" language="javascript" src="{{ STATIC_URL }}/js/jquery-1.11.3.min.js"></script>
    <!--script type="text/javascript" language="javascript" src="{{ STATIC_URL }}/js/sammy-0.7.6.min.js"></script-->
    <script type="text/javascript" language="javascript" src="{{ STATIC_URL }}/js/sammy.js"></script>
    <script type="text/javascript" language="javascript" src="{{ STATIC_URL }}/js/websockets.js"></script>
    <script type="text/javascript" language="javascript" src="{{ STATIC_URL }}/js/common.js"></script>


</head>
<body>

<div class="wrapper">
{% block maincontent %}
{% endblock %}
    <div class="push"></div>
</div>

<div class="footer">
    <p>Copyright (c) 2016</p>
</div>

    <script type="text/javascript" src="{{ STATIC_URL }}/js/script.js"></script>

</body>
</html>

