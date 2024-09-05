from datetime import datetime
import requests
from bs4 import BeautifulSoup


class HackerNewsClient:
    def __init__(self):
        self.base_url = "https://news.ycombinator.com/"

    def fetch_latest_news(self, limit=10):
        """
        获取并返回 Hacker News 网站上的最新热点新闻的标题和 URL
        """
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select('.athing')  # 查找新闻条目

        news_list = []
        news_count = 0
        for item in items:
            title = item.select_one('.titleline a').get_text()
            url = item.select_one('.titleline a')['href']

            # 如果链接是相对路径，添加 Hacker News 域名
            if not url.startswith('http'):
                url = self.base_url + url

            news_list.append((title, url))

            news_count += 1
            if news_count >= limit:
                break

        return news_list

    def save_to_markdown(self, news_list):
        """
        将新闻列表保存到 Markdown 文件
        """
        # 获取当天日期并生成文件名
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"hackernews_{date_str}.md"

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"# Hacker News 热点新闻 - {date_str}\n\n")
            for title, url in news_list:
                file.write(f"- [{title}]({url})\n")

        print(f"新闻已保存到文件: {filename}")

if __name__ == "__main__":
    client = HackerNewsClient()
    news = client.fetch_latest_news(limit=10)  # 获取前10条热点新闻
    if news:
        client.save_to_markdown(news)  # 保存到 Markdown 文件