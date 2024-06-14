"""
from selenium.webdriver.common.by import By
import time
import json

chrome_user_data_dir = "/private/var/folders/m5/yj7mn8kj37qgy9yywh0kcvxr0000gn/T/tmpa_qvd7xw/Default/Default"
boomkat_url = "https://boomkat.com/t/genre/basic-channel-slash-dub-techno?page=1"

base_url = "https://boomkat.com"  # Replace with the actual URL
url_template = "/new-releases?page=1&q[status]=recommended&q[release_date]=1900"

from seleniumbase import SB

with SB(uc=True, test=True, user_data_dir=chrome_user_data_dir) as sb:
    sb.driver.uc_open_with_tab(base_url)
    sb.sleep(1.2)

    if sb.is_element_visible('iframe[src*="challenge"]'):
        with sb.frame_switch('iframe[src*="challenge"]'):
            sb.click("span.mark")

    sb.activate_demo_mode()
    time.sleep(5)

    data = []

    # last_page_url = sb.driver.find_element(
    #     By.XPATH, '//a[text()="Last »"]'
    # ).get_attribute("href")

    total_pages = 501

    current_page_url = base_url + url_template
    sb.driver.get(current_page_url)
    time.sleep(10)

    album_elements = sb.driver.find_elements(
        By.XPATH, '//div[@class="table-row album"]'
    )

    for album_element in album_elements:
        artist = album_element.find_element(By.XPATH, ".//strong").text
        title = album_element.find_element(
            By.XPATH, './/span[@class="album-title"]'
        ).text

        # Find the label for the current album
        label_element = album_element.find_element(
            By.XPATH,
            './/span[@class="catnum"]/following-sibling::span/a[starts-with(@href, "/labels/")]',
        )
        label = label_element.text if label_element else None

        # Find the genre for the current album
        genre_element = album_element.find_element(
            By.XPATH, './/span[@class="genre"]/a'
        )
        genre = genre_element.text if genre_element else None

        data.append({"artist": artist, "title": title, "label": label, "genre": genre})

"""
"""
    for page in range(1, 3):
        time.sleep(5)
        print("time sleep 5")
        albums = sb.driver.find_elements(By.CLASS_NAME, "product_item")
        print("albums bulundu")

        element = sb.driver.find_element(
            By.XPATH, '//div[@class="table-cell-text-fit"]/a/span[@class="album-title"]'
        )
        artist_name = element.find_element(By.TAG_NAME, "strong").text
        album_name = element.text
        print("Artist Name:", artist_name)
        print("Album Name:", album_name)
        for album in albums:
            artist = album.find_element(By.CLASS_NAME, "release__artist").text.strip()

            title = album.find_element(By.CLASS_NAME, "release__title").text.strip()
            label = album.find_element(By.CLASS_NAME, "release__label").text.strip()
            genre = album.find_element(By.CLASS_NAME, "release__genre").text.strip()

            data.append(
                {
                    "title": title,
                    "artist": artist,
                    "label": label,
                    "genre": genre,
                }
            )

        print(f"Page * {page} * is scraped ")
        print(data)
        sb.driver.find_element(By.CLASS_NAME, "next").click()
        page += 1

        time.sleep(3)

"""
"""
with open("bk_albums_raw.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Data has been successfully scraped and saved to albums.json")
"""
import json

with open("boomkat/data/bk_albums_raw.json", "r") as f:
    data = json.load(f)
    print(len(data))
