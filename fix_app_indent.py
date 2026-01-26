# Fix app.py send_foundry_request function indentation
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
in_send_foundry = False
function_start = -1

for i, line in enumerate(lines):
    lineno = i + 1
    
    # Find the start of send_foundry_request function
    if 'async def send_foundry_request' in line:
        in_send_foundry = True
        function_start = lineno
        fixed_lines.append(line)
        continue
    
    # Fix lines 248-280 (inside send_foundry_request)
    if in_send_foundry and 248 <= lineno <= 280:
        stripped = line.lstrip()
        
        # Docstring
        if stripped.startswith('"""'):
            fixed_lines.append('    ' + stripped)
        # if statements at function level
        elif stripped.startswith('if not app_settings') or stripped.startswith('raise ValueError'):
            fixed_lines.append('    ' + stripped)
        # try block
        elif stripped.startswith('try:'):
            fixed_lines.append('    ' + stripped)
        # except blocks
        elif stripped.startswith('except '):
            fixed_lines.append('    ' + stripped)
            in_send_foundry = False  # End of function
        # Inside try block (indent 8 spaces)
        elif stripped and not stripped.startswith('    ') and not line.strip() == '':
            if any(stripped.startswith(x) for x in ['#', 'messages', 'foundry_client', 'logging', 'foundry_response', 'await', 'return']):
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Fixed send_foundry_request indentation")
