import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update typography selectors and sizes
html = re.sub(
    r'h1 \{ font-size: 5rem; (.*?)\}',
    r'.slide h1 { font-size: 5.5rem; \1}',
    html
)
html = re.sub(
    r'h2 \{ font-size: 4.5rem; (.*?margin-bottom: )2rem;(.*?)\}',
    r'.slide h2 { font-size: 5rem; \1 3rem;\2}',
    html
)
html = re.sub(
    r'h3 \{ font-size: 1.75rem; (.*?)\}',
    r'.slide h3 { font-size: 2.25rem; \1}',
    html
)
html = re.sub(
    r'p \{ font-size: 1.5rem; (.*?)\}',
    r'.slide p { font-size: 1.75rem; \1}',
    html
)
html = re.sub(
    r'ul \{ font-size: 1.35rem; line-height: 1.6; (.*?)\}',
    r'.slide ul { font-size: 1.6rem; line-height: 1.8; \1}',
    html
)
html = re.sub(
    r'li \{ margin-bottom: 1rem; (.*?)\}',
    r'.slide li { margin-bottom: 1.5rem; \1}',
    html
)
html = re.sub(
    r'\.grid-2 \{ display: grid; grid-template-columns: 1fr 1fr; gap: 3rem;',
    r'.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6rem;',
    html
)

# 2. Update fotomia image size
html = html.replace('w-64 h-64 rounded-full', 'w-80 h-80 rounded-full')

# 3. Add !important to font sizes in CSS just to be absolutely bulletproof against Tailwind CDN
html = html.replace('font-size: 5.5rem;', 'font-size: 5.5rem !important;')
html = html.replace('font-size: 5rem;', 'font-size: 5rem !important;')
html = html.replace('font-size: 2.25rem;', 'font-size: 2.25rem !important;')
html = html.replace('font-size: 1.75rem;', 'font-size: 1.75rem !important;')
html = html.replace('font-size: 1.6rem;', 'font-size: 1.6rem !important;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Typography updated successfully.")
