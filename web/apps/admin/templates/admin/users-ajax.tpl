<table width="100%" border=1>
<tr>
<th width="5%">ID</th>
<th>LOGIN</th>
<th width="10%">STATUS</th>
<th width="20%">LAST LOGIN</th>
</tr>
{% for user in users %}
<tr>
<td><b>{{ user.id }}</b></td>
<td class="{% if not user.is_active %}table_row_disabled {% endif %}">{{ user.login }}</td>
<td>
{% if user.status == 1 %}
Admin
{% elif user.status == 2 %}
Supervisor
{% elif user.status == 90 %}
Developer
{% else %}
User
{% endif %}
</td>
<td>{{ user.lastupdate }}</td>
</tr>
{% endfor %}
</table>
