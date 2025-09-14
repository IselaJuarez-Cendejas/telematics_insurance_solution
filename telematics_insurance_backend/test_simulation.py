#!/usr/bin/env python3
"""
Telematics Insurance System Test and Simulation Script

This script generates realistic telematics data and tests all system components
including data ingestion, processing, risk scoring, and API endpoints.
"""

import requests
import json
import random
import time
from datetime import datetime, timedelta
import math
import numpy as np

# Configuration
BASE_URL = 'http://localhost:5000/api'
SIMULATION_DURATION_MINUTES = 30
DATA_POINTS_PER_MINUTE = 6  # One data point every 10 seconds

class TelematicsSimulator:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.policyholders = []

    def create_test_policyholder(self, name, vehicle_info):
        """Create a test policyholder"""
        data = {
            'first_name': name.split()[0],
            'last_name': name.split()[1],
            'date_of_birth': '1985-06-15',
            'gender': 'Female',
            'address': '123 Test Street, Test City, TC 12345',
            'vehicle_make': vehicle_info['make'],
            'vehicle_model': vehicle_info['model'],
            'vehicle_year': vehicle_info['year'],
            'driving_history_score': random.randint(700, 900)
        }

        try:
            response = self.session.post(f'{self.base_url}/policyholders', json=data)
            if response.status_code == 201:
                policyholder = response.json()
                self.policyholders.append(policyholder)
                print(f"✓ Created policyholder: {policyholder['id']}")
                return policyholder
            else:
                print(f"✗ Failed to create policyholder: {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Error creating policyholder: {e}")
            return None

    def generate_realistic_trip(self, start_lat=37.7749, start_lon=-122.4194,
                                trip_type='commute', duration_minutes=25):
        """Generate realistic GPS and sensor data for a trip"""
        trip_data = []

        # Trip parameters based on type
        if trip_type == 'commute':
            avg_speed = 45  # km/h
            harsh_event_probability = 0.02
            max_speed = 80
        elif trip_type == 'city':
            avg_speed = 30
            harsh_event_probability = 0.05
            max_speed = 60
        elif trip_type == 'highway':
            avg_speed = 90
            harsh_event_probability = 0.01
            max_speed = 120
        else:
            avg_speed = 35
            harsh_event_probability = 0.03
            max_speed = 70

        # Generate route points
        total_points = duration_minutes * DATA_POINTS_PER_MINUTE
        distance_per_point = (avg_speed / 60) / DATA_POINTS_PER_MINUTE  # km per point

        current_lat = start_lat
        current_lon = start_lon
        current_speed = 0

        for i in range(total_points):
            timestamp = datetime.utcnow() + timedelta(seconds=i * 10)

            # Simulate realistic speed changes
            if i < 5:  # Acceleration phase
                current_speed = min(avg_speed, current_speed + random.uniform(5, 15))
            elif i > total_points - 5:  # Deceleration phase
                current_speed = max(0, current_speed - random.uniform(5, 15))
            else:  # Cruise phase with variations
                speed_variation = random.uniform(-10, 10)
                current_speed = max(0, min(max_speed, avg_speed + speed_variation))

            # Update position (simplified linear movement)
            bearing = random.uniform(0, 360)  # Random direction changes
            lat_change = (distance_per_point / 111) * math.cos(math.radians(bearing))
            lon_change = (distance_per_point / (111 * math.cos(math.radians(current_lat)))) * math.sin(math.radians(bearing))

            current_lat += lat_change * 0.1  # Reduce movement for realism
            current_lon += lon_change * 0.1

            # Generate acceleration data
            base_accel_x = random.uniform(-0.1, 0.1)
            base_accel_y = random.uniform(-0.1, 0.1)
            base_accel_z = random.uniform(0.9, 1.1)  # Gravity + vehicle movement

            # Simulate harsh events
            event_type = 'normal'
            if random.random() < harsh_event_probability:
                event_types = ['harsh_braking', 'rapid_acceleration', 'harsh_cornering']
                event_type = random.choice(event_types)

                if event_type == 'harsh_braking':
                    base_accel_x = random.uniform(-0.5, -0.3)
                    current_speed *= 0.7  # Sudden speed reduction
                elif event_type == 'rapid_acceleration':
                    base_accel_x = random.uniform(0.3, 0.5)
                    current_speed *= 1.2  # Speed increase
                elif event_type == 'harsh_cornering':
                    base_accel_y = random.uniform(-0.4, 0.4)

            trip_data.append({
                'timestamp': timestamp.isoformat() + 'Z',
                'latitude': round(current_lat, 6),
                'longitude': round(current_lon, 6),
                'speed_kph': int(current_speed),
                'acceleration_x': round(base_accel_x, 3),
                'acceleration_y': round(base_accel_y, 3),
                'acceleration_z': round(base_accel_z, 3),
                'heading_degrees': int(bearing),
                'event_type': event_type
            })

        return trip_data

    def simulate_trip(self, policyholder_id, trip_type='commute'):
        """Simulate a complete trip with data ingestion and processing"""
        print(f"\n🚗 Simulating {trip_type} trip for policyholder {policyholder_id}")

        # Generate trip data
        trip_data = self.generate_realistic_trip(trip_type=trip_type)
        device_id = f"DEVICE-{policyholder_id[-6:]}"

        # Prepare raw data for ingestion
        raw_data_batch = []
        for point in trip_data:
            raw_data_batch.append({
                'device_id': device_id,
                'policyholder_id': policyholder_id,
                **point
            })

        # Ingest raw data
        try:
            response = self.session.post(f'{self.base_url}/raw-data', json=raw_data_batch)
            if response.status_code == 201:
                print(f"✓ Ingested {len(raw_data_batch)} raw data points")
            else:
                print(f"✗ Failed to ingest raw data: {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Error ingesting raw data: {e}")
            return None

        # Process trip data
        try:
            trip_processing_data = {
                'raw_points': trip_data,
                'policyholder_id': policyholder_id,
                'start_location_name': 'Home' if trip_type == 'commute' else 'Location A',
                'end_location_name': 'Work' if trip_type == 'commute' else 'Location B',
                'weather_conditions': random.choice(['clear', 'cloudy', 'light_rain']),
                'traffic_conditions': random.choice(['light', 'moderate', 'heavy'])
            }

            response = self.session.post(f'{self.base_url}/process-trip', json=trip_processing_data)
            if response.status_code == 201:
                trip_result = response.json()
                print(f"✓ Processed trip: {trip_result['trip_id']}")
                return trip_result
            else:
                print(f"✗ Failed to process trip: {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Error processing trip: {e}")
            return None

    def test_risk_scoring(self, policyholder_id):
        """Test the risk scoring system"""
        print(f"\n📊 Testing risk scoring for policyholder {policyholder_id}")

        try:
            response = self.session.post(f'{self.base_url}/risk-score/{policyholder_id}')
            if response.status_code == 200:
                risk_data = response.json()
                print(f"✓ Risk score calculated: {risk_data['risk_score']:.3f}")
                print(f"  Premium adjustment: {risk_data['premium_adjustment']:.1f}%")
                return risk_data
            else:
                print(f"✗ Failed to calculate risk score: {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Error calculating risk score: {e}")
            return None

    def test_gamification(self, policyholder_id):
        """Test gamification features"""
        print(f"\n🎮 Testing gamification for policyholder {policyholder_id}")

        # Test achievements
        try:
            response = self.session.get(f'{self.base_url}/achievements/{policyholder_id}')
            if response.status_code == 200:
                achievements = response.json()
                print(f"✓ Found {len(achievements)} achievements")
                for achievement in achievements:
                    print(f"  🏆 {achievement['name']}: {achievement['description']}")
            else:
                print(f"✗ Failed to get achievements: {response.status_code}")
        except Exception as e:
            print(f"✗ Error getting achievements: {e}")

        # Test challenges
        try:
            response = self.session.get(f'{self.base_url}/challenges/{policyholder_id}')
            if response.status_code == 200:
                challenges = response.json()
                print(f"✓ Found {len(challenges)} challenges")
                for challenge in challenges:
                    print(f"  🎯 {challenge['name']}: {challenge['progress']['percentage']:.1f}% complete")
            else:
                print(f"✗ Failed to get challenges: {response.status_code}")
        except Exception as e:
            print(f"✗ Error getting challenges: {e}")

    def test_external_data(self):
        """Test external data integration"""
        print(f"\n🌐 Testing external data APIs")

        # Test weather API
        try:
            params = {'lat': 37.7749, 'lon': -122.4194}
            response = self.session.get(f'{self.base_url}/weather/current', params=params)
            if response.status_code == 200:
                weather = response.json()
                print(f"✓ Weather data: {weather['current']['weather_description']}, {weather['current']['temperature']}°C")
            else:
                print(f"✗ Failed to get weather data: {response.status_code}")
        except Exception as e:
            print(f"✗ Error getting weather data: {e}")

        # Test traffic API
        try:
            params = {
                'origin_lat': 37.7749, 'origin_lon': -122.4194,
                'dest_lat': 37.7849, 'dest_lon': -122.4094
            }
            response = self.session.get(f'{self.base_url}/traffic/current', params=params)
            if response.status_code == 200:
                traffic = response.json()
                print(f"✓ Traffic data: {traffic['traffic_conditions']['overall_level']} congestion")
            else:
                print(f"✗ Failed to get traffic data: {response.status_code}")
        except Exception as e:
            print(f"✗ Error getting traffic data: {e}")

        # Test contextual risk
        try:
            risk_data = {
                'lat': 37.7749,
                'lon': -122.4194,
                'time_of_day': '08:30',
                'day_of_week': 'Monday',
                'weather_conditions': 'clear'
            }
            response = self.session.post(f'{self.base_url}/contextual-risk', json=risk_data)
            if response.status_code == 200:
                risk = response.json()
                print(f"✓ Contextual risk: {risk['risk_level']} ({risk['contextual_risk_score']:.3f})")
            else:
                print(f"✗ Failed to get contextual risk: {response.status_code}")
        except Exception as e:
            print(f"✗ Error getting contextual risk: {e}")

    def test_dashboard_data(self, policyholder_id):
        """Test dashboard data retrieval"""
        print(f"\n📱 Testing dashboard data for policyholder {policyholder_id}")

        try:
            response = self.session.get(f'{self.base_url}/dashboard/{policyholder_id}')
            if response.status_code == 200:
                dashboard = response.json()
                print(f"✓ Dashboard data retrieved")
                print(f"  Total trips: {dashboard['summary']['total_trips']}")
                print(f"  Total distance: {dashboard['summary']['total_distance_km']:.1f} km")
                print(f"  Current risk score: {dashboard['summary']['current_risk_score']:.3f}")
                print(f"  Recent trips: {len(dashboard['recent_trips'])}")
                return dashboard
            else:
                print(f"✗ Failed to get dashboard data: {response.status_code}")
                return None
        except Exception as e:
            print(f"✗ Error getting dashboard data: {e}")
            return None

    def run_comprehensive_test(self):
        """Run a comprehensive test of the entire system"""
        print("🚀 Starting Comprehensive Telematics System Test")
        print("=" * 60)

        # Create test policyholders
        test_drivers = [
            ("Jane Doe", {"make": "Toyota", "model": "Camry", "year": 2020}),
            ("John Smith", {"make": "Honda", "model": "Civic", "year": 2019}),
            ("Alice Johnson", {"make": "Ford", "model": "Focus", "year": 2021})
        ]

        created_policyholders = []
        for name, vehicle in test_drivers:
            policyholder = self.create_test_policyholder(name, vehicle)
            if policyholder:
                created_policyholders.append(policyholder)

        if not created_policyholders:
            print("✗ No policyholders created. Exiting test.")
            return

        # Simulate multiple trips for each policyholder
        trip_types = ['commute', 'city', 'highway', 'city']

        for policyholder in created_policyholders:
            policyholder_id = policyholder['id']

            # Simulate multiple trips
            for i, trip_type in enumerate(trip_types):
                print(f"\n--- Trip {i+1} for {policyholder['first_name']} {policyholder['last_name']} ---")
                trip_result = self.simulate_trip(policyholder_id, trip_type)

                if trip_result:
                    # Small delay between trips
                    time.sleep(1)

            # Update aggregates
            try:
                response = self.session.post(f'{self.base_url}/update-aggregates/{policyholder_id}')
                if response.status_code == 200:
                    print(f"✓ Updated aggregates for {policyholder_id}")
                else:
                    print(f"✗ Failed to update aggregates: {response.status_code}")
            except Exception as e:
                print(f"✗ Error updating aggregates: {e}")

            # Test risk scoring
            self.test_risk_scoring(policyholder_id)

            # Test gamification
            self.test_gamification(policyholder_id)

            # Test dashboard data
            self.test_dashboard_data(policyholder_id)

        # Test external data APIs
        self.test_external_data()

        # Test leaderboard
        print(f"\n🏆 Testing leaderboard")
        try:
            response = self.session.get(f'{self.base_url}/leaderboard')
            if response.status_code == 200:
                leaderboard = response.json()
                print(f"✓ Leaderboard retrieved with {len(leaderboard)} drivers")
                for i, driver in enumerate(leaderboard[:3]):
                    print(f"  {i+1}. {driver['name']} - Risk Score: {driver['risk_score']:.3f}")
            else:
                print(f"✗ Failed to get leaderboard: {response.status_code}")
        except Exception as e:
            print(f"✗ Error getting leaderboard: {e}")

        print("\n" + "=" * 60)
        print("🎉 Comprehensive test completed!")
        print(f"Created {len(created_policyholders)} test policyholders")
        print(f"Simulated {len(created_policyholders) * len(trip_types)} trips")
        print("All system components tested")

def main():
    """Main function to run the simulation"""
    print("Telematics Insurance System - Test & Simulation")
    print("Waiting for backend server to be ready...")

    # Wait for server to be ready
    simulator = TelematicsSimulator()
    max_retries = 10
    for i in range(max_retries):
        try:
            response = simulator.session.get(f'{BASE_URL}/users')
            if response.status_code in [200, 404]:  # Server is responding
                print("✓ Backend server is ready")
                break
        except:
            pass

        if i == max_retries - 1:
            print("✗ Backend server is not responding. Please start the Flask server first.")
            return

        print(f"Waiting for server... ({i+1}/{max_retries})")
        time.sleep(2)

    # Run the comprehensive test
    simulator.run_comprehensive_test()

if __name__ == "__main__":
    main()

