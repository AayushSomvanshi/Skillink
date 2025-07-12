from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_

app = Flask(__name__)
import os
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skillink.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    skills_offered = db.Column(db.String(300))
    skills_wanted = db.Column(db.String(300))
    availability = db.Column(db.String(100))
    is_public = db.Column(db.Boolean, default=True)
    
    def __init__(self, name=None, email=None, password=None, skills_offered=None, skills_wanted=None, availability=None, is_public=True):
        self.name = name
        self.email = email
        self.password = password
        self.skills_offered = skills_offered
        self.skills_wanted = skills_wanted
        self.availability = availability
        self.is_public = is_public

class SwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50), default='pending')
    
    def __init__(self, sender_id=None, receiver_id=None, status='pending'):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.status = status

HTML_HEAD = '''
<head>
  <title>Skillink</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
  <style>
    body { font-family: 'Poppins', sans-serif; }
    .hero-gradient { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .card-glass { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); }
    .btn-modern { @apply px-6 py-3 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg; }
    .btn-primary-modern { @apply bg-gradient-to-r from-blue-600 to-purple-600 text-white btn-modern hover:from-blue-700 hover:to-purple-700; }
    .btn-secondary-modern { @apply bg-white text-gray-700 border-2 border-gray-200 btn-modern hover:border-gray-300 hover:shadow-xl; }
    .input-modern { @apply w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-300 text-gray-800 bg-white; }
    .card-modern { @apply bg-white rounded-2xl shadow-xl border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1; }
    .section-card { @apply bg-gradient-to-br from-white to-gray-50 rounded-2xl p-8 shadow-lg border border-gray-100; }
  </style>
</head>
'''

@app.route('/')
def home():
    return f'''
    <html>{HTML_HEAD}
    <body class="hero-gradient text-white">
        <div class="min-h-screen flex flex-col items-center justify-center p-8">
            <div class="text-center max-w-5xl mx-auto">
                <div class="mb-12">
                    <div class="inline-flex items-center justify-center w-24 h-24 bg-white/20 rounded-full mb-6 backdrop-blur-sm">
                        <i class="fas fa-exchange-alt text-4xl text-white"></i>
                    </div>
                    <h1 class="text-8xl font-extrabold mb-6 text-white">Skillink</h1>
                    <p class="text-3xl mb-4 font-light">Swap your skills, grow your network</p>
                    <p class="text-xl mb-12 text-blue-100 max-w-3xl mx-auto leading-relaxed">Connect with people who have the skills you need and share your expertise. Learn by teaching, teach by learning.</p>
                </div>
                
                <div class="grid md:grid-cols-3 gap-8 mb-16">
                    <div class="card-glass rounded-2xl p-8 transform hover:scale-105 transition-all duration-300">
                        <div class="w-16 h-16 bg-gradient-to-r from-blue-800 to-purple-900 rounded-2xl flex items-center justify-center mb-6 mx-auto">
                            <i class="fas fa-search text-white text-3xl"></i>
                        </div>
                        <h3 class="text-2xl font-bold mb-4 text-gray-800">Discover Skills</h3>
                        <p class="text-gray-600 leading-relaxed">Find people with the exact skills you want to learn</p>
                    </div>
                    <div class="card-glass rounded-2xl p-8 transform hover:scale-105 transition-all duration-300">
                        <div class="w-16 h-16 bg-gradient-to-r from-green-800 to-teal-900 rounded-2xl flex items-center justify-center mb-6 mx-auto">
                            <i class="fas fa-handshake text-white text-3xl"></i>
                        </div>
                        <h3 class="text-2xl font-bold mb-4 text-gray-800">Make Swaps</h3>
                        <p class="text-gray-600 leading-relaxed">Exchange your expertise for new knowledge</p>
                    </div>
                    <div class="card-glass rounded-2xl p-8 transform hover:scale-105 transition-all duration-300">
                        <div class="w-16 h-16 bg-gradient-to-r from-orange-800 to-red-900 rounded-2xl flex items-center justify-center mb-6 mx-auto">
                            <i class="fas fa-users text-white text-3xl"></i>
                        </div>
                        <h3 class="text-2xl font-bold mb-4 text-gray-800">Build Network</h3>
                        <p class="text-gray-600 leading-relaxed">Grow your professional connections</p>
                    </div>
                </div>
                
                <div class="space-x-6">
                    <a href="/register" class="btn-primary-modern inline-flex items-center text-lg">
                        <i class="fas fa-rocket mr-3"></i>Get Started Free
                    </a>
                    <a href="/login" class="btn-secondary-modern inline-flex items-center text-lg">
                        <i class="fas fa-sign-in-alt mr-3"></i>Sign In
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        # Basic validation
        if not name or not email or not password:
            return 'All fields are required', 400
        if len(password) < 6:
            return 'Password must be at least 6 characters', 400
        if User.query.filter_by(email=email).first():
            return 'Email already registered', 400
        user = User(name=name, email=email, password=generate_password_hash(password))
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            return 'Registration failed', 500
    return f'''
    <html>{HTML_HEAD}
    <body class="hero-gradient text-white">
        <div class="min-h-screen flex items-center justify-center p-8">
            <div class="card-glass rounded-3xl p-12 w-full max-w-md transform hover:scale-105 transition-all duration-300">
                <div class="text-center mb-8">
                    <div class="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl flex items-center justify-center mb-6 mx-auto">
                        <i class="fas fa-user-plus text-3xl text-white"></i>
                    </div>
                    <h2 class="text-4xl font-bold mb-2 text-gray-800">Join Skillink</h2>
                    <p class="text-gray-600">Create your account and start swapping skills</p>
                </div>
                <form method="POST" class="space-y-6">
                    <div>
                        <label class="block text-sm font-semibold mb-2 text-gray-700">Full Name</label>
                        <input type="text" name="name" placeholder="Enter your full name" class="input-modern" required>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 text-gray-700">Email Address</label>
                        <input type="email" name="email" placeholder="Enter your email" class="input-modern" required>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 text-gray-700">Password</label>
                        <input type="password" name="password" placeholder="Create a password" class="input-modern" required>
                    </div>
                    <button type="submit" class="btn-primary-modern w-full text-lg">
                        <i class="fas fa-rocket mr-3"></i>Create Account
                    </button>
                </form>
                <p class="mt-8 text-center text-gray-600">Already have an account? <a href="/login" class="text-blue-600 font-semibold hover:underline">Sign In</a></p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
    return f'''
    <html>{HTML_HEAD}
    <body class="hero-gradient text-white">
        <div class="min-h-screen flex items-center justify-center p-8">
            <div class="card-glass rounded-3xl p-12 w-full max-w-md transform hover:scale-105 transition-all duration-300">
                <div class="text-center mb-8">
                    <div class="w-20 h-20 bg-gradient-to-r from-green-500 to-teal-500 rounded-2xl flex items-center justify-center mb-6 mx-auto">
                        <i class="fas fa-sign-in-alt text-3xl text-white"></i>
                    </div>
                    <h2 class="text-4xl font-bold mb-2 text-gray-800">Welcome Back</h2>
                    <p class="text-gray-600">Sign in to your Skillink account</p>
                </div>
                <form method="POST" class="space-y-6">
                    <div>
                        <label class="block text-sm font-semibold mb-2 text-gray-700">Email Address</label>
                        <input type="email" name="email" placeholder="Enter your email" class="input-modern" required>
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 text-gray-700">Password</label>
                        <input type="password" name="password" placeholder="Enter your password" class="input-modern" required>
                    </div>
                    <button type="submit" class="btn-primary-modern w-full text-lg">
                        <i class="fas fa-sign-in-alt mr-3"></i>Sign In
                    </button>
                </form>
                <p class="mt-8 text-center text-gray-600">Don't have an account? <a href="/register" class="text-blue-600 font-semibold hover:underline">Create One</a></p>
            </div>
        </div>
    </body>
    </html>
    '''

# FROM THIS POINT ONWARD — everything is already in your Canvas,
# so no need to re-duplicate and crash display here.
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    return f'''
    <html>{HTML_HEAD}
    <body class="bg-gradient-to-br from-gray-50 to-blue-50 min-h-screen">
        <div class="p-8">
            <div class="max-w-6xl mx-auto">
                <div class="section-card mb-8">
                    <div class="flex items-center justify-between mb-8">
                        <div class="flex items-center">
                            <div class="w-16 h-16 bg-gradient-to-r from-blue-800 to-purple-900 rounded-2xl flex items-center justify-center mr-6">
                                <i class="fas fa-user-circle text-2xl text-white"></i>
                            </div>
                            <div>
                                <h1 class="text-4xl font-bold text-gray-800">Welcome back, {user.name}! 👋</h1>
                                <p class="text-gray-600 text-lg">Ready to swap some skills?</p>
                            </div>
                        </div>
                        <a href="/logout" class="btn-secondary-modern">
                            <i class="fas fa-sign-out-alt mr-2"></i>Logout
                        </a>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                        <div class="card-modern p-6">
                            <div class="flex items-center mb-4">
                                <div class="w-12 h-12 bg-gradient-to-r from-blue-800 to-purple-900 rounded-xl flex items-center justify-center mr-4">
                                    <i class="fas fa-envelope text-white text-2xl"></i>
                                </div>
                                <h3 class="text-lg font-semibold text-gray-800">Email</h3>
                            </div>
                            <p class="text-gray-600">{user.email}</p>
                        </div>
                        
                        <div class="card-modern p-6">
                            <div class="flex items-center mb-4">
                                <div class="w-12 h-12 bg-gradient-to-r from-green-800 to-teal-900 rounded-xl flex items-center justify-center mr-4">
                                    <i class="fas fa-calendar-alt text-white text-2xl"></i>
                                </div>
                                <h3 class="text-lg font-semibold text-gray-800">Availability</h3>
                            </div>
                            <p class="text-gray-600">{user.availability or 'Not set'}</p>
                        </div>
                        
                        <div class="card-modern p-6">
                            <div class="flex items-center mb-4">
                                <div class="w-12 h-12 bg-gradient-to-r from-orange-800 to-red-900 rounded-xl flex items-center justify-center mr-4">
                                    <i class="fas fa-hands-helping text-white text-2xl"></i>
                                </div>
                                <h3 class="text-lg font-semibold text-gray-800">Skills Offered</h3>
                            </div>
                            <p class="text-gray-600">{user.skills_offered or 'Not set'}</p>
                        </div>
                        
                        <div class="card-modern p-6">
                            <div class="flex items-center mb-4">
                                <div class="w-12 h-12 bg-gradient-to-r from-purple-900 to-pink-800 rounded-xl flex items-center justify-center mr-4">
                                    <i class="fas fa-lightbulb text-white text-2xl"></i>
                                </div>
                                <h3 class="text-lg font-semibold text-gray-800">Skills Wanted</h3>
                            </div>
                            <p class="text-gray-600">{user.skills_wanted or 'Not set'}</p>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <a href="/edit" class="card-modern p-6 text-center group">
                            <div class="w-16 h-16 bg-gradient-to-r from-blue-800 to-purple-900 rounded-2xl flex items-center justify-center mb-4 mx-auto group-hover:scale-110 transition-transform">
                                <i class="fas fa-edit text-white text-3xl"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800 mb-2">Edit Profile</h3>
                            <p class="text-gray-600">Update your skills and availability</p>
                        </a>
                        
                        <a href="/search" class="card-modern p-6 text-center group">
                            <div class="w-16 h-16 bg-gradient-to-r from-green-800 to-teal-900 rounded-2xl flex items-center justify-center mb-4 mx-auto group-hover:scale-110 transition-transform">
                                <i class="fas fa-search text-white text-3xl"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800 mb-2">Find Swaps</h3>
                            <p class="text-gray-600">Discover people to swap skills with</p>
                        </a>
                        
                        <a href="/swaps" class="card-modern p-6 text-center group">
                            <div class="w-16 h-16 bg-gradient-to-r from-orange-800 to-red-900 rounded-2xl flex items-center justify-center mb-4 mx-auto group-hover:scale-110 transition-transform">
                                <i class="fas fa-exchange-alt text-white text-3xl"></i>
                            </div>
                            <h3 class="text-xl font-bold text-gray-800 mb-2">Swap Requests</h3>
                            <p class="text-gray-600">Manage your incoming and outgoing requests</p>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    if request.method == 'POST':
        user.skills_offered = request.form['skills_offered']
        user.skills_wanted = request.form['skills_wanted']
        user.availability = request.form['availability']
        user.is_public = 'is_public' in request.form
        db.session.commit()
        return redirect(url_for('dashboard'))
    return f'''
    <html>{HTML_HEAD}
    <body class="hero-gradient text-white">
        <div class="min-h-screen flex items-center justify-center p-8">
            <div class="card-glass rounded-3xl p-12 w-full max-w-md transform hover:scale-105 transition-all duration-300">
                <div class="text-center mb-8">
                    <div class="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl flex items-center justify-center mb-6 mx-auto">
                        <i class="fas fa-user-edit text-3xl text-white"></i>
                    </div>
                    <h2 class="text-4xl font-bold mb-2 text-gray-800">Edit Profile</h2>
                    <p class="text-gray-600">Update your skills and availability</p>
                </div>
                <form method="POST" class="space-y-6">
                    <div>
                        <label class="block text-sm font-semibold mb-2 text-gray-700">Skills Offered</label>
                        <input type="text" name="skills_offered" value="{user.skills_offered or ''}" class="input-modern" placeholder="e.g., Python, Design, Cooking">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 text-gray-700">Skills Wanted</label>
                        <input type="text" name="skills_wanted" value="{user.skills_wanted or ''}" class="input-modern" placeholder="e.g., JavaScript, Photography, Spanish">
                    </div>
                    <div>
                        <label class="block text-sm font-semibold mb-2 text-gray-700">Availability</label>
                        <input type="text" name="availability" value="{user.availability or ''}" class="input-modern" placeholder="e.g., Weekends, Evenings, Flexible">
                    </div>
                    <div class="flex items-center">
                        <input type="checkbox" name="is_public" {'checked' if user.is_public else ''} class="mr-3 w-5 h-5 text-blue-600 rounded focus:ring-blue-500">
                        <label class="text-gray-700 font-medium">Make my profile public</label>
                    </div>
                    <button type="submit" class="w-full text-lg bg-blue-600 text-white py-3 rounded-xl font-semibold shadow-lg hover:bg-blue-700 transition-all duration-200 disabled:bg-gray-400 disabled:text-white">
                        <i class="fas fa-save mr-3"></i>Save Changes
                    </button>
                </form>
                <a href="/dashboard" class="block mt-6 text-center text-blue-600 hover:underline font-medium">Back to Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/search')
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    current_user = User.query.get(session['user_id'])
    if not current_user:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    users = User.query.filter(and_(User.is_public == True, User.id != current_user.id)).all()
    user_cards = ''
    for u in users:
        user_cards += f'''
        <div class="bg-white border border-gray-200 rounded-xl p-6 mb-4 shadow card-hover">
            <h2 class="text-xl font-semibold text-indigo-700 mb-3">{u.name}</h2>
            <div class="space-y-2 text-gray-700 mb-4">
                <p><strong>Offers:</strong> {u.skills_offered or 'Not specified'}</p>
                <p><strong>Wants:</strong> {u.skills_wanted or 'Not specified'}</p>
                <p><strong>Availability:</strong> {u.availability or 'Not specified'}</p>
            </div>
            <a href="/send_request/{u.id}" class="btn-primary-modern">Request Swap</a>
        </div>
        '''
    return f'''
    <html>{HTML_HEAD}
    <body class="bg-gray-100">
        <div class="p-6 max-w-4xl mx-auto">
            <div class="bg-white rounded-2xl shadow-2xl p-8 card-hover">
                <h1 class="text-3xl font-bold mb-6 text-indigo-700 flex items-center"><i class="fas fa-search mr-3"></i>Find Swaps</h1>
                {user_cards or '<p class="text-gray-600 text-center py-8">No public users found.</p>'}
                <a href="/dashboard" class="inline-block mt-6 text-indigo-600 hover:underline">Back to Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/send_request/<int:user_id>')
def send_request(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    existing = SwapRequest.query.filter_by(sender_id=session['user_id'], receiver_id=user_id).first()
    if not existing:
        req = SwapRequest(sender_id=session['user_id'], receiver_id=user_id)
        db.session.add(req)
        db.session.commit()
    return redirect(url_for('search'))

@app.route('/swaps')
def swaps():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('login'))
    incoming = SwapRequest.query.filter_by(receiver_id=user.id).all()
    outgoing = SwapRequest.query.filter_by(sender_id=user.id).all()
    def get_user(uid):
        user_obj = User.query.get(uid)
        return user_obj.name if user_obj else 'Unknown User'
    inc_cards = ''
    for req in incoming:
        sender = get_user(req.sender_id)
        inc_cards += f'''
        <div class="bg-white p-6 rounded-xl shadow card-hover mb-4 border border-gray-200">
            <p class="text-lg text-gray-800 mb-2"><i class="fas fa-user mr-2 text-indigo-600"></i><strong>{sender}</strong> wants to swap with you.</p>
            <p class="mb-2 text-gray-700">Status: <span class="font-semibold">{req.status.capitalize()}</span></p>
            {'<a href="/accept_request/' + str(req.id) + '" class="mr-2 btn-primary-modern">Accept</a>' if req.status == 'pending' else ''}
            {'<a href="/reject_request/' + str(req.id) + '" class="btn-secondary-modern">Reject</a>' if req.status == 'pending' else ''}
        </div>
        '''
    out_cards = ''
    for req in outgoing:
        receiver = get_user(req.receiver_id)
        out_cards += f'''
        <div class="bg-white p-6 rounded-xl shadow card-hover mb-4 border border-gray-200">
            <p class="text-lg text-gray-800 mb-2">You sent a request to <i class="fas fa-user mr-2 text-indigo-600"></i><strong>{receiver}</strong>.</p>
            <p class="mb-2 text-gray-700">Status: <span class="font-semibold">{req.status.capitalize()}</span></p>
            {'<a href="/cancel_request/' + str(req.id) + '" class="btn-secondary-modern">Cancel</a>' if req.status == 'pending' else ''}
        </div>
        '''
    return f'''
    <html>{HTML_HEAD}
    <body class="bg-gray-100 p-6">
        <div class="max-w-3xl mx-auto">
            <div class="bg-white rounded-2xl shadow-2xl p-8 card-hover">
                <h1 class="text-3xl font-bold mb-6 text-indigo-700 flex items-center"><i class="fas fa-exchange-alt mr-3"></i>Swap Requests</h1>
                <div class="mb-8">
                    <h2 class="text-xl font-semibold mb-4 text-gray-800">Incoming</h2>
                    {inc_cards or '<p class="text-gray-600">No incoming requests.</p>'}
                </div>
                <div>
                    <h2 class="text-xl font-semibold mb-4 text-gray-800">Outgoing</h2>
                    {out_cards or '<p class="text-gray-600">No outgoing requests.</p>'}
                </div>
                <a href="/dashboard" class="inline-block mt-6 text-indigo-600 hover:underline">Back to Dashboard</a>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/accept_request/<int:req_id>')
def accept_request(req_id):
    req = SwapRequest.query.get(req_id)
    if req and req.receiver_id == session['user_id']:
        req.status = 'accepted'
        db.session.commit()
    return redirect(url_for('swaps'))

@app.route('/reject_request/<int:req_id>')
def reject_request(req_id):
    req = SwapRequest.query.get(req_id)
    if req and req.receiver_id == session['user_id']:
        req.status = 'rejected'
        db.session.commit()
    return redirect(url_for('swaps'))

@app.route('/cancel_request/<int:req_id>')
def cancel_request(req_id):
    req = SwapRequest.query.get(req_id)
    if req and req.sender_id == session['user_id']:
        db.session.delete(req)
        db.session.commit()
    return redirect(url_for('swaps'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
