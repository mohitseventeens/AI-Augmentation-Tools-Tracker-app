from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Association tables
tool_tags = db.Table('tool_tags',
    db.Column('tool_id', db.Integer, db.ForeignKey('tool.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

project_tools = db.Table('project_tools',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('tool_id', db.Integer, db.ForeignKey('tool.id'))
)

skill_tools = db.Table('skill_tools',
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id')),
    db.Column('tool_id', db.Integer, db.ForeignKey('tool.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    tools = db.relationship('Tool', backref='user', lazy='dynamic')
    projects = db.relationship('Project', backref='user', lazy='dynamic')
    skills = db.relationship('Skill', backref='user', lazy='dynamic')
    activities = db.relationship('Activity', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # LLM, Agent, Framework, etc.
    description = db.Column(db.Text)
    url = db.Column(db.String(200))
    notes = db.Column(db.Text)
    logo = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tool_tags, backref='tools')
    projects = db.relationship('Project', secondary=project_tools, backref='tools')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tools = db.relationship('Tool', secondary=skill_tools, backref='skills')

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))  # 'added_tool', 'rated_tool', 'added_project'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))