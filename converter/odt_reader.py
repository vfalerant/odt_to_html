import zipfile
import xml.etree.ElementTree as ET


NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
    "style": "urn:oasis:names:tc:opendocument:xmlns:style:1.0",
    "fo": "urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"
}


def normalize_block_text(text):

    if text is None:
        return ""

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    while "  " in text:
        text = text.replace("  ", " ")

    return text.strip()


def load_style_map(content_root, styles_root):

    style_map = {}

    all_styles = []

    # content.xml style-ok
    all_styles.extend(
        content_root.findall(".//style:style", NS)
    )

    # styles.xml style-ok
    all_styles.extend(
        styles_root.findall(".//style:style", NS)
    )

    for style in all_styles:

        style_name = style.attrib.get(
            f"{{{NS['style']}}}name"
        )

        if not style_name:
            continue

        text_props = style.find(
            "style:text-properties",
            NS
        )

        is_bold = False
        is_italic = False

        if text_props is not None:

            font_weight = text_props.attrib.get(
                f"{{{NS['fo']}}}font-weight",
                ""
            ).lower()

            font_style = text_props.attrib.get(
                f"{{{NS['fo']}}}font-style",
                ""
            ).lower()

            if font_weight == "bold":
                is_bold = True

            if font_style == "italic":
                is_italic = True

        style_map[style_name] = {
            "bold": is_bold,
            "italic": is_italic
        }

    return style_map


def process_inline(element, style_map):

    result = ""

    if element.text:
        result += element.text

    for child in element:

        # SPAN
        if child.tag == f"{{{NS['text']}}}span":

            span_text = process_inline(
                child,
                style_map
            )

            style_name = child.attrib.get(
                f"{{{NS['text']}}}style-name"
            )

            style_info = style_map.get(
                style_name,
                {}
            )

            is_bold = style_info.get(
                "bold",
                False
            )

            is_italic = style_info.get(
                "italic",
                False
            )

            if is_bold and is_italic:
                span_text = (
                    f"<strong><i>{span_text}</i></strong>"
                )

            elif is_bold:
                span_text = f"<strong>{span_text}</strong>"

            elif is_italic:
                span_text = f"<i>{span_text}</i>"

            result += span_text

        else:
            result += process_inline(
                child,
                style_map
            )

        if child.tail:
            result += child.tail

    return result


def is_layout_artifact(element, text):

    if text:
        return False

    if len(list(element)) > 0:
        return False

    style_name = element.attrib.get(
        f"{{{NS['text']}}}style-name"
    )

    if style_name is None:
        return True

    return False


def process_paragraph(
    element,
    blocks,
    style_map
):

    text = normalize_block_text(
        process_inline(element, style_map)
    )

    if is_layout_artifact(element, text):
        return

    if not text:
        blocks.append({
            "type": "empty",
            "text": ""
        })
        return

    blocks.append({
        "type": "p",
        "text": text
    })


def process_heading(
    element,
    blocks,
    style_map
):

    text = normalize_block_text(
        process_inline(element, style_map)
    )

    if not text:
        return

    level = element.attrib.get(
        f"{{{NS['text']}}}outline-level",
        "1"
    )

    blocks.append({
        "type": f"h{level}",
        "text": text
    })


def process_list(
    element,
    blocks,
    style_map
):

    for item in element.findall(
        "text:list-item",
        NS
    ):

        for p in item.findall(
            "text:p",
            NS
        ):

            text = normalize_block_text(
                process_inline(p, style_map)
            )

            if not text:
                continue

            blocks.append({
                "type": "list",
                "text": text
            })


def walk_content(
    node,
    blocks,
    style_map
):

    for child in node:

        tag = child.tag

        if tag == f"{{{NS['text']}}}p":

            process_paragraph(
                child,
                blocks,
                style_map
            )

        elif tag == f"{{{NS['text']}}}h":

            process_heading(
                child,
                blocks,
                style_map
            )

        elif tag == f"{{{NS['text']}}}list":

            process_list(
                child,
                blocks,
                style_map
            )

        walk_content(
            child,
            blocks,
            style_map
        )


def read_odt_blocks(filepath):

    with zipfile.ZipFile(filepath) as z:

        content_xml = z.read("content.xml")
        styles_xml = z.read("styles.xml")

    content_root = ET.fromstring(content_xml)
    styles_root = ET.fromstring(styles_xml)

    style_map = load_style_map(
        content_root,
        styles_root
    )

    office_text = content_root.find(
        "office:body/office:text",
        NS
    )

    blocks = []

    walk_content(
        office_text,
        blocks,
        style_map
    )

    while (
        blocks
        and blocks[-1]["type"] == "empty"
    ):
        blocks.pop()

    return blocks