import pathlib

path = '/d/hermes/priblog/_config.yml'
content = open(path).read()

# Remove the deploy block (keep "deploy:" line, remove indented children)  
lines = content.split('\n')
new_lines = []
in_deploy_block = False

for line in lines:
    if line == 'deploy:':
        new_lines.append(line)  # keep "deploy:" itself
        in_deploy_block = True
        continue
    elif in_deploy_block and (line.startswith('  ') or line.startswith('\t')):
        # Skip all indented children of deploy block  
        continue
    else:
        if not in_deploy_block:
            new_lines.append(line)
        else:
            in_deploy_block = False
            new_lines.append(line)

output = '\n'.join(new_lines)
open(path, 'w').write(output)
print('Done')

# Verify  
for i, line in enumerate(open(path).read().split('\n')):
    if 'deploy' in line.lower():
        print(f'{i}: {repr(line)}')
