from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Policyholder(db.Model):
    __tablename__ = 'policyholders'

    id = db.Column(db.String(50), primary_key=True, default=lambda: f"PH-{uuid.uuid4().hex[:10]}")
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    address = db.Column(db.Text, nullable=True)
    vehicle_make = db.Column(db.String(50), nullable=True)
    vehicle_model = db.Column(db.String(50), nullable=True)
    vehicle_year = db.Column(db.Integer, nullable=True)
    driving_history_score = db.Column(db.Integer, nullable=True)
    total_mileage_ytd = db.Column(db.Float, default=0.0)
    avg_daily_trips = db.Column(db.Float, default=0.0)
    avg_harsh_events_per_100km = db.Column(db.Float, default=0.0)
    night_driving_percentage = db.Column(db.Float, default=0.0)
    peak_hour_driving_percentage = db.Column(db.Float, default=0.0)
    risk_score_current = db.Column(db.Float, default=0.5)
    last_score_update = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trips = db.relationship('Trip', backref='policyholder', lazy=True, cascade='all, delete-orphan')
    risk_history = db.relationship('RiskScoreHistory', backref='policyholder', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'address': self.address,
            'vehicle_make': self.vehicle_make,
            'vehicle_model': self.vehicle_model,
            'vehicle_year': self.vehicle_year,
            'driving_history_score': self.driving_history_score,
            'total_mileage_ytd': self.total_mileage_ytd,
            'avg_daily_trips': self.avg_daily_trips,
            'avg_harsh_events_per_100km': self.avg_harsh_events_per_100km,
            'night_driving_percentage': self.night_driving_percentage,
            'peak_hour_driving_percentage': self.peak_hour_driving_percentage,
            'risk_score_current': self.risk_score_current,
            'last_score_update': self.last_score_update.isoformat() if self.last_score_update else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    policyholder_id = db.Column(db.String(50), db.ForeignKey('policyholders.id'), nullable=False)
    start_timestamp = db.Column(db.DateTime, nullable=False)
    end_timestamp = db.Column(db.DateTime, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    avg_speed_kph = db.Column(db.Float, nullable=False)
    max_speed_kph = db.Column(db.Integer, nullable=False)
    harsh_braking_count = db.Column(db.Integer, default=0)
    rapid_acceleration_count = db.Column(db.Integer, default=0)
    harsh_cornering_count = db.Column(db.Integer, default=0)
    night_driving_minutes = db.Column(db.Integer, default=0)
    peak_hour_driving_minutes = db.Column(db.Integer, default=0)
    route_geometry = db.Column(db.Text, nullable=True)  # GeoJSON string
    start_location_name = db.Column(db.String(200), nullable=True)
    end_location_name = db.Column(db.String(200), nullable=True)
    weather_conditions = db.Column(db.String(50), nullable=True)
    traffic_conditions = db.Column(db.String(50), nullable=True)
    high_risk_area_minutes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'policyholder_id': self.policyholder_id,
            'start_timestamp': self.start_timestamp.isoformat() if self.start_timestamp else None,
            'end_timestamp': self.end_timestamp.isoformat() if self.end_timestamp else None,
            'duration_seconds': self.duration_seconds,
            'distance_km': self.distance_km,
            'avg_speed_kph': self.avg_speed_kph,
            'max_speed_kph': self.max_speed_kph,
            'harsh_braking_count': self.harsh_braking_count,
            'rapid_acceleration_count': self.rapid_acceleration_count,
            'harsh_cornering_count': self.harsh_cornering_count,
            'night_driving_minutes': self.night_driving_minutes,
            'peak_hour_driving_minutes': self.peak_hour_driving_minutes,
            'route_geometry': self.route_geometry,
            'start_location_name': self.start_location_name,
            'end_location_name': self.end_location_name,
            'weather_conditions': self.weather_conditions,
            'traffic_conditions': self.traffic_conditions,
            'high_risk_area_minutes': self.high_risk_area_minutes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class RawTelematicsData(db.Model):
    __tablename__ = 'raw_telematics_data'

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = db.Column(db.String(100), nullable=False)
    policyholder_id = db.Column(db.String(50), db.ForeignKey('policyholders.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    speed_kph = db.Column(db.Integer, nullable=False)
    acceleration_x = db.Column(db.Float, nullable=True)
    acceleration_y = db.Column(db.Float, nullable=True)
    acceleration_z = db.Column(db.Float, nullable=True)
    heading_degrees = db.Column(db.Integer, nullable=True)
    odometer_km = db.Column(db.Float, nullable=True)
    event_type = db.Column(db.String(50), default='normal')
    raw_data_payload = db.Column(db.Text, nullable=True)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'policyholder_id': self.policyholder_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'speed_kph': self.speed_kph,
            'acceleration_x': self.acceleration_x,
            'acceleration_y': self.acceleration_y,
            'acceleration_z': self.acceleration_z,
            'heading_degrees': self.heading_degrees,
            'odometer_km': self.odometer_km,
            'event_type': self.event_type,
            'raw_data_payload': self.raw_data_payload,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class RiskScoreHistory(db.Model):
    __tablename__ = 'risk_score_history'

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    policyholder_id = db.Column(db.String(50), db.ForeignKey('policyholders.id'), nullable=False)
    score_date = db.Column(db.Date, nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    premium_adjustment = db.Column(db.Float, nullable=True)  # Percentage adjustment
    factors_contributing = db.Column(db.Text, nullable=True)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'policyholder_id': self.policyholder_id,
            'score_date': self.score_date.isoformat() if self.score_date else None,
            'risk_score': self.risk_score,
            'premium_adjustment': self.premium_adjustment,
            'factors_contributing': self.factors_contributing,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
