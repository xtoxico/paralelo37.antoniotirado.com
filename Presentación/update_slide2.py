import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS update
css_addition = """
        .normapro-logo { filter: brightness(0) invert(1); }
        body.light-mode .normapro-logo { filter: none; }
"""
html = html.replace('body.light-mode h1, body.light-mode h2 {', css_addition + '\n        body.light-mode h1, body.light-mode h2 {')

# Slide 2 replacement
slide2_pattern = re.compile(r'<!-- Slide 2 -->.*?<!-- Slide 3 -->', re.DOTALL)

new_slide_2 = """<!-- Slide 2 -->
    <div class="slide">
        <h2>¿Quién demonios soy yo?</h2>
        <div class="grid-2">
            <div class="flex justify-center">
                <img src="fotomia.jpeg" class="w-80 h-80 rounded-full border-4 border-primary drop-shadow-[0_0_20px_rgba(148,168,59,0.5)] object-cover shadow-2xl">
            </div>
            <div>
                <ul>
                    <li><strong class="text-primary-light">Antonio Tirado Peña.</strong></li>
                    <li>Ingeniero Técnico en Informática de Gestión (UJA, de la tierra).</li>
                    <li>Master en Desarrollo de Producto por la IEBS.</li>
                    <li>Director de TI y Estrategia en IICE / NormaPro.</li>
                    <li>Cacharreador compulsivo: Linux (Arch, por supuesto), servidores caseros con Docker, soldador, microcontroladores y cacharros varios.</li>
                </ul>
                <div class="mt-8 grid grid-cols-2 gap-4 text-secondary text-lg font-mono">
                    <a href="https://antoniotirado.com" target="_blank" class="flex items-center gap-2 px-3 py-2 bg-secondary-dark/20 border border-secondary/50 rounded shadow-sm backdrop-blur-sm hover:bg-secondary/30 transition-colors decoration-transparent text-secondary">
                        <span>🌐 antoniotirado.com</span>
                    </a>
                    <a href="https://www.linkedin.com/in/antoniotiradopena" target="_blank" class="flex items-center gap-2 px-3 py-2 bg-secondary-dark/20 border border-secondary/50 rounded shadow-sm backdrop-blur-sm hover:bg-secondary/30 transition-colors decoration-transparent text-secondary">
                        <span>in/antoniotiradopena</span>
                    </a>
                    <a href="https://github.com/xtoxico" target="_blank" class="flex items-center gap-2 px-3 py-2 bg-secondary-dark/20 border border-secondary/50 rounded shadow-sm backdrop-blur-sm hover:bg-secondary/30 transition-colors decoration-transparent text-secondary">
                        <span>🐙 github.com/xtoxico</span>
                    </a>
                    <a href="https://normapro.es" target="_blank" class="flex items-center justify-center gap-3 px-3 py-2 bg-secondary-dark/20 border border-secondary/50 rounded shadow-sm backdrop-blur-sm hover:bg-secondary/30 transition-colors decoration-transparent">
                        <img src="assets/images/normapro_logo.png" alt="NormaPro" class="h-6 w-auto normapro-logo">
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Slide 3 -->"""

html = slide2_pattern.sub(new_slide_2, html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Slide 2 updated successfully.")
