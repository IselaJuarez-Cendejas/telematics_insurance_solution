import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  Car,
  TrendingUp,
  TrendingDown,
  MapPin,
  Clock,
  AlertTriangle,
  Shield,
  Award,
  Target,
  BarChart3,
  Zap
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import RealTimeFeedback from './RealTimeFeedback';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedPolicyholder, setSelectedPolicyholder] = useState('PH-demo123');

  // Mock data for demonstration
  const mockData = {
    policyholder: {
      id: 'PH-demo123',
      first_name: 'Jane',
      last_name: 'Doe',
      vehicle_make: 'Toyota',
      vehicle_model: 'Camry',
      vehicle_year: 2020,
      risk_score_current: 0.25,
      total_mileage_ytd: 8500,
      avg_daily_trips: 2.3,
      avg_harsh_events_per_100km: 2.1,
      night_driving_percentage: 12.5,
      peak_hour_driving_percentage: 28.0
    },
    recent_trips: [
      {
        id: '1',
        start_location_name: 'Home',
        end_location_name: 'Work',
        distance_km: 15.2,
        duration_seconds: 1800,
        avg_speed_kph: 45,
        harsh_braking_count: 1,
        rapid_acceleration_count: 0,
        start_timestamp: '2025-09-11T08:30:00Z'
      },
      {
        id: '2',
        start_location_name: 'Work',
        end_location_name: 'Grocery Store',
        distance_km: 8.5,
        duration_seconds: 900,
        avg_speed_kph: 35,
        harsh_braking_count: 0,
        rapid_acceleration_count: 1,
        start_timestamp: '2025-09-11T17:45:00Z'
      }
    ],
    risk_history: [
      { score_date: '2025-09-01', risk_score: 0.30, premium_adjustment: -15 },
      { score_date: '2025-08-01', risk_score: 0.28, premium_adjustment: -16 },
      { score_date: '2025-07-01', risk_score: 0.32, premium_adjustment: -14 },
      { score_date: '2025-06-01', risk_score: 0.35, premium_adjustment: -12 },
      { score_date: '2025-05-01', risk_score: 0.40, premium_adjustment: -8 },
      { score_date: '2025-04-01', risk_score: 0.38, premium_adjustment: -10 }
    ],
    summary: {
      total_trips: 45,
      total_distance_km: 8500,
      current_risk_score: 0.25,
      premium_adjustment: -18
    }
  };

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setDashboardData(mockData);
      setLoading(false);
    }, 1000);
  }, []);

  const getRiskLevel = (score) => {
    if (score <= 0.3) return { level: 'Low', color: 'bg-green-500', textColor: 'text-green-700' };
    if (score <= 0.6) return { level: 'Medium', color: 'bg-yellow-500', textColor: 'text-yellow-700' };
    return { level: 'High', color: 'bg-red-500', textColor: 'text-red-700' };
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const { policyholder, recent_trips, risk_history, summary } = dashboardData;
  const riskInfo = getRiskLevel(policyholder.risk_score_current);

  // Chart data
  const riskTrendData = risk_history.map(item => ({
    date: formatDate(item.score_date),
    score: (item.risk_score * 100).toFixed(1),
    adjustment: item.premium_adjustment
  })).reverse();

  const drivingPatternData = [
    { name: 'Day Driving', value: 100 - policyholder.night_driving_percentage, color: '#3b82f6' },
    { name: 'Night Driving', value: policyholder.night_driving_percentage, color: '#1e40af' }
  ];

  const trafficPatternData = [
    { name: 'Off-Peak', value: 100 - policyholder.peak_hour_driving_percentage, color: '#10b981' },
    { name: 'Peak Hours', value: policyholder.peak_hour_driving_percentage, color: '#059669' }
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Welcome back, {policyholder.first_name}!
              </h1>
              <p className="text-gray-600 mt-2">
                {policyholder.vehicle_year} {policyholder.vehicle_make} {policyholder.vehicle_model}
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="text-lg px-4 py-2">
                <Car className="w-4 h-4 mr-2" />
                {summary.total_trips} trips this month
              </Badge>
            </div>
          </div>
        </div>

        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-blue-700">Risk Score</CardTitle>
              <Shield className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-900">
                {(policyholder.risk_score_current * 100).toFixed(0)}/100
              </div>
              <div className="flex items-center mt-2">
                <Badge className={`${riskInfo.color} text-white`}>
                  {riskInfo.level} Risk
                </Badge>
              </div>
              <Progress
                value={100 - (policyholder.risk_score_current * 100)}
                className="mt-3"
              />
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-green-700">Premium Savings</CardTitle>
              <TrendingDown className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-900">
                {Math.abs(summary.premium_adjustment)}%
              </div>
              <p className="text-xs text-green-600 mt-2">
                Monthly discount applied
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-purple-700">Miles Driven</CardTitle>
              <MapPin className="h-4 w-4 text-purple-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-900">
                {summary.total_distance_km.toLocaleString()} km
              </div>
              <p className="text-xs text-purple-600 mt-2">
                This year
              </p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-orange-700">Safety Events</CardTitle>
              <AlertTriangle className="h-4 w-4 text-orange-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-900">
                {policyholder.avg_harsh_events_per_100km.toFixed(1)}
              </div>
              <p className="text-xs text-orange-600 mt-2">
                Per 100km driven
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="trips">Recent Trips</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="rewards">Rewards</TabsTrigger>
            <TabsTrigger value="feedback">Live Feedback</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Risk Score Trend */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <TrendingUp className="w-5 h-5 mr-2" />
                    Risk Score Trend
                  </CardTitle>
                  <CardDescription>
                    Your driving performance over the last 6 months
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={riskTrendData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Line
                        type="monotone"
                        dataKey="score"
                        stroke="#3b82f6"
                        strokeWidth={3}
                        dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              {/* Driving Patterns */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Clock className="w-5 h-5 mr-2" />
                    Driving Patterns
                  </CardTitle>
                  <CardDescription>
                    When you drive most often
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span>Day vs Night Driving</span>
                        <span>{policyholder.night_driving_percentage.toFixed(1)}% night</span>
                      </div>
                      <ResponsiveContainer width="100%" height={150}>
                        <PieChart>
                          <Pie
                            data={drivingPatternData}
                            cx="50%"
                            cy="50%"
                            innerRadius={40}
                            outerRadius={60}
                            dataKey="value"
                          >
                            {drivingPatternData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>

                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span>Peak Hour Driving</span>
                        <span>{policyholder.peak_hour_driving_percentage.toFixed(1)}% peak hours</span>
                      </div>
                      <Progress value={policyholder.peak_hour_driving_percentage} className="h-3" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="trips" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Recent Trips</CardTitle>
                <CardDescription>
                  Your latest driving activities
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recent_trips.map((trip) => (
                    <div key={trip.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors">
                      <div className="flex items-center space-x-4">
                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <MapPin className="w-5 h-5 text-blue-600" />
                        </div>
                        <div>
                          <div className="font-medium">
                            {trip.start_location_name} → {trip.end_location_name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {formatDate(trip.start_timestamp)} at {formatTime(trip.start_timestamp)}
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-medium">{trip.distance_km} km</div>
                        <div className="text-sm text-gray-500">
                          {Math.round(trip.duration_seconds / 60)} min
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        {trip.harsh_braking_count > 0 && (
                          <Badge variant="destructive" className="text-xs">
                            {trip.harsh_braking_count} harsh brake
                          </Badge>
                        )}
                        {trip.rapid_acceleration_count > 0 && (
                          <Badge variant="secondary" className="text-xs">
                            {trip.rapid_acceleration_count} rapid accel
                          </Badge>
                        )}
                        {trip.harsh_braking_count === 0 && trip.rapid_acceleration_count === 0 && (
                          <Badge variant="outline" className="text-xs text-green-600">
                            Smooth trip
                          </Badge>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Premium Adjustments</CardTitle>
                  <CardDescription>
                    How your driving affects your insurance costs
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={riskTrendData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="adjustment" fill="#10b981" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Driving Statistics</CardTitle>
                  <CardDescription>
                    Your driving behavior breakdown
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center p-4 bg-blue-50 rounded-lg">
                        <div className="text-2xl font-bold text-blue-900">
                          {policyholder.avg_daily_trips.toFixed(1)}
                        </div>
                        <div className="text-sm text-blue-600">Avg Daily Trips</div>
                      </div>
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-900">
                          {(summary.total_distance_km / summary.total_trips).toFixed(1)}
                        </div>
                        <div className="text-sm text-green-600">Avg Trip Distance (km)</div>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm">Night Driving</span>
                        <span className="text-sm font-medium">{policyholder.night_driving_percentage.toFixed(1)}%</span>
                      </div>
                      <Progress value={policyholder.night_driving_percentage} className="h-2" />

                      <div className="flex justify-between items-center">
                        <span className="text-sm">Peak Hour Driving</span>
                        <span className="text-sm font-medium">{policyholder.peak_hour_driving_percentage.toFixed(1)}%</span>
                      </div>
                      <Progress value={policyholder.peak_hour_driving_percentage} className="h-2" />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="rewards" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Award className="w-5 h-5 mr-2" />
                    Your Achievements
                  </CardTitle>
                  <CardDescription>
                    Badges earned through safe driving
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-4 bg-yellow-50 border-2 border-yellow-200 rounded-lg">
                      <Award className="w-8 h-8 text-yellow-600 mx-auto mb-2" />
                      <div className="font-medium text-yellow-800">Safe Driver</div>
                      <div className="text-xs text-yellow-600">Low risk score for 3 months</div>
                    </div>
                    <div className="text-center p-4 bg-green-50 border-2 border-green-200 rounded-lg">
                      <Target className="w-8 h-8 text-green-600 mx-auto mb-2" />
                      <div className="font-medium text-green-800">Smooth Operator</div>
                      <div className="text-xs text-green-600">Minimal harsh events</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Current Challenges</CardTitle>
                  <CardDescription>
                    Complete these to earn more rewards
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-4 border rounded-lg">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">Week Without Harsh Events</span>
                        <span className="text-sm text-gray-500">5/7 days</span>
                      </div>
                      <Progress value={71} className="h-2" />
                      <div className="text-xs text-gray-500 mt-1">2 more days to complete</div>
                    </div>

                    <div className="p-4 border rounded-lg">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">Reduce Night Driving</span>
                        <span className="text-sm text-gray-500">12.5%</span>
                      </div>
                      <Progress value={25} className="h-2" />
                      <div className="text-xs text-gray-500 mt-1">Target: Under 10%</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="feedback" className="space-y-6">
            <RealTimeFeedback policyholderId={selectedPolicyholder} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Dashboard;