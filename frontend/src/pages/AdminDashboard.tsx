import React, { useState, useEffect } from 'react';
import { 
  Users, FileText, Database, Activity, RefreshCw, 
  Play, Globe, CheckCircle2, AlertCircle, Clock, Eye, X, Terminal
} from 'lucide-react';
import toast from 'react-hot-toast';
import { adminApi, type AdminStats, type IngestionJob, type CrawlJobDetail } from '../api/admin';
import { sourcesApi } from '../api/sources';
import type { Source } from '../types';

const AdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [jobs, setJobs] = useState<IngestionJob[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [selectedSourceId, setSelectedSourceId] = useState<string>('');
  const [forceReindex, setForceReindex] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [actionLoading, setActionLoading] = useState<boolean>(false);

  // Job Details Modal
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null);
  const [jobDetail, setJobDetail] = useState<CrawlJobDetail | null>(null);
  const [loadingDetail, setLoadingDetail] = useState<boolean>(false);

  const fetchDashboardData = async () => {
    try {
      const [statsData, jobsData, sourcesData] = await Promise.allSettled([
        adminApi.getStats(),
        adminApi.getIngestionStatus(20),
        sourcesApi.getSources(),
      ]);

      if (statsData.status === 'fulfilled') {
        setStats(statsData.value);
      }
      if (jobsData.status === 'fulfilled') {
        setJobs(jobsData.value);
      }
      if (sourcesData.status === 'fulfilled' && Array.isArray(sourcesData.value)) {
        setSources(sourcesData.value);
        if (sourcesData.value.length > 0 && !selectedSourceId) {
          setSelectedSourceId(sourcesData.value[0].id);
        }
      }
    } catch (err) {
      console.error('Error fetching admin dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  // Auto-poll if any job is running or pending
  useEffect(() => {
    const hasRunningJobs = jobs.some((j) => j.status === 'running' || j.status === 'pending');
    if (!hasRunningJobs) return;

    const interval = setInterval(() => {
      adminApi.getIngestionStatus(20).then(setJobs).catch(() => {});
      adminApi.getStats().then(setStats).catch(() => {});
    }, 5000);

    return () => clearInterval(interval);
  }, [jobs]);

  const handleCrawlAll = async () => {
    setActionLoading(true);
    try {
      const res = await adminApi.crawlAll(forceReindex);
      toast.success(res.message || 'Crawl jobs queued for all active sources!');
      await fetchDashboardData();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to trigger crawl for all sources');
    } finally {
      setActionLoading(false);
    }
  };

  const handleCrawlSingle = async () => {
    if (!selectedSourceId) {
      toast.error('Please select a source to crawl');
      return;
    }
    setActionLoading(true);
    try {
      const res = await adminApi.triggerIngestion(selectedSourceId, forceReindex);
      toast.success(res.message || 'Crawl job queued successfully!');
      await fetchDashboardData();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Failed to trigger crawl');
    } finally {
      setActionLoading(false);
    }
  };

  const handleViewLogs = async (jobId: string) => {
    setSelectedJobId(jobId);
    setLoadingDetail(true);
    try {
      const detail = await adminApi.getJobDetail(jobId);
      setJobDetail(detail);
    } catch (err: any) {
      toast.error('Failed to load job details and logs');
    } finally {
      setLoadingDetail(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-semibold text-[#1a365d]">Admin & Web Crawler Control Center</h1>
          <p className="text-sm text-gray-500 mt-1">
            Real-time system telemetry, knowledge base index status, and Crawl4AI web scraper orchestration.
          </p>
        </div>
        <button
          onClick={fetchDashboardData}
          disabled={loading}
          className="inline-flex items-center gap-2 px-3.5 py-2 border border-gray-300 rounded-lg text-xs font-semibold text-gray-700 bg-white hover:bg-gray-50 shadow-2xs transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Data</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          {
            title: 'Knowledge Base Documents',
            value: stats ? stats.total_documents.toLocaleString() : '—',
            icon: FileText,
            color: 'text-teal-600',
            bg: 'bg-teal-50',
          },
          {
            title: 'Authoritative Sources',
            value: stats ? stats.total_sources.toLocaleString() : '—',
            icon: Database,
            color: 'text-amber-600',
            bg: 'bg-amber-50',
          },
          {
            title: 'Active Ingestion Jobs',
            value: stats ? stats.active_ingestion_jobs.toString() : '—',
            icon: Activity,
            color: 'text-blue-600',
            bg: 'bg-blue-50',
          },
          {
            title: 'Saved Assessments',
            value: stats ? stats.total_assessments.toLocaleString() : '—',
            icon: Users,
            color: 'text-purple-600',
            bg: 'bg-purple-50',
          },
        ].map((card, i) => {
          const Icon = card.icon;
          return (
            <div key={i} className="bg-white p-5 rounded-xl border border-gray-200 shadow-2xs">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-medium text-gray-500">{card.title}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{card.value}</p>
                </div>
                <div className={`p-3 rounded-xl ${card.bg} ${card.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Crawl4AI Scraper Control Panel */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 p-6 space-y-4">
        <div className="flex items-center gap-2.5 border-b border-gray-100 pb-3">
          <Globe className="w-5 h-5 text-[#2c7a7b]" />
          <div>
            <h2 className="text-base font-bold text-[#1a365d]">Crawl4AI Web Scraper Actions</h2>
            <p className="text-xs text-gray-500">
              Fetch legal statutes, gazette notifications, and rules from authoritative public domains.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-1">
          {/* Action 1: Crawl All Active Sources */}
          <div className="p-4.5 bg-gray-50 rounded-xl border border-gray-200/80 flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="p-1.5 bg-blue-100 text-blue-700 rounded-lg">
                  <Globe className="w-4 h-4" />
                </span>
                <h3 className="font-bold text-sm text-[#1a365d]">Crawl All Active Sources</h3>
              </div>
              <p className="text-xs text-gray-600 mt-2 leading-relaxed">
                Sequentially visits all registered legal sources, extracts clean markdown using Playwright Chromium, detects SHA-256 content changes, and indexes new content into Qdrant.
              </p>
            </div>

            <div className="pt-2 flex items-center justify-between gap-3">
              <label className="flex items-center gap-2 text-xs text-gray-600 cursor-pointer">
                <input
                  type="checkbox"
                  checked={forceReindex}
                  onChange={(e) => setForceReindex(e.target.checked)}
                  className="rounded border-gray-300 text-[#2c7a7b] focus:ring-[#2c7a7b]"
                />
                <span>Force re-index unchanged content</span>
              </label>

              <button
                onClick={handleCrawlAll}
                disabled={actionLoading}
                className="inline-flex items-center gap-2 px-4 py-2 bg-[#1a365d] hover:bg-[#152c4d] text-white text-xs font-semibold rounded-lg shadow-2xs transition-colors disabled:opacity-50"
              >
                <Play className="w-3.5 h-3.5" />
                <span>{actionLoading ? 'Starting Crawl...' : 'Start Crawl All'}</span>
              </button>
            </div>
          </div>

          {/* Action 2: Crawl Specific Source */}
          <div className="p-4.5 bg-gray-50 rounded-xl border border-gray-200/80 flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="p-1.5 bg-teal-100 text-teal-700 rounded-lg">
                  <Database className="w-4 h-4" />
                </span>
                <h3 className="font-bold text-sm text-[#1a365d]">Crawl Individual Legal Portal</h3>
              </div>
              <p className="text-xs text-gray-600 mt-2 leading-relaxed">
                Select an individual authoritative statutory portal or treaty database to crawl on-demand.
              </p>
            </div>

            <div className="space-y-3 pt-1">
              <select
                value={selectedSourceId}
                onChange={(e) => setSelectedSourceId(e.target.value)}
                className="w-full px-3 py-2 bg-white border border-gray-300 rounded-lg text-xs text-gray-800 focus:ring-2 focus:ring-[#2c7a7b] outline-hidden"
              >
                {sources.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.name} ({s.jurisdiction})
                  </option>
                ))}
              </select>

              <div className="flex justify-end">
                <button
                  onClick={handleCrawlSingle}
                  disabled={actionLoading || !selectedSourceId}
                  className="inline-flex items-center gap-2 px-4 py-2 bg-[#2c7a7b] hover:bg-[#235e5f] text-white text-xs font-semibold rounded-lg shadow-2xs transition-colors disabled:opacity-50"
                >
                  <Play className="w-3.5 h-3.5" />
                  <span>{actionLoading ? 'Triggering...' : 'Crawl Selected Source'}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Ingestion & Crawl Jobs Live Table */}
      <div className="bg-white rounded-xl shadow-2xs border border-gray-200 overflow-hidden">
        <div className="p-5 border-b border-gray-200 bg-[#f8fafc] flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-[#1a365d] flex items-center gap-2">
              <Activity className="w-4 h-4 text-[#2c7a7b]" />
              <span>Recent Ingestion & Crawl Jobs</span>
            </h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Live execution logs, status codes, documents processed, and vector chunks created.
            </p>
          </div>
          <span className="text-xs text-gray-400 font-mono">
            {jobs.length} jobs recorded
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-gray-50 text-gray-500 uppercase tracking-wider font-semibold border-b border-gray-200">
              <tr>
                <th className="px-5 py-3">Source Name</th>
                <th className="px-5 py-3">Type</th>
                <th className="px-5 py-3">Status</th>
                <th className="px-5 py-3">Found / Processed / Failed</th>
                <th className="px-5 py-3">Chunks</th>
                <th className="px-5 py-3">Started</th>
                <th className="px-5 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {jobs.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-5 py-8 text-center text-gray-400">
                    No crawl or ingestion jobs recorded yet. Use the controls above to trigger your first crawl.
                  </td>
                </tr>
              ) : (
                jobs.map((job) => {
                  let statusBadge = (
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-gray-100 text-gray-800">
                      <Clock className="w-3 h-3" />
                      <span>{job.status}</span>
                    </span>
                  );

                  if (job.status === 'running') {
                    statusBadge = (
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-blue-50 text-blue-800 border border-blue-200 animate-pulse">
                        <span className="w-1.5 h-1.5 rounded-full bg-blue-600 animate-ping" />
                        <span>Crawling...</span>
                      </span>
                    );
                  } else if (job.status === 'completed') {
                    statusBadge = (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-50 text-emerald-800 border border-emerald-200">
                        <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                        <span>Completed</span>
                      </span>
                    );
                  } else if (job.status === 'failed') {
                    statusBadge = (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-red-50 text-red-800 border border-red-200">
                        <AlertCircle className="w-3 h-3 text-red-600" />
                        <span>Failed</span>
                      </span>
                    );
                  }

                  return (
                    <tr key={job.id} className="hover:bg-gray-50/70 transition-colors">
                      <td className="px-5 py-3.5 font-medium text-gray-900">
                        {job.source_name || `Source ${job.source_id.slice(0, 8)}`}
                      </td>
                      <td className="px-5 py-3.5 text-gray-600 uppercase font-mono text-[11px]">
                        {job.job_type}
                      </td>
                      <td className="px-5 py-3.5">{statusBadge}</td>
                      <td className="px-5 py-3.5 text-gray-600 font-mono">
                        <span className="text-gray-900 font-semibold">{job.documents_found}</span> found •{' '}
                        <span className="text-emerald-700 font-semibold">{job.documents_processed}</span> ok •{' '}
                        <span className={job.documents_failed > 0 ? 'text-red-600 font-bold' : 'text-gray-400'}>
                          {job.documents_failed} err
                        </span>
                      </td>
                      <td className="px-5 py-3.5 font-mono text-gray-800 font-semibold">
                        {job.chunks_created}
                      </td>
                      <td className="px-5 py-3.5 text-gray-500 text-[11px]">
                        {job.started_at ? new Date(job.started_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '—'}
                      </td>
                      <td className="px-5 py-3.5 text-right">
                        <button
                          onClick={() => handleViewLogs(job.id)}
                          className="inline-flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-[#2c7a7b] hover:bg-teal-50 rounded-md transition-colors"
                        >
                          <Eye className="w-3 h-3" />
                          <span>Logs</span>
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Logs Modal */}
      {selectedJobId && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl border border-gray-200 max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden">
            {/* Modal Header */}
            <div className="p-4 px-6 border-b border-gray-200 flex items-center justify-between bg-gray-50">
              <div className="flex items-center gap-2">
                <Terminal className="w-5 h-5 text-[#1a365d]" />
                <h3 className="font-bold text-sm text-[#1a365d]">
                  Audit Logs: {jobDetail?.source_name || selectedJobId.slice(0, 8)}
                </h3>
              </div>
              <button
                onClick={() => setSelectedJobId(null)}
                className="p-1 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto space-y-3 font-mono text-xs bg-gray-950 text-gray-100 flex-1">
              {loadingDetail ? (
                <div className="py-8 text-center text-gray-400">Loading crawl logs...</div>
              ) : !jobDetail || jobDetail.logs.length === 0 ? (
                <div className="py-8 text-center text-gray-500">No logs recorded for this job.</div>
              ) : (
                jobDetail.logs.map((log) => (
                  <div key={log.id} className="flex items-start gap-2.5 text-[11px] leading-relaxed">
                    <span className="text-gray-500 shrink-0">
                      {new Date(log.created_at).toLocaleTimeString()}
                    </span>
                    <span
                      className={`font-bold px-1.5 py-0.2 rounded shrink-0 uppercase text-[10px] ${
                        log.level === 'error'
                          ? 'bg-red-900/80 text-red-200'
                          : log.level === 'warning'
                          ? 'bg-amber-900/80 text-amber-200'
                          : 'bg-blue-900/60 text-blue-300'
                      }`}
                    >
                      {log.level}
                    </span>
                    <span className="text-gray-200 break-all">{log.message}</span>
                  </div>
                ))
              )}
            </div>

            {/* Modal Footer */}
            <div className="p-3 px-6 border-t border-gray-200 bg-gray-50 flex justify-end">
              <button
                onClick={() => setSelectedJobId(null)}
                className="px-4 py-1.5 bg-white border border-gray-300 text-xs font-semibold rounded-lg text-gray-700 hover:bg-gray-100"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
