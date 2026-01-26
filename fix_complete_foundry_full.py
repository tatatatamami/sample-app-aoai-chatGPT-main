# Complete fix for complete_foundry_request function
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
for i, line in enumerate(lines):
    lineno = i + 1
    
    # Fix lines 286-351 (inside try block of complete_foundry_request)
    if 286 <= lineno <= 348:
        stripped = line.lstrip()
        if not stripped or stripped.startswith('#'):
            fixed_lines.append(line)
        elif any(stripped.startswith(x) for x in ['foundry_response', 'logging.', 'response_text', 'if ', 'elif ', 'output', 'choice', 'history_metadata', 'formatted_response', 'return ']):
            # Inside try block - needs 8 spaces
            if not line.startswith('        '):
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    elif lineno in [349, 350, 351]:
        # except block
        stripped = line.lstrip()
        if stripped.startswith('except'):
            fixed_lines.append('    ' + stripped)
        elif stripped.startswith('logging.exception') or stripped.startswith('raise'):
            fixed_lines.append('        ' + stripped)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Complete fix applied")
