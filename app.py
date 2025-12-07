from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL
import xml.etree.ElementTree as ET
import jwt
import datetime
from functools import wraps
import config

app = Flask(__name__)

#JWT Secret Key
app.config['SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NjU3OTYyMDZ9.MaK8WnxKhpjl_f2tOm10ZnPmUXg5Ez6yd82GmTUhXl'


app.config['MYSQL_HOST'] = config.MYSQL_HOST
app.config['MYSQL_USER'] = config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB
app.config['MYSQL_PORT'] = config.MYSQL_PORT

mysql = MySQL(app)



def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return make_api_response({'error': 'Token is missing'}, 401)
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return make_api_response({'error': 'Token has expired'}, 401)
        except jwt.InvalidTokenError:
            return make_api_response({'error': 'Token is invalid'}, 401)
        
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['POST'])
def login():
    """Login endpoint to get JWT token"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return make_api_response({'error': 'Username and password required'}, 400)
    
    if data['username'] == 'admin' and data['password'] == 'admin123':
        token = jwt.encode({
            'user': data['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return make_api_response({'token': token, 'message': 'Login successful'})
    
    return make_api_response({'error': 'Invalid credentials'}, 401)



def get_response_format():
    """Determine response format from query param or Accept header"""
    format_param = request.args.get('format', '').lower()
    if format_param == 'xml':
        return 'xml'
    accept_header = request.headers.get('Accept', '')
    if 'application/xml' in accept_header:
        return 'xml'
    return 'json'


def dict_to_xml(data, root_name='response'):
    """Convert dictionary or list to XML string"""
    root = ET.Element(root_name)
    
    if isinstance(data, list):
        for item in data:
            item_elem = ET.SubElement(root, 'item')
            for key, value in item.items():
                child = ET.SubElement(item_elem, str(key))
                child.text = str(value) if value is not None else ''
    elif isinstance(data, dict):
        for key, value in data.items():
            child = ET.SubElement(root, str(key))
            child.text = str(value) if value is not None else ''
    
    return ET.tostring(root, encoding='unicode')


def make_api_response(data, status_code=200):
    """Create response in JSON or XML format based on request"""
    if get_response_format() == 'xml':
        xml_data = dict_to_xml(data)
        response = make_response(xml_data, status_code)
        response.headers['Content-Type'] = 'application/xml'
        return response
    return jsonify(data), status_code



@app.route('/members', methods=['GET'])
def get_members():
    """Get all members"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM member")
    rows = cur.fetchall()
    cur.close()
    
    members = []
    for row in rows:
        members.append({
            'memberId': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'membership_id': row[3],
            'Memberships_membership_id': row[4],
            'Workouts_workout_id': row[5]
        })
    return make_api_response(members)


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Get a single member by ID"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM member WHERE memberId = %s", (member_id,))
    row = cur.fetchone()
    cur.close()
    
    if row is None:
        return make_api_response({'error': 'Member not found'}, 404)
    
    member = {
        'memberId': row[0],
        'first_name': row[1],
        'last_name': row[2],
        'membership_id': row[3],
        'Memberships_membership_id': row[4],
        'Workouts_workout_id': row[5]
    }
    return make_api_response(member)


@app.route('/members', methods=['POST'])
def create_member():
    """Create a new member"""
    data = request.get_json()
    
    if not data:
        return make_api_response({'error': 'No data provided'}, 400)
    
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO member (first_name, last_name, membership_id, Memberships_membership_id, Workouts_workout_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data.get('first_name'),
        data.get('last_name'),
        data.get('membership_id'),
        data.get('Memberships_membership_id'),
        data.get('Workouts_workout_id')
    ))
    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()
    
    return make_api_response({'message': 'Member created', 'memberId': new_id}, 201)


@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Update an existing member"""
    data = request.get_json()
    
    if not data:
        return make_api_response({'error': 'No data provided'}, 400)
    
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE member 
        SET first_name = %s, last_name = %s, membership_id = %s, 
            Memberships_membership_id = %s, Workouts_workout_id = %s
        WHERE memberId = %s
    """, (
        data.get('first_name'),
        data.get('last_name'),
        data.get('membership_id'),
        data.get('Memberships_membership_id'),
        data.get('Workouts_workout_id'),
        member_id
    ))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    
    if affected_rows == 0:
        return make_api_response({'error': 'Member not found'}, 404)
    
    return make_api_response({'message': 'Member updated'})


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete a member"""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM member WHERE memberId = %s", (member_id,))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    
    if affected_rows == 0:
        return make_api_response({'error': 'Member not found'}, 404)
    
    return make_api_response({'message': 'Member deleted'})


@app.route('/members/search', methods=['GET'])
def search_members():
    """Search members by first_name or last_name"""
    first_name = request.args.get('first_name', '')
    last_name = request.args.get('last_name', '')
    
    if not first_name and not last_name:
        return make_api_response({'error': 'Please provide first_name or last_name parameter'}, 400)
    
    cur = mysql.connection.cursor()
    
    if first_name and last_name:
        cur.execute("SELECT * FROM member WHERE first_name LIKE %s AND last_name LIKE %s", 
                    (f'%{first_name}%', f'%{last_name}%'))
    elif first_name:
        cur.execute("SELECT * FROM member WHERE first_name LIKE %s", (f'%{first_name}%',))
    else:
        cur.execute("SELECT * FROM member WHERE last_name LIKE %s", (f'%{last_name}%',))
    
    rows = cur.fetchall()
    cur.close()
    
    members = []
    for row in rows:
        members.append({
            'memberId': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'membership_id': row[3],
            'Memberships_membership_id': row[4],
            'Workouts_workout_id': row[5]
        })
    
    return make_api_response(members)



@app.route('/memberships', methods=['GET'])
def get_memberships():
    """Get all memberships"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM memberships")
    rows = cur.fetchall()
    cur.close()
    
    memberships = []
    for row in rows:
        memberships.append({
            'membership_id': row[0],
            'membership_type': row[1],
            'price': float(row[2]) if row[2] else None,
            'duration_months': row[3]
        })
    return make_api_response(memberships)


@app.route('/memberships/<int:membership_id>', methods=['GET'])
def get_membership(membership_id):
    """Get a single membership by ID"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM memberships WHERE membership_id = %s", (membership_id,))
    row = cur.fetchone()
    cur.close()
    
    if row is None:
        return make_api_response({'error': 'Membership not found'}, 404)
    
    membership = {
        'membership_id': row[0],
        'membership_type': row[1],
        'price': float(row[2]) if row[2] else None,
        'duration_months': row[3]
    }
    return make_api_response(membership)


@app.route('/memberships', methods=['POST'])
def create_membership():
    """Create a new membership"""
    data = request.get_json()
    
    if not data:
        return make_api_response({'error': 'No data provided'}, 400)
    
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO memberships (membership_type, price, duration_months)
        VALUES (%s, %s, %s)
    """, (
        data.get('membership_type'),
        data.get('price'),
        data.get('duration_months')
    ))
    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()
    
    return make_api_response({'message': 'Membership created', 'membership_id': new_id}, 201)


@app.route('/memberships/<int:membership_id>', methods=['PUT'])
def update_membership(membership_id):
    """Update an existing membership"""
    data = request.get_json()
    
    if not data:
        return make_api_response({'error': 'No data provided'}, 400)
    
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE memberships 
        SET membership_type = %s, price = %s, duration_months = %s
        WHERE membership_id = %s
    """, (
        data.get('membership_type'),
        data.get('price'),
        data.get('duration_months'),
        membership_id
    ))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    
    if affected_rows == 0:
        return make_api_response({'error': 'Membership not found'}, 404)
    
    return make_api_response({'message': 'Membership updated'})


@app.route('/memberships/<int:membership_id>', methods=['DELETE'])
def delete_membership(membership_id):
    """Delete a membership"""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM memberships WHERE membership_id = %s", (membership_id,))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    
    if affected_rows == 0:
        return make_api_response({'error': 'Membership not found'}, 404)
    
    return make_api_response({'message': 'Membership deleted'})


@app.route('/memberships/search', methods=['GET'])
def search_memberships():
    """Search memberships by membership_type"""
    membership_type = request.args.get('membership_type', '')
    
    if not membership_type:
        return make_api_response({'error': 'Please provide membership_type parameter'}, 400)
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM memberships WHERE membership_type LIKE %s", (f'%{membership_type}%',))
    rows = cur.fetchall()
    cur.close()
    
    memberships = []
    for row in rows:
        memberships.append({
            'membership_id': row[0],
            'membership_type': row[1],
            'price': float(row[2]) if row[2] else None,
            'duration_months': row[3]
        })
    
    return make_api_response(memberships)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    """Get all workouts"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM workouts")
    rows = cur.fetchall()
    cur.close()
    
    workouts = []
    for row in rows:
        workouts.append({
            'workout_id': row[0],
            'member_id': row[1],
            'workout_type': row[2],
            'duration': row[3]
        })
    return make_api_response(workouts)


@app.route('/workouts/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    """Get a single workout by ID"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM workouts WHERE workout_id = %s", (workout_id,))
    row = cur.fetchone()
    cur.close()
    
    if row is None:
        return make_api_response({'error': 'Workout not found'}, 404)
    
    workout = {
        'workout_id': row[0],
        'member_id': row[1],
        'workout_type': row[2],
        'duration': row[3]
    }
    return make_api_response(workout)


@app.route('/workouts', methods=['POST'])
def create_workout():
    """Create a new workout"""
    data = request.get_json()
    
    if not data:
        return make_api_response({'error': 'No data provided'}, 400)
    
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO workouts (member_id, workout_type, duration)
        VALUES (%s, %s, %s)
    """, (
        data.get('member_id'),
        data.get('workout_type'),
        data.get('duration')
    ))
    mysql.connection.commit()
    new_id = cur.lastrowid
    cur.close()
    
    return make_api_response({'message': 'Workout created', 'workout_id': new_id}, 201)


@app.route('/workouts/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    """Update an existing workout"""
    data = request.get_json()
    
    if not data:
        return make_api_response({'error': 'No data provided'}, 400)
    
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE workouts 
        SET member_id = %s, workout_type = %s, duration = %s
        WHERE workout_id = %s
    """, (
        data.get('member_id'),
        data.get('workout_type'),
        data.get('duration'),
        workout_id
    ))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    
    if affected_rows == 0:
        return make_api_response({'error': 'Workout not found'}, 404)
    
    return make_api_response({'message': 'Workout updated'})


@app.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """Delete a workout"""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM workouts WHERE workout_id = %s", (workout_id,))
    mysql.connection.commit()
    affected_rows = cur.rowcount
    cur.close()
    
    if affected_rows == 0:
        return make_api_response({'error': 'Workout not found'}, 404)
    
    return make_api_response({'message': 'Workout deleted'})


@app.route('/workouts/search', methods=['GET'])
def search_workouts():
    """Search workouts by workout_type"""
    workout_type = request.args.get('workout_type', '')
    
    if not workout_type:
        return make_api_response({'error': 'Please provide workout_type parameter'}, 400)
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM workouts WHERE workout_type LIKE %s", (f'%{workout_type}%',))
    rows = cur.fetchall()
    cur.close()
    
    workouts = []
    for row in rows:
        workouts.append({
            'workout_id': row[0],
            'member_id': row[1],
            'workout_type': row[2],
            'duration': row[3]
        })
    
    return make_api_response(workouts)




@app.route('/', methods=['GET'])
def index():
    """API root endpoint with available routes"""
    routes = {
        'message': 'Welcome to RUSSEL GymDB REST API',
        'endpoints': {
            'members': '/members',
            'memberships': '/memberships',
            'workouts': '/workouts'
        },
        
    }
    return make_api_response(routes)


if __name__ == '__main__':
    app.run(debug=config.DEBUG)
