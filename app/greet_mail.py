
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
    path = 'greeting_mail.html'
    send_mail = "~/sendthemail.sh %s %s" % (user,path)
    os.system(send_mail)
		
