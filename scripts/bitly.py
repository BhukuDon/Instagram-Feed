import bitlyshortener


#POST https://api-ssl.bitly.com/v4/shorten

def shortURL(url):
    """
        Takes url, Return shorterned URL. 
    """
    urlList = list()
    urlList.append(url)
    apiKey = ["4dd7daadc0962f21caab05f7e6609289c950dc84"]
    login = "o_37n6p0bq6e"
    shortener = bitlyshortener.Shortener(tokens=apiKey, max_cache_size=256)
    x=shortener.shorten_urls(urlList)
    return(x[0])
