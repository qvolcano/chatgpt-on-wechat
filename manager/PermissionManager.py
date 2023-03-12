groups=[]
users={}

def setup():
  #load config
  pass
  
def setUserGroup(user,group):
  users[user]=group
  
def setGroupPermission(group,permission):
  groups[group]=permission
  
def getUserGroup(user):
  return users.get(user)
  
def getUserPermission(user):
  group=getUserGroup(user)
  if group :
    return group['permission']
