from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app import db, bcrypt
from app.models.user import User
from app.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from app.utils.email import send_reset_email

bp = Blueprint('auth', __name__)

def admin_required(f):
    """Decorator to ensure user has admin privileges."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to view this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
                
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=False  # Default to non-admin
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = RequestResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset_request.html', title='Reset Password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
        
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/reset_token.html', title='Reset Password', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
