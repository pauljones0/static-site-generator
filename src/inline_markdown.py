import re
from textnode import TextNode, TextType
from text_node_splitter import split_nodes_delimiter

def extract_markdown_images(text):
    pattern = r"!\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[((?:[^\[\]]|\[[^\[\]]*\])*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
            
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            sections = current_text.split(image_markdown, 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            current_text = sections[1] if len(sections) > 1 else ""
            
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type not in [TextType.NORMAL, TextType.ITALIC, TextType.BOLD]:
            new_nodes.append(old_node)
            continue
            
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
            
        current_text = old_node.text
        parent_type = old_node.text_type  # Store the parent's text type
        
        for anchor_text, url in links:
            link_markdown = f"[{anchor_text}]({url})"
            sections = current_text.split(link_markdown, 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], parent_type))  # Use parent's type
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            current_text = sections[1] if len(sections) > 1 else ""
            
        if current_text:
            new_nodes.append(TextNode(current_text, parent_type))  # Use parent's type
            
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    
    # Process text styling first
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD, strict=False)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC, strict=False)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE, strict=False)
    
    # Process links and images last
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes