# Telematics Insurance API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API uses basic authentication. In production, implement JWT tokens or OAuth 2.0.

## Response Format
All API responses follow this standard format:

```json
{
  "success": true,
  "data": {},
  "message": "Success message",
  "timestamp": "2025-09-11T22:55:00Z"
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error description",
  "code": "ERROR_CODE",
  "timestamp": "2025-09-11T22:55:00Z"
}
```

## Endpoints

### User Management

#### Create Policyholder
```http
POST /api/policyholders
```

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "date_of_birth": "1985-06-15",
  "gender": "Female",
  "address": "123 Main Street, City, State 12345",
  "vehicle_make": "Toyota",
  "vehicle_model": "Camry",
  "vehicle_year": 2020,
  "driving_history_score": 850
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "pol_1234567890",
    "first_name": "Jane",
    "last_name": "Doe",
    "risk_score_current": 0.5,
    "created_at": "2025-09-11T22:55:00Z"
  }
}
```

#### Get Policyholder
```http
GET /api/policyholders/{id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "pol_1234567890",
    "first_name": "Jane",
    "last_name": "Doe",
    "vehicle_make": "Toyota",
    "vehicle_model": "Camry",
    "vehicle_year": 2020,
    "risk_score_current": 0.25,
    "total_mileage_ytd": 8500.0,
    "avg_harsh_events_per_100km": 2.1,
    "night_driving_percentage": 12.5,
    "peak_hour_driving_percentage": 28.0
  }
}
```

### Data Ingestion

#### Ingest Raw Telematics Data
```http
POST /api/raw-data
```

**Request Body:**
```json
[
  {
    "device_id": "DEVICE-123456",
    "policyholder_id": "pol_1234567890",
    "timestamp": "2025-09-11T08:30:00Z",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "speed_kph": 45,
    "acceleration_x": 0.1,
    "acceleration_y": -0.05,
    "acceleration_z": 1.02,
    "heading_degrees": 180,
    "event_type": "normal"
  }
]
```

**Response:**
```json
{
  "success": true,
  "data": {
    "ingested_count": 1,
    "processed_at": "2025-09-11T22:55:00Z"
  }
}
```

#### Process Trip Data
```http
POST /api/process-trip
```

**Request Body:**
```json
{
  "policyholder_id": "pol_1234567890",
  "raw_points": [
    {
      "timestamp": "2025-09-11T08:30:00Z",
      "latitude": 37.7749,
      "longitude": -122.4194,
      "speed_kph": 45,
      "acceleration_x": 0.1,
      "acceleration_y": -0.05,
      "acceleration_z": 1.02,
      "heading_degrees": 180,
      "event_type": "normal"
    }
  ],
  "start_location_name": "Home",
  "end_location_name": "Work",
  "weather_conditions": "clear",
  "traffic_conditions": "moderate"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "trip_id": "trip_1234567890",
    "distance_km": 15.2,
    "duration_minutes": 25,
    "avg_speed_kph": 36.5,
    "max_speed_kph": 65,
    "harsh_braking_count": 1,
    "rapid_acceleration_count": 0,
    "harsh_cornering_count": 0,
    "speeding_duration_minutes": 2.5,
    "risk_score": 0.23
  }
}
```

### Risk Assessment

#### Calculate Risk Score
```http
POST /api/risk-score/{policyholder_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "risk_score": 0.25,
    "risk_level": "low",
    "premium_adjustment": -18.0,
    "factors": {
      "harsh_events_score": 0.15,
      "speed_score": 0.20,
      "time_score": 0.35,
      "mileage_score": 0.30
    },
    "recommendations": [
      "Continue maintaining excellent driving habits",
      "Consider reducing night driving for additional savings"
    ]
  }
}
```

#### Get Dashboard Data
```http
GET /api/dashboard/{policyholder_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "current_risk_score": 0.25,
      "premium_adjustment": -18.0,
      "total_trips": 45,
      "total_distance_km": 1250.5,
      "avg_daily_trips": 2.3
    },
    "recent_trips": [
      {
        "id": "trip_1234567890",
        "start_time": "2025-09-11T08:30:00Z",
        "end_time": "2025-09-11T08:55:00Z",
        "distance_km": 15.2,
        "risk_score": 0.23,
        "start_location": "Home",
        "end_location": "Work"
      }
    ],
    "risk_trend": [
      {"date": "2025-09-01", "score": 0.30},
      {"date": "2025-09-11", "score": 0.25}
    ]
  }
}
```

### Gamification

#### Get Achievements
```http
GET /api/achievements/{policyholder_id}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "safe_driver",
      "name": "Safe Driver",
      "description": "Low risk score for 3 months",
      "icon": "award",
      "color": "yellow",
      "earned_date": "2025-09-11T22:55:00Z"
    },
    {
      "id": "smooth_operator",
      "name": "Smooth Operator",
      "description": "Minimal harsh events",
      "icon": "target",
      "color": "green",
      "earned_date": "2025-09-10T15:30:00Z"
    }
  ]
}
```

#### Get Challenges
```http
GET /api/challenges/{policyholder_id}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "week_without_harsh_events",
      "name": "Week Without Harsh Events",
      "description": "Complete 7 days without any harsh braking or acceleration",
      "duration_days": 7,
      "reward_points": 100,
      "progress": {
        "current": 5,
        "target": 7,
        "percentage": 71.4,
        "description": "5/7 days completed"
      },
      "is_completed": false
    }
  ]
}
```

#### Get Leaderboard
```http
GET /api/leaderboard
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "rank": 1,
      "name": "Jane D.",
      "risk_score": 0.15,
      "total_points": 1450,
      "vehicle": "Toyota Camry",
      "premium_savings": 22.5
    },
    {
      "rank": 2,
      "name": "John S.",
      "risk_score": 0.18,
      "total_points": 1380,
      "vehicle": "Honda Civic",
      "premium_savings": 20.0
    }
  ]
}
```

#### Real-time Feedback
```http
POST /api/real-time-feedback
```

**Request Body:**
```json
{
  "event_type": "harsh_braking",
  "severity": "medium",
  "policyholder_id": "pol_1234567890",
  "location": {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "address": "Main St & 5th Ave"
  },
  "timestamp": "2025-09-11T08:35:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "feedback_message": "Harsh braking detected. Consider increasing your following distance.",
    "feedback_type": "warning",
    "risk_impact": -0.003,
    "suggestions": [
      "Maintain 3-second following rule",
      "Scan ahead for potential hazards"
    ],
    "timestamp": "2025-09-11T08:35:00Z"
  }
}
```

### External Data Integration

#### Get Current Weather
```http
GET /api/weather/current?lat=37.7749&lon=-122.4194
```

**Response:**
```json
{
  "success": true,
  "data": {
    "location": {
      "lat": 37.7749,
      "lon": -122.4194,
      "name": "San Francisco, CA"
    },
    "current": {
      "temperature": 22.5,
      "feels_like": 24.1,
      "humidity": 65,
      "pressure": 1013,
      "visibility": 10000,
      "wind_speed": 3.2,
      "wind_direction": 180,
      "weather_main": "Clear",
      "weather_description": "clear sky",
      "clouds": 5,
      "uv_index": 6.8
    },
    "conditions": {
      "is_raining": false,
      "is_snowing": false,
      "is_foggy": false,
      "visibility_km": 10,
      "road_conditions": "dry",
      "driving_risk_level": "low"
    }
  }
}
```

#### Get Traffic Conditions
```http
GET /api/traffic/current?origin_lat=37.7749&origin_lon=-122.4194&dest_lat=37.7849&dest_lon=-122.4094
```

**Response:**
```json
{
  "success": true,
  "data": {
    "route": {
      "origin": {"lat": 37.7749, "lon": -122.4194},
      "destination": {"lat": 37.7849, "lon": -122.4094},
      "distance_km": 15.2,
      "duration_normal_minutes": 18,
      "duration_current_minutes": 25
    },
    "traffic_conditions": {
      "overall_level": "moderate",
      "congestion_level": 0.6,
      "incidents_count": 1,
      "average_speed_kph": 35,
      "expected_speed_kph": 50
    },
    "incidents": [
      {
        "type": "construction",
        "severity": "medium",
        "description": "Lane closure due to road work",
        "lat": 37.7799,
        "lon": 122.4144,
        "estimated_delay_minutes": 7
      }
    ]
  }
}
```

#### Calculate Contextual Risk
```http
POST /api/contextual-risk
```

**Request Body:**
```json
{
  "lat": 37.7749,
  "lon": -122.4194,
  "time_of_day": "08:30",
  "day_of_week": "Monday",
  "weather_conditions": "clear"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "location": {"lat": 37.7749, "lon": -122.4194},
    "contextual_risk_score": 0.45,
    "risk_level": "medium",
    "risk_factors": {
      "weather_risk": 0.1,
      "time_risk": 0.6,
      "location_risk": 0.5,
      "traffic_risk": 0.6
    },
    "recommendations": [
      {
        "category": "time",
        "message": "High-risk time period. Exercise extra caution and avoid unnecessary trips.",
        "priority": "medium"
      },
      {
        "category": "traffic",
        "message": "Heavy traffic conditions. Allow extra time and maintain safe distances.",
        "priority": "low"
      }
    ]
  }
}
```

### Data Analytics

#### Get Trip Analysis
```http
GET /api/trip-analysis/{trip_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "trip_id": "trip_1234567890",
    "summary": {
      "distance_km": 15.2,
      "duration_minutes": 25,
      "avg_speed_kph": 36.5,
      "risk_score": 0.23
    },
    "events": [
      {
        "type": "harsh_braking",
        "timestamp": "2025-09-11T08:35:00Z",
        "severity": "medium",
        "location": {"lat": 37.7749, "lon": -122.4194},
        "impact": -0.003
      }
    ],
    "route_analysis": {
      "high_risk_segments": [
        {
          "start_lat": 37.7749,
          "start_lon": -122.4194,
          "end_lat": 37.7799,
          "end_lon": -122.4144,
          "risk_level": "medium",
          "reason": "Construction zone"
        }
      ]
    },
    "recommendations": [
      "Consider alternative route to avoid construction",
      "Increase following distance in heavy traffic areas"
    ]
  }
}
```

#### Update Aggregates
```http
POST /api/update-aggregates/{policyholder_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "updated_fields": [
      "total_mileage_ytd",
      "avg_harsh_events_per_100km",
      "night_driving_percentage",
      "peak_hour_driving_percentage"
    ],
    "new_risk_score": 0.25,
    "updated_at": "2025-09-11T22:55:00Z"
  }
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_REQUEST` | Request body is malformed or missing required fields |
| `POLICYHOLDER_NOT_FOUND` | Policyholder ID does not exist |
| `TRIP_NOT_FOUND` | Trip ID does not exist |
| `INVALID_COORDINATES` | Latitude or longitude values are invalid |
| `EXTERNAL_API_ERROR` | External service (weather, traffic) is unavailable |
| `DATABASE_ERROR` | Database operation failed |
| `RATE_LIMIT_EXCEEDED` | Too many requests in a short time period |
| `UNAUTHORIZED` | Authentication required or invalid |
| `FORBIDDEN` | Insufficient permissions |
| `INTERNAL_ERROR` | Unexpected server error |

## Rate Limiting

- **Data Ingestion**: 1000 requests per minute per device
- **Dashboard APIs**: 100 requests per minute per user
- **Real-time Feedback**: 500 requests per minute per user
- **External Data APIs**: 50 requests per minute per user

## Webhooks

### Trip Completed
Triggered when a trip is processed and analyzed.

```json
{
  "event": "trip.completed",
  "data": {
    "trip_id": "trip_1234567890",
    "policyholder_id": "pol_1234567890",
    "risk_score": 0.23,
    "distance_km": 15.2,
    "duration_minutes": 25
  },
  "timestamp": "2025-09-11T22:55:00Z"
}
```

### Risk Score Updated
Triggered when a policyholder's risk score changes significantly.

```json
{
  "event": "risk_score.updated",
  "data": {
    "policyholder_id": "pol_1234567890",
    "old_score": 0.30,
    "new_score": 0.25,
    "change": -0.05,
    "premium_impact": 2.5
  },
  "timestamp": "2025-09-11T22:55:00Z"
}
```

### Achievement Earned
Triggered when a policyholder earns a new achievement.

```json
{
  "event": "achievement.earned",
  "data": {
    "policyholder_id": "pol_1234567890",
    "achievement_id": "safe_driver",
    "achievement_name": "Safe Driver",
    "points_earned": 100
  },
  "timestamp": "2025-09-11T22:55:00Z"
}
```

## SDK Examples

### Python SDK
```python
import requests

class TelematicsAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def create_policyholder(self, data):
        response = requests.post(
            f'{self.base_url}/policyholders',
            json=data,
            headers=self.headers
        )
        return response.json()
    
    def ingest_data(self, data_points):
        response = requests.post(
            f'{self.base_url}/raw-data',
            json=data_points,
            headers=self.headers
        )
        return response.json()
    
    def get_dashboard(self, policyholder_id):
        response = requests.get(
            f'{self.base_url}/dashboard/{policyholder_id}',
            headers=self.headers
        )
        return response.json()

# Usage
api = TelematicsAPI('https://localhost:5000', 'your-api-key')
dashboard = api.get_dashboard('pol_1234567890')
```

### JavaScript SDK
```javascript
class TelematicsAPI {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }
    
    async createPolicyholder(data) {
        const response = await fetch(`${this.baseUrl}/policyholders`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(data)
        });
        return response.json();
    }
    
    async ingestData(dataPoints) {
        const response = await fetch(`${this.baseUrl}/raw-data`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(dataPoints)
        });
        return response.json();
    }
    
    async getDashboard(policyholderId) {
        const response = await fetch(`${this.baseUrl}/dashboard/${policyholderId}`, {
            headers: this.headers
        });
        return response.json();
    }
}

// Usage
const api = new TelematicsAPI('https:///api', 'your-api-key');
const dashboard = await api.getDashboard('pol_1234567890');
```

## Testing

### Postman Collection
A comprehensive Postman collection is available with pre-configured requests for all endpoints. Import the collection to test the API:

```json
{
  "info": {
    "name": "Telematics Insurance API",
    "description": "Complete API collection for telematics insurance system"
  },
  "variable": [
    {
      "key": "base_url",
    }
  ]
}
```

### Test Data
Sample test data is available for:
- Policyholder creation
- Trip data simulation
- Real-time event testing
- Dashboard data validation

This API documentation provides comprehensive coverage of all available endpoints, request/response formats, and integration examples for the telematics insurance system.