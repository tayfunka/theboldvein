from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import json

chrome_user_data_dir = "/private/var/folders/m5/yj7mn8kj37qgy9yywh0kcvxr0000gn/T/tmpa_qvd7xw/Default/Default"
boomkat_url = "https://boomkat.com/t/genre/basic-channel-slash-dub-techno?page=1"

base_url = "https://boomkat.com"  # Replace with the actual URL
url_template = "/new-releases?page={}&q[status]=recommended&q[release_date]=1900"

from seleniumbase import SB

with SB(uc=True, test=True, headless=True) as sb:
    sb.driver.uc_open_with_tab(base_url)
    sb.sleep(1.2)

    if sb.is_element_visible('iframe[src*="challenge"]'):
        with sb.frame_switch('iframe[src*="challenge"]'):
            sb.click("span.mark")

    sb.activate_demo_mode()
    time.sleep(5)

    data = []

    total_pages = 501  # Set the total number of pages you want to scrape
    time.sleep(6)

    for page in range(
        95, total_pages + 1
    ):  # Corrected the range to include total_pages
        current_page_url = base_url + url_template.format(page)
        sb.driver.get(current_page_url)
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
            try:
                genre_element = album_element.find_element(
                    By.XPATH, './/span[@class="genre"]/a'
                )
                genre = genre_element.text
            except NoSuchElementException:
                genre = None

            data.append(
                {"artist": artist, "title": title, "label": label, "genre": genre}
            )

        print(f"Page * {page} * is scraped ")

        time.sleep(6)

        # if page < total_pages:  # Only click the "Next" button if there are more pages
        #     sb.driver.find_element(By.CLASS_NAME, "next").click()
        #     time.sleep(4)


with open("bk_albums_raw.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Data has been successfully scraped and saved to bk_albums_raw.json")
