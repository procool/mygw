<a href="#cabinet">Cabinet</a>
<a href="#">Adminko</a>
<br>
<br>

<div id="maincontent_wrapper">
Wait!
</div>


<script type="text/javascript">
$( document ).ready(function() {
    $.getScript('{{ url_for('mainpage:urls') }}', function(urls) {
        sammy_app.run();
    });
});

</script>

