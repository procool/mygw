<div class="admin_wrapper"><div class="admin_wrapper_tr">
<div class="menu_vertical">

  <!-- Start of Menu -->
  <div id="cssmenu">
    <ul>
      <li><a href="#adminko/status"><span>STATUS</span></a></li>
      <li><a href="#adminko/notes"><span>NOTES</span></a></li>
      <li class="has-sub"><a href="#adminko/tools"><span>TOOLS</span></a>
        <ul>
          <li><a href="#adminko/tools_speed"><span>SPEED TEST</span></a></li>
          <li><a href="#adminko/tools_ping"><span>Ping</span></a></li>
          <li><a href="#adminko/tools_traceroute"><span>Traceroute</span></a></li>
        </ul>
      </li>
      <li class="has-sub"><a href="#adminko/network"><span>NETWORK</span></a>
        <ul>
          <li><a href="#adminko/nw_access_lists"><span>Access lists</span></a></li>
          <li><a href="#adminko/nw_dhcp"><span>DHCP</span></a></li>
          <li><a href="#adminko/nw_dns"><span>DNS</span></a></li>
        </ul>
      </li>
      <li class="has-sub"><a href="#adminko"><span>SYSTEM</span></a>
        <ul>
          <li><a href="#adminko/sys_users"><span>Users</span></a></li>
          <li class="has-sub"><a href="#adminko"><span>Services</span></a>
            <ul>
              <li><a href="#adminko/sys_srv_vpn"><span>VPN Server</span></a></li>
              <li><a href="#adminko/sys_srv_dns"><span>DNS</span></a></li>
              <li><a href="#adminko/sys_srv_dhcp"><span>DHCP</span></a></li>
            </ul>
          </li>
        </ul>
      </li>
      <!--li><a href="#adminko/refresh"><span>REFRESH</span></a></li-->
      <li><a href="#logout"><span>LOGOUT</span></a></li>
    </ul>
  </div>
  <!-- End of Menu -->
</div>

<div class="admin_content_wrapper">
Admin page

<br>
<br>
</div>

</div></div>

<script type="text/javascript">
    setup_menu();
    client_session_set('{{ request.session }}');
</script>

