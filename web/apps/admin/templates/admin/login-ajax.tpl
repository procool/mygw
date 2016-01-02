<div class="login_form_wrapper">
  <h3>Adminko Login Form</h3>
<form onSubmit="admin_login();">
  <div class="login_form_username">
    <input type="text" class="username" name="username" placeholder="Username">
  </div>

  <div class="login_form_password">
    <input type="password" class="passwd" name="passwd" placeholder="Password">
  </div>

  <div class="login_form_buttons">
    <input type="button" value="Log in!" onClick="admin_login();">
  </div>
</form>
</div>

<script type="text/javascript">
    $('.login_form_wrapper .username,.passwd').on('keyup', function(e) {
        if (e.which == 13) { 
            admin_login(); 
            e.preventDefault(); 
        }
    });
</script>

