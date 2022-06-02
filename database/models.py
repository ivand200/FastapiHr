from email.policy import default
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship

from .db import Base


association_table = Table(
    "association",
    Base.metadata,
    Column("clients_id", ForeignKey("clients.id"), primary_key=True),
    Column("tags_id", ForeignKey("tags.id"), primary_key=True),
)


class Field(Base):
    __tablename__ = "fields"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(20), unique=True)
    tag = relationship("Tag")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(20), unique=True)

    clients = relationship("Client", secondary=association_table, back_populates="tags")
    field_id = Column(Integer, ForeignKey("fields.id"))


class AbstractUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(50))

    client = relationship("Client", cascade="all, delete", back_populates="users")
    manager = relationship("Manager", back_populates="users")


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tags = relationship("Tag", secondary=association_table, back_populates="clients")

    users = relationship("AbstractUser", back_populates="client")


class Manager(Base):
    __tablename__ = "managers"
    id = Column(Integer, primary_key=True, index=True)
    users_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("AbstractUser", back_populates="manager")





# class Client(Base):
#     __tablename__ = "clients"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True)
#     email = Column(String(50), unique=True)
#     password = Column(String(50))
#     # ManyToMany Tag
# 
# 
# class Manager(Base):
#     __tablename__ = "managers"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True)
#     email = Column(String(50), unique=True)
#     password = Column(String)