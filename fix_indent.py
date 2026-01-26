# Fix indentation in settings.py
with open('backend/settings.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
for i, line in enumerate(lines):
    # Line 802-806 need indentation
    if 801 <= i+1 <= 806:
        if line.strip() and not line.startswith('    ') and not line.startswith('class'):
            line = '    ' + line.lstrip()
    # Line 808-811 need indentation  
    if 808 <= i+1 <= 811:
        if line.strip() and not line.startswith('    ') and line.strip().startswith(('#', 'chat', 'datasource', 'promptflow')):
            line = '    ' + line.lstrip()
    # Line 813-814 need indentation
    if 813 <= i+1 <= 814:
        if line.strip() and not line.startswith('    '):
            line = '    ' + line.lstrip()
    # Line 815-821 check indentation
    if 815 <= i+1 <= 821:
        if line.strip() and not line.startswith('        ') and not line.startswith('    @') and not line.startswith('    def') and line.strip() not in ['try:', 'except ValidationError:', 'return self']:
            if not line.startswith('   '):
                line = '        ' + line.lstrip()
    fixed_lines.append(line)

with open('backend/settings.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Fixed indentation")
