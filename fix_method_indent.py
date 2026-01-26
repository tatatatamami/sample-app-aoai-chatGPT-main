# Fix indentation more aggressively
with open('backend/settings.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
for i, line in enumerate(lines):
    lineno = i + 1
    stripped = line.lstrip()
    
    # Line 815-821: method body
    if 815 <= lineno <= 821:
        if stripped.startswith('try:'):
            line = '        ' + stripped
        elif stripped.startswith('self.foundry'):
            line = '            ' + stripped
        elif stripped.startswith('except'):
            line = '        ' + stripped
        elif stripped.startswith('self.foundry = None'):
            line = '            ' + stripped  
        elif stripped.startswith('return self'):
            line = '        ' + stripped
    
    fixed_lines.append(line)

with open('backend/settings.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Fixed method indentation")
