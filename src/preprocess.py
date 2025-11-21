def remove_governo_headers(text: str) -> str:
    """Remove cabeçalhos repetidos do Diário Oficial."""
    linhas = text.split("\n")
    novas = []

    for l in linhas:
        s = l.strip()
        if any(frase in s for frase in [
            "Este documento pode ser verificado pelo código",
            "https://www.doe.sp.gov.br/autenticidade",
            "Documento assinado digitalmente conforme",
            "ICP-Brasil"
        ]):
            continue
        novas.append(l)

    return "\n".join(novas)


def clean_text_block(text: str) -> str:
    """Normaliza blocos de texto quebrados."""
    lines = text.split("\n")
    new_lines = []
    buffer = ""

    for line in lines:
        line_strip = line.strip()

        if not line_strip:
            if buffer:
                new_lines.append(buffer)
                buffer = ""
            continue

        if len(line_strip.split()) <= 3:
            buffer += " " + line_strip
        else:
            if buffer and not buffer.endswith((".", "!", "?", ";", ":")):
                buffer += " " + line_strip
            else:
                if buffer:
                    new_lines.append(buffer)
                buffer = line_strip

    if buffer:
        new_lines.append(buffer)

    return "\n".join(new_lines)
