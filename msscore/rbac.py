import casbin

e = casbin.Enforcer(r"../config/rbac_example_model.conf", r"../config/rbac_example_policy.csv")

if __name__ == '__main__':

    sub = "alice"  # 想要访问资源的用户
    obj = "data1"  # 将要被访问的资源
    act = "read"  # 用户对资源进行的操作

    if e.enforce(sub, obj, act):
        # 允许alice读取data1
        pass
    else:
        # 拒绝请求，抛出异常
        pass

    permission_list = e.get_permissions_for_user("alice")