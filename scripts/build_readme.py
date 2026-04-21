import os
import random

# Configuration
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif')
EXCLUDE_DIRS = ('.git', '.github', 'scripts')
MAIN_README_PATH = 'README.md'
SHOWCASE_COUNT = 2
COLUMNS = 2

def get_images(directory):
    images = []
    for f in os.listdir(directory):
        if f.lower().endswith(IMAGE_EXTENSIONS):
            images.append(f)
    return sorted(images)

def generate_image_grid(images, directory_path, columns=COLUMNS):
    if not images:
        return ""
    
    html = '<table>\n'
    for i in range(0, len(images), columns):
        html += '  <tr>\n'
        for j in range(columns):
            if i + j < len(images):
                img = images[i + j]
                # Use relative path for the image
                path = os.path.join(directory_path, img) if directory_path else img
                html += f'    <td align="center"><img src="{path}" width="400"><br><sub>{img}</sub></td>\n'
            else:
                html += '    <td></td>\n'
        html += '  </tr>\n'
    html += '</table>\n'
    return html

def main():
    root_dir = '.'
    categories = []
    
    # Identify categories (subdirectories)
    for entry in os.listdir(root_dir):
        full_path = os.path.join(root_dir, entry)
        if os.path.isdir(full_path) and entry not in EXCLUDE_DIRS:
            categories.append(entry)
    
    categories.sort()
    
    showcase_images = []
    
    for cat in categories:
        cat_images = get_images(cat)
        if not cat_images:
            continue
            
        # Generate sub-README
        sub_readme_content = f'# {cat}\n\n'
        sub_readme_content += f'[{cat} collection]\n\n'
        sub_readme_content += generate_image_grid(cat_images, "") # Images are in the same folder
        
        with open(os.path.join(cat, 'README.md'), 'w') as f:
            f.write(sub_readme_content)
            
        # Pick random images for main showcase
        sample_size = min(len(cat_images), SHOWCASE_COUNT)
        sampled = random.sample(cat_images, sample_size)
        for img in sampled:
            showcase_images.append(os.path.join(cat, img))

    # Generate main README
    header = """<div align="center">

# wallpapers

**Personal wallpaper collection. Pixel art heavy.**

![Count](https://img.shields.io/badge/wallpapers-generated-blue)
![Last Commit](https://img.shields.io/github/last-commit/samhcharles/wallpapers)

</div>

> [!NOTE]
> This README is auto-generated. All files are named `<palette>-<subject>-<nn>.ext` so you can sort by color or vibe at a glance.

## Showcase

"""
    
    # Shuffle showcase images
    random.shuffle(showcase_images)
    
    main_readme_content = header
    main_readme_content += generate_image_grid(showcase_images, "", columns=COLUMNS)
    
    main_readme_content += "\n## Categories\n\n"
    for cat in categories:
        main_readme_content += f"- [{cat}](./{cat}/)\n"
        
    with open(MAIN_README_PATH, 'w') as f:
        f.write(main_readme_content)

if __name__ == '__main__':
    main()
