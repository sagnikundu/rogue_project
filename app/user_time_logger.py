#!/usr/bin/env python
from db_setup import get_db
import time
import datetime
import crontab import CronTab

# get the timestamp for the user

def get_timestamp(username):

  # query db to get user timestamp
  con = get_db()
  t = con.execute("select timestamp from access_status where user_name='?'", (username))
  # time format returned : '2016-09-15 09:15:22' 

  # evaluating starttime from t
  start_time = get_epoch_time(t)

  # Add x-hrs to the timestamp to obtain the end-time
  end_time = start_time + 6 * 60 * 60
  
  #Convert epoch to human time
  hr, min, s = get_epoch_to_human_time(end_time)

  # CMD to delete TODO

  # Adding a cron entry with the end time values for the user:
  add_to_cron(hr, min, cmd)


def add_to_cron(hr, min, cmd):
  sys_cron = get_cron_obj()
  job1 = sys_cron.new(command=cmd, comment="set cron to delete user", user='root')
  set_time = '%s %s * * *' % (min, hr)
  status = job1.setall(set_time)
  job1.enable()
  sys_cron.write()


def del_from_cron(job1):
  sys_cron = get_cron_obj()
  job1.enable(False)
  sys_cron.remove(job1)
  sys_cron.write()


def get_cron_obj():
  return CronTab(tabfile='/etc/crontab', user='root')


def get_epoch_time(t):
  return time.mktime(datetime.datetime.strptime(t,"%Y-%m-%d %H:%M:%S").timetuple())
 

def get_epoch_to_human_time(t):
  """ returns list """
  return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)).split()[1].split(":")
