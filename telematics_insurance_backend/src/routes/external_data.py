from flask import Blueprint, jsonify, request
import requests
import json
from datetime import datetime, timedelta
import os

external_data_bp = Blueprint('external_data', __name__)

# Mock API keys for demonstration (in production, these would be environment variables)
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'demo_key')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'demo_key')

@external_data_bp.route('/weather/current', methods=['GET'])
def get_current_weather():
    """Get current weather conditions for a location"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required'}), 400

    # Mock weather data for demonstration
    # In production, this would call OpenWeatherMap API
    mock_weather_data = {
        'location': {
            'lat': lat,
            'lon': lon,
            'name': 'Current Location'
        },
        'current': {
            'temperature': 22.5,
            'feels_like': 24.1,
            'humidity': 65,
            'pressure': 1013,
            'visibility': 10000,
            'wind_speed': 3.2,
            'wind_direction': 180,
            'weather_main': 'Clear',
            'weather_description': 'clear sky',
            'weather_icon': '01d',
            'clouds': 5,
            'uv_index': 6.8
        },
        'conditions': {
            'is_raining': False,
            'is_snowing': False,
            'is_foggy': False,
            'visibility_km': 10,
            'road_conditions': 'dry',
            'driving_risk_level': 'low'
        },
        'timestamp': datetime.utcnow().isoformat(),
        'source': 'OpenWeatherMap'
    }

    # Simulate API call delay
    # In production:
    # url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    # response = requests.get(url)
    # weather_data = response.json()

    return jsonify(mock_weather_data)

@external_data_bp.route('/weather/forecast', methods=['GET'])
def get_weather_forecast():
    """Get weather forecast for a location"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    days = request.args.get('days', 5, type=int)

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required'}), 400

    # Mock forecast data
    forecast_data = {
        'location': {
            'lat': lat,
            'lon': lon,
            'name': 'Current Location'
        },
        'forecast': []
    }

    # Generate mock forecast for next few days
    for i in range(days):
        date = datetime.utcnow() + timedelta(days=i)
        forecast_data['forecast'].append({
            'date': date.strftime('%Y-%m-%d'),
            'temperature_max': 25 + (i % 3),
            'temperature_min': 15 + (i % 3),
            'weather_main': ['Clear', 'Clouds', 'Rain'][i % 3],
            'weather_description': ['clear sky', 'scattered clouds', 'light rain'][i % 3],
            'precipitation_probability': [10, 30, 80][i % 3],
            'wind_speed': 2.5 + (i * 0.5),
            'driving_conditions': ['excellent', 'good', 'caution'][i % 3]
        })

    return jsonify(forecast_data)

@external_data_bp.route('/traffic/current', methods=['GET'])
def get_current_traffic():
    """Get current traffic conditions for a route or area"""
    origin_lat = request.args.get('origin_lat', type=float)
    origin_lon = request.args.get('origin_lon', type=float)
    dest_lat = request.args.get('dest_lat', type=float)
    dest_lon = request.args.get('dest_lon', type=float)

    if not all([origin_lat, origin_lon, dest_lat, dest_lon]):
        return jsonify({'error': 'Origin and destination coordinates are required'}), 400

    # Mock traffic data
    mock_traffic_data = {
        'route': {
            'origin': {'lat': origin_lat, 'lon': origin_lon},
            'destination': {'lat': dest_lat, 'lon': dest_lon},
            'distance_km': 15.2,
            'duration_normal_minutes': 18,
            'duration_current_minutes': 25
        },
        'traffic_conditions': {
            'overall_level': 'moderate',
            'congestion_level': 0.6,  # 0-1 scale
            'incidents_count': 1,
            'average_speed_kph': 35,
            'expected_speed_kph': 50
        },
        'segments': [
            {
                'segment_id': 1,
                'start_lat': origin_lat,
                'start_lon': origin_lon,
                'end_lat': origin_lat + 0.01,
                'end_lon': origin_lon + 0.01,
                'traffic_level': 'light',
                'speed_kph': 45,
                'duration_minutes': 8
            },
            {
                'segment_id': 2,
                'start_lat': origin_lat + 0.01,
                'start_lon': origin_lon + 0.01,
                'end_lat': dest_lat,
                'end_lon': dest_lon,
                'traffic_level': 'heavy',
                'speed_kph': 25,
                'duration_minutes': 17
            }
        ],
        'incidents': [
            {
                'type': 'construction',
                'severity': 'medium',
                'description': 'Lane closure due to road work',
                'lat': origin_lat + 0.005,
                'lon': origin_lon + 0.005,
                'estimated_delay_minutes': 7
            }
        ],
        'timestamp': datetime.utcnow().isoformat(),
        'source': 'Google Maps'
    }

    return jsonify(mock_traffic_data)

@external_data_bp.route('/crime-data', methods=['GET'])
def get_crime_data():
    """Get crime statistics for an area"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius_km = request.args.get('radius_km', 5, type=float)

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required'}), 400

    # Mock crime data
    mock_crime_data = {
        'location': {
            'lat': lat,
            'lon': lon,
            'radius_km': radius_km
        },
        'crime_statistics': {
            'total_incidents_last_year': 245,
            'vehicle_theft_incidents': 12,
            'vandalism_incidents': 8,
            'break_ins': 15,
            'crime_rate_per_1000': 8.5,
            'safety_score': 7.2,  # 1-10 scale, 10 being safest
            'risk_level': 'medium'
        },
        'recent_incidents': [
            {
                'type': 'vehicle_theft',
                'date': '2025-09-08',
                'distance_km': 0.8,
                'severity': 'high'
            },
            {
                'type': 'vandalism',
                'date': '2025-09-05',
                'distance_km': 1.2,
                'severity': 'low'
            }
        ],
        'area_classification': 'suburban_residential',
        'timestamp': datetime.utcnow().isoformat(),
        'source': 'Local Crime Database'
    }

    return jsonify(mock_crime_data)

@external_data_bp.route('/accident-data', methods=['GET'])
def get_accident_data():
    """Get historical accident data for an area"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius_km = request.args.get('radius_km', 2, type=float)

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required'}), 400

    # Mock accident data
    mock_accident_data = {
        'location': {
            'lat': lat,
            'lon': lon,
            'radius_km': radius_km
        },
        'accident_statistics': {
            'total_accidents_last_year': 18,
            'fatal_accidents': 0,
            'injury_accidents': 6,
            'property_damage_only': 12,
            'accidents_per_1000_vehicles': 2.3,
            'risk_score': 6.8,  # 1-10 scale, 10 being highest risk
            'primary_causes': [
                {'cause': 'rear_end_collision', 'count': 7},
                {'cause': 'intersection_accident', 'count': 5},
                {'cause': 'weather_related', 'count': 3},
                {'cause': 'speeding', 'count': 3}
            ]
        },
        'hotspots': [
            {
                'intersection': 'Main St & Oak Ave',
                'lat': lat + 0.002,
                'lon': lon + 0.001,
                'accident_count': 5,
                'severity_avg': 6.2
            },
            {
                'intersection': 'Highway 101 On-ramp',
                'lat': lat - 0.001,
                'lon': lon + 0.003,
                'accident_count': 3,
                'severity_avg': 7.8
            }
        ],
        'time_patterns': {
            'peak_hours': ['07:00-09:00', '17:00-19:00'],
            'high_risk_days': ['Friday', 'Saturday'],
            'weather_correlation': {
                'rain': 0.35,
                'fog': 0.28,
                'clear': 0.15
            }
        },
        'timestamp': datetime.utcnow().isoformat(),
        'source': 'Department of Transportation'
    }

    return jsonify(mock_accident_data)

@external_data_bp.route('/road-conditions', methods=['GET'])
def get_road_conditions():
    """Get current road conditions and construction information"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius_km = request.args.get('radius_km', 10, type=float)

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required'}), 400

    # Mock road conditions data
    mock_road_data = {
        'location': {
            'lat': lat,
            'lon': lon,
            'radius_km': radius_km
        },
        'road_conditions': {
            'overall_condition': 'good',
            'surface_quality': 8.2,  # 1-10 scale
            'maintenance_score': 7.5,
            'lighting_quality': 'adequate',
            'signage_quality': 'good'
        },
        'construction_zones': [
            {
                'project_id': 'CONST-2025-001',
                'location': 'Highway 101, Mile 15-18',
                'lat': lat + 0.01,
                'lon': lon + 0.02,
                'type': 'lane_closure',
                'severity': 'medium',
                'expected_delay_minutes': 5,
                'start_date': '2025-09-01',
                'end_date': '2025-10-15',
                'active_hours': '06:00-18:00'
            }
        ],
        'road_closures': [],
        'special_conditions': [
            {
                'type': 'school_zone',
                'location': 'Elementary School Area',
                'lat': lat - 0.005,
                'lon': lon - 0.003,
                'speed_limit': 25,
                'active_hours': '07:00-09:00, 14:00-16:00',
                'active_days': 'Monday-Friday'
            }
        ],
        'timestamp': datetime.utcnow().isoformat(),
        'source': 'Department of Transportation'
    }

    return jsonify(mock_road_data)

@external_data_bp.route('/contextual-risk', methods=['POST'])
def calculate_contextual_risk():
    """Calculate contextual risk score based on multiple external factors"""
    data = request.json

    lat = data.get('lat')
    lon = data.get('lon')
    time_of_day = data.get('time_of_day')  # 24-hour format
    day_of_week = data.get('day_of_week')  # Monday, Tuesday, etc.
    weather_conditions = data.get('weather_conditions', 'clear')

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required'}), 400

    # Calculate risk factors
    risk_factors = {
        'weather_risk': calculate_weather_risk(weather_conditions),
        'time_risk': calculate_time_risk(time_of_day, day_of_week),
        'location_risk': calculate_location_risk(lat, lon),
        'traffic_risk': calculate_traffic_risk(lat, lon, time_of_day)
    }

    # Calculate overall contextual risk score (0-1 scale)
    weights = {
        'weather_risk': 0.3,
        'time_risk': 0.2,
        'location_risk': 0.3,
        'traffic_risk': 0.2
    }

    overall_risk = sum(risk_factors[factor] * weights[factor] for factor in risk_factors)

    # Generate recommendations
    recommendations = generate_risk_recommendations(risk_factors)

    return jsonify({
        'location': {'lat': lat, 'lon': lon},
        'contextual_risk_score': round(overall_risk, 3),
        'risk_level': get_risk_level(overall_risk),
        'risk_factors': risk_factors,
        'recommendations': recommendations,
        'timestamp': datetime.utcnow().isoformat()
    })

# Helper functions
def calculate_weather_risk(weather_conditions):
    """Calculate risk based on weather conditions"""
    weather_risk_map = {
        'clear': 0.1,
        'partly_cloudy': 0.2,
        'cloudy': 0.3,
        'light_rain': 0.6,
        'heavy_rain': 0.8,
        'snow': 0.9,
        'fog': 0.7,
        'ice': 0.95
    }
    return weather_risk_map.get(weather_conditions.lower(), 0.3)

def calculate_time_risk(time_of_day, day_of_week):
    """Calculate risk based on time and day"""
    hour = int(time_of_day.split(':')[0]) if time_of_day else 12

    # Higher risk during night hours and weekends
    time_risk = 0.3  # Base risk

    if 22 <= hour or hour <= 6:  # Night hours
        time_risk += 0.4
    elif 7 <= hour <= 9 or 17 <= hour <= 19:  # Rush hours
        time_risk += 0.2

    if day_of_week in ['Friday', 'Saturday']:  # Weekend nights
        time_risk += 0.2

    return min(time_risk, 1.0)

def calculate_location_risk(lat, lon):
    """Calculate risk based on location (crime, accidents, etc.)"""
    # Mock calculation based on coordinates
    # In reality, this would query crime and accident databases
    base_risk = 0.3

    # Simulate urban vs rural risk
    if abs(lat) > 40:  # Simulate urban area
        base_risk += 0.2

    return min(base_risk, 1.0)

def calculate_traffic_risk(lat, lon, time_of_day):
    """Calculate risk based on traffic conditions"""
    hour = int(time_of_day.split(':')[0]) if time_of_day else 12

    # Higher risk during heavy traffic
    if 7 <= hour <= 9 or 17 <= hour <= 19:
        return 0.6
    elif 10 <= hour <= 16:
        return 0.3
    else:
        return 0.2

def get_risk_level(risk_score):
    """Convert risk score to categorical level"""
    if risk_score <= 0.3:
        return 'low'
    elif risk_score <= 0.6:
        return 'medium'
    else:
        return 'high'

def generate_risk_recommendations(risk_factors):
    """Generate recommendations based on risk factors"""
    recommendations = []

    if risk_factors['weather_risk'] > 0.5:
        recommendations.append({
            'category': 'weather',
            'message': 'Adverse weather conditions detected. Reduce speed and increase following distance.',
            'priority': 'high'
        })

    if risk_factors['time_risk'] > 0.6:
        recommendations.append({
            'category': 'time',
            'message': 'High-risk time period. Exercise extra caution and avoid unnecessary trips.',
            'priority': 'medium'
        })

    if risk_factors['location_risk'] > 0.5:
        recommendations.append({
            'category': 'location',
            'message': 'Higher crime/accident area. Stay alert and secure your vehicle.',
            'priority': 'medium'
        })

    if risk_factors['traffic_risk'] > 0.5:
        recommendations.append({
            'category': 'traffic',
            'message': 'Heavy traffic conditions. Allow extra time and maintain safe distances.',
            'priority': 'low'
        })

    return recommendations
