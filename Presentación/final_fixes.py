import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Parse slides
matches = list(re.finditer(r'\s*<!-- Slide \d+.*?-->', html))

slides = []
for i in range(len(matches)):
    start = matches[i].start()
    end = matches[i+1].start() if i + 1 < len(matches) else html.find('<script>')
    slides.append(html[start:end])

# Base html before slides and after slides
header_html = html[:matches[0].start()]
footer_html = html[html.find('<script>'):]

# 2. Modify Slide 20 (index 19 in 0-based array)
# It starts with: <!-- Slide 20 --> ... <h2>Demo en directo: Nitrokey 3A en acción</h2>
slide_20 = slides[19]
slide_20 = slide_20.replace(
    '<h2>Demo en directo: Nitrokey 3A en acción</h2>',
    '<h2>Demo en directo: Nitrokey 3A en acción</h2>\n        <div class="flex justify-center mb-8"><div class="bg-white/95 px-6 py-3 rounded-2xl shadow-[0_0_20px_rgba(148,168,59,0.3)]"><img src="Nitrokey_Logo.svg" class="h-8 w-auto"></div></div>'
)
slides[19] = slide_20

# 3. Modify Slide 27 (index 26)
slide_27 = slides[26]
# Replace QR SVG with the actual image
qr_svg_regex = re.compile(r'<svg viewBox="0 0 100 100" class="w-full h-full">.*?</svg>', re.DOTALL)
slide_27 = qr_svg_regex.sub('<img src="assets/images/qr_paralelo37.png" class="w-full h-full object-contain rounded-xl">', slide_27)

# Replace github.com/xtoxico/... with the repo and the URL
slide_27 = slide_27.replace(
    '<span class="font-mono text-primary text-xl font-bold bg-primary/20 border border-primary px-4 py-2 rounded">github.com/xtoxico/...</span>',
    '<span class="font-mono text-primary text-xl font-bold bg-primary/20 border border-primary px-4 py-2 rounded flex items-center gap-3"><a href="https://github.com/xtoxico/paralelo37" target="_blank" class="text-primary hover:text-primary-light">github.com/xtoxico/paralelo37</a> <img src="assets/images/logoparalelo.png" class="h-6 w-auto"></span>\n                <div class="mt-4 font-mono text-lg text-text-main flex items-center gap-3"><a href="https://paralelo37.antoniotirado.com" target="_blank" class="hover:text-primary-light">paralelo37.antoniotirado.com</a> <img src="assets/images/logoparalelo.png" class="h-5 w-auto"></div>'
)
slides[26] = slide_27

# Modify Slide 1 (to add the logo next to text if they want it everywhere, but we already have the huge logo above the text)
# Actually, I'll leave Slide 1 as is since we put the logo literally on top of the text in a huge format.

# 4. Reorder slides: 1-9 (idx 0-8), 17-19 (idx 16-18), 10-16 (idx 9-15), 20-28 (idx 19-27)
new_slides = slides[0:9] + slides[16:19] + slides[9:16] + slides[19:28]

# 5. Renumber the HTML comments so the source code is clean
for i in range(len(new_slides)):
    # Replace the first HTML comment with the correct slide number
    new_slides[i] = re.sub(r'<!-- Slide \d+.*?-->', f'<!-- Slide {i+1} -->', new_slides[i], count=1)

# Assemble final HTML
final_html = header_html + "".join(new_slides) + footer_html

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Slides reordered and updated successfully.")
