from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from .. import db
from ..models import User, Order
from . import admin
from ..decorators import admin_required
from datetime import datetime, timedelta

@admin.route('/admin')
@login_required
@admin_required
def dashboard():
    # Get counts for the dashboard
    total_users = User.query.count()
    total_orders = Order.query.count()
    
    # Get today's orders
    today = datetime.utcnow().date()
    today_orders = Order.query.filter(
        Order.delivery_date == today
    ).order_by(Order.delivery_time.asc()).all()
    
    # Get recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # Get recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    # Get order statistics
    order_stats = {
        'pending': Order.query.filter_by(status='pending').count(),
        'confirmed': Order.query.filter_by(status='confirmed').count(),
        'delivered': Order.query.filter_by(status='delivered').count(),
        'cancelled': Order.query.filter_by(status='cancelled').count()
    }
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_orders=total_orders,
                         today_orders=today_orders,
                         recent_users=recent_users,
                         recent_orders=recent_orders,
                         order_stats=order_stats)

@admin.route('/admin/users')
@login_required
@admin_required
def user_list():
    page = request.args.get('page', 1, type=int)
    query = User.query
    
    # Search functionality
    search = request.args.get('search', '')
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )
    
    # Pagination
    pagination = query.order_by(User.created_at.desc()).paginate(
        page, per_page=current_app.config['USERS_PER_PAGE'], error_out=False)
    users = pagination.items
    
    return render_template('admin/users.html',
                         title='Users',
                         users=users,
                         pagination=pagination,
                         search=search)

@admin.route('/admin/orders')
@login_required
@admin_required
def order_list():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    
    # Filter by status
    query = Order.query
    if status != 'all':
        query = query.filter_by(status=status)
    
    # Search functionality
    search = request.args.get('search', '')
    if search:
        query = query.join(User).filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (Order.name.ilike(f'%{search}%')) |
            (Order.phone.ilike(f'%{search}%'))
        )
    
    # Date range filter
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        query = query.filter(Order.delivery_date >= start_date)
    
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        query = query.filter(Order.delivery_date <= end_date)
    
    # Pagination
    pagination = query.order_by(Order.delivery_date.desc(), Order.delivery_time.asc()).paginate(
        page, per_page=current_app.config['ORDERS_PER_PAGE'], error_out=False)
    orders = pagination.items
    
    return render_template('admin/orders.html',
                         title='Orders',
                         orders=orders,
                         pagination=pagination,
                         status=status,
                         search=search,
                         start_date=start_date.strftime('%Y-%m-%d') if start_date else '',
                         end_date=end_date.strftime('%Y-%m-%d') if end_date else '')

@admin.route('/admin/order/<int:order_id>')
@login_required
@admin_required
def view_order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order.html', order=order)

@admin.route('/admin/order/<int:order_id>/update_status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'confirmed', 'delivered', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.id} status updated to {new_status}.', 'success')
    else:
        flash('Invalid status.', 'danger')
    
    return redirect(url_for('admin.view_order', order_id=order.id))

@admin.route('/admin/user/<int:user_id>')
@login_required
@admin_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Get user's orders
    page = request.args.get('page', 1, type=int)
    orders_pagination = Order.query.filter_by(user_id=user.id)\
        .order_by(Order.created_at.desc())\
        .paginate(page, per_page=10, error_out=False)
    
    return render_template('admin/user.html',
                         user=user,
                         orders_pagination=orders_pagination)

@admin.route('/admin/user/<int:user_id>/toggle_admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    if user_id == current_user.id:
        flash('You cannot modify your own admin status.', 'danger')
        return redirect(url_for('admin.view_user', user_id=user_id))
    
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'granted' if user.is_admin else 'revoked'
    flash(f'Admin privileges {status} for {user.username}.', 'success')
    return redirect(url_for('admin.view_user', user_id=user.id))
