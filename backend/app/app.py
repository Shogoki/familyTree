from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from flask_graphql import GraphQLView
#################################
app = Flask(__name__)
app.debug = True

basedir = os.path.abspath(os.path.dirname(__file__))
# Configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Modules
db = SQLAlchemy(app)

# Models
class Person(db.Model):
#     Vorname
# Name
# Geburtsname
# weiterer Familienname
# Geschlecht
# Spitzname
# Geburtstag
# Geburtsort
# Sterbetag
# Sterbeort
# Beruf
# Wohnorte
# Notizen


# Ehepartner
# Kinder
# Geschwister

    __tablename__ = 'persons'
    uuid = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(256))
    name = db.Column(db.String(256))
    birthname = db.Column(db.String(256))
    additional_name = db.Column(db.String(256))
    nickname = db.Column(db.String(256))
    gender =  db.Column("gender", db.Enum("female", "male", name="gender_enum", create_type=False))
    birthday =  db.Column(db.Datetime())
    birth_location = db.Column(db.String(50))
    death_day = db.Column(db.Datetime())
    death_location = db.Column(db.String(50))
    job = db.Column(db.String(256))
    locations = db.Column(db.String(256))
    comments = db.Column(db.String(256))

    spouse = 

    posts = db.relationship('Post', backref='author')
    
    def __repr__(self):
        return '<User %r>' % self.username
class Post(db.Model):
    __tablename__ = 'posts'
    uuid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.uuid'))
    def __repr__(self):
        return '<Post %r>' % self.title

# Schema Objects
class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )
class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       interfaces = (graphene.relay.Node, )
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostObject)
    all_users = SQLAlchemyConnectionField(UserObject)

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        body = graphene.String(required=True) 
        username = graphene.String(required=True)
    post = graphene.Field(lambda: PostObject)
    def mutate(self, info, title, body, username):
        user = User.query.filter_by(username=username).first()
        post = Post(title=title, body=body)
        if user is not None:
            post.author = user
        db.session.add(post)
        db.session.commit()
        return CreatePost(post=post)
class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
#### views
@app.route('/')
def index():
    return '<p> Hello World!</p>'

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

##################################
if __name__ == '__main__':
     app.run(host='0.0.0.0')