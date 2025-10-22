from playwright.sync_api import sync_playwright
from utils import get_logger

logger = get_logger(__name__)

def save_cookies_to_txt(cookies, path):
    """
    Converte cookies do Playwright para o formato Netscape compatível com yt-dlp
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# Netscape HTTP Cookie File\n")
        for cookie in cookies:
            domain = cookie.get("domain", "")
            flag = "TRUE" if domain.startswith(".") else "FALSE"
            path_cookie = cookie.get("path", "/")
            secure = "TRUE" if cookie.get("secure", False) else "FALSE"
            expiry = str(int(cookie.get("expires", 0))) if cookie.get("expires") else "0"
            name = cookie.get("name", "")
            value = cookie.get("value", "")
            line = f"{domain}\t{flag}\t{path_cookie}\t{secure}\t{expiry}\t{name}\t{value}\n"
            f.write(line)
        

def generate_youtube_cookies():
    """
    Abre o YouTube com Playwright (headless Chromium) e salva cookies no formato Netscape.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.youtube.com")
        page.wait_for_timeout(5000) 

        cookies = context.cookies()
        save_cookies_to_txt(cookies, "/tmp/cookies.txt")

        # Log the contents of the saved cookies.txt for debugging
        try:
            with open("/tmp/cookies.txt", "r", encoding="utf-8") as cf:
                contents = cf.read()
                logger.debug("Contents of /tmp/cookies.txt:\n%s", contents)
                # Also print to stdout explicitly for immediate console visibility
                print(contents)
        except Exception as e:
            logger.error("Failed to read /tmp/cookies.txt: %s", e)

        browser.close()

if __name__ == "__main__":
    generate_youtube_cookies()
