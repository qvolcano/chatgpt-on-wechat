from manager import PermissionManager
def default():
    PermissionManager.setUserGroup("QV","admin")
    return "test"
