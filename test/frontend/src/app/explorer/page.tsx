'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  flexRender,
  createColumnHelper,
} from '@tanstack/react-table';
import { apiClient, Story } from '@/lib/api';

const columnHelper = createColumnHelper<Story>();

const columns = [
  columnHelper.accessor('title', {
    header: 'Title',
    cell: ({ row }) => (
      <a
        href={row.original.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:text-blue-800 font-medium"
      >
        {row.original.title}
      </a>
    ),
  }),
  columnHelper.accessor('author', {
    header: 'Author',
    cell: ({ getValue }) => (
      <span className="text-black font-medium">{getValue() || 'Unknown'}</span>
    ),
  }),
  columnHelper.accessor('score', {
    header: 'Score',
    cell: ({ getValue }) => (
      <span className="text-black font-bold">{getValue()}</span>
    ),
  }),
  columnHelper.accessor('descendants', {
    header: 'Comments',
    cell: ({ getValue }) => (
      <span className="text-black">{getValue()}</span>
    ),
  }),
  columnHelper.accessor('time', {
    header: 'Date',
    cell: ({ getValue }) => (
      <span className="text-black">{new Date(getValue()).toLocaleDateString()}</span>
    ),
  }),
];

export default function Explorer() {
  const [stories, setStories] = useState<Story[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [keyword, setKeyword] = useState('');
  const [domain, setDomain] = useState('');
  const [totalStories, setTotalStories] = useState(0);
  const [currentPage, setCurrentPage] = useState(0);
  const [pageSize, setPageSize] = useState(20);
  const [debouncedKeyword, setDebouncedKeyword] = useState('');
  const [debouncedDomain, setDebouncedDomain] = useState('');
  const keywordInputRef = useRef<HTMLInputElement>(null);
  const domainInputRef = useRef<HTMLInputElement>(null);

  const table = useReactTable({
    data: stories,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    state: {
      pagination: {
        pageIndex: currentPage,
        pageSize: pageSize,
      },
    },
    onPaginationChange: (updater) => {
      if (typeof updater === 'function') {
        const newState = updater({
          pageIndex: currentPage,
          pageSize: pageSize,
        });
        setCurrentPage(newState.pageIndex);
        setPageSize(newState.pageSize);
      }
    },
  });

  const fetchStories = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiClient.getStories({
        skip: currentPage * pageSize,
        limit: pageSize,
        keyword: debouncedKeyword || undefined,
        domain: debouncedDomain || undefined,
      });
      setStories(response.data.stories);
      setTotalStories(response.data.total);
      setError(null);
    } catch (err) {
      setError('Failed to fetch stories');
      console.error('Stories fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, [currentPage, pageSize, debouncedKeyword, debouncedDomain]);

  // Debounce keyword and domain changes
  useEffect(() => {
    const keywordTimer = setTimeout(() => {
      setDebouncedKeyword(keyword);
    }, 500);

    return () => clearTimeout(keywordTimer);
  }, [keyword]);

  useEffect(() => {
    const domainTimer = setTimeout(() => {
      setDebouncedDomain(domain);
    }, 500);

    return () => clearTimeout(domainTimer);
  }, [domain]);

  useEffect(() => {
    fetchStories();
  }, [fetchStories]);

  const handleSearch = () => {
    setCurrentPage(0);
    setDebouncedKeyword(keyword);
    setDebouncedDomain(domain);
  };

  const handleClear = () => {
    setKeyword('');
    setDomain('');
    setDebouncedKeyword('');
    setDebouncedDomain('');
    setCurrentPage(0);
    // Restore focus to keyword input after clearing
    setTimeout(() => {
      keywordInputRef.current?.focus();
    }, 0);
  };

  if (loading && stories.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading stories...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Story Explorer</h1>
          <p className="text-gray-600">
            Search and filter through all Hacker News stories
          </p>
        </div>

        {/* Search Filters */}
        <div className="bg-white p-6 rounded-lg shadow mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Keyword Search
              </label>
              <input
                ref={keywordInputRef}
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="Search in titles..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black placeholder-gray-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Domain Filter
              </label>
              <input
                ref={domainInputRef}
                type="text"
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                placeholder="Filter by domain..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-black placeholder-gray-500"
              />
            </div>
            <div className="flex items-end gap-2">
              <button
                onClick={handleSearch}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Search
              </button>
              <button
                onClick={handleClear}
                className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
              >
                Clear
              </button>
            </div>
          </div>
        </div>

        {/* Results Summary */}
        <div className="mb-4">
          <p className="text-gray-600">
            Showing {stories.length} of {totalStories} stories
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        {/* Stories Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                {table.getHeaderGroups().map((headerGroup) => (
                  <tr key={headerGroup.id}>
                    {headerGroup.headers.map((header) => (
                      <th
                        key={header.id}
                        className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {table.getRowModel().rows.map((row) => (
                  <tr key={row.id} className="hover:bg-gray-50">
                    {row.getVisibleCells().map((cell) => (
                      <td key={cell.id} className="px-6 py-4 whitespace-nowrap text-black !important">
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
            <div className="flex-1 flex justify-between sm:hidden">
              <button
                onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
                disabled={currentPage === 0}
                className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Previous
              </button>
              <button
                onClick={() => setCurrentPage(currentPage + 1)}
                disabled={stories.length < pageSize}
                className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Next
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Showing{' '}
                  <span className="font-medium">{currentPage * pageSize + 1}</span> to{' '}
                  <span className="font-medium">
                    {Math.min((currentPage + 1) * pageSize, totalStories)}
                  </span>{' '}
                  of <span className="font-medium">{totalStories}</span> results
                </p>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                  <button
                    onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
                    disabled={currentPage === 0}
                    className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                  >
                    Previous
                  </button>
                  <button
                    onClick={() => setCurrentPage(currentPage + 1)}
                    disabled={stories.length < pageSize}
                    className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                  >
                    Next
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 