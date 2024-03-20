import requests
from loguru import logger

def url_unaccessible(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("URL is accessible.")
            return 0
            # Do something here if the status code is 200
        else:
            print(f"URL is not accessible. Status code: {response.status_code}")
            # Do something else here if the status code is not 200
            return 1
    except requests.ConnectionError:
        print("Failed to connect to the URL.")



# Example usage:
url_to_check = "https://ec5ye5oa230o.share.zrok.io/"
# url_unaccessible(url_to_check)
from rent import pickup_first_available_gpu, rent_gpu_by_id
from sqlite import LinksTable
if __name__ == "__main__":
    link_table = LinksTable()
    link_table.create_table()
    link_table.insert_link(url_to_check)
    links = link_table.execute_query("SELECT links FROM links_gpu").fetchall()
    for link in links:
        logger.info(f"link is {link}")
        if url_unaccessible(link):
            first_id = pickup_first_available_gpu()
            rent_gpu_by_id(first_id)

