import requests
import bs4

def open_url(url):
    res = requests.get(url)
    return res

def find_movies(html_data):
    soup = bs4.BeautifulSoup(html_data, "html.parser")
    target = soup.find_all("div", class_ = "item")

    d = dict()
    for i in target:
        rank = i.find_all("div",  class_="pic")[0].em.text
        name = i.find_all("span", class_="title")[0].text
        d[rank] = name
    return d

def main():
    url = "https://movie.douban.com/top250"
    movie_dict = dict()
    for i in range(0, 250, 25):
        append = "?start=%d&filter=" % i
        new_url = url + append
        # print(new_url)
        res = open_url(new_url)
        movie_dict.update(find_movies(res.text))
    print(movie_dict)
    f = open("douban_top250.txt", "w", encoding= "utf-8")
    f.write("%s, %s\n" % ("ID", "Name"))
    for (k, v) in movie_dict.items():
        f.write("%s, \"%s\"\n" % (k, v))
    f.close()

if __name__ == "__main__":
    main()

