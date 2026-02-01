from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, Table, Column



db = SQLAlchemy()

User_Post_table = Table(
    "User_Post_table",
    db.Model.metadata,
    Column("User.id", ForeignKey("user.id"), primary_key=True),
    Column("Post.id", ForeignKey("post.id"), primary_key=True)
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    posts = relationship("Post", back_populates="user")


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
           
           }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(String(500))
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="posts")
       


    def serialize(self):
        return {
            "id": self.id,
            "Caption": self.caption,
            "image": self.image,
            "user_id": self.user_id,
             }


class Follow(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    following_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "following_id": self.following_id
            }


class Like(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user = relationship("User")
    

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post.id,

        }

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    user = relationship("User")
    

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "user_id": self.user_id,
            "post_id": self.post.id,

        }
