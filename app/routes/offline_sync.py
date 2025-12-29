"""Offline sync endpoint for downloading all data at once."""
from flask import Blueprint, jsonify
from app import db
from app.models.building import Building
from app.models.college import College
from app.models.department import Department
from app.models.lecturer import Lecturer
from app.models.route import Route
from app.models.route_card import RouteCard

offline_sync_bp = Blueprint('offline_sync', __name__)


@offline_sync_bp.route('/api/offline-sync', methods=['GET'])
def offline_sync():
    """
    Offline Sync API endpoint.
    
    Returns all data in one optimized payload:
    - buildings
    - colleges
    - departments
    - lecturers
    - routes
    - route_cards
    
    No authentication required.
    """
    try:
        # Fetch all data from database
        buildings = Building.query.all()
        colleges = College.query.all()
        departments = Department.query.all()
        lecturers = Lecturer.query.all()
        routes = Route.query.all()
        route_cards = RouteCard.query.all()

        # Convert to dictionaries
        buildings_data = [building.to_dict() for building in buildings]
        colleges_data = [college.to_dict() for college in colleges]
        departments_data = [department.to_dict() for department in departments]
        lecturers_data = [lecturer.to_dict() for lecturer in lecturers]
        routes_data = [route.to_dict() for route in routes]
        route_cards_data = [route_card.to_dict() for route_card in route_cards]

        # Return optimized response with no nesting
        return jsonify({
            'success': True,
            'data': {
                'buildings': buildings_data,
                'colleges': colleges_data,
                'departments': departments_data,
                'lecturers': lecturers_data,
                'routes': routes_data,
                'route_cards': route_cards_data
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

