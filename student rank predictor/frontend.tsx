import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Alert, AlertDescription } from '@/components/ui/alert';

const Dashboard = () => {
  const [performanceData, setPerformanceData] = useState({
    topic_performance: {
      'Physics': 75,
      'Chemistry': 82,
      'Biology': 68
    },
    improvement_trends: {
      trend: 'improving',
      rate: 2.5,
      recent_scores: [65, 68, 72, 75, 78]
    },
    weak_areas: ['Thermodynamics', 'Organic Chemistry']
  });

  const [predictedRank, setPredictedRank] = useState({
    predicted_rank: 1500,
    confidence: 0.85
  });

  const scoreData = performanceData.improvement_trends.recent_scores.map((score, index) => ({
    quiz: `Quiz ${index + 1}`,
    score: score
  }));

  return (
    <div className="p-6 space-y-6 max-w-6xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Performance Overview */}
        <Card>
          <CardHeader>
            <CardTitle>Quiz Performance Trends</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={scoreData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="quiz" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="score" stroke="#2563eb" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Topic Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Subject-wise Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(performanceData.topic_performance).map(([subject, score]) => (
                <div key={subject} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>{subject}</span>
                    <span>{score}%</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full">
                    <div
                      className="h-full bg-blue-600 rounded-full"
                      style={{ width: `${score}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Rank Prediction */}
        <Card>
          <CardHeader>
            <CardTitle>Predicted NEET Rank</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600">
                {predictedRank.predicted_rank.toLocaleString()}
              </div>
              <div className="text-sm text-gray-500 mt-2">
                Confidence: {(predictedRank.confidence * 100).toFixed(1)}%
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Areas for Improvement */}
        <Card>
          <CardHeader>
            <CardTitle>Areas for Improvement</CardTitle>
          </CardHeader>
          <CardContent>
            <Alert>
              <AlertDescription>
                <div className="space-y-2">
                  <p className="font-medium">Focus on these topics:</p>
                  <ul className="list-disc pl-4">
                    {performanceData.weak_areas.map((area) => (
                      <li key={area}>{area}</li>
                    ))}
                  </ul>
                </div>
              </AlertDescription>
            </Alert>
            <div className="mt-4">
              <p className="text-sm text-gray-600">
                Your performance is {performanceData.improvement_trends.trend} at a rate of{' '}
                {performanceData.improvement_trends.rate.toFixed(1)}% per quiz
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
