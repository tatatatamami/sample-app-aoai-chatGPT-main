# Fix complete_foundry_request function indentation
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
for i, line in enumerate(lines):
    lineno = i + 1
    
    # Fix lines 284-351 (complete_foundry_request function)
    if 284 <= lineno <= 351:
        stripped = line.lstrip()
        if lineno == 284 and stripped.startswith('"""'):
            fixed_lines.append('    ' + stripped)
        elif lineno == 285 and stripped == 'try:\n':
            fixed_lines.append('    ' + stripped)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Fixed complete_foundry_request function")
