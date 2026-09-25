import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Slide 1
slide1_old = r'<p class="text-2xl mt-8 text-primary font-mono font-bold tracking-widest bg-navy/50 p-4 rounded-xl shadow-lg border border-primary/20 backdrop-blur-sm">Paralelo 37 · XauenDevs · Jaén</p>'
slide1_new = """<div class="mt-12 flex flex-col items-center gap-6 bg-bg-dark/50 p-8 rounded-3xl shadow-[0_0_30px_rgba(148,168,59,0.15)] border border-primary/20 backdrop-blur-md">
            <img src="assets/images/logoparalelo.png" alt="Paralelo 37 Logo" class="h-28 w-auto drop-shadow-[0_0_15px_rgba(255,255,255,0.2)]" />
            <p class="text-xl text-primary font-mono font-bold tracking-widest m-0 !text-center">Paralelo 37 · XauenDevs · Jaén</p>
        </div>"""

html = html.replace(slide1_old, slide1_new)

# Update Slide 27
slide27_old = """<div class="flex flex-wrap gap-4 mt-8">
                    <span class="badge border-primary text-primary-light bg-primary/20">Paralelo 37</span>"""
slide27_new = """<div class="flex flex-wrap items-center gap-6 mt-8">
                    <div class="bg-white/5 p-2 rounded-xl border border-primary/20 backdrop-blur-sm shadow-sm"><img src="assets/images/logoparalelo.png" alt="Paralelo 37 Logo" class="h-10 w-auto" /></div>"""

html = html.replace(slide27_old, slide27_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Logos updated successfully.")
