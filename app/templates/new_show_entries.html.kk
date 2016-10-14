{% extends "layout.html" %}
{% block body %}

<html>
  <head>	
{# <style>
.nav ul         { list-style-type: none; margin: 0; padding: 0; overflow: hidden; background-color: #377BA8;}
.nav li         { float: right; color: white;}
.nav li a       { display: block; color: white; text-align: center; padding: 16px; text-decoration: none;}
.nav li a:hover { background-color: #111111;}

</style>
#}
<style>
ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #377BA8;
}

li {
    float: right;
    color: white;
}

li a, .dropbtn {
    display: inline-block;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
}

li a:hover, .dropdown:hover .dropbtn {
    background-color: black;
}

li.dropdown {
    display: inline-block;
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
}

.dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
    text-align: left;
}

.dropdown-content a:hover {background-color: #f1f1f1}

.dropdown:hover .dropdown-content {
    display: block;
}
</style>
{#
	<div class="nav">
        	<ul>
        		<li><a href="{{ url_for('request_entry') }}">Access to environments</a></li>
        		<li><a href="{{ url_for('add_entry') }}">Sign-up</a></li>
        	</ul>
	</div>
#}
<ul>
  <li><a class="active" href="#home">Home</a></li>
  <li class="dropdown">
    <a href="#" class="dropbtn">Dropdown</a>
    <div class="dropdown-content">
      <a href="{{ url_for('add_entry') }}">Sign-up</a>
      <a href="{{ url_for('request_entry') }}">Access to environments</a>
    </div>
  </li>
</ul

	{% include 'panel.html' %}
  </head>
  <body>
	
	 {% include 'doc.html' %}
  </body>
</html>

{% endblock %}
