import React, { useState } from 'react';
import {
  Database,
  Search,
  ExternalLink,
  BookOpen,
  Scale,
  ShieldCheck,
  Globe2,
} from 'lucide-react';

const sources = [
  {
    title: 'Indian Patent Office',
    category: 'IPR',
    description:
      'Official information related to patents, applications and intellectual property procedures in India.',
    icon: Scale,
  },
  {
    title: 'Traditional Knowledge Digital Library',
    category: 'Traditional Knowledge',
    description:
      'Knowledge resource supporting identification and protection of documented traditional knowledge.',
    icon: BookOpen,
  },
  {
    title: 'Biological Diversity Framework',
    category: 'Biodiversity',
    description:
      'Regulatory information relevant to access, utilisation and benefit-sharing of biological resources.',
    icon: ShieldCheck,
  },
  {
    title: 'Ayurvedic Regulatory Resources',
    category: 'Regulatory',
    description:
      'Reference material for understanding regulatory considerations surrounding Ayurvedic products.',
    icon: Database,
  },
];

const Sources: React.FC = () => {
  const [query, setQuery] = useState('');

  const filteredSources = sources.filter(
    (source) =>
      source.title.toLowerCase().includes(query.toLowerCase()) ||
      source.category.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="space-y-6">

      {/* Hero */}
      <section className="rounded-3xl bg-gradient-to-br from-slate-950 via-slate-900 to-teal-950 p-8 text-white shadow-xl">
        <div className="flex items-center gap-3 text-teal-300 text-sm font-semibold mb-3">
          <Database size={18} />
          TRUSTED KNOWLEDGE
        </div>

        <h1 className="text-3xl lg:text-4xl font-bold">
          Source Explorer
        </h1>

        <p className="mt-3 max-w-2xl text-slate-300">
          Explore the authoritative legal, regulatory and traditional knowledge
          sources that support Ayur-Lex-AI responses.
        </p>
      </section>

      {/* Search */}
      <section className="card">
        <div className="relative">
          <Search
            size={19}
            className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search sources..."
            className="w-full rounded-xl border border-slate-200 bg-slate-50 pl-11 pr-4 py-3 outline-none focus:ring-2 focus:ring-teal-500"
          />
        </div>
      </section>

      {/* Trust strip */}
      <div className="grid sm:grid-cols-3 gap-4">

        <div className="rounded-2xl bg-emerald-50 border border-emerald-100 p-5">
          <ShieldCheck className="text-emerald-600 mb-3" size={24} />
          <h3 className="font-bold text-emerald-900">
            Evidence-backed
          </h3>
          <p className="text-sm text-emerald-700 mt-1">
            Responses are designed around grounded source material.
          </p>
        </div>

        <div className="rounded-2xl bg-blue-50 border border-blue-100 p-5">
          <Globe2 className="text-blue-600 mb-3" size={24} />
          <h3 className="font-bold text-blue-900">
            Jurisdiction aware
          </h3>
          <p className="text-sm text-blue-700 mt-1">
            Regulatory context can vary by country and region.
          </p>
        </div>

        <div className="rounded-2xl bg-purple-50 border border-purple-100 p-5">
          <BookOpen className="text-purple-600 mb-3" size={24} />
          <h3 className="font-bold text-purple-900">
            Research ready
          </h3>
          <p className="text-sm text-purple-700 mt-1">
            Useful references for innovators and researchers.
          </p>
        </div>

      </div>

      {/* Sources */}
      <section className="space-y-4">

        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold text-slate-900">
            Available Sources
          </h2>

          <span className="text-sm text-slate-500">
            {filteredSources.length} sources
          </span>
        </div>

        {filteredSources.map((source, index) => {
          const Icon = source.icon;

          return (
            <div
              key={index}
              className="card card-hover flex flex-col md:flex-row gap-5 md:items-center"
            >
              <div className="p-3 rounded-xl bg-teal-50 text-teal-700">
                <Icon size={25} />
              </div>

              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-3">
                  <h3 className="font-bold text-slate-900">
                    {source.title}
                  </h3>

                  <span className="badge bg-slate-100 text-slate-600">
                    {source.category}
                  </span>
                </div>

                <p className="text-sm text-slate-500 mt-2 max-w-3xl">
                  {source.description}
                </p>
              </div>

              <button className="btn-secondary flex items-center justify-center gap-2">
                Explore
                <ExternalLink size={16} />
              </button>
            </div>
          );
        })}

        {filteredSources.length === 0 && (
          <div className="card text-center py-12">
            <Search className="mx-auto text-slate-300" size={40} />
            <h3 className="mt-4 font-bold text-slate-900">
              No sources found
            </h3>
            <p className="text-sm text-slate-500 mt-1">
              Try another search term.
            </p>
          </div>
        )}

      </section>

      <p className="text-xs text-slate-400 text-center">
        Source availability and regulatory information should be verified
        against the latest official publications.
      </p>
    </div>
  );
};

export default Sources;