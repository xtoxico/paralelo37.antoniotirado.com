import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update titles font size
html = html.replace('h1 { font-size: 4rem;', 'h1 { font-size: 5rem;')
html = html.replace('h2 { font-size: 3rem;', 'h2 { font-size: 4.5rem;')

# 2. Add light mode CSS before </style>
light_mode_css = """
        /* Light Mode Styles */
        body.light-mode {
            --bg-dark: #f8fafc;
            --bg-light: #e2e8f0;
            --text-main: #0f172a;
            --text-muted: #334155;
            --primary: #7a8c30;
            --secondary: #d97706;
        }
        body.light-mode .grid-pattern {
            background-image: linear-gradient(rgba(0,0,0, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0,0,0, 0.05) 1px, transparent 1px);
        }
        body.light-mode .card {
            background: rgba(255, 255, 255, 0.8);
            border-color: rgba(122, 140, 48, 0.3);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }
        body.light-mode .slide-counter {
            background: rgba(255,255,255,0.9);
            color: var(--primary);
        }
        body.light-mode .diagram-box {
            fill: #ffffff;
            stroke: var(--primary);
        }
        body.light-mode .diagram-text {
            fill: var(--text-main);
        }
        body.light-mode .badge {
            background: rgba(122, 140, 48, 0.15);
        }
        body.light-mode .glow-card {
            background: rgba(122, 140, 48, 0.1);
            box-shadow: 0 0 15px rgba(122, 140, 48, 0.2);
        }
        body.light-mode h1, body.light-mode h2 {
            -webkit-text-fill-color: transparent;
        }
"""
html = html.replace('</style>', light_mode_css + '\n    </style>')

# 3. Add sun/moon SVGs
icons = """<symbol id="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></symbol>
        <symbol id="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></symbol>"""
html = html.replace('</svg>\n\n    <!-- Slide 1 -->', icons + '\n    </svg>\n\n    <!-- Slide 1 -->')

# 4. Add the button HTML
btn_html = """
    <button id="theme-toggle" class="fixed bottom-6 left-6 z-50 p-3 rounded-full bg-primary/20 border border-primary text-primary hover:bg-primary/40 transition-colors backdrop-blur-sm cursor-pointer shadow-lg" title="Cambiar tema">
        <svg class="w-6 h-6 block" id="sun-icon"><use href="#icon-sun"></use></svg>
        <svg class="w-6 h-6 hidden" id="moon-icon"><use href="#icon-moon"></use></svg>
    </button>
"""
html = html.replace('<div class="progress-bar"', btn_html + '\n    <div class="progress-bar"')

# 5. Add JS logic
js_logic = """
        const themeToggle = document.getElementById('theme-toggle');
        const sunIcon = document.getElementById('sun-icon');
        const moonIcon = document.getElementById('moon-icon');
        
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('light-mode');
            if (document.body.classList.contains('light-mode')) {
                sunIcon.classList.add('hidden');
                sunIcon.classList.remove('block');
                moonIcon.classList.add('block');
                moonIcon.classList.remove('hidden');
            } else {
                moonIcon.classList.add('hidden');
                moonIcon.classList.remove('block');
                sunIcon.classList.add('block');
                sunIcon.classList.remove('hidden');
            }
        });

        updateSlides();
"""
html = html.replace('updateSlides();\n    </script>', js_logic + '    </script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated titles and light mode toggle.")
