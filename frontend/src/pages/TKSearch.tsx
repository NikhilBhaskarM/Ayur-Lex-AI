import React, { useState } from 'react';
import {
  BookOpen,
  Search,
  Sparkles,
  ShieldCheck,
  Database,
  ArrowRight,
} from 'lucide-react';

const TKSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [searched, setSearched] = useState(false);

  const handleSearch = () => {
    if (!query.trim()) return;
    setSearched(true);
  };

  return (
    <div className="space-y-6">

      {/* Hero */}
      <section className="rounded-3xl bg-gradient-to-br from-slate-950 via-indigo-950 to-teal-900 p-8 text-white shadow-xl">
        <div className="flex flex-col lg:flex-row lg:justify-between lg:items-center gap-6">

          <div>
            <div className="flex items-center gap-2 text-teal-300 text-sm font-semibold mb-3">
              <BookOpen size={18} />
              TRADITIONAL KNOWLEDGE INTELLIGENCE
            </div>

            <h1 className="text-3xl lg:text-4xl font-bold">
              Traditional Knowledge Search
            </h1>

            <p className="mt-3 max-w-2xl text-slate-300 leading-relaxed">
              Search Ayurvedic concepts, formulations and traditional uses to
              identify potential prior knowledge relevant to IPR assessment.
            </p>
          </div>

          <div className="hidden lg:flex h-20 w-20 rounded-2xl bg-white/10 items-center justify-center">
            <Database size={38} className="text-teal-300" />
          </div>

        </div>
      </section>

      {/* Search */}
      <section className="card">
        <div className="flex items-center gap-3 mb-5">
          <div className="p-3 rounded-xl bg-teal-50 text-teal-700">
            <Search size={22} />
          </div>

          <div>
            <h2 className="text-xl font-bold text-slate-900">
              Search Knowledge Base
            </h2>
            <p className="text-sm text-slate-500">
              Enter a formulation, ingredient or traditional practice.
            </p>
          </div>
        </div>

        <div className="flex flex-col md:flex-row gap-3">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSearch();
            }}
            placeholder="Example: Ashwagandha traditional uses..."
            className="flex-1 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 outline-none focus:ring-2 focus:ring-teal-500"
          />

          <button
            onClick={handleSearch}
            disabled={!query.trim()}
            className="btn-primary flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <Search size={18} />
            Search
          </button>
        </div>
      </section>

      {/* Empty state */}
      {!searched && (
        <section className="grid md:grid-cols-3 gap-5">

          <div className="card card-hover">
            <BookOpen className="text-indigo-600 mb-4" size={26} />
            <h3 className="font-bold text-slate-900">
              Classical Sources
            </h3>
            <p className="text-sm text-slate-500 mt-2">
              Explore evidence associated with established Ayurvedic knowledge.
            </p>
          </div>

          <div className="card card-hover">
            <Sparkles className="text-teal-600 mb-4" size={26} />
            <h3 className="font-bold text-slate-900">
              Semantic Search
            </h3>
            <p className="text-sm text-slate-500 mt-2">
              Find related concepts even when terminology differs.
            </p>
          </div>

          <div className="card card-hover">
            <ShieldCheck className="text-emerald-600 mb-4" size={26} />
            <h3 className="font-bold text-slate-900">
              IPR Context
            </h3>
            <p className="text-sm text-slate-500 mt-2">
              Use knowledge discovery as part of prior-art and IPR assessment.
            </p>
          </div>

        </section>
      )}

      {/* Results */}
      {searched && (
        <section className="space-y-5">

          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-900">
                Knowledge Matches
              </h2>
              <p className="text-sm text-slate-500">
                Results related to "{query}"
              </p>
            </div>

            <span className="badge bg-teal-50 text-teal-700">
              Semantic Search
            </span>
          </div>

          {[
            {
              title: 'Traditional Ayurvedic References',
              text: 'Potentially relevant traditional knowledge references identified for further verification.',
              score: '92%',
            },
            {
              title: 'Related Formulations',
              text: 'Related formulations and ingredient combinations may require prior-knowledge review.',
              score: '87%',
            },
            {
              title: 'Historical Usage Context',
              text: 'Historical usage information may provide useful context for an IPR assessment.',
              score: '81%',
            },
          ].map((result, index) => (
            <div
              key={index}
              className="card card-hover flex flex-col md:flex-row md:items-center gap-5"
            >
              <div className="p-3 rounded-xl bg-indigo-50 text-indigo-700">
                <BookOpen size={24} />
              </div>

              <div className="flex-1">
                <div className="flex items-center gap-3">
                  <h3 className="font-bold text-slate-900">
                    {result.title}
                  </h3>

                  <span className="text-xs font-semibold px-2 py-1 rounded-full bg-emerald-50 text-emerald-700">
                    {result.score} match
                  </span>
                </div>

                <p className="text-sm text-slate-500 mt-2">
                  {result.text}
                </p>
              </div>

              <button className="btn-secondary flex items-center gap-2">
                View Source
                <ArrowRight size={16} />
              </button>
            </div>
          ))}

        </section>
      )}

      <p className="text-xs text-slate-400 text-center">
        Search results should be independently verified against authoritative
        traditional knowledge and legal sources.
      </p>
    </div>
  );
};

export default TKSearch;