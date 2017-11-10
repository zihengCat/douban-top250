import requests
import bs4

def open_url(url):
    res = requests.get(url)
    return res

def get_next(html_data):
    soup = bs4.BeautifulSoup(html_data, "html.parser")
    target = soup.find_all("span", class_="next")
    if target[0].a != None:
        return target[0].a["href"]
    else:
        return None

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
        res = open_url(url + append)
        append = get_next(res.text)
        if append == None:
            break
        else:
            print(url + append)
        movie_dict.update(find_movies(res.text))

    print(movie_dict)
    f = open("douban_top250.txt", "w", encoding= "utf-8")
    f.write("%s, %s, %s, %s\n" % ("ID", "Name", "Rating", "Quote"))
    for (k, v) in movie_dict.items():
        f.write("%s, \"%s\", \"%s\", \"%s\"\n" %
               (k, v[0], v[1], ""))
    f.close()

if __name__ == "__main__":
    main()

