<div class="wrapper">
    <div class="tabs_wrapper">
      <ul class="tabs">
        <li><a href="#cabinet" class="cabinet" title="Cabinet">Cabinet</a></li>
        <li><a href="#adminko" class="adminko" title="Adminko">Adminko</a></li>
      </ul>
    </div>

    <div class="middle">
      <div id="maincontent_wrapper">
        Wait!
      </div>
    </div>

    <div class="push"></div>
</div>


<script type="text/javascript">
$( document ).ready(function() {
    $.getScript('{{ url_for('mainpage:urls') }}', function(urls) {
        sammy_app.run();
    });
});

</script>

