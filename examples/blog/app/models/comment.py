from noodle.model_base import *

class Comment(Base, ModelBase):
  __tablename__ = 'comments'

  id = Column(Integer, primary_key=True)
  content = Column(String)
  post_id = Column(Integer, ForeignKey('posts.id'))


  def __init__(self, content):
    self.content = content

