import requests
import bs4

def open_url(url):
    res = requests.get(url)
    return res

def find_next(html_data):
    soup = bs4.BeautifulSoup(html_data, "html.parser")
    target = soup.find_all("span", class_ = "next")

    print(target[0].a['href'])
    #return target.a.text

def find_movies(html_data):
    soup = bs4.BeautifulSoup(html_data, "html.parser")
    target = soup.find_all("div", class_ = "hd")

    name = list()
    for i in target:
        name.append(i.a.span.text)
    return name

def main():

    url = "https://movie.douban.com/top250"
    l = list()
    for i in range(0, 250, 25):
        append = "?start=%d&filter=" % i
        new_url = url + append
        # print(new_url)
        res = open_url(new_url)
        l.extend(find_movies(res.text))
    print(l)

if __name__ == "__main__":
    main()

