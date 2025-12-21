from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True, nullable=False)
    # パスワードそのものではなく、ハッシュ化した値を保存する
    hashed_password = Column(String(256), nullable=False)

    #done = relationship("Done", back_populates="task", cascade="delete")

