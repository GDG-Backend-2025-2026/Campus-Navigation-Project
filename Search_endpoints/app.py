from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError
from models import Building, Lecturer
from schemas import buildings_schema, lecturers_schema
from database import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    @app.route('/')
    def home():
        return jsonify({
            'message': 'Search Endpoints API',
            'version': '1.0.0',
            'endpoints': {
                'search_buildings': {
                    'method': 'GET',
                    'url': '/api/buildings/search',
                    'query_parameter': 'q (search term)',
                    'description': 'Search buildings by name (case-insensitive)'
                },
                'search_lecturers': {
                    'method': 'GET',
                    'url': '/api/lecturers/search',
                    'query_parameter': 'q (search term)',
                    'description': 'Search lecturers by first name or last name (case-insensitive)'
                },
                'health_check': {
                    'method': 'GET',
                    'url': '/health',
                    'description': 'API health check'
                }
            }
        })

    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'service': 'search-endpoints-api'})

    def _parse_positive_int(value, default):
        try:
            n = int(value)
            return n if n > 0 else default
        except Exception:
            return default

    @app.route('/api/buildings/search', methods=['GET'])
    def search_buildings():
        search_term = (request.args.get('q') or '').strip()
        page = _parse_positive_int(request.args.get('page', 1), 1)
        per_page = _parse_positive_int(request.args.get('per_page', 20), 20)
        per_page = min(per_page, 100)
        try:
            query = Building.query
            if search_term:
                pattern = f"%{search_term}%"
                query = query.filter(Building.name.ilike(pattern))
            pagination = query.order_by(Building.name).paginate(page=page, per_page=per_page, error_out=False)
            items = pagination.items
            result = buildings_schema.dump(items)
            return jsonify({'search_term': search_term, 'page': page, 'per_page': per_page, 'total': pagination.total, 'count': len(result), 'results': result})
        except SQLAlchemyError:
            return jsonify({'error': 'Database error', 'message': 'Could not perform search'}), 500

    @app.route('/api/lecturers/search', methods=['GET'])
    def search_lecturers():
        search_term = (request.args.get('q') or '').strip()
        page = _parse_positive_int(request.args.get('page', 1), 1)
        per_page = _parse_positive_int(request.args.get('per_page', 20), 20)
        per_page = min(per_page, 100)
        try:
            query = Lecturer.query
            if search_term:
                pattern = f"%{search_term}%"
                query = query.filter(db.or_(Lecturer.first_name.ilike(pattern), Lecturer.last_name.ilike(pattern)))
            pagination = query.order_by(Lecturer.last_name, Lecturer.first_name).paginate(page=page, per_page=per_page, error_out=False)
            items = pagination.items
            result = lecturers_schema.dump(items)
            return jsonify({'search_term': search_term, 'page': page, 'per_page': per_page, 'total': pagination.total, 'count': len(result), 'results': result})
        except SQLAlchemyError:
            return jsonify({'error': 'Database error', 'message': 'Could not perform search'}), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'message': 'The requested endpoint does not exist'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500

    return app


def add_sample_data():
    if Building.query.count() == 0:
        buildings = [
            Building(name='Science Building', code='SCI', address='123 Science St'),
            Building(name='Arts Complex', code='ART', address='456 Arts Ave'),
            Building(name='Engineering Hall', code='ENG', address='789 Engineer Rd'),
            Building(name='Main Library', code='LIB', address='101 Library Ln'),
            Building(name='Student Center', code='STU', address='202 Student Blvd')
        ]
        for b in buildings:
            db.session.add(b)
        lecturers = [
            Lecturer(first_name='John', last_name='Smith', email='john.smith@university.edu', department='Computer Science', title='Professor'),
            Lecturer(first_name='Sarah', last_name='Johnson', email='sarah.johnson@university.edu', department='Mathematics', title='Associate Professor'),
            Lecturer(first_name='Michael', last_name='Williams', email='michael.williams@university.edu', department='Physics', title='Professor'),
            Lecturer(first_name='Emily', last_name='Brown', email='emily.brown@university.edu', department='Biology', title='Assistant Professor'),
            Lecturer(first_name='David', last_name='Jones', email='david.jones@university.edu', department='History', title='Professor')
        ]
        for l in lecturers:
            db.session.add(l)
        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        try:
            add_sample_data()
        except Exception:
            pass
    app.run(host='0.0.0.0', port=5000, debug=True)
