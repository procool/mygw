

        <!----------------------- Right ------------------------>
        <div class="admin_data" style="overflow: hidden; padding: 0px 0px 0px 35px; font-size: 18px;">
            <div class="admin_wrapper_buttons left" style="background-color: none; text-align: center; overflow: hidden;">
              <div class="button left" style="margin: 10px;" onClick="admin_geturl('{{ url_for('admin:system_shutdown', command='reboot') }}')">REBOOT</div>
              <div class="button left" style="margin: 10px;" onClick="admin_geturl('{{ url_for('admin:system_shutdown', command='poweroff') }}')">Power OFF</div>
            </div>                      <!-- Close for <div class="admin_wrapper_buttons"> -->
            <div class="admin_states right" style="border-radius: 5px; background-color: #edeeee; font-size: 15px; margin: 0px 50px 15px 0px; padding: 10px 5px 10px 5px; overflow: hidden; white-space: nowrap;">
              <div class="admin_states_uptime" style="padding: 0px 0px 25px 0px;">
                  <div class="admin_state_var left" style="background-color: none; width: 150px;">Up time:</div>
                  <div class="admin_state_val left js-admin-status-uptime"> -- </div></div>
              <div>
                  <div class="admin_state_var left" style="background-color: none; width: 150px;">Load average: </div>
                  <div class="admin_state_val left js-admin-status-avg"> --, --, -- </div>
              </div>
            </div>                      <!-- Close for <div class="admin_states" -->
            <div class="admin_messages js-admin-status-messages-wrap" style="border-radius: 10px; background-color: whute; border: 2px #666666 solid; margin: 100px 5px 5px 5px; padding: 10px; overflow-y:scroll; width:95%; height:350px;">
                <h5>tail -f /var/log/messages</h5>
<div class="js-admin-status-messages" style="font-size: 12px;">
</div>
            </div>                      <!-- Close for <div class="admin_messages" -->
        </div>                          <!-- Close for <div class="admin_data"> -->
        <!----------------------- Right ------------------------>


