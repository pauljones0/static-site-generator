import os
import shutil
from block_markdown import markdown_to_html_node, extract_title

def copy_files_recursive(src_dir, dest_dir):
    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created directory: {dest_dir}")
    
    # Get all files and directories in source
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        # If it's a file, copy it
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied file: {src_path} -> {dest_path}")
        # If it's a directory, recursively copy it
        else:
            copy_files_recursive(src_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown content
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read template
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract title
    title = extract_title(markdown_content)
    
    # Replace placeholders
    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    
    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write output file
    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Walk through all files in content directory
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        
        # If it's a directory, recurse into it
        if not os.path.isfile(src_path):
            # Get relative path from content dir
            rel_path = os.path.relpath(src_path, dir_path_content)
            # Create corresponding destination path
            new_dest_dir = os.path.join(dest_dir_path, rel_path)
            # Recurse into directory
            generate_pages_recursive(src_path, template_path, new_dest_dir)
        # If it's a markdown file
        elif src_path.endswith('.md'):
            # Get relative path from content dir
            rel_path = os.path.relpath(src_path, dir_path_content)
            # Create destination path, replacing .md with .html
            dest_path = os.path.join(dest_dir_path, rel_path.replace('.md', '.html'))
            # Generate the page
            generate_page(src_path, template_path, dest_path)

def main():
    # Define directories
    static_dir = "static"
    public_dir = "public"
    content_dir = "content"
    template_path = "template.html"
    
    # Delete public directory if it exists
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
        print(f"Deleted existing directory: {public_dir}")
    
    # Copy static files to public directory
    copy_files_recursive(static_dir, public_dir)
    
    # Generate pages recursively
    generate_pages_recursive(content_dir, template_path, public_dir)
    
    print("Site generation complete!")

if __name__ == "__main__":
    main()