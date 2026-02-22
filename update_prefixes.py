import os
import re
import glob

base_dir = os.path.dirname(os.path.abspath(__file__))

# Find all category directories (e.g., 001-audio-midi)
cat_dirs = glob.glob(os.path.join(base_dir, '[0-9][0-9][0-9]-*'))

for cat_dir in cat_dirs:
    if not os.path.isdir(cat_dir):
        continue

    dir_name = os.path.basename(cat_dir)

    # Match 001-category-name
    match = re.match(r'^(\d{3})-(.*)$', dir_name)
    if not match:
        continue

    old_cat_num_3d = match.group(1)
    cat_name = match.group(2)

    # Convert 001 to 01
    new_cat_num_2d = str(int(old_cat_num_3d)).zfill(2)
    new_dir_name = f"{new_cat_num_2d}-{cat_name}"
    new_cat_dir = os.path.join(base_dir, new_dir_name)

    # 1. Rename category folder
    os.rename(cat_dir, new_cat_dir)

    # 2. Rename project files and update contents
    project_files = glob.glob(os.path.join(new_cat_dir, '*.md'))

    for file_path in project_files:
        filename = os.path.basename(file_path)

        if filename == 'projects.md':
            # Update index file
            with open(file_path, 'r') as f:
                content = f.read()

            # Replace links: 001-001-slug.md -> 01-001-slug.md
            content = re.sub(rf'{old_cat_num_3d}-(\d{{3}})', rf'{new_cat_num_2d}-\1', content)

            with open(file_path, 'w') as f:
                f.write(content)
            continue

        # Match project file: 001-001-slug.md
        file_match = re.match(rf'^{old_cat_num_3d}-(\d{{3}})-(.*\.md)$', filename)
        if file_match:
            proj_num = file_match.group(1)
            slug = file_match.group(2)

            new_filename = f"{new_cat_num_2d}-{proj_num}-{slug}"
            new_file_path = os.path.join(new_cat_dir, new_filename)

            with open(file_path, 'r') as f:
                content = f.read()

            # Update number in frontmatter
            content = re.sub(rf'^number:\s*"?{old_cat_num_3d}-(\d{{3}})"?$', rf'number: "{new_cat_num_2d}-\1"', content, flags=re.MULTILINE)

            # Add Exit Criteria section if it doesn't exist
            if '## Exit Criteria' not in content:
                # Insert before ## Progress
                content = content.replace('## Progress', '## Exit Criteria\n- [ ] Define what done looks like for this project\n\n## Progress')

            with open(new_file_path, 'w') as f:
                f.write(content)

            if file_path != new_file_path:
                os.remove(file_path)

# 3. Update README.md
readme_file = os.path.join(base_dir, 'README.md')
if os.path.exists(readme_file):
    with open(readme_file, 'r') as f:
        readme_content = f.read()

    # Replace links in README.md: 001-audio-midi -> 01-audio-midi
    readme_content = re.sub(r'\((\d{3})-(.*?)/projects\.md\)', lambda m: f"({str(int(m.group(1))).zfill(2)}-{m.group(2)}/projects.md)", readme_content)

    with open(readme_file, 'w') as f:
        f.write(readme_content)

print("Update complete.")
