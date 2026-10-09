import React from 'react';
import { ShieldAlert, Compass, FileCheck } from 'lucide-react';

export const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
              HazardLens
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800/60">
                Baseline v0.1.0
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              Evidence-First Philippine Hazard Intelligence
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 text-xs text-slate-400">
          <span className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-slate-800/80 border border-slate-700/60">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            System Ready
          </span>
        </div>
      </header>

      <main className="flex-1 max-w-5xl w-full mx-auto px-6 py-12 flex flex-col items-center justify-center text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-medium mb-6">
          <Compass className="w-3.5 h-3.5" />
          Sprint 1 — Foundation Architecture
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mb-4">
          Evidence First. AI Second.
        </h2>
        <p className="text-slate-400 max-w-2xl text-base sm:text-lg mb-8">
          Authoritative multi-hazard lookup across MGB flood, rain-induced landslide, PHIVOLCS liquefaction, and active faults in the Philippines.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-3xl w-full text-left">
          <div className="p-5 rounded-xl bg-slate-900/50 border border-slate-800 hover:border-slate-700 transition">
            <div className="text-emerald-400 font-semibold text-sm mb-1">Authoritative Sources</div>
            <p className="text-xs text-slate-400">Direct integration with official agency GIS services.</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/50 border border-slate-800 hover:border-slate-700 transition">
            <div className="text-blue-400 font-semibold text-sm mb-1">5 Rigorous Statuses</div>
            <p className="text-xs text-slate-400">Never map missing evidence or network timeouts to "safe".</p>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/50 border border-slate-800 hover:border-slate-700 transition">
            <div className="text-purple-400 font-semibold text-sm mb-1">Grounded AI Analysis</div>
            <p className="text-xs text-slate-400">AI explains and queries evidence without hallucinating facts.</p>
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-900 px-6 py-4 text-center text-xs text-slate-500 flex items-center justify-center gap-2">
        <FileCheck className="w-3.5 h-3.5" />
        HazardLens is a web-systems technology practice project. Source data is retrieved from government services and displayed as published.
      </footer>
    </div>
  );
};

export default App;
