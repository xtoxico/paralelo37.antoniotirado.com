import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Slide moving (17, 18, 19 after 9)
# To do this safely, I will use regular expressions to extract the slides.
# Each slide starts with <!-- Slide X --> and ends right before the next <!-- Slide Y --> or <script>

slides_match = re.split(r'(?=\s*<!-- Slide \d+.*?\n)', html)

# slides_match[0] is everything before Slide 1
# slides_match[1] is Slide 1
# ...
# slides_match[28] is Slide 28
# slides_match[29] is everything after Slide 28? No, the split might keep the trailing script in the last slide.

# Let's inspect the split output lengths
print(f"Number of parts: {len(slides_match)}")
for i, part in enumerate(slides_match):
    print(f"Part {i} starts with: {part[:40].strip()}")
