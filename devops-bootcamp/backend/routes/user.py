from flask import Blueprint, request, jsonify
from functools import wraps
import firebase_admin
from firebase_admin import auth, credentials
import logging

# Initialize Blueprint
user_bp = Blueprint('user', __name__)

# Setup logging
logger = logging.getLogger(__name__)

def token_required(f):
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
            current_user = decoded_token
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@user_bp.route('/login', methods=['POST'])
def login():
    """Process Firebase token for Google OAuth login"""
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({'error': 'No token provided'}), 400

        # Verify the Firebase token
        decoded_token = auth.verify_id_token(token)
        
        # Return user info
        return jsonify({
            'message': 'Login successful',
            'user': {
                'uid': decoded_token['uid'],
                'email': decoded_token.get('email', ''),
                'name': decoded_token.get('name', '')
            }
        }), 200
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 401

@user_bp.route('/courses', methods=['GET'])
@token_required
def get_courses(current_user):
    """Retrieve available courses and curriculum details"""
    try:
        # Mock course data - In production, this would come from a database
        courses = [
            {
                'id': 1,
                'title': 'Server Virtualization with Proxmox',
                'description': 'Learn VM creation, template management, and HA configuration',
                'chapters': [
                    {'title': 'VM Creation and Management', 'status': 'locked'},
                    {'title': 'Template Management', 'status': 'locked'},
                    {'title': 'High Availability Configuration', 'status': 'locked'}
                ]
            },
            {
                'id': 2,
                'title': 'Networking Fundamentals',
                'description': 'Master DNS, MikroTik routing, and subnetting',
                'chapters': [
                    {'title': 'Basic Network Concepts', 'status': 'locked'},
                    {'title': 'DNS Configuration', 'status': 'locked'},
                    {'title': 'MikroTik Routing', 'status': 'locked'},
                    {'title': 'Subnetting Practice', 'status': 'locked'}
                ]
            }
            # Additional courses would be added here
        ]
        return jsonify({'courses': courses}), 200
    except Exception as e:
        logger.error(f"Error fetching courses: {str(e)}")
        return jsonify({'error': 'Failed to fetch courses'}), 500

@user_bp.route('/purchase', methods=['POST'])
@token_required
def purchase_course(current_user):
    """Process course purchase"""
    try:
        data = request.json
        course_id = data.get('course_id')
        payment_method = data.get('payment_method')
        payment_details = data.get('payment_details')

        if not all([course_id, payment_method, payment_details]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Mock payment processing - In production, integrate with actual payment gateway
        payment_response = {
            'status': 'pending',
            'message': 'Payment is being processed',
            'transaction_id': 'mock_transaction_123',
            'payment_method': payment_method
        }

        return jsonify(payment_response), 200
    except Exception as e:
        logger.error(f"Purchase failed: {str(e)}")
        return jsonify({'error': 'Purchase failed'}), 500

@user_bp.route('/submit', methods=['POST'])
@token_required
def submit_assignment(current_user):
    """Submit video assignment"""
    try:
        data = request.json
        course_id = data.get('course_id')
        chapter_id = data.get('chapter_id')
        video_url = data.get('video_url')

        if not all([course_id, chapter_id, video_url]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Validate video URL (should be a LinkedIn URL)
        if 'linkedin.com' not in video_url.lower():
            return jsonify({'error': 'Invalid video URL. Please submit a LinkedIn video URL'}), 400

        # Mock submission storage - In production, save to database
        submission = {
            'user_id': current_user['uid'],
            'course_id': course_id,
            'chapter_id': chapter_id,
            'video_url': video_url,
            'status': 'pending_review'
        }

        return jsonify({
            'message': 'Assignment submitted successfully',
            'submission': submission
        }), 200
    except Exception as e:
        logger.error(f"Submission failed: {str(e)}")
        return jsonify({'error': 'Submission failed'}), 500

@user_bp.route('/progress', methods=['GET'])
@token_required
def get_progress(current_user):
    """Get user's course progress"""
    try:
        # Mock progress data - In production, fetch from database
        progress = {
            'courses_enrolled': [
                {
                    'course_id': 1,
                    'progress': 25,
                    'chapters_completed': 1,
                    'total_chapters': 4,
                    'last_activity': '2024-01-20T10:30:00Z'
                }
            ],
            'certificates_earned': [],
            'next_deadline': '2024-02-20T00:00:00Z'  # 30 days from enrollment
        }

        return jsonify(progress), 200
    except Exception as e:
        logger.error(f"Error fetching progress: {str(e)}")
        return jsonify({'error': 'Failed to fetch progress'}), 500
