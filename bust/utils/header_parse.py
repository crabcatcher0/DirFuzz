def parse_header(header):
    headers = {}
    if header:
        for i in header.split(","):
            key, value = i.split(":")
            headers[key.strip()] = value.strip()
    return headers
