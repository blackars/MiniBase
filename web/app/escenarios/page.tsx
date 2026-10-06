"use client";
import { useEffect, useState } from "react";

// MAQUETA Escenarios — botones no funcionales + placeholders.
// Módulos futuros (cada uno con su API): ficha, partes, tile-editor, montajes,
// iluminación, audio, correlator minis↔escenarios. La DB vendrá después.
const TABS = ["Ficha", "Partes", "Editor Tile", "Montajes", "Iluminación", "Audio", "API"];

function Soon({ label }: { label: string }) {
  const [n, setN] = useState(0);
  return (<button onClick={() => setN(n + 1)}
    className="text-xs bg-zinc-800 border border-zinc-700 rounded px-3 py-2 hover:border-emerald-400">
    {label}{n > 0 && <span className="text-amber-400"> · próximamente ({n})</span>}
  </button>);
}

function Ph({ label, h = "h-24" }: { label: string; h?: string }) {
  return (<div className={`bg-zinc-900 border border-dashed border-zinc-700 rounded flex items-center justify-center ${h}`}>
    <span className="text-xs text-zinc-600">{label} · placeholder</span>
  </div>);
}

export default function Escenarios() {
  const [ok, setOk] = useState(false);
  const [tab, setTab] = useState("Ficha");

  useEffect(() => {
    try {
      const raw = localStorage.getItem("mb_session");
      if (!raw || !JSON.parse(raw)?.access_token) location.href = "/";
      else setOk(true);
    } catch { location.href = "/"; }
  }, []);

  if (!ok) return (<main className="p-6"><p className="text-zinc-500 text-sm">Verificando acceso…</p></main>);

  return (<main className="p-6 max-w-6xl mx-auto">
    <a href="/" className="text-zinc-400 text-sm">← Volver</a>
    <h1 className="text-2xl font-bold mt-2">◈ Escenarios <span className="text-xs text-amber-400 font-normal border border-amber-900 rounded px-2 py-0.5 ml-2">MAQUETA</span></h1>
    <p className="text-xs text-zinc-500 mt-1">Escenarios para pantalla o proyección. Contexto para el modelo gestor y el narrador.</p>

    <div className="flex gap-1 mt-4 flex-wrap">
      {TABS.map(t => (
        <button key={t} onClick={() => setTab(t)}
          className={`text-xs rounded px-3 py-2 border ${tab === t ? "bg-white text-black font-semibold" : "bg-zinc-900 border-zinc-800"}`}>{t}</button>))}
    </div>

    {tab === "Ficha" && (
      <section className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="bg-zinc-900 border border-zinc-800 rounded p-4">
          <h2 className="font-bold text-sm">Ficha del escenario</h2>
          {[["Nombre", "Bosque Élfico — claro central"], ["Tipo", "físico / digital / híbrido"],
            ["Medidas", "60 × 60 cm · tiles 10cm"], ["Colores", "verde, marrón, niebla"],
            ["Textura", "musgo, corteza, piedra"], ["Usos posibles", "emboscada, ritual, descanso"],
            ["Descripción", "Claro circular con piedras rúnicas…"], ["Comentarios", ""],
            ["URL referencia", ""]].map(([k, v]) => (
            <div key={k} className="flex gap-2 mt-1 text-sm">
              <span className="text-zinc-500 w-32 shrink-0 text-xs pt-0.5">{k}</span>
              <span className="text-zinc-300">{v || "—"}</span>
            </div>))}
          <div className="flex gap-2 mt-3 flex-wrap">
            <Soon label="＋ Nuevo escenario" /><Soon label="✎ Editar ficha" /><Soon label="⧉ Duplicar" />
          </div>
        </div>
        <div>
          <Ph label="portada del escenario 16:9" h="h-40" />
          <div className="grid grid-cols-3 gap-1 mt-1">
            <Ph label="variación día" /><Ph label="variación noche" /><Ph label="variación niebla" />
          </div>
        </div>
      </section>)}

    {tab === "Partes" && (
      <section className="mt-4">
        <h2 className="font-bold text-sm">Partes y variaciones (reutilizables por el modelo)</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2">
          {["suelo bosque", "río", "puente", "claro rúnico", "ladera", "cueva", "ruina", "camino"].map(p => (
            <Ph key={p} label={`parte · ${p}`} />))}
        </div>
        <div className="flex gap-2 mt-3 flex-wrap">
          <Soon label="＋ Nueva parte" /><Soon label="Variaciones de parte" /><Soon label="Medidas por parte" />
        </div>
      </section>)}

    {tab === "Editor Tile" && (
      <section className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="md:col-span-2 bg-zinc-900 border border-zinc-800 rounded p-3">
          <h2 className="font-bold text-sm">Canvas 12 × 8 (mock)</h2>
          <div className="grid grid-cols-12 gap-px mt-2 bg-zinc-800 border border-zinc-800">
            {Array.from({ length: 96 }).map((_, i) => (
              <div key={i} className={`aspect-square ${i % 7 === 0 ? "bg-emerald-900" : i % 5 === 0 ? "bg-sky-900" : "bg-zinc-900"}`} />))}
          </div>
        </div>
        <div className="bg-zinc-900 border border-zinc-800 rounded p-3">
          <h2 className="font-bold text-sm">Presets del modelo</h2>
          <div className="grid gap-1 mt-2">
            {["bosque denso 12×8", "aldea + río", "mazmorra 3 niveles", "desierto + oasis"].map(p => (
              <Soon key={p} label={p} />))}
          </div>
          <div className="flex gap-2 mt-3 flex-wrap">
            <Soon label="Guardar preset" /><Soon label="Exportar mapa" />
          </div>
        </div>
      </section>)}

    {tab === "Montajes" && (
      <section className="mt-4">
        <h2 className="font-bold text-sm">Ejemplos de montaje: escenario + escenografía (de tu base) + minis</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-2 mt-2">
          {[1, 2, 3].map(i => (
            <div key={i}>
              <Ph label={`montaje ejemplo ${i}`} h="h-36" />
              <p className="text-xs text-zinc-500 mt-1">escenografía: — · minis: — (correlación futura)</p>
            </div>))}
        </div>
        <div className="flex gap-2 mt-3 flex-wrap">
          <Soon label="Combinar PNGs" /><Soon label="Correlacionar minis" /><Soon label="Guardar montaje" />
        </div>
      </section>)}

    {tab === "Iluminación" && (
      <section className="mt-4">
        <h2 className="font-bold text-sm">Ejemplos de iluminación</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2">
          {["día", "atardecer", "noche + antorchas", "niebla + luna"].map(l => (
            <Ph key={l} label={l} />))}
        </div>
        <div className="flex gap-2 mt-3 flex-wrap">
          <Soon label="Preset día/noche" /><Soon label="Enviar al proyector" />
        </div>
      </section>)}

    {tab === "Audio" && (
      <section className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="bg-zinc-900 border border-zinc-800 rounded p-4">
          <h2 className="font-bold text-sm">Soundtrack del escenario</h2>
          <Ph label="player · bosque_noche.mp3" h="h-16" />
          <div className="flex gap-2 mt-2 flex-wrap">
            <Soon label="Subir soundtrack" /><Soon label="Por género" />
          </div>
        </div>
        <div className="bg-zinc-900 border border-zinc-800 rounded p-4">
          <h2 className="font-bold text-sm">Efectos por zona/género</h2>
          {["pasos en hojas", "agua", "ritual", "combate"].map(s => (
            <div key={s} className="flex items-center gap-2 mt-1">
              <span className="text-xs flex-1">{s}</span><Soon label="▶" /><Soon label="subir" />
            </div>))}
        </div>
      </section>)}

    {tab === "API" && (
      <section className="mt-4 bg-zinc-900 border border-zinc-800 rounded p-4">
        <h2 className="font-bold text-sm">Microservicios futuros (diseño modular)</h2>
        <ul className="text-xs text-zinc-400 mt-2 space-y-1 font-mono">
          <li>GET /api/scenarios — lista + filtros por género/tipo</li>
          <li>POST /api/scenarios — crear ficha (fases: ficha → partes → tile → audio)</li>
          <li>GET /api/scenarios/{"{id}"}/parts — partes y variaciones</li>
          <li>POST /api/scenarios/{"{id}"}/tile/presets — guardar preset del editor</li>
          <li>GET /api/scenarios/{"{id}"}/montajes — ejemplos con escenografía + minis</li>
          <li>POST /api/scenarios/{"{id}"}/project — enviar al proyector (fase, grid, luz)</li>
          <li>GET /api/scenarios/{"{id}"}/dataset — contexto para el narrador/DM</li>
        </ul>
        <p className="text-xs text-zinc-600 mt-2">Cada tarjeta de esta maqueta será un microservicio con su tabla. La DB se diseña sobre esta maqueta.</p>
      </section>)}
  </main>);
}
