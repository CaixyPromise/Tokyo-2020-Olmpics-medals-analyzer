import bcrypt

# 密码加密
def register_user(password: str):
    # 生成随机盐值并将密码哈希
    salt = bcrypt.gensalt()  # 自动生成盐值
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# 密码校验
def login_user(password: str, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
