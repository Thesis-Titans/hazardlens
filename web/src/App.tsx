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
              <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                Prototype v0.1.0
              </span>
            </h1>
            <p className="text-xs text-slate-400">
              Evidence-First Philippine Hazard Information
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3 text-xs text-slate-400">
          <span
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-amber-950/50 border border-amber-800/60 text-amber-300"
            role="status"
            aria-label="Project status: prototype scaffold; live integrations are not connected"
          >
            <span className="w-2 h-2 rounded-full bg-amber-400"></span>
            Prototype scaffold
          </span>
        </div>
      </header>

      <main className="flex-1 max-w-5xl w-full mx-auto px-6 py-12 flex flex-col items-center justify-center text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-medium mb-6">
          <Compass className="w-3.5 h-3.5" />
          Development baseline
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mb-4">
          Evidence First. AI Second.
        </h2>
        <p className="text-slate-400 max-w-2xl text-base sm:text-lg mb-8">
          HazardLens is being built to help people explore what official Philippine hazard datasets report about a selected place. This prototype does not yet perform live hazard lookups. Source integrations, the investigation API, evidence cards, and grounded AI are still under development.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-3xl w-full text-left">
          <div className="p-5 rounded-xl bg-slate-900/50 border border-slate-800">
            <div className="text-emerald-400 font-semibold text-sm mb-1">Official sources planned</div>
            <p className="text-xs text-slate-400">
              MGB and PHIVOLCS integrations will be verified against their published services before evidence is presented.
            </p>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/50 border border-slate-800">
            <div className="text-blue-400 font-semibold text-sm mb-1">Evidence states planned</div>
            <p className="text-xs text-slate-400">
              Results will distinguish findings, valid empty results, coverage limits, unavailable sources, and unsupported operations.
            </p>
          </div>
          <div className="p-5 rounded-xl bg-slate-900/50 border border-slate-800">
            <div className="text-purple-400 font-semibold text-sm mb-1">AI is optional</div>
            <p className="text-xs text-slate-400">
              AI explanations will be considered after source evidence is available. Core hazard lookup must not depend on AI.
            </p>
          </div>
        </div>
      </main>

      <footer className="border-t border-slate-900 px-6 py-4 text-center text-xs text-slate-500 flex items-center justify-center gap-2">
        <FileCheck className="w-3.5 h-3.5" />
        HazardLens is a web-systems technology practice project, not an official hazard assessment. This prototype does not yet provide live hazard results. Absence of data must never be interpreted as safety.
      </footer>
    </div>
  );
};

export default App;
