from flask import render_template, request, jsonify
from app.errors import bp
from app import db

@bp.app_errorhandler(400)
def bad_request_error(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'bad request'})
        response.status_code = 400
        return response
    return render_template('errors/400.html'), 400

@bp.app_errorhandler(403)
def forbidden_error(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('errors/403.html'), 403

@bp.app_errorhandler(404)
def not_found_error(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(405)
def method_not_allowed_error(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'method not allowed'})
        response.status_code = 405
        return response
    return render_template('errors/405.html'), 405

@bp.app_errorhandler(429)
def ratelimit_error(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': 'too many requests',
            'message': 'You have exceeded your request limit.'
        })
        response.status_code = 429
        return response
    return render_template('errors/429.html'), 429

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('errors/500.html'), 500

@bp.app_errorhandler(CSRFError)
def handle_csrf_error(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': 'invalid csrf token',
            'message': 'The CSRF token is missing or invalid.'
        })
        response.status_code = 400
        return response
    return render_template('errors/csrf_error.html'), 400
