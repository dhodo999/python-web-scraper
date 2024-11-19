import requests
from .url import URLConfig
from bs4 import BeautifulSoup

def CheckURL(urls) -> list:
    new_urls = []

    if not urls or len(urls) == 0:
        return new_urls
    
    for url in urls:
        if url in new_urls:
            continue
        new_urls.append(url)

    return new_urls

def ValidateURL(domain, url) -> bool:
    """
    Validating URL based on configuration
    """
    if URLConfig['must_start_with']['enable']:
        if not url.startswith(URLConfig['must_start_with']['protocol']):
            print(f"URL {url} must start with {URLConfig['must_start_with']['protocol']}")
            return False
    
    if ("http" not in url or "https" not in url) and URLConfig['must_contain']['https']:
        print(f"URL {url} must contain https protocol")
        return False
    
    if "www" not in url and URLConfig['must_contain']['www']:
        print(f"URL {url} must contain www")
        return False
    
    if domain not in url and URLConfig['must_contain']['domain']:
        print(f"URL {url} must contain {domain}")
        return False
    
    print (f"URL {url} is valid")

    return True

def QueryGenerator(domain, keyword, search_engine="google") -> str:
    """
    Generating query based on search engine
    """
    if search_engine == "bing":
        return f"sites:{domain} {keyword}"
    
    return f"site:{domain} {keyword}"

def SafeSearchBypass(url) -> str:
    """
    Bypassing SafeSearch by adding paramter to the URL
    """
    if "google" in url:
        return f"{url}&safe=off"
    elif "bing" in url:
        return f"{url}&SafeSearch=Off"
    
    return url

def FetchFromSearchEngine(domain, keyword) -> list:
    """
    Fetching URLs from search engine
    """
    urls = []
    blocked = False
    search_engine_url = URLConfig['search_engine_url']

    if len(search_engine_url) == 0:
        print("No search engine URL found")

        return urls
    
    blocked_text = URLConfig['blocked_text']

    for search_engine in search_engine_url:
        blocked = False

        query = QueryGenerator(domain, keyword).replace(" ", "+")
        response = requests.get(SafeSearchBypass(search_engine + query), headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code != 200:
            print(f"Failed to fetch from {search_engine}")
            continue

        for block in blocked_text:
            if block in response.text:
                print(f"Blocked by {search_engine}")
                blocked = True
                break

        if blocked:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        for a in soup.find_all('a', href=True):
            if not ValidateURL(domain, a['href']):
                continue
            urls.append(a['href'])

    filtered_urls = CheckURL(urls)
    print(f"Gathered {len(filtered_urls)} urls from search engine for keyword: {keyword}")

    return filtered_urls