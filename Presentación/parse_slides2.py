import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Instead of re.split, let's just find the indexes.
matches = list(re.finditer(r'\s*<!-- Slide \d+.*?-->', html))

slides = []
for i in range(len(matches)):
    start = matches[i].start()
    end = matches[i+1].start() if i + 1 < len(matches) else html.find('<script>')
    slides.append(html[start:end])
    
print(f"Found {len(slides)} slides.")
for i, slide in enumerate(slides):
    print(f"Slide {i+1} starts with: {slide.strip()[:40]}")
