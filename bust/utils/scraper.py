import requests
from bs4 import BeautifulSoup


def extract_links_from_html(url: str):
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        links = set()

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]

            if href.startswith("/"):
                links.add(url.rstrip("/") + href)
            elif href.startswith("http") and url in href:
                links.add(href)

        return links
    except requests.RequestException as e:
        print(f"Error in HTML: {e}")
        return set()


def generate_dynamic_wordlist(base_url: str):
    html_links = extract_links_from_html(base_url)
    dynamic_wordlist = set()
    for link_set in [html_links]:
        for link in link_set:
            if link.endswith("/"):
                dynamic_wordlist.add(link)

    print(dynamic_wordlist)


generate_dynamic_wordlist("https://scrapeme.live/shop/")
