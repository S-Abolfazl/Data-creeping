import csv
import re
from urllib.parse import urlparse, unquote
import requests
from bs4 import BeautifulSoup


def remove_link(the_datas):
    arr = []
    for data in the_datas:
        d = data.text
        parsed_url = urlparse(d)
        cleaned_text = unquote(parsed_url.path + parsed_url.query)
        arr.append(cleaned_text[14:])
        # arr.append("".join(re.findall(r"[\u0600-\u06FF]+", x))) # bad
    return arr


urls = [
    "https://www.mehrnews.com/",
    "https://www.asriran.com/",
    "https://namanews.com/",
    "https://www.irna.ir/",
    "https://www.isna.ir/"
]
sitemaps = []
datas = dict()

for url in urls:
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    label = None
    le = soup.find('meta', attrs={'property': 'nastooh:pageType'})
    if le:
        label = le.get('content')
    robots_txt_response = requests.get(url + 'robots.txt').content
    robots_txt_string = robots_txt_response.decode('utf-8')
    sitemaps = re.findall(r'Sitemap:\s*(https?://[^\s]+)', robots_txt_string)
    for link in sitemaps:
        if '1402' in link:
            response = requests.get(link).content
            robots_string_based_date = response.decode('utf-8')
            soup = BeautifulSoup(robots_string_based_date, 'html.parser')
            sitemaps1 = soup.find_all('loc')
            for i in range(0, len(sitemaps1)):
                response = requests.get(sitemaps1[i].text).content
                robots_string_based_data = response.decode('utf-8')
                soup = BeautifulSoup(robots_string_based_data, 'html.parser')
                sitemaps2 = soup.find_all('loc')
                strings = remove_link(sitemaps2)
                for string in strings:
                    datas[string] = [url, label]

print('The length of collected datas is : ', len(datas))
# write the datas in a csv file
csv_file_path = 'output.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Data', 'Website', 'Label'])
    for key, values in datas.items():
        csv_writer.writerow([key] + values)

    csvfile.close()

print('completed !')
