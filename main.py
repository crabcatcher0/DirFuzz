import argparse
import logging


from bust.buster import DirFuzz


logging.basicConfig(
    format="%(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Directory scanner for web applications.\n\n"
            "Example:\n"
            "python main.py -u http://example.com/ -w wordlist.txt -D 2 -T 0.5 -M\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="Target URL to scan (e.g: http://example.com/)",
    )
    parser.add_argument(
        "-w",
        "--wordlist",
        type=str,
        required=True,
        help="Path to the wordlist file (e.g: custom.txt)",
    )
    parser.add_argument(
        "-D",
        "--max-depth",
        type=int,
        default=1,
        help="Maximum depth to scan (default: 1)",
    )
    parser.add_argument(
        "-T",
        "--delay",
        type=float,
        default=0,
        help="Delay time in seconds between requests (default: 0)",
    )

    args = parser.parse_args()

    url = args.url.strip()
    if not url.endswith("/"):
        url += "/"

    max_depth = args.max_depth
    wordlist = args.wordlist
    delay = args.delay

    total_words_tried = 0
    total_requests_sent = 0
    req_per_sec = 0

    urls_to_scan = [(url, 0)]
    scanned_urls = set()

    try:
        while urls_to_scan:
            current_url, current_depth = urls_to_scan.pop(0)

            if current_url in scanned_urls:
                continue
            scanned_urls.add(current_url)

            logging.info(f"\nScanning: {current_url} at depth {current_depth}")

            words_tried, requests_sent, found_dirs, req_per_sec = DirFuzz.find_dir(
                current_url,
                wordlist=wordlist,
                max_depth=max_depth,
                delay=delay,
                current_depth=current_depth,
            )
            total_words_tried += words_tried
            total_requests_sent += requests_sent

            for directory in found_dirs:
                if directory not in scanned_urls and current_depth + 1 < max_depth:
                    urls_to_scan.append((directory, current_depth + 1))

    except KeyboardInterrupt:
        logging.warning("Scan interrupted.")

    logging.info(
        f"\nTotal matched words: {total_words_tried} | Total requests sent: {total_requests_sent} | Avg. req in 1sec: {round(req_per_sec)}"
    )
    logging.info("Thank you for using the Dir_Fuzz!")


if __name__ == "__main__":
    main()
