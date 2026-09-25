import json

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Adiós a las contraseñas: FIDO2 y WebAuthn</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #080c10;
            --bg-light: #0f172a;
            --primary: #10b981;
            --primary-light: #84cc16;
            --secondary: #fbbf24;
            --secondary-dark: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --danger: #ef4444;
        }
        
        body, html { margin: 0; padding: 0; width: 100%; height: 100%; overflow: hidden; background: linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-light) 100%); color: var(--text-main); font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }
        
        .slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; opacity: 0; visibility: hidden; transition: opacity 0.4s ease, transform 0.4s ease; transform: translateX(30px) scale(0.98); padding: 4rem; box-sizing: border-box; }
        .slide.active { opacity: 1; visibility: visible; transform: translateX(0) scale(1); z-index: 10; }
        .slide.prev { transform: translateX(-30px) scale(0.98); }
        
        .progress-bar { position: fixed; top: 0; left: 0; height: 4px; background: linear-gradient(90deg, var(--primary), var(--secondary)); transition: width 0.3s ease; z-index: 50; box-shadow: 0 0 10px rgba(16,185,129,0.5); }
        .slide-counter { position: fixed; bottom: 1.5rem; right: 1.5rem; font-size: 1rem; font-weight: 600; font-family: 'Fira Code', monospace; color: var(--primary); z-index: 50; background: rgba(8, 12, 16, 0.8); padding: 0.5rem 1rem; border-radius: 9999px; border: 1px solid var(--primary-light); box-shadow: 0 0 10px rgba(16,185,129,0.2); }
        
        h1 { font-size: 4rem; font-weight: 800; margin-bottom: 1.5rem; background: linear-gradient(to right, var(--secondary), var(--primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; line-height: 1.2; letter-spacing: -0.02em; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5)); }
        h2 { font-size: 3rem; font-weight: 700; margin-bottom: 2rem; background: linear-gradient(to right, var(--secondary), var(--primary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; letter-spacing: -0.01em; }
        h3 { font-size: 1.75rem; font-weight: 600; margin-bottom: 1rem; color: var(--text-main); }
        p { font-size: 1.5rem; line-height: 1.6; margin-bottom: 1rem; max-width: 1000px; text-align: center; color: var(--text-muted); }
        ul { font-size: 1.35rem; line-height: 1.6; color: var(--text-muted); list-style-type: none; padding: 0; max-width: 900px; }
        li { margin-bottom: 1rem; position: relative; padding-left: 2rem; text-align: left; }
        li::before { content: "»"; position: absolute; left: 0; color: var(--primary); font-weight: bold; }
        
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; width: 100%; max-width: 1200px; align-items: center; justify-items: center; }
        
        /* Glassmorphism Cards */
        .card { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 1rem; padding: 2.5rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 0 20px rgba(16, 185, 129, 0.05); width: 100%; }
        
        /* Glow Cards for replacing emojis */
        .glow-card { display: inline-flex; justify-content: center; align-items: center; width: 4rem; height: 4rem; border-radius: 1rem; background: rgba(16, 185, 129, 0.1); border: 1px solid var(--primary); box-shadow: 0 0 15px rgba(16, 185, 129, 0.3); color: var(--primary); margin-bottom: 1rem; }
        
        /* Duct Tape style */
        .duct-tape-container { position: relative; padding-top: 2rem; }
        .duct-tape {
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%) rotate(-1.5deg);
            width: 160px;
            height: 40px;
            background: linear-gradient(180deg, #9ca3af 0%, #d1d5db 40%, #9ca3af 100%);
            border-top: 1px dashed #6b7280;
            border-bottom: 1px dashed #6b7280;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), inset 0 2px 4px rgba(255,255,255,0.3);
            z-index: 20;
            opacity: 0.9;
            clip-path: polygon(2% 0, 98% 2%, 100% 98%, 0 100%);
        }
        
        /* Terminal Code Blocks */
        .code-window { width: 100%; max-width: 1000px; border-radius: 0.75rem; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 20px rgba(16,185,129,0.1); border: 1px solid rgba(148, 163, 184, 0.2); }
        .window-header { background: #1e293b; padding: 0.75rem 1rem; display: flex; gap: 0.5rem; align-items: center; border-bottom: 1px solid rgba(0,0,0,0.2); }
        .dot { width: 12px; height: 12px; border-radius: 50%; }
        .dot.red { background: #ff5f56; }
        .dot.yellow { background: #ffbd2e; }
        .dot.green { background: #27c93f; }
        pre { background: #0b0f14; padding: 1.5rem; margin: 0; overflow-x: auto; font-family: 'Fira Code', monospace; font-size: 1.2rem; text-align: left; line-height: 1.6; }
        code { font-family: 'Fira Code', monospace; color: #e2e8f0; }
        .keyword { color: #c678dd; } /* Purple */
        .string { color: #98c379; } /* Green */
        .comment { color: #5c6370; font-style: italic; } /* Gray */
        .function { color: #61afef; } /* Blue */
        .property { color: #d19a66; } /* Orange */
        .highlight { color: var(--secondary); font-weight: 700; text-shadow: 0 0 8px rgba(245,158,11,0.5); }
        
        .badge { display: inline-block; padding: 0.5rem 1.5rem; background: rgba(16, 185, 129, 0.1); border: 1px solid var(--primary); border-radius: 9999px; font-size: 1.1rem; font-weight: 600; color: var(--primary); box-shadow: 0 0 10px rgba(16,185,129,0.2); }
        .badge.danger { background: rgba(239, 68, 68, 0.1); border-color: var(--danger); color: #fca5a5; box-shadow: 0 0 10px rgba(239, 68, 68, 0.2); }
        
        /* SVG Diagrams (Cyberpunk/Neon) */
        svg { max-width: 100%; height: auto; overflow: visible; filter: drop-shadow(0 0 5px rgba(0,0,0,0.5)); }
        .diagram-box { fill: rgba(15,23,42,0.8); stroke: var(--primary); stroke-width: 2; rx: 12; filter: drop-shadow(0 0 10px rgba(16,185,129,0.4)); }
        .diagram-box.danger { stroke: var(--danger); filter: drop-shadow(0 0 10px rgba(239,68,68,0.4)); }
        .diagram-text { fill: var(--text-main); font-size: 16px; font-weight: 600; dominant-baseline: middle; text-anchor: middle; }
        .diagram-arrow { stroke: var(--secondary); stroke-width: 3; fill: none; marker-end: url(#arrowhead); stroke-dasharray: 8; animation: dash 20s linear infinite; filter: drop-shadow(0 0 5px rgba(245,158,11,0.5)); }
        .diagram-arrow-solid { stroke: var(--secondary); stroke-width: 3; fill: none; marker-end: url(#arrowhead); filter: drop-shadow(0 0 5px rgba(245,158,11,0.5)); }
        @keyframes dash { to { stroke-dashoffset: -1000; } }
        
        .pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 15px rgba(16,185,129,0.4); } 50% { opacity: .8; transform: scale(1.02); box-shadow: 0 0 25px rgba(16,185,129,0.8); } }
        
        .img-glow { border-radius: 1rem; border: 1px solid rgba(16,185,129,0.3); }
    </style>
</head>
<body>
    <div class="progress-bar" id="progress"></div>
    <div class="slide-counter" id="counter">1 / 26</div>

    <svg width="0" height="0" style="position:absolute;">
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#f59e0b" />
            </marker>
        </defs>
    </svg>

    <!-- Icons definitions (Lucide/Heroicons inspired) -->
    <svg style="display:none;">
        <symbol id="icon-dog" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 5.172C10 3.782 8.423 2.679 8.328 2.617a1.5 1.5 0 0 0-2.099.182L5 4.5 2.5 7v4.5l2 2v4l3 3h3v-3l2-2h4l2 2h3v-3l3-3V7.5L20 5l-2.229-1.701a1.5 1.5 0 0 0-2.099-.182L15 4.5v.672C15 6.562 13.88 7.5 12.5 7.5S10 6.562 10 5.172z"/></symbol>
        <symbol id="icon-globe" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/><path d="M2 12h20"/></symbol>
        <symbol id="icon-bot" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></symbol>
        <symbol id="icon-skull" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="9" cy="12" r="1"/><circle cx="15" cy="12" r="1"/><path d="M8 20v2h8v-2"/><path d="m12.5 17-.5-1-.5 1h1z"/><path d="M16 20a2 2 0 0 0 1.56-3.25 8 8 0 1 0-11.12 0A2 2 0 0 0 8 20"/></symbol>
        <symbol id="icon-bank" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 10h16v10H4z"/><path d="M2 22h20"/><path d="M12 2 2 8h20z"/><path d="M8 10v10"/><path d="M16 10v10"/></symbol>
        <symbol id="icon-plug" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/></symbol>
        <symbol id="icon-fingerprint" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 12C2 6.5 6.5 2 12 2a10 10 0 0 1 8 4"/><path d="M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2"/><path d="M8.65 22c.21-.66.45-1.32.57-2"/><path d="M11.5 22c.19-.92.35-1.5.5-2"/><path d="M15.5 22c-.22-1.28-.48-2.61-.83-4"/><path d="M19 18.5c-.32-1.31-.69-2.68-1.12-4"/><path d="M8.5 13a4 4 0 0 1 7 0"/><path d="M5.5 12a6.5 6.5 0 0 1 13 0"/></symbol>
        <symbol id="icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></symbol>
        <symbol id="icon-laptop" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="2" y1="20" x2="22" y2="20"/></symbol>
        <symbol id="icon-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="2" width="14" height="20" rx="2"/><line x1="12" y1="18" x2="12" y2="18"/></symbol>
        <symbol id="icon-key" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></symbol>
        <symbol id="icon-cookie" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-5-5 4 4 0 0 1-5-5"/><path d="M8.5 8.5v.01"/><path d="M16 15.5v.01"/><path d="M12 12v.01"/><path d="M11 17v.01"/><path d="M7 14v.01"/></symbol>
        <symbol id="icon-wrench" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></symbol>
        <symbol id="icon-eye-off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" y1="2" x2="22" y2="22"/></symbol>
    </svg>

    <!-- Slide 1 -->
    <div class="slide">
        <div class="badge mb-8 border-primary text-primary">Con el apoyo y hardware de Nitrokey</div>
        <h1>Adiós a las contraseñas: FIDO2 y WebAuthn,<br>del concepto al código (y a tu propia llave de seguridad)</h1>
        <p class="text-2xl mt-8 text-primary-light font-mono font-bold tracking-widest">Paralelo 37 · XauenDevs · Jaén</p>
    </div>

    <!-- Slide 2 -->
    <div class="slide">
        <h2>¿Quién demonios soy yo?</h2>
        <div class="grid-2">
            <div class="flex justify-center">
                <svg viewBox="0 0 200 200" class="w-64 h-64 filter drop-shadow-[0_0_20px_rgba(16,185,129,0.3)]">
                    <circle cx="100" cy="100" r="100" fill="rgba(15,23,42,0.8)" stroke="#10b981" stroke-width="2"/>
                    <path d="M50,180 Q100,100 150,180" fill="none" stroke="#f59e0b" stroke-width="8" stroke-linecap="round"/>
                    <circle cx="100" cy="70" r="35" fill="#10b981"/>
                </svg>
            </div>
            <div>
                <ul>
                    <li><strong class="text-primary-light">Antonio Tirado Peña.</strong></li>
                    <li>Ingeniero Técnico en Informática de Gestión (UJA, de la tierra).</li>
                    <li>Director de TI y Estrategia en IICE / NormaPro.</li>
                    <li>Cacharreador compulsivo: Linux (Arch, por supuesto), servidores caseros con Docker, soldador, microcontroladores y cacharros varios.</li>
                </ul>
                <div class="mt-8 flex gap-6 text-secondary text-xl font-mono">
                    <span class="px-3 py-1 bg-secondary-dark/10 border border-secondary/30 rounded">github.com/xtoxico</span>
                    <span class="px-3 py-1 bg-secondary-dark/10 border border-secondary/30 rounded">normapro.es</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Slide 3 -->
    <div class="slide">
        <h2>Desmitificando la sopa de letras (Nota mental)</h2>
        <div class="card w-full max-w-4xl text-left border-dashed duct-tape-container">
            <div class="duct-tape"></div>
            <div class="border-b border-primary/20 pb-6 mb-6 mt-4">
                <h3 class="flex items-center gap-6 text-2xl">
                    <div class="glow-card"><svg class="w-8 h-8"><use href="#icon-dog"></use></svg></div>
                    <span><span class="highlight">FIDO2</span> no es una raza de perro ni un Pokémon.</span>
                </h3>
            </div>
            <div class="border-b border-primary/20 pb-6 mb-6">
                <h3 class="flex items-center gap-6 text-2xl">
                    <div class="glow-card"><svg class="w-8 h-8"><use href="#icon-globe"></use></svg></div>
                    <span><span class="highlight">WebAuthn</span> no es la nueva red social para programadores solitarios.</span>
                </h3>
            </div>
            <div>
                <h3 class="flex items-center gap-6 text-2xl">
                    <div class="glow-card"><svg class="w-8 h-8"><use href="#icon-bot"></use></svg></div>
                    <span><span class="highlight">CTAP2</span> no es el primo hermano de R2-D2.</span>
                </h3>
            </div>
        </div>
    </div>

    <!-- Slide 4 -->
    <div class="slide">
        <h2>El auténtico problema: Este es Alberto</h2>
        <div class="grid-2">
            <div class="flex justify-center w-full">
                <img src="assets/images/alberto_password.jpg" alt="Alberto y su Password" class="img-glow drop-shadow-[0_20px_50px_rgba(245,158,11,0.2)] w-full h-auto object-cover aspect-video">
            </div>
            <div class="card">
                <p class="text-left text-xl"><strong>Correo:</strong> <span class="text-primary-light">albertthegreat@hotmail.com</span></p>
                <p class="text-left text-sm text-text-muted mb-6">(creado en 2004)</p>
                <p class="text-left text-xl"><strong>Contraseña maestra:</strong> <span class="font-mono text-danger font-bold tracking-widest bg-danger/10 px-2 py-1 rounded">P4$$w0rd</span></p>
                <div class="mt-8 p-6 bg-bg-dark rounded-lg border border-primary/30 relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1 h-full bg-secondary"></div>
                    <p class="text-lg italic text-text-main">"Lleva una mayúscula, un cuatro, dos dólares y un cero. Es criptografía cuántica."</p>
                    <p class="text-right text-sm text-text-muted mt-4">— Motivo de su orgullo</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Slide 5 -->
    <div class="slide">
        <h2>Alberto en el mundo real</h2>
        <div class="relative w-full max-w-5xl">
            <div class="absolute inset-0 z-0">
                <img src="assets/images/have_i_been_pwned.jpg" alt="Data Breach" class="w-full h-full object-cover img-glow opacity-40">
            </div>
            <div class="card bg-bg-dark/80 border-danger z-10 relative flex flex-col items-center py-12">
                <h1 class="text-danger font-mono text-7xl mb-4 tracking-tighter" style="background:none;-webkit-text-fill-color:var(--danger);filter:drop-shadow(0 0 10px rgba(239,68,68,0.8));">YOU'VE BEEN PWNED!</h1>
                <p class="text-2xl mb-8 font-mono text-text-main">haveibeenpwned.com</p>
                <p class="text-xl mb-12 text-center text-text-main font-semibold">El foro de petancas de Albacete guardaba las contraseñas en MD5 plano en un MySQL de 2011.</p>
                <div class="flex gap-6 w-full justify-center">
                    <div class="badge danger text-center w-auto py-3 px-8 text-xl">Steam 🔓</div>
                    <div class="badge danger text-center w-auto py-3 px-8 text-xl">Intranet 🔓</div>
                    <div class="badge danger text-center w-auto py-3 px-8 text-xl">Banco 🔓</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Slide 6 -->
    <div class="slide">
        <h2>El parche infinito (BriConsejo de Seguridad)</h2>
        <p class="text-xl text-primary-light mb-10 font-mono">Treinta años metiéndole parches a algo roto por diseño</p>
        <div class="grid grid-cols-2 gap-6 w-full max-w-5xl duct-tape-container">
            <div class="duct-tape" style="top: -5px; transform: translateX(-50%) rotate(1.5deg);"></div>
            <div class="card bg-bg-dark border-primary/30">
                <h3 class="text-xl text-primary">Complejidad absurda</h3>
                <p class="text-lg text-left m-0">Mayúsculas, minúsculas, números, caracteres raros y el grupo sanguíneo.</p>
            </div>
            <div class="card bg-bg-dark border-primary/30">
                <h3 class="text-xl text-primary">Caducidad</h3>
                <p class="text-lg text-left m-0">"Tu contraseña caduca en 90 días" <br>→ <span class="font-mono text-secondary">Primavera2026!</span>, <span class="font-mono text-secondary">Verano2026!</span></p>
            </div>
            <div class="card bg-bg-dark border-primary/30">
                <h3 class="text-xl text-primary">SMS 2FA</h3>
                <p class="text-lg text-left m-0">SIM swapping te saluda con la mano.</p>
            </div>
            <div class="card bg-bg-dark border-primary/30">
                <h3 class="text-xl text-primary">Apps autenticadoras</h3>
                <p class="text-lg text-left m-0">Fatiga de push: le das a "Aceptar" a las 3 AM solo para que el móvil se calle.</p>
            </div>
        </div>
    </div>

    <!-- Slide 7 -->
    <div class="slide">
        <h2>El cambio de paradigma: Clave pública vs Secreto compartido</h2>
        <div class="grid-2 mt-8">
            <div class="card text-center border-danger bg-danger/5">
                <h3 class="text-danger">Tradicional</h3>
                <div class="text-6xl my-8 font-mono">🧑 ↔️ 🔑 ↔️ 🖥️</div>
                <p class="text-lg text-text-main">Usuario y servidor comparten el <strong class="text-danger">mismo secreto</strong>.<br>Si el servidor cae, caen todos.</p>
            </div>
            <div class="card text-center border-primary bg-primary/5 pulse">
                <h3 class="text-primary-light">FIDO2</h3>
                <div class="text-6xl my-8 font-mono">🧑[🗝️] ↔️ 🔒[🖥️]</div>
                <p class="text-lg text-text-main">El usuario tiene la <strong class="text-primary">llave privada</strong> en su hardware (nunca sale).<br>El servidor solo tiene la cerradura (<strong class="text-secondary">clave pública</strong>).</p>
            </div>
        </div>
    </div>

    <!-- Slide 8 -->
    <div class="slide">
        <h2>Los tres mosqueteros de la arquitectura</h2>
        <svg viewBox="0 0 800 250" class="w-full max-w-5xl mt-12">
            <rect x="50" y="80" width="200" height="90" class="diagram-box" />
            <text x="150" y="115" class="diagram-text">Authenticator</text>
            <text x="150" y="140" class="diagram-text" style="font-size: 12px; fill: var(--text-muted);">(Sensor / Nitrokey / RP2350)</text>
            
            <path d="M250,125 L340,125" class="diagram-arrow" />
            <text x="295" y="110" class="diagram-text" style="font-size: 14px; fill: var(--secondary); font-family: 'Fira Code', monospace;">CTAP2</text>
            
            <rect x="350" y="80" width="160" height="90" class="diagram-box" />
            <text x="430" y="115" class="diagram-text">Client</text>
            <text x="430" y="140" class="diagram-text" style="font-size: 12px; fill: var(--text-muted);">(Navegador / SO)</text>

            <path d="M510,125 L590,125" class="diagram-arrow" />
            <text x="550" y="110" class="diagram-text" style="font-size: 14px; fill: var(--secondary); font-family: 'Fira Code', monospace;">WebAuthn</text>
            
            <rect x="600" y="80" width="160" height="90" class="diagram-box" />
            <text x="680" y="115" class="diagram-text">Relying Party</text>
            <text x="680" y="140" class="diagram-text" style="font-size: 12px; fill: var(--text-muted);">(Tu Backend Node)</text>
        </svg>
    </div>

    <!-- Slide 9 -->
    <div class="slide">
        <h2>Por qué FIDO2 extermina el Phishing (El superpoder)</h2>
        <div class="flex flex-col items-center gap-6 w-full max-w-4xl">
            <div class="card w-full border-danger bg-danger/5 p-6 flex justify-between items-center">
                <h3 class="text-danger m-0 flex items-center gap-3"><svg class="w-6 h-6"><use href="#icon-skull"></use></svg> Phishing Site</h3>
                <span class="font-mono text-lg bg-danger/20 p-2 rounded text-red-200 border border-danger/50">https://banc0-santander-phishing.com</span>
            </div>
            
            <div class="text-xl text-secondary font-mono py-2 font-bold drop-shadow-[0_0_8px_rgba(245,158,11,0.8)]">⬇️ Navegador inyecta ORIGEN en la firma ⬇️</div>
            
            <div class="card w-full border-primary bg-primary/5 p-6 pulse">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-primary-light m-0 flex items-center gap-3"><svg class="w-6 h-6"><use href="#icon-bank"></use></svg> Banco Real</h3>
                    <span class="font-mono text-lg bg-primary/20 p-2 rounded text-primary-light border border-primary/50">https://banco-santander.com</span>
                </div>
                <div class="bg-bg-dark p-4 rounded border border-primary/30">
                    <p class="text-left text-lg font-mono text-text-main m-0">Validando origen de firma:</p>
                    <p class="text-left text-lg font-mono m-0 mt-2">
                        <span class="text-danger">banc0-santander-phishing.com</span> <span class="text-text-muted">!=</span> <span class="text-primary-light">banco-santander.com</span>
                    </p>
                </div>
                <p class="text-center text-2xl font-bold text-danger mt-6 m-0" style="filter:drop-shadow(0 0 5px rgba(239,68,68,0.8));">Firma rechazada matemáticamente.</p>
            </div>
        </div>
    </div>

    <!-- Slide 10 -->
    <div class="slide">
        <h2>El flujo de Registro (Sin dolor)</h2>
        <svg viewBox="0 0 900 350" class="w-full max-w-5xl bg-bg-dark/50 rounded-xl p-4 border border-primary/20 backdrop-blur-sm">
            <text x="150" y="40" class="diagram-text text-primary-light" style="fill: var(--primary-light);">Backend</text>
            <text x="450" y="40" class="diagram-text text-primary-light" style="fill: var(--primary-light);">Navegador</text>
            <text x="750" y="40" class="diagram-text text-primary-light" style="fill: var(--primary-light);">Llave</text>
            
            <line x1="150" y1="60" x2="150" y2="330" stroke="#334155" stroke-width="2" stroke-dasharray="5,5"/>
            <line x1="450" y1="60" x2="450" y2="330" stroke="#334155" stroke-width="2" stroke-dasharray="5,5"/>
            <line x1="750" y1="60" x2="750" y2="330" stroke="#334155" stroke-width="2" stroke-dasharray="5,5"/>
            
            <path d="M150,90 L440,90" class="diagram-arrow-solid" />
            <text x="300" y="75" class="diagram-text" style="font-size: 13px;">1. "Toma este reto aleatorio (challenge)"</text>
            
            <path d="M450,140 L740,140" class="diagram-arrow-solid" />
            <text x="600" y="125" class="diagram-text" style="font-size: 13px;">2. "Créame par de claves y firma reto"</text>
            
            <rect x="670" y="160" width="160" height="40" fill="var(--primary)" rx="5" class="pulse" style="filter: drop-shadow(0 0 10px rgba(16,185,129,0.8));"/>
            <text x="750" y="180" class="diagram-text" style="font-size: 12px; fill: #000; font-weight: 800;">Toque de dedo (Presencia)</text>
            
            <path d="M750,230 L460,230" class="diagram-arrow-solid" />
            <text x="600" y="215" class="diagram-text" style="font-size: 13px;">3. Devuelve clave pública firmada</text>
            
            <path d="M450,280 L160,280" class="diagram-arrow-solid" />
            <text x="300" y="265" class="diagram-text" style="font-size: 13px;">4. Comprueba firma y guarda en BBDD</text>
        </svg>
    </div>

    <!-- Slide 11 -->
    <div class="slide">
        <h2>El flujo de Login</h2>
        <svg viewBox="0 0 900 350" class="w-full max-w-5xl bg-bg-dark/50 rounded-xl p-4 border border-primary/20 backdrop-blur-sm">
            <text x="150" y="40" class="diagram-text text-primary-light" style="fill: var(--primary-light);">Backend</text>
            <text x="450" y="40" class="diagram-text text-primary-light" style="fill: var(--primary-light);">Navegador</text>
            <text x="750" y="40" class="diagram-text text-primary-light" style="fill: var(--primary-light);">Llave</text>
            
            <line x1="150" y1="60" x2="150" y2="330" stroke="#334155" stroke-width="2" stroke-dasharray="5,5"/>
            <line x1="450" y1="60" x2="450" y2="330" stroke="#334155" stroke-width="2" stroke-dasharray="5,5"/>
            <line x1="750" y1="60" x2="750" y2="330" stroke="#334155" stroke-width="2" stroke-dasharray="5,5"/>
            
            <path d="M150,90 L440,90" class="diagram-arrow-solid" />
            <text x="300" y="75" class="diagram-text" style="font-size: 13px;">1. "¿Quieres entrar? Firma este challenge"</text>
            
            <path d="M450,140 L740,140" class="diagram-arrow-solid" />
            <text x="600" y="125" class="diagram-text" style="font-size: 13px;">2. Pide firma a la llave</text>
            
            <rect x="670" y="160" width="160" height="40" fill="var(--primary)" rx="5" class="pulse" style="filter: drop-shadow(0 0 10px rgba(16,185,129,0.8));"/>
            <text x="750" y="180" class="diagram-text" style="font-size: 12px; fill: #000; font-weight: 800;">Firma con Clave Privada</text>
            
            <path d="M750,230 L460,230" class="diagram-arrow-solid" />
            <text x="600" y="215" class="diagram-text" style="font-size: 13px;">3. Devuelve firma al navegador</text>
            
            <path d="M450,280 L160,280" class="diagram-arrow-solid" />
            <text x="300" y="265" class="diagram-text" style="font-size: 13px;">4. Comprueba firma con Pública. ¡Dentro!</text>
        </svg>
    </div>

    <!-- Slide 12 -->
    <div class="slide">
        <h2>BriConsejo de Arquitectura</h2>
        <h3 class="mb-12 font-mono text-primary-light">"1 Servicio, 3 Componentes y me sobra 1"</h3>
        <div class="flex justify-center items-center gap-12 w-full max-w-4xl bg-bg-dark/80 p-12 rounded-2xl border border-primary/30 duct-tape-container">
            <div class="duct-tape" style="top: -10px; transform: translateX(-50%) rotate(-2deg); width: 180px;"></div>
            <div class="text-center">
                <div class="text-7xl mb-6 font-mono font-bold text-text-main">ex</div>
                <p class="font-mono text-xl m-0 font-bold text-secondary">Express</p>
            </div>
            <div class="text-5xl text-primary font-bold">+</div>
            <div class="text-center">
                <div class="text-7xl mb-6 font-mono font-bold text-danger">A</div>
                <p class="font-mono text-xl m-0 font-bold text-secondary">Angular</p>
            </div>
            <div class="text-5xl text-primary font-bold">+</div>
            <div class="text-center card border-primary bg-primary/10 p-6 m-0 w-auto shadow-[0_0_30px_rgba(16,185,129,0.3)]">
                <div class="text-5xl mb-4 font-mono font-bold text-primary">npm</div>
                <p class="font-mono text-xl text-primary-light font-bold m-0">@simplewebauthn</p>
            </div>
        </div>
    </div>

    <!-- Slide 13 -->
    <div class="slide">
        <h2>LAB 1 — Backend con Express.js</h2>
        <div class="code-window">
            <div class="window-header">
                <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
                <span class="ml-4 font-mono text-sm text-text-muted">server.ts</span>
            </div>
            <pre><code><span class="keyword">import</span> { <span class="function">generateRegistrationOptions</span>, <span class="function">verifyRegistrationResponse</span> } <span class="keyword">from</span> <span class="string">'@simplewebauthn/server'</span>;

<span class="comment">// 4 Endpoints mágicos</span>
app.<span class="function">post</span>(<span class="string">'/auth/register/begin'</span>, ...);
app.<span class="function">post</span>(<span class="string">'/auth/register/complete'</span>, ...);

app.<span class="function">post</span>(<span class="string">'/auth/login/begin'</span>, ...);
app.<span class="function">post</span>(<span class="string">'/auth/login/complete'</span>, ...);

<span class="comment">// (Bonus) Curiosear qué se ha guardado</span>
app.<span class="function">get</span>(<span class="string">'/auth/users'</span>, ...);

<span class="comment">// ⚠️ ATENCIÓN: Discrepancias de origen = Error #1</span>
<span class="keyword">const</span> <span class="property">rpID</span> = <span class="string">'localhost'</span>; 
<span class="keyword">const</span> <span class="property">expectedOrigin</span> = <span class="string">'http://localhost:4200'</span>;</code></pre>
        </div>
    </div>

    <!-- Slide 14 -->
    <div class="slide">
        <h2>LAB 1 en vivo: El Contador Anti-Replay</h2>
        <div class="code-window">
            <div class="window-header">
                <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
                <span class="ml-4 font-mono text-sm text-text-muted">login.controller.ts</span>
            </div>
            <pre><code><span class="keyword">let</span> verification;
<span class="keyword">try</span> {
  verification = <span class="keyword">await</span> <span class="function">verifyAuthenticationResponse</span>({
    response: body,
    expectedChallenge,
    expectedOrigin,
    expectedRPID,
    authenticator: {
      credentialID: authenticator.credentialID,
      credentialPublicKey: authenticator.credentialPublicKey,
      <span class="highlight">counter: authenticator.counter,</span> <span class="comment">// 🛡️ El contador interno</span>
    },
  });
} <span class="keyword">catch</span> (error) { ... }

<span class="comment">// Si a nuestro servidor le llega una petición con</span>
<span class="comment">// un número <= que en el login anterior...</span>
<span class="comment">// ¡Peligro! Hardware clonado o petición repetida.</span></code></pre>
        </div>
    </div>

    <!-- Slide 15 -->
    <div class="slide">
        <h2>Pausa técnica / El salvavidas de Chrome</h2>
        <div class="card w-full max-w-4xl border-primary bg-primary/5 shadow-[0_0_30px_rgba(16,185,129,0.15)]">
            <div class="flex items-center gap-4 border-b border-primary/20 pb-4 mb-6">
                <div class="glow-card"><svg class="w-8 h-8"><use href="#icon-wrench"></use></svg></div>
                <span class="text-xl font-mono text-primary-light">Chrome DevTools &gt; More tools &gt; WebAuthn</span>
            </div>
            <ul class="text-left text-lg">
                <li>Emulador completo de llaves por software nativo en Chrome.</li>
                <li>Ideal si estás en un portátil sin lector de huella.</li>
                <li>Perfecto para desarrollo en Linux sin biometría configurada.</li>
            </ul>
            <div class="mt-8 p-6 bg-bg-dark rounded border border-primary/30 font-mono text-primary-light relative overflow-hidden">
                <div class="absolute left-0 top-0 w-1 h-full bg-primary"></div>
                [x] Enable virtual authenticator environment<br>
                Protocol: ctap2<br>
                Transport: usb<br>
                Supports resident keys: Yes
            </div>
        </div>
    </div>

    <!-- Slide 16 -->
    <div class="slide">
        <h2>LAB 2 — Frontend con Angular</h2>
        <div class="code-window">
            <div class="window-header">
                <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
                <span class="ml-4 font-mono text-sm text-text-muted">auth.service.ts</span>
            </div>
            <pre><code><span class="keyword">import</span> { <span class="function">startRegistration</span>, <span class="function">startAuthentication</span> } <span class="keyword">from</span> <span class="string">'@simplewebauthn/browser'</span>;

@<span class="function">Injectable</span>({ providedIn: <span class="string">'root'</span> })
<span class="keyword">export class</span> <span class="function">AuthService</span> {
  
  <span class="keyword">async</span> <span class="function">startRegistration</span>(username: <span class="keyword">string</span>) {
    <span class="comment">// 1. Pedimos opciones al backend</span>
    <span class="keyword">const</span> options = <span class="keyword">await</span> <span class="keyword">this</span>.api.<span class="function">getRegistrationOptions</span>(username);
    
    <span class="comment">// 2. Levanta el cuadro de diálogo nativo del SO</span>
    <span class="keyword">const</span> response = <span class="keyword">await</span> <span class="function">startRegistration</span>(options);
    
    <span class="comment">// 3. Enviamos resultado al backend</span>
    <span class="keyword">await</span> <span class="keyword">this</span>.api.<span class="function">verifyRegistration</span>(username, response);
  }
}</code></pre>
        </div>
    </div>

    <!-- Slide 17 -->
    <div class="slide">
        <h2>El zoo de autenticadores: Plataforma vs Roaming</h2>
        <div class="grid-2">
            <div class="card bg-bg-dark border-primary/30 p-8 h-full">
                <h3 class="text-primary-light border-b border-primary/20 pb-4">Plataforma</h3>
                <div class="my-6 flex gap-4 justify-center">
                    <div class="glow-card"><svg class="w-8 h-8"><use href="#icon-laptop"></use></svg></div>
                    <div class="glow-card"><svg class="w-8 h-8"><use href="#icon-phone"></use></svg></div>
                </div>
                <ul class="text-lg">
                    <li>Windows Hello, Touch ID, Face ID, huella de Android.</li>
                    <li>Atados al cacharro o sincronizados en passkeys (nube).</li>
                    <li>Comodísimos.</li>
                </ul>
            </div>
            <div class="card bg-bg-dark border-secondary/30 p-8 h-full shadow-[0_0_30px_rgba(245,158,11,0.15)]">
                <h3 class="text-secondary border-b border-secondary/20 pb-4">Roaming (Externos)</h3>
                <div class="my-6 flex gap-4 justify-center">
                    <div class="glow-card" style="border-color:var(--secondary);color:var(--secondary);box-shadow:0 0 15px rgba(245,158,11,0.3);background:rgba(245,158,11,0.1);"><svg class="w-8 h-8"><use href="#icon-key"></use></svg></div>
                    <div class="glow-card" style="border-color:var(--secondary);color:var(--secondary);box-shadow:0 0 15px rgba(245,158,11,0.3);background:rgba(245,158,11,0.1);"><svg class="w-8 h-8"><use href="#icon-plug"></use></svg></div>
                </div>
                <ul class="text-lg">
                    <li>Llaves de seguridad físicas por USB, NFC o BLE.</li>
                    <li>Seguridad absoluta: no dependen de ninguna nube corporativa.</li>
                    <li>Infraestructura crítica.</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- Slide 18 -->
    <div class="slide">
        <h2 class="text-primary-light mb-2 text-2xl tracking-widest font-mono">SPONSOR OFICIAL & HARDWARE</h2>
        <h1 class="text-6xl mb-12" style="background:none;-webkit-text-fill-color:var(--text-main);">Nitrokey al rescate</h1>
        <div class="grid-2">
            <div class="flex flex-col items-center justify-center w-full">
                <img src="assets/images/nitrokey_3a.jpg" alt="Nitrokey 3A" class="img-glow drop-shadow-[0_20px_50px_rgba(16,185,129,0.3)] w-full h-auto aspect-video object-cover mb-6">
                <div class="text-2xl font-bold tracking-widest text-primary font-mono">NITROKEY 3A</div>
            </div>
            <div class="w-full">
                <ul class="text-left text-xl space-y-4">
                    <li><strong>100% Open Source</strong> (firmware y hardware).</li>
                    <li>Fabricado en Alemania · Seguridad Auditable.</li>
                    <li>Chip con <strong>Secure Element</strong> resistente a ataques físicos.</li>
                    <li>FIDO2/WebAuthn, U2F, OpenPGP, TOTP/HOTP.</li>
                </ul>
                <div class="mt-8 p-4 bg-primary/10 border border-primary rounded-lg text-center pulse">
                    <p class="text-primary-light font-bold text-xl m-0">¡Tenemos llaves Nitrokey 3A aquí en la sala para probar en directo!</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Slide 19 -->
    <div class="slide">
        <h2>Demo en directo: Nitrokey 3A en acción</h2>
        <div class="card text-center py-20 px-8 border-primary bg-primary/5 max-w-4xl shadow-[0_0_50px_rgba(16,185,129,0.15)]">
            <div class="flex justify-center items-center gap-8 mb-12">
                <div class="glow-card w-24 h-24 pulse"><svg class="w-12 h-12"><use href="#icon-plug"></use></svg></div>
                <span class="text-secondary font-bold text-3xl">→</span>
                <div class="glow-card w-24 h-24 pulse" style="animation-delay: 0.5s"><svg class="w-12 h-12"><use href="#icon-fingerprint"></use></svg></div>
                <span class="text-secondary font-bold text-3xl">→</span>
                <div class="glow-card w-24 h-24 pulse" style="animation-delay: 1s"><svg class="w-12 h-12"><use href="#icon-check"></use></svg></div>
            </div>
            <h3 class="text-4xl text-text-main mb-6">Conexión USB &gt; User Presence &gt; Login concedido</h3>
            <p class="text-xl text-text-muted font-mono">Autenticado en milisegundos sin escribir una sola tecla.</p>
        </div>
    </div>

    <!-- Slide 20 -->
    <div class="slide">
        <h2>Momento Cacharreo Maker</h2>
        <h3 class="text-4xl mt-4 mb-12 text-primary-light font-mono">¿Y si la fabricamos nosotros por 5€?</h3>
        <div class="flex justify-center w-full max-w-4xl">
            <img src="assets/images/raspberry_pi_pico.jpg" alt="Raspberry Pi Pico 2" class="img-glow drop-shadow-[0_20px_50px_rgba(16,185,129,0.3)] w-full h-auto aspect-video object-cover">
        </div>
    </div>

    <!-- Slide 21 -->
    <div class="slide">
        <h2>RP2350 vs RP2040: Por qué importa el silicio</h2>
        <div class="grid-2">
            <div class="card border-danger/50 bg-danger/5 h-full">
                <h3 class="text-danger text-center text-3xl font-mono mb-6 border-b border-danger/20 pb-4">Pico 1 (RP2040)</h3>
                <ul class="text-xl space-y-4">
                    <li>Sin protección en flash.</li>
                    <li>Cualquiera lee la memoria en crudo con una pinza.</li>
                </ul>
            </div>
            <div class="card border-primary bg-primary/10 h-full shadow-[0_0_30px_rgba(16,185,129,0.2)]">
                <h3 class="text-primary-light text-center text-3xl font-mono mb-6 border-b border-primary/20 pb-4">Pico 2 (RP2350)</h3>
                <ul class="text-xl space-y-4">
                    <li><strong>Secure Boot</strong> y arquitectura ARM TrustZone.</li>
                    <li>Memoria <strong>OTP</strong> (One-Time Programmable) para quemar la clave maestra permanentemente.</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- Slide 22 -->
    <div class="slide">
        <h2>Pico FIDO contra nuestra aplicación</h2>
        <div class="card w-full max-w-4xl p-10 border-secondary bg-secondary/5">
            <ul class="text-2xl space-y-8 font-mono mb-10">
                <li class="text-text-main">1. Flasheamos firmware libre <span class="text-secondary font-bold">Pico FIDO</span> (.uf2).</li>
                <li class="text-text-main">2. El SO detecta el dispositivo HID <span class="text-secondary font-bold">(sin drivers)</span>.</li>
                <li class="text-text-main">3. Login en nuestro frontend Angular...</li>
            </ul>
            <div class="text-center p-6 bg-primary/20 border border-primary rounded-xl pulse">
                <p class="text-primary-light font-bold text-4xl m-0">¡Y entra a la primera!</p>
                <p class="mt-4 text-text-main text-lg m-0">Exactamente igual que con la Nitrokey.</p>
            </div>
            <p class="mt-10 text-center text-xl text-text-muted italic m-0">La belleza de los estándares abiertos: a tu código le da igual el fabricante del silicio.</p>
        </div>
    </div>

    <!-- Slide 23 -->
    <div class="slide">
        <h2>¿Y qué pasa si pierdo la llave? (Gestión del mundo real)</h2>
        <div class="card w-full max-w-4xl border-secondary bg-secondary/10 p-10 shadow-[0_0_40px_rgba(245,158,11,0.15)]">
            <h3 class="text-secondary mb-10 flex items-center justify-center gap-4 text-3xl">
                <svg class="w-10 h-10"><use href="#icon-check"></use></svg> Regla de oro: Registrar siempre ≥ 2 credenciales
            </h3>
            <ul class="text-xl space-y-6">
                <li><strong>Backup de llaves:</strong> Tu Nitrokey en el llavero + la biometría del portátil.</li>
                <li><strong>Recovery codes:</strong> Códigos de recuperación de emergencia de un solo uso.</li>
                <li><strong>Attestation:</strong> La capacidad del backend de exigir llaves certificadas (por qué un banco aceptaría una Nitrokey y no nuestra Raspberry casera).</li>
            </ul>
        </div>
    </div>

    <!-- Slide 24 -->
    <div class="slide">
        <h2>Lo que FIDO2 NO puede solucionar (Honestidad brutal)</h2>
        <div class="grid grid-cols-3 gap-8 w-full max-w-6xl">
            <div class="card text-center p-8 border-danger/30 bg-danger/5 h-full flex flex-col items-center justify-start">
                <div class="glow-card mb-6" style="border-color:var(--danger);color:var(--danger);box-shadow:0 0 15px rgba(239,68,68,0.3);background:rgba(239,68,68,0.1);"><svg class="w-8 h-8"><use href="#icon-cookie"></use></svg></div>
                <h3 class="text-2xl text-danger mb-4">Robo de Sesión</h3>
                <p class="text-base text-text-muted m-0">Session Hijacking. Si te roban la cookie ya emitida, FIDO2 no te salva.</p>
            </div>
            <div class="card text-center p-8 border-danger/30 bg-danger/5 h-full flex flex-col items-center justify-start">
                <div class="glow-card mb-6" style="border-color:var(--danger);color:var(--danger);box-shadow:0 0 15px rgba(239,68,68,0.3);background:rgba(239,68,68,0.1);"><svg class="w-8 h-8"><use href="#icon-wrench"></use></svg></div>
                <h3 class="text-2xl text-danger mb-4">Coacción Física</h3>
                <p class="text-base text-text-muted m-0">El ataque de la llave inglesa de 5 dólares de XKCD.</p>
            </div>
            <div class="card text-center p-8 border-danger/30 bg-danger/5 h-full flex flex-col items-center justify-start">
                <div class="glow-card mb-6" style="border-color:var(--danger);color:var(--danger);box-shadow:0 0 15px rgba(239,68,68,0.3);background:rgba(239,68,68,0.1);"><svg class="w-8 h-8"><use href="#icon-eye-off"></use></svg></div>
                <h3 class="text-2xl text-danger mb-4">Descuido</h3>
                <p class="text-base text-text-muted m-0">Poner el dedo sin mirar la pantalla para qué estás dando permiso.</p>
            </div>
        </div>
    </div>

    <!-- Slide 25 -->
    <div class="slide">
        <h2>Resumen, Recursos y Agradecimientos</h2>
        <div class="grid-2 max-w-5xl">
            <div class="flex flex-col items-center">
                <div class="bg-white p-6 rounded-2xl w-64 h-64 flex justify-center items-center mb-6 shadow-[0_0_30px_rgba(16,185,129,0.3)]">
                    <svg viewBox="0 0 100 100" class="w-full h-full">
                        <rect width="100" height="100" fill="#fff"/>
                        <path d="M10,10 h25 v25 h-25 z M15,15 h15 v15 h-15 z M65,10 h25 v25 h-25 z M70,15 h15 v15 h-15 z M10,65 h25 v25 h-25 z M15,70 h15 v15 h-15 z M45,10 h10 v10 h-10 z M45,25 h15 v15 h-15 z M45,45 h20 v10 h-20 z M10,45 h25 v10 h-25 z M75,45 h15 v10 h-15 z M45,65 h10 v25 h-10 z M65,65 h25 v10 h-25 z M80,80 h10 v10 h-10 z M65,85 h10 v5 h-10 z M25,45 h10 v5 h-10 z" fill="#000"/>
                    </svg>
                </div>
                <span class="font-mono text-primary text-xl font-bold bg-primary/10 border border-primary px-4 py-2 rounded">github.com/xtoxico/...</span>
            </div>
            <div class="w-full">
                <ul class="text-xl space-y-4 mb-10 font-mono">
                    <li>» simplewebauthn.dev</li>
                    <li>» webauthn.io</li>
                    <li>» nitrokey.com</li>
                    <li>» picokeys.com</li>
                </ul>
                <div class="flex flex-wrap gap-4 mt-8">
                    <span class="badge border-primary text-primary-light">Paralelo 37</span>
                    <span class="badge border-primary text-primary-light">XauenDevs</span>
                    <span class="badge border-secondary text-secondary" style="box-shadow: 0 0 10px rgba(245,158,11,0.2); background: rgba(245,158,11,0.1);">Nitrokey</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Slide 26 -->
    <div class="slide">
        <div class="card border-primary/50 bg-bg-dark/80 p-16 mb-12 max-w-5xl shadow-[0_0_50px_rgba(16,185,129,0.15)] relative overflow-hidden">
            <div class="absolute left-0 top-0 w-2 h-full bg-gradient-to-b from-secondary to-primary"></div>
            <p class="text-4xl italic text-text-main leading-relaxed m-0 text-center font-serif">
                "El futuro no es sin contraseñas...<br>es con una autenticación que por fin<br><span class="text-primary-light font-bold not-italic font-sans">está a la altura de las personas.</span>"
            </p>
        </div>
        <div class="text-center mt-8">
            <h3 class="text-3xl mb-4 text-text-main">Antonio Tirado Peña</h3>
            <p class="text-xl text-text-muted font-mono m-0">yosoy@antoniotirado.com · @xtoxico · normapro.es</p>
            <div class="mt-12 p-4 bg-primary/10 border border-primary rounded-xl inline-block pulse">
                <p class="text-2xl text-primary-light font-bold m-0">¡Quedan micrófonos abiertos para dudas!</p>
                <p class="text-primary mt-2 m-0">(y veníos a probar las llaves Nitrokey y Pico en directo)</p>
            </div>
        </div>
    </div>

    <script>
        const slides = document.querySelectorAll('.slide');
        const progressBar = document.getElementById('progress');
        const counter = document.getElementById('counter');
        let currentSlide = 0;

        function updateSlides() {
            slides.forEach((slide, index) => {
                slide.classList.remove('active', 'prev');
                if (index === currentSlide) {
                    slide.classList.add('active');
                } else if (index < currentSlide) {
                    slide.classList.add('prev');
                }
            });
            
            const progress = (currentSlide / (slides.length - 1)) * 100;
            progressBar.style.width = `${progress}%`;
            counter.textContent = `${currentSlide + 1} / ${slides.length}`;
        }

        function nextSlide() {
            if (currentSlide < slides.length - 1) {
                currentSlide++;
                updateSlides();
            }
        }

        function prevSlide() {
            if (currentSlide > 0) {
                currentSlide--;
                updateSlides();
            }
        }

        function toggleFullScreen() {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    console.log(`Error al entrar en fullscreen: ${err.message}`);
                });
            } else {
                document.exitFullscreen();
            }
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
                e.preventDefault();
                nextSlide();
            } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
                e.preventDefault();
                prevSlide();
            } else if (e.key.toLowerCase() === 'f') {
                e.preventDefault();
                toggleFullScreen();
            }
        });

        // Mouse wheel navigation with debounce
        let lastScrollTime = 0;
        document.addEventListener('wheel', (e) => {
            const now = new Date().getTime();
            if (now - lastScrollTime < 300) return; // 300ms debounce
            
            if (e.deltaY > 0) {
                nextSlide();
                lastScrollTime = now;
            } else if (e.deltaY < 0) {
                prevSlide();
                lastScrollTime = now;
            }
        });

        updateSlides();
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated index.html successfully.")
