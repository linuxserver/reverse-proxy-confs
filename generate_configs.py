# generate_configs.py

import os
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader

# --- Configuration ---
YAML_FILE = 'config_data.yml'
TEMPLATE_DIR = 'templates'
CUSTOM_DIR = 'custom_configs'
OUTPUT_DIR = 'output'
# ---------------------

def generate_configs():
    """
    Generates Nginx config files from a YAML data source and Jinja2 templates.
    """
    print("--- Starting Nginx Config Generation ---")

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory '{OUTPUT_DIR}' is ready.")

    # Load data from YAML file
    try:
        with open(YAML_FILE, 'r') as f:
            data = yaml.safe_load(f)
        print(f"Successfully loaded data from '{YAML_FILE}'.")
    except FileNotFoundError:
        print(f"ERROR: Data file not found at '{YAML_FILE}'. Exiting.")
        return
    except yaml.YAMLError as e:
        print(f"ERROR: Could not parse YAML file '{YAML_FILE}': {e}. Exiting.")
        return

    # Set up Jinja2 environment
    try:
        env = Environment(
            loader=FileSystemLoader(TEMPLATE_DIR),
            trim_blocks=True,
            lstrip_blocks=True
        )
        subdomain_template = env.get_template('subdomain.conf.j2')
        subfolder_template = env.get_template('subfolder.conf.j2')
        print("Jinja2 templates loaded successfully.")
    except Exception as e:
        print(f"ERROR: Failed to load Jinja2 templates from '{TEMPLATE_DIR}': {e}. Exiting.")
        return

    # Generate templated subdomain configs
    print("\n--- Generating Templated Subdomain Configs ---")
    subdomain_items = data.get('subdomains', [])
    for item in subdomain_items:
        filename = f"{item['name']}.subdomain.conf.sample"
        output_path = os.path.join(OUTPUT_DIR, filename)
        rendered_content = subdomain_template.render(item=item)
        with open(output_path, 'w') as f:
            f.write(rendered_content)
        print(f"  [OK] Generated {filename}")

    # Generate templated subfolder configs
    print("\n--- Generating Templated Subfolder Configs ---")
    subfolder_items = data.get('subfolders', [])
    for item in subfolder_items:
        filename = f"{item['name']}.subfolder.conf.sample"
        output_path = os.path.join(OUTPUT_DIR, filename)
        rendered_content = subfolder_template.render(item=item)
        with open(output_path, 'w') as f:
            f.write(rendered_content)
        print(f"  [OK] Generated {filename}")

    # Copy custom configs
    print("\n--- Copying Custom Configs ---")
    if not os.path.isdir(CUSTOM_DIR):
        print(f"WARNING: Custom configs directory '{CUSTOM_DIR}' not found. Skipping copy.")
    else:
        # Process custom subdomains
        for app_name in data.get('custom', {}).get('subdomains', []):
            filename = f"{app_name}.subdomain.conf.sample"
            source_path = os.path.join(CUSTOM_DIR, filename)
            dest_path = os.path.join(OUTPUT_DIR, filename)
            if os.path.exists(source_path):
                shutil.copy(source_path, dest_path)
                print(f"  [OK] Copied {filename}")
            else:
                print(f"  [!!] WARNING: Custom config file not found: {source_path}")
        
        # Process custom subfolders
        for app_name in data.get('custom', {}).get('subfolders', []):
            filename = f"{app_name}.subfolder.conf.sample"
            source_path = os.path.join(CUSTOM_DIR, filename)
            dest_path = os.path.join(OUTPUT_DIR, filename)
            if os.path.exists(source_path):
                shutil.copy(source_path, dest_path)
                print(f"  [OK] Copied {filename}")
            else:
                print(f"  [!!] WARNING: Custom config file not found: {source_path}")

    print("\n--- Generation Complete ---")

if __name__ == "__main__":
    generate_configs()
