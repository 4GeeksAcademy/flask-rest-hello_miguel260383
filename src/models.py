from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()
metadata = db.metadata

#TABLAS

user_table = Table("user",metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(120), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("is_active", Boolean, nullable=False)
)


post_table = Table("post",metadata,
    Column("id", Integer, primary_key=True),
    Column("caption", String(500)),
    Column("image", String(255), nullable=False),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
)



follow_table = Table("follow",metadata,
    Column("id", Integer, primary_key=True),
    Column("follower_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("following_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
)



like_table = Table("like",metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("post_id", Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable=False),
)



comment_table = Table("comment",metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String(500), nullable=False),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False),
    Column("post_id", Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
)

#MODELOS

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts = relationship("Post", back_populates="user", cascade="all, delete")
    likes = relationship("Like", back_populates="user")
    comments = relationship("Comment", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
        }



class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    caption: Mapped[str] = mapped_column(String(500))
    image: Mapped[str] = mapped_column(String(255), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", back_populates="posts")

    likes = relationship("Like", back_populates="post")
    comments = relationship("Comment", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "caption": self.caption,
            "image": self.image,
            "user_id": self.user_id
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

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id
        }



class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "user_id": self.user_id,
            "post_id": self.post_id
        }
