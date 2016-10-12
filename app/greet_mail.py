
import os
import jinja2
from jinja2 import Template
from flask import render_template
from datetime import datetime, timedelta

def greet_mail(user, env, end_ts, blackout_ts):

  end_time =  datetime.strptime(str(end_ts), "%Y-%m-%d %H:%M:%S.%f")
  date = str(end_time.date())
  hr = str(end_time.hour)
  min = str(end_time.minute)
  sec = str(end_time.second)

  e_ts = hr+":"+min+":"+sec+" "+date

  blackout_time =  datetime.strptime(str(blackout_ts), "%Y-%m-%d %H:%M:%S.%f")
  b_date = str(blackout_time.date())
  b_hr = str(blackout_time.hour)
  b_min = str(blackout_time.minute)
  b_sec = str(blackout_time.second)
  b_ts = b_hr+":"+b_min+":"+b_sec+" "+b_date

  with open('greeting_mail.html', 'w+') as f:
    f.write(render_template("greeting_msg.html",user=user,env=env,e_ts=e_ts,b_ts=b_ts))


  if os.path.exists('greeting_mail.html'):
    send_mail = "~/sendthemail.sh %s" % user
    os.system(send_mail)
		
#def render(tpl_path, context):
#  path, filename = os.path.split(tpl_path)
#  return jinja2.Environment(
#      loader=jinja2.FileSystemLoader(path or './')
#  ).get_template(filename).render(context)


#def warn_mail(user, end_ts, alert_ts):

#  end_time =  datetime.strptime(str(end_ts), "%Y-%m-%d %H:%M:%S.%f")
#  date = str(end_time.date())
#  hr = str(end_time.hour)
#  min = str(end_time.minute)
#  sec = str(end_time.second)
#  end_ts = hr+":"+min+":"+sec+" "+date

#  alert_time = datetime.strptime(str(alert_ts), "%Y-%m-%d %H:%M:%S.%f")
#  a_date = str(alert_time.date())
#  a_hr = str(alert_time.hour)
#  a_min = str(alert_time.minute)
#  a_sec = str(alert_time.second)
#  end_ts = a_hr+":"+a_min+":"+a_sec+" "+a_date

 # context = {'user': user, 'end_ts': end_ts, 'alert_ts': alert_ts}

 # with open('warn_mail.html', 'w+') as f:
 #   f.write(render("templates/warn_msg.html", context))


#  if os.path.exists('warn_mail.html'):
#    send_mail = "~/sendthemail.sh %s" % user
#    os.system(send_mail)
