from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import json
import os
from models.user import User
from models.recommender import InternshipRecommender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pm-internship-scheme-2024'

# Initialize user management
user_manager = User()

# Initialize recommender
recommender = InternshipRecommender()

# Load internship data (for explore, etc.)
def load_internships():
    with open('data/internships.json', 'r') as f:
        return json.load(f)

# Use advanced recommender for all recommendations
def get_internship_recommendations(candidate_data):
    # Convert skills to list if string
    skills = candidate_data.get('skills', '')
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]
    candidate_data = candidate_data.copy()
    candidate_data['skills'] = skills
    return recommender.get_recommendations(candidate_data)

def get_available_sectors():
    return recommender.get_available_sectors()

def get_available_locations():
    return recommender.get_available_locations()

@app.route('/')
def welcome():
    """Welcome screen with language selection"""
    return render_template('welcome.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard - requires login"""
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    user = user_manager.get_user(session['user_email'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    # Get user applications
    applications = user_manager.get_user_applications(session['user_email'])
    
    # Get recommendations if profile is complete
    recommendations = []
    if user.get('profile_complete'):
        recommendations = get_internship_recommendations(user['profile'])
    
    # Hardcoded platform statistics for demo
    platform_stats = {
        'total_internships': 2847,
        'active_applications': len(applications) if applications else 0,
        'companies_partnered': 524,
        'success_rate': 87,
        'avg_stipend': '₹28,500',
        'top_sectors': [
            {'name': 'Information Technology', 'count': 892},
            {'name': 'Finance & Banking', 'count': 456},
            {'name': 'E-commerce', 'count': 324},
            {'name': 'Healthcare', 'count': 298},
            {'name': 'Automotive', 'count': 267}
        ],
        'recent_activities': [
            {
                'type': 'application',
                'message': '47 new internships posted today',
                'time': '2 hours ago',
                'icon': 'fas fa-briefcase',
                'color': 'success'
            },
            {
                'type': 'interview',
                'message': '892 interviews scheduled this week',
                'time': '4 hours ago', 
                'icon': 'fas fa-users',
                'color': 'info'
            },
            {
                'type': 'offer',
                'message': '234 internship offers extended today',
                'time': '6 hours ago',
                'icon': 'fas fa-trophy',
                'color': 'warning'
            },
            {
                'type': 'placement',
                'message': '156 students successfully placed',
                'time': '8 hours ago',
                'icon': 'fas fa-graduation-cap', 
                'color': 'primary'
            }
        ],
        'trending_skills': [
            'Python', 'JavaScript', 'React', 'Machine Learning', 'AWS',
            'Digital Marketing', 'Data Analysis', 'UI/UX Design', 'Java', 'SQL'
        ],
        'featured_companies': [
            'Google', 'Microsoft', 'Amazon', 'Flipkart', 'Tata Motors',
            'HDFC Bank', 'Infosys', 'TCS', 'Wipro', 'Accenture'
        ]
    }
    
    return render_template('dashboard.html', 
                         user=user, 
                         applications=applications, 
                         recommendations=recommendations,
                         stats=platform_stats)

@app.route('/profile')
def profile():
    """User profile page"""
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    user = user_manager.get_user(session['user_email'])
    return render_template('profile.html', user=user)

@app.route('/explore')
def explore():
    """Explore all internships"""
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    internships = load_internships()
    return render_template('explore.html', internships=internships)

@app.route('/applications')
def applications():
    """Track all applications"""
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    applications = user_manager.get_user_applications(session['user_email'])
    return render_template('applications.html', applications=applications)

@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html')

@app.route('/signup')
def signup():
    """Signup page"""
    return render_template('signup.html')

@app.route('/api/signup', methods=['POST'])
def api_signup():
    """API endpoint for user signup"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'error': f'Missing {field}'}), 400
        
        result = user_manager.create_user(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            phone=data.get('phone')
        )
        
        if result['success']:
            session['user_email'] = data['email']
            return jsonify({'success': True, 'redirect': '/profile'})
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for user login"""
    try:
        data = request.get_json()
        
        result = user_manager.authenticate_user(
            email=data['email'],
            password=data['password']
        )
        
        if result['success']:
            session['user_email'] = data['email']
            user = result['user']
            if user.get('profile_complete'):
                return jsonify({'success': True, 'redirect': '/dashboard'})
            else:
                return jsonify({'success': True, 'redirect': '/profile'})
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """API endpoint for user logout"""
    session.clear()
    return jsonify({'success': True, 'redirect': '/'})

@app.route('/api/profile', methods=['POST'])
def api_update_profile():
    """API endpoint to update user profile"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        profile_data = request.get_json()
        
        result = user_manager.update_profile(session['user_email'], profile_data)
        
        if result['success']:
            return jsonify({'success': True, 'redirect': '/dashboard'})
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/apply', methods=['POST'])
def api_apply():
    """API endpoint to apply to internship"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        result = user_manager.apply_to_internship(
            user_email=session['user_email'],
            internship_id=data['internship_id'],
            internship_title=data['internship_title']
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
def api_save():
    """API endpoint to save internship"""
    if 'user_email' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        
        result = user_manager.save_internship(
            user_email=session['user_email'],
            internship_id=data['internship_id'],
            internship_title=data['internship_title']
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    """API endpoint to get internship recommendations"""
    try:
        # Get candidate data from request
        candidate_data = request.get_json()
        
        # Validate required fields
        required_fields = ['education', 'skills', 'sector', 'location']
        for field in required_fields:
            if field not in candidate_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get recommendations from the engine
        recommendations = get_internship_recommendations(candidate_data)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'total_count': len(recommendations)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sectors', methods=['GET'])
def get_sectors():
    """API endpoint to get available sectors"""
    try:
        sectors = get_available_sectors()
        return jsonify({
            'success': True,
            'sectors': sectors
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """API endpoint to get available locations"""
    try:
        locations = get_available_locations()
        return jsonify({
            'success': True,
            'locations': locations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/mobile-demo')
def mobile_demo():
    """Mobile compatibility demonstration page"""
    return render_template('mobile-demo.html')

@app.route('/feedback')
def feedback():
    """Feedback page"""
    return render_template('feedback.html')

@app.route('/review')
def review():
    """Internship Review & Experience page"""
    return render_template('review.html')

@app.route('/easy-apply')
def easy_apply():
    """Easy Apply page"""
    return render_template('easy_apply.html')

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Run the app in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)