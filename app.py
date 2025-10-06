import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cukcu.db'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Leader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    achievements = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class TeamMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('Save')

class LeaderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    achievements = TextAreaField('Achievements')
    image = FileField('Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('Save')

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid duplicates
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return filename
    return None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/team')
def team():
    team_members = TeamMember.query.all()
    return render_template('team.html', team_members=team_members)

@app.route('/leaders')
def leaders():
    leaders = Leader.query.all()
    return render_template('leaders.html', leaders=leaders)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    team_members = TeamMember.query.all()
    leaders = Leader.query.all()
    return render_template('admin/dashboard.html', team_members=team_members, leaders=leaders)

@app.route('/admin/team/add', methods=['GET', 'POST'])
@login_required
def add_team_member():
    form = TeamMemberForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = save_image(form.image.data)
        
        team_member = TeamMember(
            name=form.name.data,
            position=form.position.data,
            bio=form.bio.data,
            image_filename=filename
        )
        db.session.add(team_member)
        db.session.commit()
        flash('Team member added successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/team_form.html', form=form, title='Add Team Member')

@app.route('/admin/team/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team_member(id):
    team_member = TeamMember.query.get_or_404(id)
    form = TeamMemberForm(obj=team_member)
    
    if form.validate_on_submit():
        team_member.name = form.name.data
        team_member.position = form.position.data
        team_member.bio = form.bio.data
        
        if form.image.data:
            # Delete old image if it exists
            if team_member.image_filename:
                old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], team_member.image_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Save new image
            filename = save_image(form.image.data)
            team_member.image_filename = filename
        
        db.session.commit()
        flash('Team member updated successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/team_form.html', form=form, title='Edit Team Member')

@app.route('/admin/team/delete/<int:id>', methods=['POST'])
@login_required
def delete_team_member(id):
    team_member = TeamMember.query.get_or_404(id)
    
    # Delete image file if it exists
    if team_member.image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], team_member.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(team_member)
    db.session.commit()
    flash('Team member deleted successfully!')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/leader/add', methods=['GET', 'POST'])
@login_required
def add_leader():
    form = LeaderForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = save_image(form.image.data)
        
        leader = Leader(
            name=form.name.data,
            position=form.position.data,
            bio=form.bio.data,
            achievements=form.achievements.data,
            image_filename=filename
        )
        db.session.add(leader)
        db.session.commit()
        flash('Leader added successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/leader_form.html', form=form, title='Add Leader')

@app.route('/admin/leader/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_leader(id):
    leader = Leader.query.get_or_404(id)
    form = LeaderForm(obj=leader)
    
    if form.validate_on_submit():
        leader.name = form.name.data
        leader.position = form.position.data
        leader.bio = form.bio.data
        leader.achievements = form.achievements.data
        
        if form.image.data:
            # Delete old image if it exists
            if leader.image_filename:
                old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], leader.image_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Save new image
            filename = save_image(form.image.data)
            leader.image_filename = filename
        
        db.session.commit()
        flash('Leader updated successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/leader_form.html', form=form, title='Edit Leader')

@app.route('/admin/leader/delete/<int:id>', methods=['POST'])
@login_required
def delete_leader(id):
    leader = Leader.query.get_or_404(id)
    
    # Delete image file if it exists
    if leader.image_filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], leader.image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(leader)
    db.session.commit()
    flash('Leader deleted successfully!')
    return redirect(url_for('admin_dashboard'))

# Create admin user
@app.before_first_request
def create_admin():
    db.create_all()
    # Check if admin user exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('admin123')  # Change this to a secure password
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)