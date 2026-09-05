import React from 'react';
import { Link } from 'react-router-dom';
import {
  MessageSquare,
  Layers,
  Shield,
  Leaf,
  BookOpen,
  Database,
  FileText,
  Users,
  Scale,
  ArrowRight,
  Sparkles,
  CheckCircle2,
} from 'lucide-react';

const Dashboard: React.FC = () => {
  const features = [
    {
      name: 'AI Regulatory Assistant',
      desc: 'Ask complex IPR and regulatory questions and receive citation-grounded answers.',
      icon: MessageSquare,
      link: '/chat',
      tag: 'AI',
    },
    {
      name: 'Formulation Classification',
      desc: 'Determine the regulatory category of an Ayurvedic formulation.',
      icon: Layers,
      link: '/classify',
      tag: 'CLASSIFY',
    },
    {
      name: 'Patent & IP Assessment',
      desc: 'Explore patentability, IP options and potential protection pathways.',
      icon: Shield,
      link: '/ip-assessment',
      tag: 'IPR',
    },
    {
      name: 'Traditional Knowledge',
      desc: 'Search traditional knowledge and identify potential prior-art concerns.',
      icon: BookOpen,
      link: '/tk',
      tag: 'TK',
    },
    {
      name: 'ABS Compliance',
      desc: 'Evaluate biodiversity access and benefit-sharing requirements.',
      icon: Leaf,
      link: '/abs',
      tag: 'ABS',
    },
    {
      name: 'Regulatory Classification',
      desc: 'Review applicable Indian and international regulatory frameworks.',
      icon: Scale,
      link: '/classify',
      tag: 'LEGAL',
    },
    {
      name: 'Source Explorer',
      desc: 'Explore the trusted knowledge base behind AI-generated answers.',
      icon: Database,
      link: '/sources',
      tag: 'SOURCES',
    },
    {
      name: 'Saved Assessments',
      desc: 'Review your previous analysis, assessments and reports.',
      icon: FileText,
      link: '/assessments',
      tag: 'REPORTS',
    },
    {
      name: 'Human Review',
      desc: 'Request expert review when an AI response needs additional validation.',
      icon: Users,
      link: '/review',
      tag: 'EXPERT',
    },
  ];

  return (
    <div className="space-y-8">

      {/* HERO */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-teal-950 via-emerald-900 to-slate-900 p-7 text-white shadow-xl sm:p-10">
        <div className="absolute -right-20 -top-24 h-80 w-80 rounded-full bg-emerald-400/10 blur-3xl" />
        <div className="absolute -bottom-32 left-1/3 h-72 w-72 rounded-full bg-teal-400/10 blur-3xl" />

        <div className="relative z-10 max-w-3xl">
          <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-3 py-1.5 text-xs font-medium text-teal-100 backdrop-blur">
            <Sparkles className="h-3.5 w-3.5" />
            RAG-powered Ayurvedic IPR intelligence
          </div>

          <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Your Ayurvedic IPR
            <span className="block text-emerald-300">
              intelligence workspace.
            </span>
          </h1>

          <p className="mt-4 max-w-2xl text-sm leading-7 text-slate-300 sm:text-base">
            Research patents, trademarks, traditional knowledge, biodiversity
            requirements and regulatory pathways with evidence-backed AI.
          </p>

          <div className="mt-7 flex flex-wrap gap-3">
            <Link
              to="/chat"
              className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-bold text-teal-900 shadow-lg transition hover:bg-teal-50"
            >
              <MessageSquare className="h-4 w-4" />
              Start AI Research
              <ArrowRight className="h-4 w-4" />
            </Link>

            <Link
              to="/sources"
              className="inline-flex items-center gap-2 rounded-xl border border-white/20 bg-white/5 px-5 py-3 text-sm font-semibold text-white backdrop-blur transition hover:bg-white/10"
            >
              Explore sources
            </Link>
          </div>
        </div>
      </section>

      {/* TRUST STRIP */}
      <div className="grid gap-4 sm:grid-cols-3">
        {[
          ['RAG grounded', 'Answers retrieved from indexed sources'],
          ['Citation aware', 'Trace answers back to evidence'],
          ['Multilingual', 'English, Hindi & Kannada support'],
        ].map(([title, desc]) => (
          <div
            key={title}
            className="flex items-start gap-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"
          >
            <div className="mt-0.5 rounded-full bg-emerald-100 p-1.5">
              <CheckCircle2 className="h-4 w-4 text-emerald-700" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-800">{title}</p>
              <p className="mt-1 text-xs leading-5 text-slate-500">{desc}</p>
            </div>
          </div>
        ))}
      </div>

      {/* TOOLS */}
      <section>
        <div className="mb-5 flex items-end justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.18em] text-teal-700">
              Workspace
            </p>
            <h2 className="mt-1 text-2xl font-bold text-slate-900">
              Tools & intelligence
            </h2>
          </div>

          <span className="hidden text-sm text-slate-400 sm:block">
            {features.length} capabilities
          </span>
        </div>

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {features.map((item) => {
            const Icon = item.icon;

            return (
              <Link
                key={item.name}
                to={item.link}
                className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition duration-200 hover:-translate-y-1 hover:border-teal-200 hover:shadow-xl"
              >
                <div className="flex items-start justify-between">
                  <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-teal-50 text-teal-700 transition group-hover:bg-teal-700 group-hover:text-white">
                    <Icon className="h-5 w-5" />
                  </div>

                  <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[10px] font-bold tracking-wider text-slate-500">
                    {item.tag}
                  </span>
                </div>

                <h3 className="mt-5 text-base font-bold text-slate-900">
                  {item.name}
                </h3>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  {item.desc}
                </p>

                <div className="mt-5 flex items-center gap-1 text-xs font-bold text-teal-700 opacity-0 transition group-hover:opacity-100">
                  Open tool
                  <ArrowRight className="h-3.5 w-3.5" />
                </div>
              </Link>
            );
          })}
        </div>
      </section>
    </div>
  );
};

export default Dashboard;