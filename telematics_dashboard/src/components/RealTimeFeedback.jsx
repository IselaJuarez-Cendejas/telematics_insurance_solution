import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  AlertTriangle,
  CheckCircle,
  Info,
  Zap,
  TrendingUp,
  TrendingDown,
  Clock,
  MapPin
} from 'lucide-react';

const RealTimeFeedback = ({ policyholderId }) => {
  const [feedbackHistory, setFeedbackHistory] = useState([]);
  const [currentScore, setCurrentScore] = useState(75);
  const [isSimulating, setIsSimulating] = useState(false);

  // Mock real-time events for demonstration
  const mockEvents = [
    {
      type: 'harsh_braking',
      severity: 'medium',
      location: 'Main St & 5th Ave',
      message: 'Harsh braking detected. Consider increasing your following distance.',
      suggestions: ['Maintain 3-second following rule', 'Scan ahead for potential hazards'],
      impact: -2
    },
    {
      type: 'smooth_driving',
      severity: 'low',
      location: 'Highway 101',
      message: 'Great job! Smooth driving detected.',
      suggestions: ['Keep up the excellent driving'],
      impact: +1
    },
    {
      type: 'rapid_acceleration',
      severity: 'low',
      location: 'Oak Street',
      message: 'Gentle reminder: Gradual acceleration helps improve fuel efficiency.',
      suggestions: ['Accelerate gradually', 'Anticipate green lights'],
      impact: -1
    },
    {
      type: 'speeding',
      severity: 'medium',
      location: 'Residential Area',
      message: 'Speeding detected. Please observe posted speed limits.',
      suggestions: ['Reduce speed immediately', 'Allow extra time for trips'],
      impact: -3
    }
  ];

  const simulateRealTimeEvent = () => {
    const randomEvent = mockEvents[Math.floor(Math.random() * mockEvents.length)];
    const timestamp = new Date().toLocaleTimeString();

    const newFeedback = {
      id: Date.now(),
      ...randomEvent,
      timestamp,
      read: false
    };

    setFeedbackHistory(prev => [newFeedback, ...prev.slice(0, 9)]); // Keep last 10 events
    setCurrentScore(prev => Math.max(0, Math.min(100, prev + randomEvent.impact)));
  };

  const startSimulation = () => {
    setIsSimulating(true);
    const interval = setInterval(() => {
      simulateRealTimeEvent();
    }, 3000); // New event every 3 seconds

    // Stop after 30 seconds
    setTimeout(() => {
      clearInterval(interval);
      setIsSimulating(false);
    }, 30000);
  };

  const markAsRead = (id) => {
    setFeedbackHistory(prev =>
      prev.map(item =>
        item.id === id ? { ...item, read: true } : item
      )
    );
  };

  const getFeedbackIcon = (type, severity) => {
    if (type === 'smooth_driving') return <CheckCircle className="w-5 h-5 text-green-500" />;
    if (severity === 'high') return <AlertTriangle className="w-5 h-5 text-red-500" />;
    if (severity === 'medium') return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
    return <Info className="w-5 h-5 text-blue-500" />;
  };

  const getFeedbackColor = (type, severity) => {
    if (type === 'smooth_driving') return 'border-green-200 bg-green-50';
    if (severity === 'high') return 'border-red-200 bg-red-50';
    if (severity === 'medium') return 'border-yellow-200 bg-yellow-50';
    return 'border-blue-200 bg-blue-50';
  };

  const unreadCount = feedbackHistory.filter(item => !item.read).length;

  return (
    <div className="space-y-6">
      {/* Real-time Score */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span className="flex items-center">
              <Zap className="w-5 h-5 mr-2" />
              Real-time Driving Score
            </span>
            <div className="flex items-center space-x-2">
              <Badge variant={currentScore >= 80 ? "default" : currentScore >= 60 ? "secondary" : "destructive"}>
                {currentScore}/100
              </Badge>
              {currentScore >= 80 ? (
                <TrendingUp className="w-4 h-4 text-green-500" />
              ) : (
                <TrendingDown className="w-4 h-4 text-red-500" />
              )}
            </div>
          </CardTitle>
          <CardDescription>
            Your current trip performance score
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
            <div
              className={`h-3 rounded-full transition-all duration-500 ${
                currentScore >= 80 ? 'bg-green-500' :
                currentScore >= 60 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${currentScore}%` }}
            ></div>
          </div>

          <div className="flex justify-between items-center">
            <Button
              onClick={startSimulation}
              disabled={isSimulating}
              variant={isSimulating ? "secondary" : "default"}
            >
              {isSimulating ? 'Simulating...' : 'Start Driving Simulation'}
            </Button>

            {unreadCount > 0 && (
              <Badge variant="destructive">
                {unreadCount} new alert{unreadCount > 1 ? 's' : ''}
              </Badge>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Live Feedback Feed */}
      <Card>
        <CardHeader>
          <CardTitle>Live Feedback</CardTitle>
          <CardDescription>
            Real-time driving events and suggestions
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {feedbackHistory.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Info className="w-8 h-8 mx-auto mb-2" />
                <p>No recent driving events</p>
                <p className="text-sm">Start the simulation to see real-time feedback</p>
              </div>
            ) : (
              feedbackHistory.map((feedback) => (
                <div
                  key={feedback.id}
                  className={`p-4 rounded-lg border-2 transition-all duration-300 ${
                    getFeedbackColor(feedback.type, feedback.severity)
                  } ${!feedback.read ? 'ring-2 ring-blue-200' : ''}`}
                  onClick={() => markAsRead(feedback.id)}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3">
                      {getFeedbackIcon(feedback.type, feedback.severity)}
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="font-medium text-sm">
                            {feedback.message}
                          </span>
                          {!feedback.read && (
                            <Badge variant="secondary" className="text-xs">New</Badge>
                          )}
                        </div>

                        <div className="flex items-center text-xs text-gray-500 mb-2">
                          <Clock className="w-3 h-3 mr-1" />
                          {feedback.timestamp}
                          <MapPin className="w-3 h-3 ml-3 mr-1" />
                          {feedback.location}
                        </div>

                        {feedback.suggestions && feedback.suggestions.length > 0 && (
                          <div className="mt-2">
                            <p className="text-xs font-medium text-gray-600 mb-1">Suggestions:</p>
                            <ul className="text-xs text-gray-600 space-y-1">
                              {feedback.suggestions.map((suggestion, index) => (
                                <li key={index} className="flex items-center">
                                  <span className="w-1 h-1 bg-gray-400 rounded-full mr-2"></span>
                                  {suggestion}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="text-right">
                      <Badge
                        variant={feedback.impact > 0 ? "default" : "destructive"}
                        className="text-xs"
                      >
                        {feedback.impact > 0 ? '+' : ''}{feedback.impact}
                      </Badge>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* Driving Tips */}
      <Card>
        <CardHeader>
          <CardTitle>Smart Driving Tips</CardTitle>
          <CardDescription>
            Personalized recommendations based on your driving patterns
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <Alert>
              <Info className="h-4 w-4" />
              <AlertDescription>
                <strong>Tip:</strong> Maintain a 3-second following distance to reduce harsh braking events.
              </AlertDescription>
            </Alert>

            <Alert>
              <CheckCircle className="h-4 w-4" />
              <AlertDescription>
                <strong>Great job!</strong> Your smooth acceleration technique is improving fuel efficiency.
              </AlertDescription>
            </Alert>

            <Alert>
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>
                <strong>Watch out:</strong> You tend to brake harder in residential areas. Try anticipating stops earlier.
              </AlertDescription>
            </Alert>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default RealTimeFeedback;

