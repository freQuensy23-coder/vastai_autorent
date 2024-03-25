import requests
from loguru import logger
from rent import rent_and_setup_new_llm
from sqlite import LinksTable


def url_unaccessible(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("URL is accessible.")
            return 0
        else:
            logger.info(f"URL is not accessible. Status code: {response.status_code}")
            return 1
    except requests.ConnectionError:
        logger.info("Failed to connect to the URL.")



url_to_check = "https://ray-evolved-gannet.ngrok-free.app"

if __name__ == "__main__":
    link_table = LinksTable()
    link_table.create_table()
    link_table.insert_link(url_to_check)
    links = link_table.execute_query("SELECT links FROM links_gpu")[0]
    for link in links:
        logger.info(f"link is {link}")
        if url_unaccessible(link):
            rent_and_setup_new_llm()

