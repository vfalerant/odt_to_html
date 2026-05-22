def map_block(text, element_type, is_first):

    # üres sor
    if element_type == "empty":
        return '<p style="text-align:center;">*</p>'

    # első valódi tartalom
    if is_first:
        return f"<h2>{text}</h2>"

    # heading
    if element_type.startswith("h"):

        try:
            level = int(element_type[1])
        except:
            level = 2

        if level == 1:
            return f"<h2>{text}</h2>"

        return f"<h{level}>{text}</h{level}>"

    # lista
    if element_type == "list":
        return f'<p style="text-align:justify;">• {text}</p>'

    # normál paragraph
    return f'<p style="text-align:justify;">{text}</p>'


def generate_html(blocks):

    html_parts = []

    first_text_found = False

    for block in blocks:

        html = map_block(
            text=block["text"],
            element_type=block["type"],
            is_first=(
                not first_text_found
                and block["type"] != "empty"
            )
        )

        if block["type"] != "empty":
            first_text_found = True

        html_parts.append(html)

    return "\n\n".join(html_parts)