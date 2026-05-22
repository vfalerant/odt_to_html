import zipfile
import xml.etree.ElementTree as ET


NS = {
    "office": "urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0"
}


def normalize_text(text):

    if text is None:
        return ""

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    text = " ".join(text.split())

    return text.strip()


def extract_text(element):

    text = "".join(element.itertext())

    return normalize_text(text)


def is_layout_artifact(element, text):

    # ha van szöveg → biztos nem artifact
    if text:
        return False

    # ha vannak child node-ok → lehet valódi tartalom
    if len(list(element)) > 0:
        return False

    # csak akkor artifact,
    # ha SEMMI nincs benne
    # és nincs style sem

    style_name = element.attrib.get(
        f"{{{NS['text']}}}style-name"
    )

    if style_name is None:
        return True

    return False

def process_paragraph(element, blocks):

    text = extract_text(element)

    # technikai/layout paragraph skip
    if is_layout_artifact(element, text):
        return

    # valódi üres sor
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


def process_heading(element, blocks):

    text = extract_text(element)

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


def process_list(element, blocks):

    for item in element.findall("text:list-item", NS):

        for p in item.findall("text:p", NS):

            text = extract_text(p)

            if not text:
                continue

            blocks.append({
                "type": "list",
                "text": text
            })


def walk_content(node, blocks):

    for child in node:

        tag = child.tag

        # paragraph
        if tag == f"{{{NS['text']}}}p":
            process_paragraph(child, blocks)

        # heading
        elif tag == f"{{{NS['text']}}}h":
            process_heading(child, blocks)

        # list
        elif tag == f"{{{NS['text']}}}list":
            process_list(child, blocks)

        # rekurzió
        walk_content(child, blocks)


def read_odt_blocks(filepath):

    with zipfile.ZipFile(filepath) as z:
        xml_content = z.read("content.xml")

    root = ET.fromstring(xml_content)

    office_text = root.find(
        "office:body/office:text",
        NS
    )

    blocks = []

    walk_content(office_text, blocks)

    # trailing empty cleanup
    while blocks and blocks[-1]["type"] == "empty":
        blocks.pop()

    return blocks