import requests
import time
import logging


class DirFuzz:
    @staticmethod
    def find_dir(
        url: str,
        wordlist: str,
        max_depth: int,
        delay: float,
        current_depth: int = 0,
        headers: dict = None
    ):
        total_words_tried = 0
        total_requests_sent = 0
        found_directories = []
        requests_per_second = 0
        start_time = time.time()

        if current_depth >= max_depth:
            return (
                total_words_tried,
                total_requests_sent,
                found_directories,
                requests_per_second,
            )

        try:
            with open(wordlist, "r") as file:
                with requests.Session() as session:
                    start_time = time.time()
                    for line in file:
                        main_to_search = f"{url}{line.strip()}/"

                        try:
                            response = session.get(main_to_search, timeout=5, headers=headers)
                            total_requests_sent += 1

                            STATUS_CODES = [200, 301, 302, 401, 403]
                            if response.status_code in STATUS_CODES:
                                if (
                                    "Page not found" not in response.text
                                    and "404" not in response.text
                                ):
                                    content_size = len(response.content)
                                    logging.info(
                                        f"Success: {response.status_code} - Size: {content_size} - Found {main_to_search}"
                                    )
                                    total_words_tried += 1
                                    found_directories.append(main_to_search)

                        except requests.RequestException:
                            logging.warning(f"Failed to connect to {main_to_search}")

                        time.sleep(delay)

                    elapsed_time = time.time() - start_time
                    if elapsed_time > 0:
                        requests_per_second = total_requests_sent / elapsed_time

        except FileNotFoundError:
            logging.error(f"The wordlist file '{wordlist}' was not found.")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        return (
            total_words_tried,
            total_requests_sent,
            found_directories,
            requests_per_second,
        )
