import openpyxl as opx
import requests
from bs4 import BeautifulSoup


# creating our Excel file header
wb = opx.Workbook()
ws = wb.active
xlsx_header = ["Name", "Release", "Duration", "Rate"]
ws.append(xlsx_header)

url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
# WE add User-Agent cause IMdb had blocked web scrapping in the website
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

}
response = requests.get(url, headers=header)
html_content = response.content


class IMDBScrapping:
    def movies_scrapping():
        """This function scrape movie's name, release date, duration and at the end scrapes the ratings"""

        soup = BeautifulSoup(html_content, "html.parser")
        movies = soup.find_all(
            "li",  {'class': 'ipc-metadata-list-summary-item sc-bca49391-0 eypSaE cli-parent'})
        for movie in movies:
            name = movie.find(
                "h3", class_="ipc-title__text").text.strip("1234567890.")
            release = movie.find(
                "span", class_="sc-14dd939d-6 kHVqMR cli-title-metadata-item").text
            # WE choosed [1] cause there are three html codes with same cursor and class name that we should use index for duration's data
            duration = movie.find_all(
                "span", {'class': 'sc-14dd939d-6 kHVqMR cli-title-metadata-item'})[1].text
            rate = movie.find(
                "span", class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating").text
            # Adding final rows to our Excel file
            xlsx_rows = [name, release, duration, rate]
            ws.append(xlsx_rows)
        wb.save("IMDB250.xlsx")


IMDBScrapping.movies_scrapping()
