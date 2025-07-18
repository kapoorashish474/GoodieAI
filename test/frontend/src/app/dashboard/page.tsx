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
          setTimeout(() => {
            fetchDashboardData();
            setTimeout(() => setTaskStatus(null), 1500); // Clear status after refresh
          }, 1000);
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
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-24 w-24 border-b-4 border-blue-500 mx-auto mb-6"></div>
          <p className="mt-4 text-xl text-gray-700 font-semibold">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-pink-100">
        <div className="text-center bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-xl">
          <div className="text-red-600 text-2xl font-bold mb-4">Error</div>
          <p className="text-gray-700 mb-4 text-lg">{error}</p>
          <button
            onClick={fetchDashboardData}
            className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-2 rounded-full font-semibold shadow hover:from-blue-600 hover:to-purple-600 transition"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-10 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900 mb-2 tracking-tight drop-shadow-sm">
              🚀 Hacker News Analytics
            </h1>
            <p className="text-lg text-gray-600 font-medium">
              Real-time analytics for AI-related stories and trends
            </p>
          </div>
          <button
            onClick={triggerFetchStories}
            disabled={taskStatus?.includes('Starting') || taskStatus?.includes('PENDING')}
            className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-8 py-3 rounded-full font-bold shadow-lg hover:from-blue-600 hover:to-purple-600 disabled:opacity-50 transition text-lg"
          >
            Fetch Latest Stories
          </button>
        </div>
        {taskStatus && (
          <div className="mb-6 text-center md:text-right text-base text-purple-700 font-medium animate-pulse">
            {taskStatus}
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-10">
          <div className="bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-xl flex flex-col items-center hover:scale-105 transition-transform">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Total Stories</h3>
            <p className="text-4xl font-extrabold text-blue-600 drop-shadow">{dashboardData?.total_stories || 0}</p>
          </div>
          <div className="bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-xl flex flex-col items-center hover:scale-105 transition-transform">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">AI Keywords</h3>
            <p className="text-4xl font-extrabold text-green-500 drop-shadow">{dashboardData?.total_keywords || 0}</p>
          </div>
          <div className="bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-xl flex flex-col items-center hover:scale-105 transition-transform">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Domains</h3>
            <p className="text-4xl font-extrabold text-purple-500 drop-shadow">{dashboardData?.total_domains || 0}</p>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 mb-10">
          {/* Top Keywords Chart */}
          <div className="bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Top AI Keywords</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={dashboardData?.analytics || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="keyword" tick={{ fontSize: 14 }} />
                <YAxis tick={{ fontSize: 14 }} />
                <Tooltip />
                <Bar dataKey="count" fill="#0088FE" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Top Domains Chart */}
          <div className="bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Top Domains</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={dashboardData?.domains || []}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ domain, percent }) => `${domain} ${((percent || 0) * 100).toFixed(0)}%`}
                  outerRadius={90}
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
        <div className="bg-white/80 backdrop-blur-md p-8 rounded-2xl shadow-xl">
          <h3 className="text-2xl font-bold text-gray-800 mb-6">Recent Stories</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {dashboardData?.stories.map((story) => (
              <div key={story.id} className="bg-gradient-to-br from-blue-100 via-purple-100 to-pink-100 rounded-xl p-5 shadow hover:shadow-lg transition flex flex-col h-full">
                <a href={story.url} target="_blank" rel="noopener noreferrer" className="text-lg font-bold text-blue-700 hover:underline mb-2 line-clamp-2">
                  {story.title}
                </a>
                <div className="flex-1"></div>
                <div className="flex items-center justify-between mt-4 text-sm text-gray-600">
                  <span className="font-medium">by {story.author}</span>
                  <span>{new Date(story.time).toLocaleDateString()}</span>
                </div>
                <div className="flex gap-4 mt-2 text-xs text-gray-500">
                  <span>⭐ {story.score}</span>
                  <span>💬 {story.descendants}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
} 