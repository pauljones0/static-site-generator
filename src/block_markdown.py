from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
import re

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.strip().startswith('# '):
            return line.strip()[2:].strip()
    raise ValueError("No H1 title found in markdown file")

def markdown_to_blocks(markdown):
    print("\n=== Starting markdown_to_blocks ===")
    print("Input markdown:")
    print(markdown)
    
    # Split by newlines
    lines = markdown.split("\n")
    print("\nSplit lines:")
    for i, line in enumerate(lines):
        print(f"Line {i}: '{line}'")
    
    # Initialize variables
    blocks = []
    current_block = []
    
    def is_ordered_list_item(line):
        return bool(re.match(r'^\d+\.\s', line.strip()))
    
    for line in lines:
        stripped_line = line.strip()
        # If we hit an empty line, finish the current block
        if not stripped_line:
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        # If it's a non-empty line
        else:
            # Check if this line should start a new block
            if current_block:
                current_first = current_block[0].strip()
                # Start new block if:
                # - Current line is a header
                # - Previous line was a header
                # - Current line is a list item but previous block wasn't
                # - Previous block was a list item but this isn't
                # - Current line is a quote but previous block wasn't
                # - Previous block was a quote but this isn't
                if (stripped_line.startswith('#') or
                    current_first.startswith('#') or
                    (stripped_line.startswith(('* ', '- ')) != current_first.startswith(('* ', '- '))) or
                    (is_ordered_list_item(stripped_line) != is_ordered_list_item(current_first)) or
                    (stripped_line.startswith('>') != current_first.startswith('>'))):
                    blocks.append("\n".join(current_block))
                    current_block = []
            current_block.append(stripped_line)
            
    # Add the last block if there is one
    if current_block:
        blocks.append("\n".join(current_block))

    print("\nFinal blocks:")
    for i, block in enumerate(blocks):
        print(f"Block {i}: '{block}'")
    
    return blocks

def block_to_block_type(block):
    # Check for code blocks first (must start and end with ```)
    if block.startswith("```") and block.endswith("```"):
        return "code"
        
    # Split into lines for multi-line block analysis
    lines = block.split("\n")
    first_line = lines[0]
    
    # Check for heading (starts with #)
    if first_line.startswith("#"):
        marker_end = 0
        while marker_end < len(first_line) and first_line[marker_end] == "#":
            marker_end += 1
        if marker_end <= 6 and marker_end < len(first_line) and first_line[marker_end] == " ":
            return "heading"
            
    # Check for quote block (all lines start with >)
    if all(line.startswith(">") for line in lines):
        return "quote"
        
    # Check for unordered list (all lines must start with the same marker, either * or -)
    if len(lines) > 0:
        if all(line.startswith("* ") for line in lines):
            return "unordered_list"
        if all(line.startswith("- ") for line in lines):
            return "unordered_list"
            
    # Check for ordered list (lines start with 1., 2., etc)
    if len(lines) > 0:
        try:
            for i, line in enumerate(lines, 1):
                if not line.startswith(f"{i}. "):
                    return "paragraph"
            return "ordered_list"
        except:
            return "paragraph"
            
    # Default to paragraph
    return "paragraph" 

def text_to_children(text):
    nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in nodes]

def paragraph_to_html_node(text):
    return ParentNode("p", text_to_children(text))

def heading_to_html_node(text):
    # Count number of #s at start
    level = 0
    while level < len(text) and text[level] == '#':
        level += 1
    content = text[level:].strip()
    return ParentNode(f"h{level}", text_to_children(content))

def code_to_html_node(text):
    # Remove the ``` from start and end
    content = text.strip('`').strip()
    return ParentNode("pre", [LeafNode("code", content)])

def quote_to_html_node(text):
    # Remove > from start of each line and get lines
    lines = [line[1:].strip() for line in text.split('\n')]
    
    # Group lines into paragraphs
    paragraphs = []
    current_paragraph = []
    
    for line in lines:
        if line:  # If line is not empty
            current_paragraph.append(line)
        elif current_paragraph:  # If line is empty and we have a paragraph
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []
    
    # Add the last paragraph if it exists
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
    
    # Create paragraph nodes for each paragraph
    children = []
    for paragraph in paragraphs:
        children.append(ParentNode("p", text_to_children(paragraph)))
    
    return ParentNode("blockquote", children)

def list_item_to_html_node(text):
    # Find the end of the list marker
    marker_end = 0
    while marker_end < len(text) and (text[marker_end] in '*-0123456789.' or text[marker_end].isspace()):
        marker_end += 1
    
    # Extract the content after the marker
    content = text[marker_end:].strip()
    
    # Process the content for nested markdown
    children = text_to_children(content)
    return ParentNode("li", children)

def unordered_list_to_html_node(text):
    items = text.split('\n')
    children = [list_item_to_html_node(item) for item in items]
    return ParentNode("ul", children)

def ordered_list_to_html_node(text):
    items = text.split('\n')
    children = [list_item_to_html_node(item) for item in items]
    return ParentNode("ol", children)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "paragraph":
            children.append(paragraph_to_html_node(block))
        elif block_type == "heading":
            children.append(heading_to_html_node(block))
        elif block_type == "code":
            children.append(code_to_html_node(block))
        elif block_type == "quote":
            children.append(quote_to_html_node(block))
        elif block_type == "unordered_list":
            children.append(unordered_list_to_html_node(block))
        elif block_type == "ordered_list":
            children.append(ordered_list_to_html_node(block))
            
    return ParentNode("div", children) 