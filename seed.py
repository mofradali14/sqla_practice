from models import User, Post, db, Tag, PostTag
from app import app

db.drop_all()
db.create_all()

ali = User(first_name='Ali', last_name='Mofrad')

p1 = Post(title='Test', content='This is a test post',user_id=1)
p2 = Post(title='Test2', content='This is another test post',user_id=1)

db.session.add(ali)
db.session.commit()

db.session.add_all([p1, p2])
db.session.commit()

tag1 = Tag(name='test')

db.session.add(tag1)
db.session.commit()