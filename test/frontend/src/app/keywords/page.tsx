'use client';
import { useEffect, useState } from 'react';
import { apiClient, AIKeyword } from '@/lib/api';

export default function KeywordsPage() {
  const [aiKeywords, setAIKeywords] = useState<AIKeyword[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAIKeywords();
  }, []);

  const fetchAIKeywords = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getAIKeywords();
      setAIKeywords(response.data);
      setError(null);
    } catch {
      setError('Failed to fetch AI keywords');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">AI Keywords</h1>
        {loading ? (
          <div className="text-gray-600">Loading keywords...</div>
        ) : error ? (
          <div className="text-red-600">{error}</div>
        ) : (
          <div className="overflow-x-auto rounded-lg shadow bg-white">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Keyword</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {aiKeywords.map((kw) => (
                  <tr key={kw.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{kw.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{kw.keyword}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{kw.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
} 