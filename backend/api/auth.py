import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
import os

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# パスワードをハッシュ化する
def get_password_hash(password: str) -> str:
    # パスワードをバイト列に変換
    password_bytes = password.encode('utf-8')
    # ソルトを生成してハッシュ化
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # データベース保存用に文字列に戻す
    return hashed.decode('utf-8')

#入力されたパスワードと保存されたハッシュを比較する
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def create_access_token(data: dict):
    to_encode = data.copy()
    # 有効期限設定
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # JWT作成
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt