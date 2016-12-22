from jinja2 import Template
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime, timedelta

def alert_mail(user, end_ts, alert_ts, u_file):

  end_time =  datetime.strptime(str(end_ts), "%Y-%m-%d %H:%M:%S.%f")
  date = str(end_time.date())
  hr = str(end_time.hour)
  min = str(end_time.minute)
  sec = str(end_time.second)

  e_ts = hr+":"+min+":"+sec+" "+date

  alert_time = datetime.strptime(str(alert_ts), "%Y-%m-%d %H:%M:%S.%f")
  a_date = str(alert_time.date())
  a_hr = str(alert_time.hour)
  a_min = str(alert_time.minute)
  a_sec = str(alert_time.second)

  a_ts =  a_hr+":"+a_min+":"+a_sec+" "+a_date

  env = Environment(loader=FileSystemLoader('/root/workspace/rogue/project/app'))
  template = env.get_template('templates/warn_msg.html')

  #u_file = '/root/workspace/rogue/project/app/mail/%s.alert_mail.html' % user
  output_from_parsed_template = template.render(user=user,end_ts=e_ts)

  with open(u_file, 'w+') as f:
    f.write(output_from_parsed_template)
  
  if os.path.exists(u_file):
    path = 'mail/%s.alert_mail.html' % user
    send_mail = "~/sendthemail.sh %s %s " % (user,path)
    os.system(send_mail)  
