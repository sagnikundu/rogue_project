#!/usr/bin/env python

import ldap
import random

server = "ldapserver.lightaria.com"
username = "cn=admin,dc=lightaria,dc=com"
password = "admin"
baseDN="dc=lightaria,dc=com"
scope=ldap.SCOPE_SUBTREE
retrieveAttributes = None

def get_ldap():
  try:
    con = ldap.open(server)
    con.simple_bind(username, password)
  except ldap.LDAPError, e:
    print "Error : %s " % str(e)
  return con


def get_uidNum():
  rno = random_uid_gen()
  # search the ldap db for matching entries of uidNumber
  con = get_ldap()
  searchFilter = "uidNumber="+rno
  ldap_result_id = con.search(baseDN, scope, searchFilter, retrieveAttributes)
  result_type, result_data = con.result(ldap_result_id, 0)
  if (result_data == []):
    return rno
  else:
    get_uidNum()


def random_uid_gen():
  rno = random.randint(1000, 60000)
  return str(rno)
