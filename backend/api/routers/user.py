from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..models import user as user_model
from ..schemas import user as user_schema
from ..auth import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/signup", response_model=user_schema.UserResponse)
async def signup(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    # 1. ユーザー名の重複確認
    statement = select(user_model.User).where(user_model.User.username == user_in.username)
    result = await db.execute(statement)
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code=400, detail="このユーザー名は既に使用されています")
    
    # 2.パスワードハッシュ化, 新規ユーザーオブジェクト作成
    hashed_password = get_password_hash(user_in.password)
    new_user = user_model.User(
        username=user_in.username,
        hashed_password=hashed_password
    )

    # 3. データベースに保存
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # 1. ユーザー検索
    statement = select(user_model.User).where(user_model.User.username == form_data.username)
    result = await db.execute(statement)
    user = result.scalars().first()

    # 2. ユーザーの存在とパスワードの検証
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. アクセストークン発行
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}