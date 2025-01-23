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
            
        # Count delimiters to ensure they're balanced
        if delimiter not in node.text or node.text.count(delimiter) % 2 != 0:
            if strict:
                raise ValueError(f"Invalid Markdown syntax: Unmatched delimiter {delimiter}")
            new_nodes.append(node)
            continue
            
        parts = re.split(f'({re.escape(delimiter)})', node.text)
        current_type = TextType.NORMAL
        
        for i, part in enumerate(parts):
            if part == delimiter:
                current_type = text_type if current_type == TextType.NORMAL else TextType.NORMAL
                continue
            # Special handling for empty content between delimiters
            if current_type == text_type and part.strip() == "":
                new_nodes.append(TextNode("", current_type))
            else:
                new_nodes.append(TextNode(part, current_type))
                
    return new_nodes 