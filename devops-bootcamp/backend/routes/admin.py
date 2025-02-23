from flask import Blueprint, request, jsonify
from functools import wraps
import firebase_admin
from firebase_admin import auth
import logging

# Initialize Blueprint
admin_bp = Blueprint('admin', __name__)

# Setup logging
logger = logging.getLogger(__name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            # Verify Firebase token
            decoded_token = auth.verify_id_token(token)
            # Check if user has admin role (you would need to implement this logic)
            if not decoded_token.get('admin', False):
                return jsonify({'message': 'Admin privileges required!'}), 403
            current_admin = decoded_token
        except Exception as e:
            logger.error(f"Admin token verification failed: {str(e)}")
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_admin, *args, **kwargs)
    return decorated

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """Process admin login"""
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({'error': 'No token provided'}), 400

        # Verify the Firebase token
        decoded_token = auth.verify_id_token(token)
        
        # Check if user has admin privileges
        # In production, you would check against your admin users database
        if not decoded_token.get('admin', False):
            return jsonify({'error': 'Not authorized as admin'}), 403

        return jsonify({
            'message': 'Admin login successful',
            'admin': {
                'uid': decoded_token['uid'],
                'email': decoded_token.get('email', '')
            }
        }), 200
    except Exception as e:
        logger.error(f"Admin login failed: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 401

@admin_bp.route('/submissions', methods=['GET'])
@admin_required
def get_submissions(current_admin):
    """Get list of pending submissions"""
    try:
        # Mock submission data - In production, fetch from database
        submissions = [
            {
                'id': '1',
                'user_id': 'user123',
                'course_id': 1,
                'chapter_id': 2,
                'video_url': 'https://linkedin.com/video123',
                'status': 'pending_review',
                'submitted_at': '2024-01-20T10:30:00Z'
            }
        ]
        return jsonify({'submissions': submissions}), 200
    except Exception as e:
        logger.error(f"Error fetching submissions: {str(e)}")
        return jsonify({'error': 'Failed to fetch submissions'}), 500

@admin_bp.route('/verify-payment', methods=['POST'])
@admin_required
def verify_payment(current_admin):
    """Manually verify course payment"""
    try:
        data = request.json
        transaction_id = data.get('transaction_id')
        user_id = data.get('user_id')
        
        if not all([transaction_id, user_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Mock payment verification - In production, update database
        verification_result = {
            'status': 'verified',
            'transaction_id': transaction_id,
            'user_id': user_id,
            'verified_by': current_admin['uid'],
            'verified_at': '2024-01-20T10:30:00Z'
        }

        return jsonify({
            'message': 'Payment verified successfully',
            'verification': verification_result
        }), 200
    except Exception as e:
        logger.error(f"Payment verification failed: {str(e)}")
        return jsonify({'error': 'Verification failed'}), 500

@admin_bp.route('/grade', methods=['POST'])
@admin_required
def grade_submission(current_admin):
    """Grade a video submission"""
    try:
        data = request.json
        submission_id = data.get('submission_id')
        grade = data.get('grade')  # 'pass' or 'fail'
        feedback = data.get('feedback')

        if not all([submission_id, grade]):
            return jsonify({'error': 'Missing required fields'}), 400

        if grade not in ['pass', 'fail']:
            return jsonify({'error': 'Invalid grade value'}), 400

        # Mock grading - In production, update database
        grading_result = {
            'submission_id': submission_id,
            'grade': grade,
            'feedback': feedback,
            'graded_by': current_admin['uid'],
            'graded_at': '2024-01-20T10:30:00Z'
        }

        return jsonify({
            'message': 'Submission graded successfully',
            'grading': grading_result
        }), 200
    except Exception as e:
        logger.error(f"Grading failed: {str(e)}")
        return jsonify({'error': 'Grading failed'}), 500

@admin_bp.route('/course', methods=['POST'])
@admin_required
def manage_course(current_admin):
    """Add or update course content"""
    try:
        data = request.json
        action = data.get('action')  # 'add', 'update', or 'delete'
        course_data = data.get('course')

        if not all([action, course_data]):
            return jsonify({'error': 'Missing required fields'}), 400

        if action not in ['add', 'update', 'delete']:
            return jsonify({'error': 'Invalid action'}), 400

        # Mock course management - In production, update database
        course_result = {
            'action': action,
            'course_id': course_data.get('id', 'new_id'),
            'updated_by': current_admin['uid'],
            'updated_at': '2024-01-20T10:30:00Z'
        }

        return jsonify({
            'message': f'Course {action}d successfully',
            'result': course_result
        }), 200
    except Exception as e:
        logger.error(f"Course management failed: {str(e)}")
        return jsonify({'error': 'Course management failed'}), 500

@admin_bp.route('/certificates', methods=['POST'])
@admin_required
def manage_certificates(current_admin):
    """Generate and manage certificates"""
    try:
        data = request.json
        user_id = data.get('user_id')
        course_id = data.get('course_id')
        action = data.get('action')  # 'generate' or 'revoke'

        if not all([user_id, course_id, action]):
            return jsonify({'error': 'Missing required fields'}), 400

        if action not in ['generate', 'revoke']:
            return jsonify({'error': 'Invalid action'}), 400

        # Mock certificate management - In production, generate/revoke actual certificates
        certificate_result = {
            'user_id': user_id,
            'course_id': course_id,
            'action': action,
            'certificate_id': 'cert_123',
            'processed_by': current_admin['uid'],
            'processed_at': '2024-01-20T10:30:00Z'
        }

        return jsonify({
            'message': f'Certificate {action}d successfully',
            'result': certificate_result
        }), 200
    except Exception as e:
        logger.error(f"Certificate management failed: {str(e)}")
        return jsonify({'error': 'Certificate management failed'}), 500
