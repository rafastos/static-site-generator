import re

def extract_markdown_images(text):
    # text -> [(alt_text, url), ...]
    img_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(img_regex, text)

def extract_markdown_links(text):
    # text -> [(anchor_text, url), ...]
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_regex, text)