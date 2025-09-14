from flask import Blueprint, jsonify, request
from src.models.telematics import Policyholder, Trip, RawTelematicsData, RiskScoreHistory, db
from datetime import datetime, date
import json

telematics_bp = Blueprint('telematics', __name__)

# Policyholder routes
@telematics_bp.route('/policyholders', methods=['GET'])
def get_policyholders():
    """Get all policyholders"""
    policyholders = Policyholder.query.all()
    return jsonify([ph.to_dict() for ph in policyholders])

@telematics_bp.route('/policyholders', methods=['POST'])
def create_policyholder():
    """Create a new policyholder"""
    data = request.json

    # Convert date string to date object
    dob = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None

    policyholder = Policyholder(
        first_name=data['first_name'],
        last_name=data['last_name'],
        date_of_birth=dob,
        gender=data.get('gender'),
        address=data.get('address'),
        vehicle_make=data.get('vehicle_make'),
        vehicle_model=data.get('vehicle_model'),
        vehicle_year=data.get('vehicle_year'),
        driving_history_score=data.get('driving_history_score')
    )

    db.session.add(policyholder)
    db.session.commit()
    return jsonify(policyholder.to_dict()), 201

@telematics_bp.route('/policyholders/<string:policyholder_id>', methods=['GET'])
def get_policyholder(policyholder_id):
    """Get a specific policyholder"""
    policyholder = Policyholder.query.get_or_404(policyholder_id)
    return jsonify(policyholder.to_dict())

@telematics_bp.route('/policyholders/<string:policyholder_id>', methods=['PUT'])
def update_policyholder(policyholder_id):
    """Update a policyholder"""
    policyholder = Policyholder.query.get_or_404(policyholder_id)
    data = request.json

    # Update fields if provided
    if 'first_name' in data:
        policyholder.first_name = data['first_name']
    if 'last_name' in data:
        policyholder.last_name = data['last_name']
    if 'date_of_birth' in data:
        policyholder.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
    if 'gender' in data:
        policyholder.gender = data['gender']
    if 'address' in data:
        policyholder.address = data['address']
    if 'vehicle_make' in data:
        policyholder.vehicle_make = data['vehicle_make']
    if 'vehicle_model' in data:
        policyholder.vehicle_model = data['vehicle_model']
    if 'vehicle_year' in data:
        policyholder.vehicle_year = data['vehicle_year']
    if 'driving_history_score' in data:
        policyholder.driving_history_score = data['driving_history_score']
    if 'risk_score_current' in data:
        policyholder.risk_score_current = data['risk_score_current']
        policyholder.last_score_update = datetime.utcnow()

    policyholder.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(policyholder.to_dict())

# Trip routes
@telematics_bp.route('/trips', methods=['GET'])
def get_trips():
    """Get all trips, optionally filtered by policyholder"""
    policyholder_id = request.args.get('policyholder_id')

    if policyholder_id:
        trips = Trip.query.filter_by(policyholder_id=policyholder_id).all()
    else:
        trips = Trip.query.all()

    return jsonify([trip.to_dict() for trip in trips])

@telematics_bp.route('/trips', methods=['POST'])
def create_trip():
    """Create a new trip"""
    data = request.json

    # Convert timestamp strings to datetime objects
    start_timestamp = datetime.fromisoformat(data['start_timestamp'].replace('Z', '+00:00'))
    end_timestamp = datetime.fromisoformat(data['end_timestamp'].replace('Z', '+00:00'))

    trip = Trip(
        policyholder_id=data['policyholder_id'],
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
        duration_seconds=data['duration_seconds'],
        distance_km=data['distance_km'],
        avg_speed_kph=data['avg_speed_kph'],
        max_speed_kph=data['max_speed_kph'],
        harsh_braking_count=data.get('harsh_braking_count', 0),
        rapid_acceleration_count=data.get('rapid_acceleration_count', 0),
        harsh_cornering_count=data.get('harsh_cornering_count', 0),
        night_driving_minutes=data.get('night_driving_minutes', 0),
        peak_hour_driving_minutes=data.get('peak_hour_driving_minutes', 0),
        route_geometry=data.get('route_geometry'),
        start_location_name=data.get('start_location_name'),
        end_location_name=data.get('end_location_name'),
        weather_conditions=data.get('weather_conditions'),
        traffic_conditions=data.get('traffic_conditions'),
        high_risk_area_minutes=data.get('high_risk_area_minutes', 0)
    )

    db.session.add(trip)
    db.session.commit()
    return jsonify(trip.to_dict()), 201

@telematics_bp.route('/trips/<string:trip_id>', methods=['GET'])
def get_trip(trip_id):
    """Get a specific trip"""
    trip = Trip.query.get_or_404(trip_id)
    return jsonify(trip.to_dict())

# Raw telematics data routes
@telematics_bp.route('/raw-data', methods=['POST'])
def ingest_raw_data():
    """Ingest raw telematics data"""
    data = request.json

    # Handle single record or batch
    if isinstance(data, list):
        records = []
        for record in data:
            raw_data = RawTelematicsData(
                device_id=record['device_id'],
                policyholder_id=record['policyholder_id'],
                timestamp=datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00')),
                latitude=record['latitude'],
                longitude=record['longitude'],
                speed_kph=record['speed_kph'],
                acceleration_x=record.get('acceleration_x'),
                acceleration_y=record.get('acceleration_y'),
                acceleration_z=record.get('acceleration_z'),
                heading_degrees=record.get('heading_degrees'),
                odometer_km=record.get('odometer_km'),
                event_type=record.get('event_type', 'normal'),
                raw_data_payload=json.dumps(record.get('raw_data_payload')) if record.get('raw_data_payload') else None
            )
            records.append(raw_data)

        db.session.add_all(records)
        db.session.commit()
        return jsonify({'message': f'Ingested {len(records)} records'}), 201
    else:
        raw_data = RawTelematicsData(
            device_id=data['device_id'],
            policyholder_id=data['policyholder_id'],
            timestamp=datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00')),
            latitude=data['latitude'],
            longitude=data['longitude'],
            speed_kph=data['speed_kph'],
            acceleration_x=data.get('acceleration_x'),
            acceleration_y=data.get('acceleration_y'),
            acceleration_z=data.get('acceleration_z'),
            heading_degrees=data.get('heading_degrees'),
            odometer_km=data.get('odometer_km'),
            event_type=data.get('event_type', 'normal'),
            raw_data_payload=json.dumps(data.get('raw_data_payload')) if data.get('raw_data_payload') else None
        )

        db.session.add(raw_data)
        db.session.commit()
        return jsonify(raw_data.to_dict()), 201

@telematics_bp.route('/raw-data', methods=['GET'])
def get_raw_data():
    """Get raw telematics data, optionally filtered by policyholder and time range"""
    policyholder_id = request.args.get('policyholder_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    limit = request.args.get('limit', 100, type=int)

    query = RawTelematicsData.query

    if policyholder_id:
        query = query.filter_by(policyholder_id=policyholder_id)

    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(RawTelematicsData.timestamp >= start_dt)

    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(RawTelematicsData.timestamp <= end_dt)

    raw_data = query.order_by(RawTelematicsData.timestamp.desc()).limit(limit).all()
    return jsonify([data.to_dict() for data in raw_data])

# Risk scoring routes
@telematics_bp.route('/risk-score/<string:policyholder_id>', methods=['POST'])
def calculate_risk_score(policyholder_id):
    """Calculate and update risk score for a policyholder"""
    policyholder = Policyholder.query.get_or_404(policyholder_id)

    # Simple risk scoring algorithm (placeholder)
    # In a real implementation, this would use the ML model
    recent_trips = Trip.query.filter_by(policyholder_id=policyholder_id).order_by(Trip.start_timestamp.desc()).limit(30).all()

    if not recent_trips:
        risk_score = 0.5  # Default neutral score
    else:
        total_harsh_events = sum(trip.harsh_braking_count + trip.rapid_acceleration_count + trip.harsh_cornering_count for trip in recent_trips)
        total_distance = sum(trip.distance_km for trip in recent_trips)

        if total_distance > 0:
            harsh_events_per_100km = (total_harsh_events / total_distance) * 100
            # Normalize to 0-1 scale (assuming 10+ harsh events per 100km is very high risk)
            risk_score = min(harsh_events_per_100km / 10.0, 1.0)
        else:
            risk_score = 0.5

    # Update policyholder risk score
    policyholder.risk_score_current = risk_score
    policyholder.last_score_update = datetime.utcnow()

    # Create risk score history record
    risk_history = RiskScoreHistory(
        policyholder_id=policyholder_id,
        score_date=date.today(),
        risk_score=risk_score,
        premium_adjustment=calculate_premium_adjustment(risk_score),
        factors_contributing=json.dumps({
            'harsh_events_per_100km': harsh_events_per_100km if 'harsh_events_per_100km' in locals() else 0,
            'total_trips': len(recent_trips)
        })
    )

    db.session.add(risk_history)
    db.session.commit()

    return jsonify({
        'policyholder_id': policyholder_id,
        'risk_score': risk_score,
        'premium_adjustment': calculate_premium_adjustment(risk_score),
        'updated_at': datetime.utcnow().isoformat()
    })

@telematics_bp.route('/risk-history/<string:policyholder_id>', methods=['GET'])
def get_risk_history(policyholder_id):
    """Get risk score history for a policyholder"""
    history = RiskScoreHistory.query.filter_by(policyholder_id=policyholder_id).order_by(RiskScoreHistory.score_date.desc()).all()
    return jsonify([record.to_dict() for record in history])

# Dashboard data routes
@telematics_bp.route('/dashboard/<string:policyholder_id>', methods=['GET'])
def get_dashboard_data(policyholder_id):
    """Get comprehensive dashboard data for a policyholder"""
    policyholder = Policyholder.query.get_or_404(policyholder_id)

    # Get recent trips
    recent_trips = Trip.query.filter_by(policyholder_id=policyholder_id).order_by(Trip.start_timestamp.desc()).limit(10).all()

    # Get risk score history
    risk_history = RiskScoreHistory.query.filter_by(policyholder_id=policyholder_id).order_by(RiskScoreHistory.score_date.desc()).limit(12).all()

    # Calculate summary statistics
    total_trips = Trip.query.filter_by(policyholder_id=policyholder_id).count()
    total_distance = db.session.query(db.func.sum(Trip.distance_km)).filter_by(policyholder_id=policyholder_id).scalar() or 0

    return jsonify({
        'policyholder': policyholder.to_dict(),
        'recent_trips': [trip.to_dict() for trip in recent_trips],
        'risk_history': [record.to_dict() for record in risk_history],
        'summary': {
            'total_trips': total_trips,
            'total_distance_km': total_distance,
            'current_risk_score': policyholder.risk_score_current,
            'premium_adjustment': calculate_premium_adjustment(policyholder.risk_score_current)
        }
    })

def calculate_premium_adjustment(risk_score):
    """Calculate premium adjustment percentage based on risk score"""
    # Simple linear adjustment: 0.0 risk = -20% premium, 1.0 risk = +30% premium
    base_adjustment = -20  # 20% discount for perfect score
    risk_penalty = 50 * risk_score  # Up to 50% penalty for worst score
    return base_adjustment + risk_penalty