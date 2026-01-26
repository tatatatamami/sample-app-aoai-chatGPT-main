# Fix complete_foundry_request function - preserve latest logic
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
in_function = False
function_end = -1

for i, line in enumerate(lines):
    lineno = i + 1
    
    # Detect start of complete_foundry_request function
    if lineno == 283 and 'async def complete_foundry_request' in line:
        in_function = True
        fixed_lines.append(line)  # Keep function definition
        continue
    
    # Fix lines 284-360 (complete_foundry_request function body)
    if in_function and 284 <= lineno <= 360:
        stripped = line.lstrip()
        
        # Docstring (line 284)
        if lineno == 284 and stripped.startswith('"""'):
            fixed_lines.append('    """Complete a Foundry agent request and format the response."""\n')
        # try statement (line 285)
        elif lineno == 285 and stripped == 'try:\n':
            fixed_lines.append('    try:\n')
        # except statement
        elif stripped.startswith('except Exception'):
            fixed_lines.append('    except Exception as e:\n')
            function_end = lineno + 2  # except block is 2 lines
        # Inside except block
        elif function_end > 0 and lineno <= function_end:
            if stripped.startswith('logging.exception') or stripped.startswith('raise'):
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append(line)
        # Inside try block - need 8 spaces
        elif not stripped.startswith('#') and stripped:
            if not line.startswith('        '):
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append(line)
        else:
            # Comments and empty lines
            if line.strip():
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append(line)
        
        # Check if we reached the end of the function
        if function_end > 0 and lineno >= function_end:
            in_function = False
    else:
        fixed_lines.append(line)

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Fixed complete_foundry_request indentation")
