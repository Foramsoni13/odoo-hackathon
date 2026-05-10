import glob

templates = glob.glob('templates/*.html')

for file in templates:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<div class="nav-links">' not in content or 'href="/community"' in content:
        continue
        
    lines = content.split('\n')
    new_lines = []
    in_nav_links = False
    
    for line in lines:
        if '<div class="nav-links">' in line:
            in_nav_links = True
            new_lines.append(line)
        elif in_nav_links and '</div>' in line:
            in_nav_links = False
            
            has_search = any('href="/search"' in l for l in new_lines[-5:])
            if not has_search:
                new_lines.append('      <a href="/search" class="nav-link">Search</a>')
                
            new_lines.append('      <a href="/community" class="nav-link">Community</a>')
            new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    print(f'Updated {file}')
