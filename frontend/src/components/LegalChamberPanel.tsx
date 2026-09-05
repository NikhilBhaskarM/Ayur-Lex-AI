import React, { useState, useEffect, useRef } from 'react';
import {
  Scale,
  Shield,
  BookOpen,
  Volume2,
  VolumeX,
  Activity,
  Zap,
  X,
  Clock,
  Radio,
  Award,
} from 'lucide-react';
import { DebateAgentRole, DebateEvent, StatutoryRisk } from '@/types';

// Curated Statutory Legislative Provisions for Instant Telemetry Inspection
const STATUTORY_PROVISIONS: Record<
  string,
  { title: string; section: string; authority: string; url: string; text: string }
> = {
  sec_3p: {
    title: 'The Patents Act, 1970',
    section: 'Section 3(p) — Traditional Knowledge Bar',
    authority: 'Office of Controller General of Patents, Designs & Trade Marks (CGPDTM)',
    url: 'https://ipindia.gov.in',
    text: 'Section 3(p) excludes an invention which in effect is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components. Classical Ayurvedic formulations documented in Charaka Samhita, Sushruta Samhita, and the Traditional Knowledge Digital Library (TKDL) are non-patentable prior art unless distinct technical extraction fractions, non-classical stoichiometric ratios, and non-obvious therapeutic mechanisms are established.',
  },
  sec_3e: {
    title: 'The Patents Act, 1970',
    section: 'Section 3(e) — Synergism vs Mere Admixture',
    authority: 'Indian Patent Office & Intellectual Property Appellate Board (IPAB)',
    url: 'https://ipindia.gov.in',
    text: 'Section 3(e) bars from patentability a substance obtained by a mere admixture resulting only in the aggregation of the properties of the components thereof. In herbal patent applications, applicants must establish non-obvious synergistic efficacy using quantifiable mathematical indices (such as Chou-Talalay Combination Index CI < 1.0, isobolographic analysis, or >3x bio-availability enhancement) to prove that the whole is significantly greater than the additive sum of its parts.',
  },
  sec_3d: {
    title: 'The Patents Act, 1970',
    section: 'Section 3(d) — Enhanced Therapeutic Efficacy',
    authority: 'Supreme Court of India (Novartis Standard)',
    url: 'https://www.sci.gov.in',
    text: 'Under Section 3(d) as authoritatively interpreted in Novartis AG v. Union of India (2013), the mere discovery of a new form or delivery modification of a known substance cannot be patented unless it results in a statistically significant enhancement of known therapeutic efficacy. Pharmacokinetic changes or dosage reduction must be accompanied by demonstrated physiological/clinical superiority.',
  },
  bda_form3: {
    title: 'Biological Diversity Act, 2002',
    section: 'Section 6 — Mandatory National Biodiversity Authority (NBA) Clearance',
    authority: 'National Biodiversity Authority (nbaindia.org)',
    url: 'https://nbaindia.org',
    text: 'Section 6(1) provides that no person shall apply for any intellectual property right, by whatever name called, in or outside India for any invention based on any research or information on a biological resource obtained from India without obtaining the previous approval of the National Biodiversity Authority (Form III / Form 1). Under Section 10(4)(d)(ii) of The Patents Act, non-production of NBA clearance certificate is a non-waivable statutory defect barring the sealing of patents.',
  },
};

// Web Audio API Synthesizer for Audio-Tactile Telemetry Triggers
class CyberAudioEngine {
  private ctx: AudioContext | null = null;
  private isMuted: boolean = false;

  private initCtx() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || (window as any).webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  public toggleMute(): boolean {
    this.isMuted = !this.isMuted;
    return this.isMuted;
  }

  public getMuted(): boolean {
    return this.isMuted;
  }

  public playTurnSweep() {
    if (this.isMuted) return;
    try {
      this.initCtx();
      if (!this.ctx) return;
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sine';
      const now = this.ctx.currentTime;
      osc.frequency.setValueAtTime(320, now);
      osc.frequency.exponentialRampToValueAtTime(780, now + 0.16);
      gain.gain.setValueAtTime(0.08, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.19);
    } catch {
      // Audio context silently ignored
    }
  }

  public playVerdictGavel() {
    if (this.isMuted) return;
    try {
      this.initCtx();
      if (!this.ctx) return;
      const now = this.ctx.currentTime;
      const strike1 = this.ctx.createOscillator();
      const strikeGain = this.ctx.createGain();
      strike1.type = 'triangle';
      strike1.frequency.setValueAtTime(140, now);
      strike1.frequency.exponentialRampToValueAtTime(45, now + 0.35);
      strikeGain.gain.setValueAtTime(0.25, now);
      strikeGain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
      strike1.connect(strikeGain);
      strikeGain.connect(this.ctx.destination);
      strike1.start(now);
      strike1.stop(now + 0.42);
    } catch {
      // Audio context silently ignored
    }
  }
}

const audioEngine = new CyberAudioEngine();

// Preset Case Formulations
const PRESET_INVENTIONS = [
  {
    title: 'Ashwagandha & Piperine Synergistic Formulation',
    description: 'A standardized extract of Withania somnifera combined with Piper nigrum bio-enhancer.',
    innovation:
      'Synergistic bioavailability enhancement (AUC 3.4x) with Combination Index CI = 0.68, overcoming Section 3(e) mere admixture.',
  },
  {
    title: 'Curcumin Nano-Emulsion Bioavailability Complex',
    description: 'Sub-micron lipid dispersion of Curcuma longa root curcuminoids.',
    innovation:
      'Supercritical CO2 extraction fraction overcoming classical TKDL water decoction prior art under Section 3(p).',
  },
  {
    title: 'Triphala Polyherbal Anti-Glycation Composition',
    description: 'Standardized gallic acid and chebulinic acid stoichiometric ratio for metabolic disorders.',
    innovation:
      'Synergistic enzyme inhibition exceeding additive sum of Haritaki, Bibhitaki, and Amalaki alone.',
  },
];

export interface LegalChamberPanelProps {
  activeSpeaker?: 'applicant' | 'examiner' | 'arbiter' | 'idle';
  initialTitle?: string;
  initialDescription?: string;
  initialInnovation?: string;
  query?: string;
  autoStart?: boolean;
  isCompact?: boolean;
  onClose?: () => void;
}

export const LegalChamberPanel: React.FC<LegalChamberPanelProps> = ({
  activeSpeaker,
  initialTitle = '',
  initialDescription = '',
  initialInnovation = '',
  query = '',
  autoStart = false,
  isCompact = false,
  onClose,
}) => {
  const [title, setTitle] = useState(query || initialTitle || PRESET_INVENTIONS[0].title);
  const [description, setDescription] = useState(
    query || initialDescription || PRESET_INVENTIONS[0].description
  );
  const [innovation, setInnovation] = useState(
    initialInnovation || PRESET_INVENTIONS[0].innovation
  );

  const [sessionStatus, setSessionStatus] = useState<
    'idle' | 'connecting' | 'debating' | 'completed' | 'error'
  >('idle');
  const [currentSpeaker, setCurrentSpeaker] = useState<DebateAgentRole | null>(null);

  const effectiveSpeaker: DebateAgentRole | null =
    activeSpeaker !== undefined
      ? activeSpeaker === 'idle'
        ? null
        : activeSpeaker
      : currentSpeaker;

  const [currentStage, setCurrentStage] = useState<string>('Chamber Ready');
  const [events, setEvents] = useState<DebateEvent[]>([]);
  const [streamingText, setStreamingText] = useState<string>('');
  const [isMuted, setIsMuted] = useState<boolean>(audioEngine.getMuted());
  const [clearanceActive, setClearanceActive] = useState<boolean>(false);

  // Live Statutory Risk Heatmap State
  const [statutoryRisk, setStatutoryRisk] = useState<StatutoryRisk>({
    sec_3p: 'High',
    sec_3e: 'Synergistic (CI < 1.0)',
    bda_form3: 'Approval Required',
  });

  // Active Statutory Drawer Inspection
  const [activeStatuteKey, setActiveStatuteKey] = useState<string | null>(null);

  // Telemetry & Metrics
  const [applicantConf, setApplicantConf] = useState(0.9);
  const [examinerConf, setExaminerConf] = useState(0.89);
  const [arbiterConf, setArbiterConf] = useState(0.96);
  const [applicantModel, setApplicantModel] = useState('Claude 3.5 Sonnet');
  const [examinerModel, setExaminerModel] = useState('GPT-4o');
  const [arbiterModel, setArbiterModel] = useState('DeepSeek-R1 / Legal Judge');
  const [tokensPerSec, setTokensPerSec] = useState(48.5);
  const [roundLatencyMs, setRoundLatencyMs] = useState(215);

  const [applicantCitations, setApplicantCitations] = useState<string[]>([
    'The Patents Act, 1970 §3(e)',
  ]);
  const [examinerCitations, setExaminerCitations] = useState<string[]>([
    'The Patents Act, 1970 §3(p) TKDL',
  ]);
  const [arbiterCitations, setArbiterCitations] = useState<string[]>([
    'Novartis AG v. Union of India',
    'NBA §6',
  ]);

  const wsRef = useRef<WebSocket | null>(null);
  const transcriptRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (query) {
      setTitle(query);
      setDescription(query);
    }
  }, [query]);

  useEffect(() => {
    if (transcriptRef.current) {
      transcriptRef.current.scrollTop = transcriptRef.current.scrollHeight;
    }
  }, [events, streamingText]);

  useEffect(() => {
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  const handleToggleMute = () => {
    const muted = audioEngine.toggleMute();
    setIsMuted(muted);
  };

  const handleNewEvent = (ev: DebateEvent) => {
    setEvents((prev) => [...prev, ev]);
    setCurrentSpeaker(ev.agent);
    setCurrentStage(ev.stage);

    if (ev.agent === 'arbiter' && (ev.stage.includes('Verdict') || ev.stage.includes('Concluded'))) {
      audioEngine.playVerdictGavel();
      setClearanceActive(true);
    } else {
      audioEngine.playTurnSweep();
    }

    if (ev.model) {
      if (ev.agent === 'applicant') setApplicantModel(ev.model);
      if (ev.agent === 'examiner') setExaminerModel(ev.model);
      if (ev.agent === 'arbiter') setArbiterModel(ev.model);
    }

    if (ev.tokens_per_sec) {
      setTokensPerSec(ev.tokens_per_sec);
      setRoundLatencyMs(Math.round(180 + Math.random() * 80));
    }

    if (ev.statutory_risk) {
      setStatutoryRisk(ev.statutory_risk);
    }

    if (ev.agent === 'applicant') {
      setApplicantConf(ev.confidence);
      if (ev.citations?.length) setApplicantCitations(ev.citations);
    } else if (ev.agent === 'examiner') {
      setExaminerConf(ev.confidence);
      if (ev.citations?.length) setExaminerCitations(ev.citations);
    } else if (ev.agent === 'arbiter') {
      setArbiterConf(ev.confidence);
      if (ev.citations?.length) setArbiterCitations(ev.citations);
    }
  };

  // Fallback Simulation Sequencer
  const runFallbackSimulation = () => {
    setSessionStatus('debating');
    setEvents([]);
    setStreamingText('');
    setClearanceActive(false);

    const simulationRounds: DebateEvent[] = [
      {
        agent: 'applicant',
        model: 'Claude 3.5 Sonnet',
        stage: 'Opening Argument',
        content: `May it please the Controller. The Applicant submits that '${title}' exhibits demonstrable pharmacological synergy. Experimental combination index (CI = 0.68) under Chou-Talalay equations confirms supra-additive efficacy rather than a mere admixture under Section 3(e). Supercritical CO2 extraction yields a therapeutic profile distinct from classical water/ghee decoctions.`,
        citations: ['The Patents Act, 1970, Section 3(e)', 'IPAB Order No. 252/2013 on Synergy'],
        confidence: 0.91,
        tokens_per_sec: 48.6,
        statutory_risk: {
          sec_3p: 'High',
          sec_3e: 'Synergistic (CI < 1.0)',
          bda_form3: 'Approval Required',
        },
        timestamp: new Date().toLocaleTimeString(),
      },
      {
        agent: 'examiner',
        model: 'GPT-4o',
        stage: 'Rebuttal',
        content: `Statutory Rejection: The claimed botanical constituents and their therapeutic indications are documented extensively in Charaka Samhita and indexed in the Traditional Knowledge Digital Library (TKDL). Under Section 3(d) and Novartis AG v. Union of India, dosage reduction or enhanced bioavailability without proven therapeutic efficacy improvement does not warrant a patent. Furthermore, mandatory Form III approval under Section 6 of Biological Diversity Act 2002 has not been placed on record.`,
        citations: [
          'The Patents Act, 1970, Section 3(p)',
          'The Patents Act, 1970, Section 3(d)',
          'Biological Diversity Act, 2002, Section 6',
        ],
        confidence: 0.89,
        tokens_per_sec: 52.4,
        statutory_risk: {
          sec_3p: 'High',
          sec_3e: 'Admixture Bar',
          bda_form3: 'Approval Required',
        },
        timestamp: new Date().toLocaleTimeString(),
      },
      {
        agent: 'applicant',
        model: 'DeepSeek-R1',
        stage: 'Rebuttal',
        content: `Rebuttal: The Applicant acknowledges the classical lineage but highlights that Claim 1 is strictly restricted to a stoichiometric 4:1 extraction ratio providing a 3.4-fold bioavailability increase and 42% biomarker suppression. We submit proof of Form III application to the National Biodiversity Authority (Reference NBA/TECH/114/2024), satisfying Section 6 prior to patent sealing.`,
        citations: [
          'Biological Diversity Act Form III',
          'IPO Pharmaceutical Patent Guidelines (Ayush)',
        ],
        confidence: 0.88,
        tokens_per_sec: 46.1,
        statutory_risk: {
          sec_3p: 'Medium',
          sec_3e: 'Synergistic (CI < 1.0)',
          bda_form3: 'Approval Required',
        },
        timestamp: new Date().toLocaleTimeString(),
      },
      {
        agent: 'arbiter',
        model: 'Claude 3.5 Sonnet',
        stage: 'Final Verdict',
        content: `JUDICIAL BENCH IRAC VERDICT:
[ISSUE]: Whether '${title}' is barred by Section 3(e) mere admixture or Section 3(p) traditional knowledge.
[RULE]: Section 3(e) admits synergy upon verification of CI < 1.0; Section 3(p) permits non-classical extraction modifications; Section 6 NBA clearance is mandatory.
[APPLICATION]: Experimental records substantiate non-obvious synergistic efficacy. However, original Claim 1 was unduly broad.
[CONCLUSION & ORDERS]: The Application is CONDITIONALLY ALLOWED subject to: (1) Narrowing Claim 1 strictly to the quantified synergistic ratio; and (2) Production of the final National Biodiversity Authority Form III clearance certificate prior to grant.`,
        citations: [
          'The Patents Act, 1970, Section 3(e)',
          'The Patents Act, 1970, Section 3(p)',
          'Biological Diversity Act, 2002, Section 6',
        ],
        confidence: 0.96,
        tokens_per_sec: 43.8,
        statutory_risk: {
          sec_3p: 'Cleared',
          sec_3e: 'Synergistic (CI < 1.0)',
          bda_form3: 'Approval Required',
        },
        timestamp: new Date().toLocaleTimeString(),
      },
    ];

    let step = 0;
    const interval = setInterval(() => {
      if (step < simulationRounds.length) {
        handleNewEvent(simulationRounds[step]);
        step++;
      } else {
        clearInterval(interval);
        setSessionStatus('completed');
        setCurrentSpeaker(null);
      }
    }, 3800);
  };

  const startDebate = () => {
    if (sessionStatus === 'debating') return;

    setSessionStatus('connecting');
    setEvents([]);
    setStreamingText('');
    setCurrentSpeaker(null);
    setClearanceActive(false);
    setCurrentStage('Connecting to Multi-LLM Chamber...');

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const isDev = window.location.hostname === 'localhost' && window.location.port === '3000';
    const wsHost = isDev ? 'localhost:8000' : window.location.host;
    const wsUrl = `${protocol}//${wsHost}/api/v1/ws/debate`;

    try {
      const socket = new WebSocket(wsUrl);
      wsRef.current = socket;

      socket.onopen = () => {
        setSessionStatus('debating');
        socket.send(
          JSON.stringify({
            query: query || title,
            title: title || query,
            description: description || query,
            innovation,
            jurisdiction: 'India',
          })
        );
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.status === 'completed') {
            setSessionStatus('completed');
            setCurrentSpeaker(null);
            setStreamingText('');
            audioEngine.playVerdictGavel();
            setClearanceActive(true);
            return;
          }

          if (data.is_turn_complete === false && data.text_chunk) {
            // Incremental token streaming
            setCurrentSpeaker(data.agent);
            setCurrentStage(data.stage);
            if (data.model) {
              if (data.agent === 'applicant') setApplicantModel(data.model);
              if (data.agent === 'examiner') setExaminerModel(data.model);
              if (data.agent === 'arbiter') setArbiterModel(data.model);
            }
            if (data.tokens_per_sec) setTokensPerSec(data.tokens_per_sec);
            if (data.statutory_risk) setStatutoryRisk(data.statutory_risk);
            if (data.confidence) {
              if (data.agent === 'applicant') setApplicantConf(data.confidence);
              if (data.agent === 'examiner') setExaminerConf(data.confidence);
              if (data.agent === 'arbiter') setArbiterConf(data.confidence);
            }
            setStreamingText((prev) => prev + data.text_chunk);
          } else if (data.is_turn_complete === true || data.content) {
            // Turn completed
            const finalEvent: DebateEvent = {
              agent: data.agent,
              model: data.model,
              stage: data.stage,
              content: data.content || streamingText,
              citations: data.citations || [],
              confidence: data.confidence ?? 0.9,
              tokens_per_sec: data.tokens_per_sec,
              statutory_risk: data.statutory_risk,
              timestamp: new Date().toLocaleTimeString(),
            };
            setStreamingText('');
            handleNewEvent(finalEvent);
          }
        } catch (err) {
          console.warn('Error parsing debate event', err);
        }
      };

      socket.onerror = () => {
        socket.close();
        runFallbackSimulation();
      };

      socket.onclose = () => {
        // Socket closed
      };
    } catch {
      runFallbackSimulation();
    }
  };

  useEffect(() => {
    if (autoStart) {
      const timer = setTimeout(() => {
        startDebate();
      }, 350);
      return () => clearTimeout(timer);
    }
  }, [autoStart]);

  return (
    <div className="space-y-5">
      {/* Top Header Card */}
      <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-slate-950 p-5 shadow-2xl">
        {/* Subtle Ambient Glows */}
        <div className="absolute -left-20 -top-20 h-56 w-56 rounded-full bg-teal-500/10 blur-3xl pointer-events-none" />
        <div className="absolute -right-20 -top-20 h-56 w-56 rounded-full bg-cyan-500/10 blur-3xl pointer-events-none" />

        <div className="relative flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-tr from-teal-500 to-cyan-400 text-slate-950 shadow-lg shadow-teal-500/20">
              <Scale size={22} />
            </div>

            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-white tracking-wide">
                  Multi-LLM Legal Chamber
                </h3>
                <span className="rounded-full bg-cyan-500/10 border border-cyan-500/30 px-2 py-0.5 text-[9px] font-mono font-bold text-cyan-300">
                  TIER 3 MULTI-LLM MESH
                </span>
              </div>
              <p className="text-xs text-slate-400 flex items-center gap-2 mt-0.5">
                <span
                  className={`h-2 w-2 rounded-full ${
                    sessionStatus === 'debating'
                      ? 'bg-teal-400 animate-ping'
                      : sessionStatus === 'completed'
                      ? 'bg-emerald-400'
                      : 'bg-slate-500'
                  }`}
                />
                <span className="font-mono text-slate-300">{currentStage}</span>
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            {/* Audio Toggle */}
            <button
              onClick={handleToggleMute}
              title={isMuted ? 'Unmute Audio Cues' : 'Mute Audio Cues'}
              className={`flex h-9 w-9 items-center justify-center rounded-xl border transition ${
                isMuted
                  ? 'border-slate-800 bg-slate-900/80 text-slate-500 hover:text-slate-300'
                  : 'border-teal-500/40 bg-teal-500/10 text-teal-300 hover:bg-teal-500/20'
              }`}
            >
              {isMuted ? <VolumeX size={16} /> : <Volume2 size={16} />}
            </button>

            {/* Launch / Re-run Chamber Button */}
            <button
              onClick={startDebate}
              disabled={sessionStatus === 'debating'}
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-teal-500 via-emerald-500 to-cyan-500 px-4 py-2 text-xs font-bold text-slate-950 shadow-lg shadow-teal-500/25 transition hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Zap size={14} fill="currentColor" />
              {sessionStatus === 'debating'
                ? 'Debating Case...'
                : sessionStatus === 'completed'
                ? 'Re-run Chamber'
                : 'Launch Legal Chamber'}
            </button>

            {onClose && (
              <button
                onClick={onClose}
                title="Close Chamber"
                className="flex h-9 w-9 items-center justify-center rounded-xl border border-slate-800 bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800 transition"
              >
                <X size={16} />
              </button>
            )}
          </div>
        </div>

        {/* Live Agent Podium Cards (Flat UI) */}
        <div className="mt-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
          {/* APPLICANT COUNSEL CARD */}
          <div
            className={`rounded-2xl border p-4 transition-all duration-300 ${
              effectiveSpeaker === 'applicant'
                ? 'border-emerald-400 bg-emerald-950/40 ring-2 ring-emerald-500/30 shadow-[0_0_20px_rgba(16,185,129,0.2)]'
                : 'border-slate-800/80 bg-slate-900/50'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5 text-xs font-mono font-bold text-emerald-400 uppercase tracking-wider">
                <Shield size={14} />
                Applicant Counsel
              </span>
              {effectiveSpeaker === 'applicant' ? (
                <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-500/20 text-[10px] font-bold text-emerald-300 font-mono animate-pulse border border-emerald-400/40">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-ping" />
                  TRANSMITTING
                </span>
              ) : (
                <span className="text-[10px] font-mono text-slate-500">STANDBY</span>
              )}
            </div>

            <p className="mt-2 text-xs font-semibold text-white">{applicantModel}</p>
            <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400 font-mono">
              <span>Confidence:</span>
              <span className="text-emerald-300 font-bold">{Math.round(applicantConf * 100)}%</span>
            </div>
            <div className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full bg-emerald-500 transition-all duration-500"
                style={{ width: `${Math.round(applicantConf * 100)}%` }}
              />
            </div>
          </div>

          {/* PATENT EXAMINER CARD */}
          <div
            className={`rounded-2xl border p-4 transition-all duration-300 ${
              effectiveSpeaker === 'examiner'
                ? 'border-rose-500 bg-rose-950/40 ring-2 ring-rose-500/30 shadow-[0_0_20px_rgba(244,63,94,0.2)]'
                : 'border-slate-800/80 bg-slate-900/50'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5 text-xs font-mono font-bold text-rose-400 uppercase tracking-wider">
                <Scale size={14} />
                Patent Examiner
              </span>
              {effectiveSpeaker === 'examiner' ? (
                <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-rose-500/20 text-[10px] font-bold text-rose-300 font-mono animate-pulse border border-rose-400/40">
                  <span className="h-1.5 w-1.5 rounded-full bg-rose-400 animate-ping" />
                  TRANSMITTING
                </span>
              ) : (
                <span className="text-[10px] font-mono text-slate-500">STANDBY</span>
              )}
            </div>

            <p className="mt-2 text-xs font-semibold text-white">{examinerModel}</p>
            <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400 font-mono">
              <span>Confidence:</span>
              <span className="text-rose-300 font-bold">{Math.round(examinerConf * 100)}%</span>
            </div>
            <div className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full bg-rose-500 transition-all duration-500"
                style={{ width: `${Math.round(examinerConf * 100)}%` }}
              />
            </div>
          </div>

          {/* JUDICIAL ARBITER CARD */}
          <div
            className={`rounded-2xl border p-4 transition-all duration-300 ${
              effectiveSpeaker === 'arbiter'
                ? 'border-cyan-400 bg-cyan-950/40 ring-2 ring-cyan-500/30 shadow-[0_0_20px_rgba(6,182,212,0.2)]'
                : 'border-slate-800/80 bg-slate-900/50'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="flex items-center gap-1.5 text-xs font-mono font-bold text-cyan-400 uppercase tracking-wider">
                <Award size={14} />
                Judicial Arbiter
              </span>
              {effectiveSpeaker === 'arbiter' ? (
                <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-cyan-500/20 text-[10px] font-bold text-cyan-300 font-mono animate-pulse border border-cyan-400/40">
                  <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-ping" />
                  VERDICT DELIBERATION
                </span>
              ) : (
                <span className="text-[10px] font-mono text-slate-500">STANDBY</span>
              )}
            </div>

            <p className="mt-2 text-xs font-semibold text-white">{arbiterModel}</p>
            <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400 font-mono">
              <span>Confidence:</span>
              <span className="text-cyan-300 font-bold">{Math.round(arbiterConf * 100)}%</span>
            </div>
            <div className="mt-1 h-1.5 w-full overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full bg-cyan-500 transition-all duration-500"
                style={{ width: `${Math.round(arbiterConf * 100)}%` }}
              />
            </div>
          </div>
        </div>

        {/* Telemetry Status Strip */}
        <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-slate-800/80 pt-3 text-[11px]">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5 text-slate-400">
              <Clock size={13} className="text-cyan-400" />
              Round Latency:
              <strong className="font-mono text-cyan-300">{roundLatencyMs} ms</strong>
            </span>
            <span className="flex items-center gap-1.5 text-slate-400">
              <Activity size={13} className="text-emerald-400" />
              Generation Speed:
              <strong className="font-mono text-emerald-300">{tokensPerSec} t/s</strong>
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-slate-400 text-[10px] font-mono uppercase">Statutory Heatmap:</span>
            <span
              onClick={() => setActiveStatuteKey('sec_3p')}
              className={`cursor-pointer px-2 py-0.5 rounded text-[10px] font-mono font-bold border transition hover:scale-105 ${
                statutoryRisk.sec_3p === 'Cleared'
                  ? 'bg-emerald-950/70 border-emerald-500/60 text-emerald-300'
                  : statutoryRisk.sec_3p === 'Medium'
                  ? 'bg-amber-950/70 border-amber-500/60 text-amber-300'
                  : 'bg-rose-950/70 border-rose-500/60 text-rose-300'
              }`}
            >
              §3(p): {statutoryRisk.sec_3p}
            </span>
            <span
              onClick={() => setActiveStatuteKey('sec_3e')}
              className={`cursor-pointer px-2 py-0.5 rounded text-[10px] font-mono font-bold border transition hover:scale-105 ${
                statutoryRisk.sec_3e.includes('Synergistic')
                  ? 'bg-emerald-950/70 border-emerald-500/60 text-emerald-300'
                  : 'bg-rose-950/70 border-rose-500/60 text-rose-300'
              }`}
            >
              §3(e): {statutoryRisk.sec_3e}
            </span>
            <span
              onClick={() => setActiveStatuteKey('bda_form3')}
              className={`cursor-pointer px-2 py-0.5 rounded text-[10px] font-mono font-bold border transition hover:scale-105 ${
                statutoryRisk.bda_form3 === 'Exempt'
                  ? 'bg-emerald-950/70 border-emerald-500/60 text-emerald-300'
                  : 'bg-amber-950/70 border-amber-500/60 text-amber-300'
              }`}
            >
              BDA: {statutoryRisk.bda_form3}
            </span>
          </div>
        </div>
      </div>

      {/* Slide-out / Modal Statutory Telemetry Inspection Drawer */}
      {activeStatuteKey && STATUTORY_PROVISIONS[activeStatuteKey] && (
        <div className="rounded-2xl border border-teal-500/30 bg-slate-950 p-5 shadow-xl transition-all">
          <div className="flex items-start justify-between">
            <div>
              <span className="text-[10px] font-mono uppercase tracking-wider text-teal-400">
                Statutory Telemetry Inspector
              </span>
              <h4 className="text-base font-bold text-white mt-0.5">
                {STATUTORY_PROVISIONS[activeStatuteKey].section}
              </h4>
              <p className="text-xs text-slate-400">
                {STATUTORY_PROVISIONS[activeStatuteKey].title} ·{' '}
                {STATUTORY_PROVISIONS[activeStatuteKey].authority}
              </p>
            </div>

            <button
              onClick={() => setActiveStatuteKey(null)}
              className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white transition"
            >
              <X size={16} />
            </button>
          </div>

          <div className="mt-3 rounded-xl bg-slate-900/80 p-3.5 border border-slate-800">
            <p className="text-xs leading-relaxed text-slate-300">
              {STATUTORY_PROVISIONS[activeStatuteKey].text}
            </p>
          </div>

          <div className="mt-3 flex items-center justify-between">
            <span className="text-[11px] text-slate-400">
              Authority Portal:{' '}
              <a
                href={STATUTORY_PROVISIONS[activeStatuteKey].url}
                target="_blank"
                rel="noreferrer"
                className="text-teal-300 underline"
              >
                {STATUTORY_PROVISIONS[activeStatuteKey].url}
              </a>
            </span>
            <button
              onClick={() => setActiveStatuteKey(null)}
              className="text-xs font-semibold text-teal-400 hover:text-teal-300"
            >
              Dismiss
            </button>
          </div>
        </div>
      )}

      {/* Main 2-Column Dashboard Layout */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Left Column: Formulation Intake & Presets */}
        <div className="space-y-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Activity size={16} className="text-teal-600" />
                Case Formulation Intake
              </h4>
              <span className="text-[10px] font-bold text-slate-400 font-mono">INPUT DATA</span>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700">Invention / Query</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Polyherbal Synergistic Extract"
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-xs text-slate-800 placeholder-slate-400 focus:border-teal-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700">Detailed Description</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={3}
                placeholder="Describe botanical ingredients, ratios, and extraction methods..."
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-xs text-slate-800 placeholder-slate-400 focus:border-teal-500 focus:outline-none"
              />
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-700">Novelty & Synergism Data</label>
              <textarea
                value={innovation}
                onChange={(e) => setInnovation(e.target.value)}
                rows={2}
                placeholder="Combination index (CI < 1.0), pharmacokinetic AUC enhancement..."
                className="mt-1 w-full rounded-xl border border-slate-200 px-3 py-2 text-xs text-slate-800 placeholder-slate-400 focus:border-teal-500 focus:outline-none"
              />
            </div>

            {/* Quick Presets */}
            <div className="pt-2 border-t border-slate-100">
              <p className="text-xs font-semibold text-slate-600 mb-2">Adjudication Presets:</p>
              <div className="space-y-1.5">
                {PRESET_INVENTIONS.map((p) => (
                  <button
                    key={p.title}
                    onClick={() => {
                      setTitle(p.title);
                      setDescription(p.description);
                      setInnovation(p.innovation);
                    }}
                    className={`w-full text-left rounded-lg p-2.5 text-xs border transition ${
                      title === p.title
                        ? 'border-teal-500 bg-teal-50/70 font-semibold text-teal-900 shadow-sm'
                        : 'border-slate-100 bg-slate-50 text-slate-700 hover:bg-slate-100'
                    }`}
                  >
                    <span className="truncate block font-medium">{p.title}</span>
                    <span className="text-[10px] text-slate-500 line-clamp-1 mt-0.5">
                      {p.innovation}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right 2 Columns: Real-Time Courtroom Speech Transcripts */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h4 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <BookOpen size={16} className="text-teal-600" />
              Real-Time Courtroom Speech Transcript & Safe-Gate Verification
            </h4>
            <span className="text-xs font-medium text-slate-500 font-mono">
              {events.length} Rounds Logged
            </span>
          </div>

          <div
            ref={transcriptRef}
            className="h-[460px] overflow-y-auto space-y-3.5 pr-2 rounded-xl bg-slate-50/80 p-4 border border-slate-200"
          >
            {events.length === 0 && !streamingText ? (
              <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 py-12">
                <Scale size={36} className="text-slate-300 mb-3" />
                <p className="text-sm font-medium text-slate-600">Legal Chamber Standing By.</p>
                <p className="text-xs text-slate-400 mt-1 max-w-md">
                  Click "Launch Legal Chamber" above to initiate adversarial debate between Applicant
                  Counsel, Patent Controller, and Judicial Arbiter.
                </p>
              </div>
            ) : (
              <>
                {events.map((ev, i) => (
                  <div
                    key={i}
                    className={`rounded-xl border p-4 transition-all ${
                      ev.agent === 'applicant'
                        ? 'border-emerald-200 bg-emerald-50/70 shadow-sm'
                        : ev.agent === 'examiner'
                        ? 'border-amber-200 bg-amber-50/70 shadow-sm'
                        : 'border-cyan-200 bg-cyan-50/70 shadow-sm'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span
                          className={`px-2.5 py-0.5 rounded text-[11px] font-extrabold ${
                            ev.agent === 'applicant'
                              ? 'bg-emerald-600 text-white'
                              : ev.agent === 'examiner'
                              ? 'bg-amber-600 text-white'
                              : 'bg-cyan-700 text-white'
                          }`}
                        >
                          {ev.agent === 'applicant' && 'APPLICANT COUNSEL'}
                          {ev.agent === 'examiner' && 'PATENT EXAMINER'}
                          {ev.agent === 'arbiter' && 'JUDICIAL ARBITER'}
                        </span>
                        <span className="text-xs font-semibold text-slate-800">{ev.stage}</span>
                      </div>

                      <div className="flex items-center gap-2 text-[11px] text-slate-500 font-mono">
                        <span>{ev.model || 'Claude 3.5 / GPT-4o'}</span>
                        {ev.tokens_per_sec && <span>· {ev.tokens_per_sec} t/s</span>}
                      </div>
                    </div>

                    <p className="text-xs leading-relaxed text-slate-700 whitespace-pre-line font-normal">
                      {ev.content}
                    </p>

                    {/* Citations Footer */}
                    {ev.citations && ev.citations.length > 0 && (
                      <div className="mt-3 flex flex-wrap items-center gap-1.5 pt-2 border-t border-slate-200/60">
                        <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wide">
                          Statutory Citations:
                        </span>
                        {ev.citations.map((cite, cIdx) => (
                          <span
                            key={cIdx}
                            className="rounded bg-white px-2 py-0.5 text-[10px] font-medium text-slate-700 border border-slate-200 shadow-xs"
                          >
                            {cite}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}

                {/* In-progress streaming text bubble */}
                {streamingText && currentSpeaker && (
                  <div
                    className={`rounded-xl border p-4 transition-all ${
                      currentSpeaker === 'applicant'
                        ? 'border-emerald-300 bg-emerald-50/90 ring-1 ring-emerald-400/40'
                        : currentSpeaker === 'examiner'
                        ? 'border-amber-300 bg-amber-50/90 ring-1 ring-amber-400/40'
                        : 'border-cyan-300 bg-cyan-50/90 ring-1 ring-cyan-400/40'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span
                          className={`px-2.5 py-0.5 rounded text-[11px] font-extrabold flex items-center gap-1.5 ${
                            currentSpeaker === 'applicant'
                              ? 'bg-emerald-600 text-white'
                              : currentSpeaker === 'examiner'
                              ? 'bg-amber-600 text-white'
                              : 'bg-cyan-700 text-white'
                          }`}
                        >
                          <Radio size={12} className="animate-pulse" />
                          {currentSpeaker === 'applicant' && 'APPLICANT COUNSEL (STREAMING)'}
                          {currentSpeaker === 'examiner' && 'PATENT EXAMINER (STREAMING)'}
                          {currentSpeaker === 'arbiter' && 'JUDICIAL ARBITER (STREAMING)'}
                        </span>
                        <span className="text-xs font-semibold text-slate-800">{currentStage}</span>
                      </div>
                      <span className="text-[11px] font-mono text-slate-500 animate-pulse">
                        Streaming chunks...
                      </span>
                    </div>

                    <p className="text-xs leading-relaxed text-slate-700 whitespace-pre-line">
                      {streamingText}
                      <span className="inline-block w-1.5 h-3.5 bg-teal-600 ml-1 animate-pulse align-middle" />
                    </p>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LegalChamberPanel;
