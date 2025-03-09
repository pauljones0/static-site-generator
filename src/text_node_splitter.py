import re
import logging
from textnode import TextNode, TextType

logging.basicConfig(level=logging.DEBUG)

def split_nodes_delimiter(old_nodes, delimiter, text_type, strict=True):
    """
    Splits text nodes based on the specified delimiter and assigns the appropriate text type.

    Args:
        old_nodes (list of TextNode): The original list of text nodes.
        delimiter (str): The markdown delimiter to split by (e.g., '*', '**', '`').
        text_type (TextType): The type to assign to the split text (e.g., TextType.BOLD).
        strict (bool): If True, raise ValueError for malformed markdown. If False, handle gracefully.

    Returns:
        list of TextNode: The new list of text nodes after splitting.
    """
    if not delimiter:
        raise ValueError("Delimiter cannot be empty")
        
    logging.debug(f"Splitting nodes with delimiter: '{delimiter}' and text type: {text_type}")
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
            
        # Special handling for underscore delimiter to avoid splitting within words
        if delimiter == '_':
            pattern = r'(?:^|[^a-zA-Z0-9])_([^_]+)_(?:$|[^a-zA-Z0-9])'
        else:
            # Use regex pattern that matches delimiter with optional whitespace
            pattern = f'{re.escape(delimiter)}([^{re.escape(delimiter)}]+){re.escape(delimiter)}'
            
        matches = list(re.finditer(pattern, node.text))
        
        if not matches:
            new_nodes.append(node)
            continue
            
        current_pos = 0
        for match in matches:
            # Add text before the match
            if match.start() > current_pos:
                new_nodes.append(TextNode(node.text[current_pos:match.start()], TextType.NORMAL))
            
            # Add the matched text (without delimiters)
            content = match.group(1).strip()
            new_nodes.append(TextNode(content, text_type))
            
            current_pos = match.end()
        
        # Add any remaining text
        if current_pos < len(node.text):
            new_nodes.append(TextNode(node.text[current_pos:], TextType.NORMAL))
                
    return new_nodes 