# Complete fix for _FoundrySettings class
with open('backend/settings.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
for i, line in enumerate(lines):
    lineno = i + 1
    
    # Lines 87-112: _FoundrySettings class
    if 87 <= lineno <= 112:
        stripped = line.lstrip()
        if lineno == 87:  # class line
            fixed_lines.append(line)
        elif lineno in [88, 89, 90, 91, 92, 93]:  # model_config
            if stripped.startswith('model_config'):
                fixed_lines.append('    ' + stripped)
            elif stripped.startswith('env_'):
                fixed_lines.append('        ' + stripped)
            elif stripped.startswith('extra'):
                fixed_lines.append('        ' + stripped)
            elif stripped == ')\n':
                fixed_lines.append('    ' + stripped)
            else:
                fixed_lines.append(line)
        elif lineno in [95, 96, 97, 98, 99, 100, 101, 102, 103, 104]:  # fields
            if stripped and not line.startswith('    ') and not line.strip() == '':
                fixed_lines.append('    ' + stripped)
            else:
                fixed_lines.append(line)
        elif lineno in [106, 107, 108, 109, 110, 111, 112]:  # methods
            if stripped.startswith('def '):
                fixed_lines.append('    ' + stripped)
            elif stripped.startswith('"""') or stripped.startswith('return'):
                fixed_lines.append('        ' + stripped)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    else:
        fixed_lines.append(line)

with open('backend/settings.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Fixed _FoundrySettings class")
