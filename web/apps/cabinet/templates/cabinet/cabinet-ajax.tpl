    <div class="lk_network_attributes">

      <div class="lk_network_attribute">
        <div class="lk_network_attr_var">
          IP:
        </div>
        <div class="lk_network_attr_val">
          {{ REQUEST.remote_addr }}
        </div>
      </div>

      <div class="lk_network_attribute">
        <div class="lk_network_attr_var">
          MAC:
        </div>
        <div class="lk_network_attr_val">
          {{ REQUEST.remote_ether }}
        </div>
      </div>

      <div class="lk_network_attribute">
        <div class="lk_network_attr_var">
          <div>Inet:</div>
          <div class="lk_contype_selection"><a href="#/cabinet/set/access/none">DIRECT</a></div>
          <div class="lk_contype_selection"><a href="#/cabinet/set/access/tor">TOR</a></div>
          <!--div class="lk_contype_selection"><a href="">Squid</a></div-->
        </div>
        <div class="lk_network_attr_val lk_contype_val">
          <span id="lk_contypemsg">{{ access_type }}</span>
          {% if access_type == "TOR" %}
          <img id="alert" src="{{ STATIC_URL }}/img/alert.gif" width="30px">
          {% endif %}
        </div>
      </div>

    </div>



