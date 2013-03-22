from model_base import *

class Post(Base, ModelBase):
  __tablename__ = 'posts'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  author = Column(String)
  content = Column(String)
  comments = relationship('Comment', backref='post')

  def __init__(self, title, author, content):
    self.title = title
    self.author = author
    self.content = content

