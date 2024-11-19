from main.get_url import FetchFromSearchEngine
from main.file import WriteFile, GenerateName

def main():
    print("Simple Web Scraper in python")
    domain = input("Enter domain (use * for wildcard): ")
    keyword = input("Enter keyword (example: food recipe): ")
    print("========================================")
    print("Fetching URLs from search engine")
    urls = FetchFromSearchEngine(domain, keyword)
    filename = GenerateName()
    print("========================================")
    WriteFile(urls, filename)
    print("========================================")

if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("\nExiting...")
    exit(0)