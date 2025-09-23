import json
import os
from datetime import datetime
import uuid

class User:
    def __init__(self):
        self.users_file = 'data/users.json'
        self.applications_file = 'data/applications.json'
        self.ensure_data_files()
    
    def ensure_data_files(self):
        """Ensure user and application data files exist"""
        os.makedirs('data', exist_ok=True)
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.applications_file):
            with open(self.applications_file, 'w') as f:
                json.dump({}, f)
    
    def load_users(self):
        """Load users from JSON file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def load_applications(self):
        """Load applications from JSON file"""
        try:
            with open(self.applications_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_applications(self, applications):
        """Save applications to JSON file"""
        with open(self.applications_file, 'w') as f:
            json.dump(applications, f, indent=2)
    
    def create_user(self, email, password, name, phone=None):
        """Create a new user account"""
        users = self.load_users()
        
        if email in users:
            return {'success': False, 'error': 'User already exists'}
        
        user_id = str(uuid.uuid4())
        users[email] = {
            'id': user_id,
            'email': email,
            'password': password,  # In production, this should be hashed
            'name': name,
            'phone': phone,
            'profile_complete': False,
            'created_at': datetime.now().isoformat(),
            'profile': {}
        }
        
        self.save_users(users)
        return {'success': True, 'user_id': user_id, 'user': users[email]}
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        users = self.load_users()
        
        if email not in users:
            return {'success': False, 'error': 'User not found'}
        
        if users[email]['password'] != password:
            return {'success': False, 'error': 'Invalid password'}
        
        return {'success': True, 'user': users[email]}
    
    def update_profile(self, email, profile_data):
        """Update user profile"""
        users = self.load_users()
        
        if email not in users:
            return {'success': False, 'error': 'User not found'}
        
        users[email]['profile'] = profile_data
        users[email]['profile_complete'] = True
        users[email]['updated_at'] = datetime.now().isoformat()
        
        self.save_users(users)
        return {'success': True, 'user': users[email]}
    
    def get_user(self, email):
        """Get user by email"""
        users = self.load_users()
        return users.get(email)
    
    def apply_to_internship(self, user_email, internship_id, internship_title):
        """Apply user to an internship"""
        applications = self.load_applications()
        
        if user_email not in applications:
            applications[user_email] = []
        
        application = {
            'id': str(uuid.uuid4()),
            'internship_id': internship_id,
            'internship_title': internship_title,
            'status': 'applied',
            'applied_at': datetime.now().isoformat()
        }
        
        # Check if already applied
        existing = [app for app in applications[user_email] if app['internship_id'] == internship_id]
        if existing:
            return {'success': False, 'error': 'Already applied to this internship'}
        
        applications[user_email].append(application)
        self.save_applications(applications)
        return {'success': True, 'application': application}
    
    def save_internship(self, user_email, internship_id, internship_title):
        """Save internship for later"""
        applications = self.load_applications()
        
        if user_email not in applications:
            applications[user_email] = []
        
        application = {
            'id': str(uuid.uuid4()),
            'internship_id': internship_id,
            'internship_title': internship_title,
            'status': 'saved',
            'saved_at': datetime.now().isoformat()
        }
        
        # Check if already saved
        existing = [app for app in applications[user_email] if app['internship_id'] == internship_id and app['status'] == 'saved']
        if existing:
            return {'success': False, 'error': 'Already saved this internship'}
        
        applications[user_email].append(application)
        self.save_applications(applications)
        return {'success': True, 'application': application}
    
    def get_user_applications(self, user_email):
        """Get all applications for a user"""
        applications = self.load_applications()
        return applications.get(user_email, [])
    
    def update_application_status(self, user_email, application_id, status):
        """Update application status"""
        applications = self.load_applications()
        
        if user_email not in applications:
            return {'success': False, 'error': 'No applications found'}
        
        for app in applications[user_email]:
            if app['id'] == application_id:
                app['status'] = status
                app['updated_at'] = datetime.now().isoformat()
                self.save_applications(applications)
                return {'success': True, 'application': app}
        
        return {'success': False, 'error': 'Application not found'}