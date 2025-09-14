from flask import Blueprint, jsonify, request
from src.models.telematics import Policyholder, Trip, db
from datetime import datetime, timedelta, date
import json

gamification_bp = Blueprint('gamification', __name__)

# Achievement definitions
ACHIEVEMENTS = {
    'safe_driver': {
        'name': 'Safe Driver',
        'description': 'Low risk score for 3 months',
        'icon': 'award',
        'color': 'yellow',
        'criteria': {'risk_score_threshold': 0.3, 'duration_months': 3}
    },
    'smooth_operator': {
        'name': 'Smooth Operator',
        'description': 'Minimal harsh events',
        'icon': 'target',
        'color': 'green',
        'criteria': {'harsh_events_per_100km_threshold': 3.0}
    },
    'eco_driver': {
        'name': 'Eco Driver',
        'description': 'Efficient driving patterns',
        'icon': 'leaf',
        'color': 'green',
        'criteria': {'avg_speed_threshold': 60}
    },
    'night_owl': {
        'name': 'Night Owl',
        'description': 'Reduced night driving',
        'icon': 'moon',
        'color': 'blue',
        'criteria': {'night_driving_threshold': 10.0}
    },
    'consistent_driver': {
        'name': 'Consistent Driver',
        'description': 'Regular driving patterns',
        'icon': 'calendar',
        'color': 'purple',
        'criteria': {'min_trips_per_month': 20}
    }
}

# Challenge definitions
CHALLENGES = {
    'week_without_harsh_events': {
        'name': 'Week Without Harsh Events',
        'description': 'Complete 7 days without any harsh braking or acceleration',
        'duration_days': 7,
        'reward_points': 100,
        'criteria': {'max_harsh_events': 0}
    },
    'reduce_night_driving': {
        'name': 'Reduce Night Driving',
        'description': 'Keep night driving under 10% for the month',
        'duration_days': 30,
        'reward_points': 150,
        'criteria': {'night_driving_target': 10.0}
    },
    'smooth_month': {
        'name': 'Smooth Month',
        'description': 'Maintain less than 2 harsh events per 100km for a month',
        'duration_days': 30,
        'reward_points': 200,
        'criteria': {'harsh_events_per_100km_target': 2.0}
    },
    'mileage_master': {
        'name': 'Mileage Master',
        'description': 'Drive 1000km with excellent behavior',
        'duration_days': 60,
        'reward_points': 250,
        'criteria': {'target_distance': 1000, 'max_risk_score': 0.3}
    }
}

@gamification_bp.route('/achievements/<string:policyholder_id>', methods=['GET'])
def get_achievements(policyholder_id):
    """Get earned achievements for a policyholder"""
    policyholder = Policyholder.query.get_or_404(policyholder_id)

    earned_achievements = []

    # Check each achievement
    for achievement_id, achievement in ACHIEVEMENTS.items():
        if check_achievement_earned(policyholder_id, achievement_id, achievement):
            earned_achievements.append({
                'id': achievement_id,
                'name': achievement['name'],
                'description': achievement['description'],
                'icon': achievement['icon'],
                'color': achievement['color'],
                'earned_date': datetime.utcnow().isoformat()  # In real implementation, store this
            })

    return jsonify(earned_achievements)

@gamification_bp.route('/challenges/<string:policyholder_id>', methods=['GET'])
def get_challenges(policyholder_id):
    """Get active challenges for a policyholder"""
    policyholder = Policyholder.query.get_or_404(policyholder_id)

    active_challenges = []

    # Check each challenge
    for challenge_id, challenge in CHALLENGES.items():
        progress = calculate_challenge_progress(policyholder_id, challenge_id, challenge)

        active_challenges.append({
            'id': challenge_id,
            'name': challenge['name'],
            'description': challenge['description'],
            'duration_days': challenge['duration_days'],
            'reward_points': challenge['reward_points'],
            'progress': progress,
            'is_completed': progress['percentage'] >= 100
        })

    return jsonify(active_challenges)

@gamification_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard of top drivers"""
    # Get top drivers by risk score (lower is better)
    top_drivers = Policyholder.query.order_by(Policyholder.risk_score_current.asc()).limit(10).all()

    leaderboard = []
    for i, driver in enumerate(top_drivers):
        # Calculate total points (simplified)
        total_points = calculate_driver_points(driver.id)

        leaderboard.append({
            'rank': i + 1,
            'name': f"{driver.first_name} {driver.last_name[0]}.",  # Privacy-friendly
            'risk_score': driver.risk_score_current,
            'total_points': total_points,
            'vehicle': f"{driver.vehicle_make} {driver.vehicle_model}",
            'premium_savings': abs(calculate_premium_adjustment(driver.risk_score_current))
        })

    return jsonify(leaderboard)

@gamification_bp.route('/driver-score/<string:policyholder_id>', methods=['GET'])
def get_driver_score(policyholder_id):
    """Get comprehensive driver score and ranking"""
    policyholder = Policyholder.query.get_or_404(policyholder_id)

    # Calculate various scores
    safety_score = calculate_safety_score(policyholder_id)
    efficiency_score = calculate_efficiency_score(policyholder_id)
    consistency_score = calculate_consistency_score(policyholder_id)

    # Overall score (weighted average)
    overall_score = (safety_score * 0.5 + efficiency_score * 0.3 + consistency_score * 0.2)

    # Calculate rank among all drivers
    better_drivers = Policyholder.query.filter(
        Policyholder.risk_score_current < policyholder.risk_score_current
    ).count()
    total_drivers = Policyholder.query.count()
    rank = better_drivers + 1

    return jsonify({
        'overall_score': round(overall_score, 1),
        'safety_score': round(safety_score, 1),
        'efficiency_score': round(efficiency_score, 1),
        'consistency_score': round(consistency_score, 1),
        'rank': rank,
        'total_drivers': total_drivers,
        'percentile': round((total_drivers - rank) / total_drivers * 100, 1),
        'total_points': calculate_driver_points(policyholder_id)
    })

@gamification_bp.route('/real-time-feedback', methods=['POST'])
def real_time_feedback():
    """Process real-time driving event and provide immediate feedback"""
    data = request.json

    event_type = data.get('event_type')  # 'harsh_braking', 'rapid_acceleration', 'speeding', etc.
    severity = data.get('severity', 'medium')  # 'low', 'medium', 'high'
    policyholder_id = data.get('policyholder_id')
    location = data.get('location', {})
    timestamp = data.get('timestamp', datetime.utcnow().isoformat())

    # Generate appropriate feedback message
    feedback = generate_feedback_message(event_type, severity)

    # Calculate impact on risk score (immediate estimate)
    risk_impact = calculate_event_risk_impact(event_type, severity)

    # Store the event for later processing
    # In a real implementation, this would go to a real-time processing queue

    response = {
        'feedback_message': feedback['message'],
        'feedback_type': feedback['type'],  # 'warning', 'tip', 'congratulation'
        'risk_impact': risk_impact,
        'suggestions': feedback['suggestions'],
        'timestamp': timestamp
    }

    return jsonify(response)

@gamification_bp.route('/driving-tips/<string:policyholder_id>', methods=['GET'])
def get_driving_tips(policyholder_id):
    """Get personalized driving tips based on behavior"""
    policyholder = Policyholder.query.get_or_404(policyholder_id)

    tips = []

    # Analyze driving patterns and generate tips
    if policyholder.avg_harsh_events_per_100km > 5:
        tips.append({
            'category': 'Safety',
            'title': 'Reduce Harsh Events',
            'description': 'Try to anticipate traffic changes and brake more gradually. This will improve your safety score and reduce vehicle wear.',
            'priority': 'high'
        })

    if policyholder.night_driving_percentage > 20:
        tips.append({
            'category': 'Risk Reduction',
            'title': 'Limit Night Driving',
            'description': 'Consider adjusting your schedule to drive during daylight hours when possible. Night driving increases accident risk.',
            'priority': 'medium'
        })

    if policyholder.peak_hour_driving_percentage > 40:
        tips.append({
            'category': 'Efficiency',
            'title': 'Avoid Peak Hours',
            'description': 'Try to schedule trips outside of rush hours (7-9 AM, 5-7 PM) to reduce stress and improve fuel efficiency.',
            'priority': 'medium'
        })

    # Add general tips if no specific issues
    if not tips:
        tips.append({
            'category': 'Maintenance',
            'title': 'Keep Up Great Driving!',
            'description': 'Your driving behavior is excellent. Remember to maintain your vehicle regularly and stay alert on the road.',
            'priority': 'low'
        })

    return jsonify(tips)

# Helper functions
def check_achievement_earned(policyholder_id, achievement_id, achievement):
    """Check if a policyholder has earned a specific achievement"""
    policyholder = Policyholder.query.get(policyholder_id)
    criteria = achievement['criteria']

    if achievement_id == 'safe_driver':
        # Check if risk score has been below threshold for required months
        return policyholder.risk_score_current <= criteria['risk_score_threshold']

    elif achievement_id == 'smooth_operator':
        return policyholder.avg_harsh_events_per_100km <= criteria['harsh_events_per_100km_threshold']

    elif achievement_id == 'night_owl':
        return policyholder.night_driving_percentage <= criteria['night_driving_threshold']

    elif achievement_id == 'consistent_driver':
        # Check average trips per month
        return policyholder.avg_daily_trips * 30 >= criteria['min_trips_per_month']

    return False

def calculate_challenge_progress(policyholder_id, challenge_id, challenge):
    """Calculate progress for a specific challenge"""
    policyholder = Policyholder.query.get(policyholder_id)

    if challenge_id == 'week_without_harsh_events':
        # Check last 7 days for harsh events
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_trips = Trip.query.filter(
            Trip.policyholder_id == policyholder_id,
            Trip.start_timestamp >= seven_days_ago
        ).all()

        days_without_events = 0
        for i in range(7):
            day = datetime.utcnow() - timedelta(days=i)
            day_trips = [t for t in recent_trips if t.start_timestamp.date() == day.date()]

            total_harsh_events = sum(
                t.harsh_braking_count + t.rapid_acceleration_count + t.harsh_cornering_count
                for t in day_trips
            )

            if total_harsh_events == 0:
                days_without_events += 1

        return {
            'current': days_without_events,
            'target': 7,
            'percentage': min(days_without_events / 7 * 100, 100),
            'description': f"{days_without_events}/7 days completed"
        }

    elif challenge_id == 'reduce_night_driving':
        target = challenge['criteria']['night_driving_target']
        current = policyholder.night_driving_percentage

        # Progress is based on how close to target (lower is better)
        if current <= target:
            percentage = 100
        else:
            # Assume starting point was 20% for calculation
            percentage = max(0, (20 - current) / (20 - target) * 100)

        return {
            'current': current,
            'target': target,
            'percentage': min(percentage, 100),
            'description': f"{current:.1f}% night driving (target: <{target}%)"
        }

    # Default progress
    return {
        'current': 0,
        'target': 100,
        'percentage': 0,
        'description': 'Not started'
    }

def calculate_driver_points(policyholder_id):
    """Calculate total points for a driver based on achievements and challenges"""
    # Simplified point calculation
    policyholder = Policyholder.query.get(policyholder_id)

    base_points = 1000
    risk_bonus = max(0, (1 - policyholder.risk_score_current) * 500)  # Up to 500 bonus points

    # Achievement bonuses (simplified)
    achievement_bonus = 0
    for achievement_id, achievement in ACHIEVEMENTS.items():
        if check_achievement_earned(policyholder_id, achievement_id, achievement):
            achievement_bonus += 100

    return int(base_points + risk_bonus + achievement_bonus)

def calculate_safety_score(policyholder_id):
    """Calculate safety score (0-100)"""
    policyholder = Policyholder.query.get(policyholder_id)

    # Base score from risk score (inverted)
    base_score = (1 - policyholder.risk_score_current) * 100

    # Adjust for harsh events
    harsh_penalty = min(policyholder.avg_harsh_events_per_100km * 5, 30)

    return max(0, base_score - harsh_penalty)

def calculate_efficiency_score(policyholder_id):
    """Calculate efficiency score (0-100)"""
    policyholder = Policyholder.query.get(policyholder_id)

    # Base score
    score = 70

    # Bonus for avoiding peak hours
    if policyholder.peak_hour_driving_percentage < 30:
        score += 20

    # Bonus for reasonable mileage
    if 5000 <= policyholder.total_mileage_ytd <= 15000:
        score += 10

    return min(score, 100)

def calculate_consistency_score(policyholder_id):
    """Calculate consistency score (0-100)"""
    policyholder = Policyholder.query.get(policyholder_id)

    # Base score for regular driving
    if 1.5 <= policyholder.avg_daily_trips <= 3.0:
        score = 80
    else:
        score = 60

    # Bonus for consistent patterns
    if policyholder.night_driving_percentage < 15:
        score += 20

    return min(score, 100)

def generate_feedback_message(event_type, severity):
    """Generate real-time feedback message for driving events"""
    messages = {
        'harsh_braking': {
            'low': {
                'message': 'Gentle reminder: Try to brake more gradually for a smoother ride.',
                'type': 'tip',
                'suggestions': ['Increase following distance', 'Anticipate traffic changes']
            },
            'medium': {
                'message': 'Harsh braking detected. Consider increasing your following distance.',
                'type': 'warning',
                'suggestions': ['Maintain 3-second following rule', 'Scan ahead for potential hazards']
            },
            'high': {
                'message': 'Very harsh braking! Please ensure you maintain a safe following distance.',
                'type': 'warning',
                'suggestions': ['Increase following distance immediately', 'Reduce speed in heavy traffic']
            }
        },
        'rapid_acceleration': {
            'low': {
                'message': 'Smooth acceleration helps improve fuel efficiency.',
                'type': 'tip',
                'suggestions': ['Accelerate gradually', 'Anticipate green lights']
            },
            'medium': {
                'message': 'Rapid acceleration detected. Gradual acceleration is safer and more efficient.',
                'type': 'warning',
                'suggestions': ['Accelerate smoothly', 'Plan ahead for merging']
            },
            'high': {
                'message': 'Very rapid acceleration! This can be dangerous and affects your safety score.',
                'type': 'warning',
                'suggestions': ['Accelerate gradually', 'Check for safe merging opportunities']
            }
        },
        'speeding': {
            'low': {
                'message': 'You\'re slightly over the speed limit. Stay safe!',
                'type': 'tip',
                'suggestions': ['Check speed limit signs', 'Use cruise control on highways']
            },
            'medium': {
                'message': 'Speeding detected. Please observe posted speed limits.',
                'type': 'warning',
                'suggestions': ['Reduce speed immediately', 'Allow extra time for trips']
            },
            'high': {
                'message': 'Significant speeding detected! This greatly increases accident risk.',
                'type': 'warning',
                'suggestions': ['Reduce speed immediately', 'Consider the safety of all road users']
            }
        }
    }

    return messages.get(event_type, {}).get(severity, {
        'message': 'Drive safely and stay alert!',
        'type': 'tip',
        'suggestions': ['Maintain focus on the road']
    })

def calculate_event_risk_impact(event_type, severity):
    """Calculate the impact of a driving event on risk score"""
    impact_values = {
        'harsh_braking': {'low': 0.001, 'medium': 0.003, 'high': 0.005},
        'rapid_acceleration': {'low': 0.001, 'medium': 0.002, 'high': 0.004},
        'speeding': {'low': 0.002, 'medium': 0.004, 'high': 0.008},
        'harsh_cornering': {'low': 0.001, 'medium': 0.002, 'high': 0.003}
    }

    return impact_values.get(event_type, {}).get(severity, 0.001)

def calculate_premium_adjustment(risk_score):
    """Calculate premium adjustment percentage based on risk score"""
    # Simple linear adjustment: 0.0 risk = -20% premium, 1.0 risk = +30% premium
    base_adjustment = -20  # 20% discount for perfect score
    risk_penalty = 50 * risk_score  # Up to 50% penalty for worst score
    return base_adjustment + risk_penalty

