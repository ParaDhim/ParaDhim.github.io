import os
import glob
import yaml
from jinja2 import Environment, FileSystemLoader

def build_site():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Load _config.yml
    config_path = os.path.join(base_dir, '_config.yml')
    with open(config_path, 'r', encoding='utf-8') as f:
        site_config = yaml.safe_load(f) or {}

    # 2. Load all _data/*.yml
    data_dir = os.path.join(base_dir, '_data')
    site_data = {}
    if os.path.exists(data_dir):
        for yml_file in glob.glob(os.path.join(data_dir, '*.yml')):
            key = os.path.splitext(os.path.basename(yml_file))[0]
            with open(yml_file, 'r', encoding='utf-8') as f:
                site_data[key] = yaml.safe_load(f)

    site_config['data'] = site_data
    site_config['time'] = '2026'

    # 3. Setup Jinja Environment
    search_paths = [
        base_dir,
        os.path.join(base_dir, '_layouts'),
        os.path.join(base_dir, '_includes')
    ]
    env = Environment(
        loader=FileSystemLoader(search_paths),
        autoescape=False
    )

    template = env.get_template('resume.html')
    rendered_html = template.render(site=site_config, page={})

    # 4. Write output to preview.html
    preview_path = os.path.join(base_dir, 'preview.html')
    with open(preview_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    print(f"Preview successfully generated at: {preview_path}")

if __name__ == '__main__':
    build_site()
