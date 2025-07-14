'use client';

import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { apiClient, DashboardResponse } from '@/lib/api';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [taskStatus, setTaskStatus] = useState<string | null>(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getDashboard();
      setDashboardData(response.data);
      setError(null);
    } catch {
      setError('Failed to fetch dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const triggerFetchStories = async () => {
    try {
      setTaskStatus('Starting story fetch...');
      const response = await apiClient.triggerFetchStories();
      setTaskStatus(`Task started: ${response.data.task_id}`);
      
      // Poll for task completion
      pollTaskStatus(response.data.task_id);
    } catch {
      setTaskStatus('Failed to start task');
    }
  };

  const pollTaskStatus = async (taskId: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await apiClient.getTaskStatus(taskId);
        setTaskStatus(`${response.data.state}: ${response.data.status}`);
        
        if (response.data.state === 'SUCCESS') {
          setTaskStatus('Task completed! Refreshing data...');
          clearInterval(interval);
          setTimeout(fetchDashboardData, 1000);
        } else if (response.data.state === 'FAILURE') {
          setTaskStatus('Task failed');
          clearInterval(interval);
        }
      } catch {
        setTaskStatus('Failed to check task status');
        clearInterval(interval);
      }
    }, 2000);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 text-xl mb-4">Error</div>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchDashboardData}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Hacker News Analytics Dashboard
          </h1>
          <p className="text-gray-600">
            Real-time analytics for AI-related stories and trends
          </p>
        </div>

        {/* Action Buttons */}
        <div className="mb-6 flex gap-4">
          <button
            onClick={triggerFetchStories}
            disabled={taskStatus?.includes('Starting') || taskStatus?.includes('PENDING')}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            Fetch Latest Stories
          </button>
          {taskStatus && (
            <div className="text-sm text-gray-600 self-center">
              {taskStatus}
            </div>
          )}
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900">Total Stories</h3>
            <p className="text-3xl font-bold text-blue-600">{dashboardData?.total_stories || 0}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900">AI Keywords</h3>
            <p className="text-3xl font-bold text-green-600">{dashboardData?.total_keywords || 0}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-900">Domains</h3>
            <p className="text-3xl font-bold text-purple-600">{dashboardData?.total_domains || 0}</p>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Top Keywords Chart */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Top AI Keywords</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={dashboardData?.analytics || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="keyword" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#0088FE" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Top Domains Chart */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Top Domains</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={dashboardData?.domains || []}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ domain, percent }) => `${domain} ${((percent || 0) * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {(dashboardData?.domains || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Stories */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Recent Stories</h3>
          <div className="space-y-4">
            {dashboardData?.stories.map((story) => (
              <div key={story.id} className="border-b border-gray-200 pb-4 last:border-b-0">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 hover:text-blue-600">
                      <a href={story.url} target="_blank" rel="noopener noreferrer">
                        {story.title}
                      </a>
                    </h4>
                    <div className="text-sm text-gray-500 mt-1">
                      by {story.author} • {new Date(story.time).toLocaleDateString()} • 
                      {story.score} points • {story.descendants} comments
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
} 