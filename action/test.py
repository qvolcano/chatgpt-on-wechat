from manager import PermissionManager
def default(args):
    PermissionManager.setUserGroup("QV","admin")
    return "test"
