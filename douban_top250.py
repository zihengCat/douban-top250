import requests
import bs4
import time

# Open URL, return Request Object
def open_url(url):
    ua_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
    res = requests.get(url, headers = ua_headers)
    return res

# Get the next URL from target HTML
def get_next(html_data):
    soup = bs4.BeautifulSoup(html_data, "html.parser")
    target = soup.find_all("span", class_="next")
    if target[0].a != None:
        return target[0].a["href"]
    else:
        return None

# Find infomations, return a dict
def find_movies(html_data):
    soup = bs4.BeautifulSoup(html_data, "html.parser")
    target = soup.find_all("div", class_ = "item")

    d = dict()
    for i in target:
        m_id = i.find_all("div",  class_="pic")[0].em.text
        m_name = i.find_all("span", class_="title")[0].text
        m_rating = i.find_all("span", class_="rating_num")[0].text
        # m_quote = i.find_all("span", class_="inq")[0].text
        d[m_id] = [m_name, m_rating]
    return d

def main():
    movie_dict = dict()

    url = "https://movie.douban.com/top250"
    append = ""
    while True:
        time.sleep(1)
        res = open_url(url + append)
        append = get_next(res.text)
        if append == None:
            break
        else:
            print(url + append)
        movie_dict.update(find_movies(res.text))

    # Save to .txt File
    print(movie_dict)
    f = open("douban_top250.txt", "w", encoding= "utf-8")
    f.write("%s, %s, %s, %s\n" % ("ID", "Name", "Rating", "Quote"))
    for (k, v) in movie_dict.items():
        f.write("%s, \"%s\", \"%s\", \"%s\"\n" %
               (k, v[0], v[1], ""))
    f.close()

if __name__ == "__main__":
    main()

