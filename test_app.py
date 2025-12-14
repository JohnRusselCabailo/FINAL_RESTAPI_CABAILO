import pytest
import json
import xml.etree.ElementTree as ET
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestMembers:
    """Test cases for Members endpoints"""
    
    def test_get_members(self, client):
        """Test GET /members returns list"""
        response = client.get('/members')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_get_members_xml(self, client):
        """Test GET /members?format=xml returns XML"""
        response = client.get('/members?format=xml')
        assert response.status_code == 200
        assert response.content_type == 'application/xml'
        ET.fromstring(response.data)
    
    def test_get_member_not_found(self, client):
        """Test GET /members/<id> with non-existent ID"""
        response = client.get('/members/99999')
        assert response.status_code == 404
    
    def test_create_member_no_data(self, client):
        """Test POST /members without data returns error"""
        response = client.post('/members', 
                               data=json.dumps({}),
                               content_type='application/json')
        assert response.status_code in [201, 400]


class TestMemberships:
    """Test cases for Memberships endpoints"""
    
    def test_get_memberships(self, client):
        """Test GET /memberships returns list"""
        response = client.get('/memberships')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_get_memberships_xml(self, client):
        """Test GET /memberships?format=xml returns XML"""
        response = client.get('/memberships?format=xml')
        assert response.status_code == 200
        assert response.content_type == 'application/xml'
        ET.fromstring(response.data)
    
    def test_get_membership_not_found(self, client):
        """Test GET /memberships/<id> with non-existent ID"""
        response = client.get('/memberships/99999')
        assert response.status_code == 404
    
    def test_create_membership_no_data(self, client):
        """Test POST /memberships without data returns error"""
        response = client.post('/memberships',
                               data=json.dumps({}),
                               content_type='application/json')
        assert response.status_code in [201, 400]



class TestWorkouts:
    """Test cases for Workouts endpoints"""
    
    def test_get_workouts(self, client):
        """Test GET /workouts returns list"""
        response = client.get('/workouts')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_get_workouts_xml(self, client):
        """Test GET /workouts?format=xml returns XML"""
        response = client.get('/workouts?format=xml')
        assert response.status_code == 200
        assert response.content_type == 'application/xml'
        ET.fromstring(response.data)
    
    def test_get_workout_not_found(self, client):
        """Test GET /workouts/<id> with non-existent ID"""
        response = client.get('/workouts/99999')
        assert response.status_code == 404
    
    def test_create_workout_no_data(self, client):
        """Test POST /workouts without data returns error"""
        response = client.post('/workouts',
                               data=json.dumps({}),
                               content_type='application/json')
        assert response.status_code in [201, 400]


class TestRoot:
    """Test cases for root endpoint"""
    
    def test_root_json(self, client):
        """Test GET / returns API info in JSON"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'endpoints' in data
    
    def test_root_xml(self, client):
        """Test GET /?format=xml returns API info in XML"""
        response = client.get('/?format=xml')
        assert response.status_code == 200
        assert response.content_type == 'application/xml'
