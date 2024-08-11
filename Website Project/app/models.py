from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    username = db.Column(db.String(24), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    roles = db.relationship("Role", backref="user", lazy="joined", passive_deletes=True, secondary="user_roles")
    is_active = db.Column(db.Boolean, default=True, index=True, nullable=False)
    name_first = db.Column(db.String(32))
    name_last = db.Column(db.String(32))
    contact_number = db.Column(db.String(38), unique=True)

    def set_user_role(self):
        user_role = Role.query.filter_by(role_name = "User").first()
        self.roles = [user_role,]

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"user('{self.id}', '{self.username}', '{self.email}', '{self.is_active}', '{self.roles}')"


class Role(db.Model):
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    role_name = db.Column(db.String(32), unique=True, nullable=False)

    def __repr__(self):
        return f"role('{self.role_id}', '{self.role_name}')"


class UserRoles(db.Model):
    __tablename_ = "user_roles"
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id", ondelete="CASCADE"))