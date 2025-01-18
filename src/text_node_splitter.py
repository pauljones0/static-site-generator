from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    text_to_process = ""
    normal_node_indices = []
    
    # Collect all NORMAL text and track which nodes they came from
    for i, node in enumerate(old_nodes):
        if node.text_type == TextType.NORMAL:
            text_to_process += node.text
            normal_node_indices.extend([i] * len(node.text))
    
    # If no delimiters found, return original nodes
    if delimiter not in text_to_process:
        return old_nodes
        
    # Check for balanced delimiters in combined text
    parts = text_to_process.split(delimiter)
    if len(parts) % 2 == 0:
        raise ValueError(f"Invalid Markdown syntax: Unmatched delimiter {delimiter}")
    
    # Process the parts and rebuild nodes
    current_pos = 0
    in_delimiter = False
    result = []
    
    for i, old_node in enumerate(old_nodes):
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
            
        node_text = ""
        while current_pos < len(text_to_process) and normal_node_indices[current_pos] == i:
            if text_to_process.startswith(delimiter, current_pos):
                if node_text:
                    new_nodes.append(TextNode(node_text, TextType.NORMAL if not in_delimiter else text_type))
                node_text = ""
                current_pos += len(delimiter)
                in_delimiter = not in_delimiter
            else:
                node_text += text_to_process[current_pos]
                current_pos += 1
                
        if node_text:
            new_nodes.append(TextNode(node_text, TextType.NORMAL if not in_delimiter else text_type))
    
    return new_nodes 