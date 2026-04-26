# 这是一个示例 Python 脚本。
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin


URL = "https://www.pythonscraping.com/pages/page3.html"


def get_html(url):
    """
    English: Send a request to the website and return HTML content.
    中文：向网站发送请求，并返回 HTML 内容。
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print("Website connected successfully.")
        print("网站连接成功。")
        return response.text

    except requests.exceptions.RequestException as error:
        print("Failed to connect to the website.")
        print("网站连接失败。")
        print("Error:", error)
        return None


def scrape_gifts(html):
    """
    English: Extract gift name, description, price, and image link.
    中文：提取礼物名称、描述、价格和图片链接。
    """
    soup = BeautifulSoup(html, "html.parser")

    gift_table = soup.find("table", id="giftList")
    gift_rows = gift_table.find_all("tr", class_="gift")

    gift_data = []

    for row in gift_rows:
        columns = row.find_all("td")

        name = columns[0].get_text(strip=True)
        description = columns[1].get_text(" ", strip=True)
        price = columns[2].get_text(strip=True)

        image_tag = columns[3].find("img")
        image_link = urljoin(URL, image_tag["src"]) if image_tag else "No image"

        gift_data.append({
            "name": name,
            "description": description,
            "price": price,
            "image_link": image_link
        })

    return gift_data


def print_gifts(gift_data):
    """
    English: Print the scraped gift information.
    中文：打印爬取到的礼物信息。
    """
    print("\n*** Gift Information / 礼物信息 ***")

    for index, gift in enumerate(gift_data, start=1):
        print(f"\nGift {index} / 第 {index} 个礼物")
        print("Name / 名称:", gift["name"])
        print("Description / 描述:", gift["description"])
        print("Price / 价格:", gift["price"])
        print("Image Link / 图片链接:", gift["image_link"])

    print("\n*** END / 结束 ***")


def save_to_csv(gift_data, filename):
    """
    English: Save the scraped data into a CSV file.
    中文：把爬取的数据保存到 CSV 文件中。
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["name", "description", "price", "image_link"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(gift_data)

    print(f"\nData saved as {filename}")
    print(f"数据已保存为 {filename}")


def main():
    """
    English: Run the full scraping process.
    中文：运行完整的爬虫流程。
    """
    html = get_html(URL)

    if html:
        gift_data = scrape_gifts(html)
        print_gifts(gift_data)
        save_to_csv(gift_data, "gift_data.csv")


main()