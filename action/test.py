from manager import PermissionManager
permission=["test"]
def default(args):
    PermissionManager.setUserGroup("QV","admin")
    return "test"
