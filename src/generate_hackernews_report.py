import os
import json
from llm import LLM  # 导入LLM类以使用语言模型生成报告
from hackernews_client import HackerNewsClient  # 导入Hacker News客户端类
from logger import LOG  # 导入日志模块

def read_prompt_from_file(file_path):
    """
    从指定文件中读取提示词
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            prompt = file.read()
        LOG.info(f"从文件 {file_path} 成功读取提示词。")
        return prompt
    except FileNotFoundError:
        LOG.error(f"提示词文件未找到: {file_path}")
        return ""
    except Exception as e:
        LOG.error(f"读取提示词文件时发生错误：{e}")
        return ""

def generate_hackernews_report(hackernews_client, llm, prompt_file_path):
    """
    使用 LLM 对 Hacker News 消息生成报告
    """
    # 从文件中读取系统提示词
    system_prompt = read_prompt_from_file(prompt_file_path)
    if not system_prompt:
        LOG.error("提示词读取失败，无法生成报告。")
        return

    # 获取最新的 Hacker News 消息
    news_list = hackernews_client.fetch_latest_news(limit=10)
    if not news_list:
        LOG.error("未能获取到 Hacker News 消息。")
        return

    # 将新闻消息转换为文本格式，用于生成报告
    news_content = "\n".join([f"- {title}: {url}" for title, url in news_list])

    # 使用 LLM 生成报告
    report = llm.generate_daily_report(news_content, system_prompt=system_prompt)

    # 将生成的报告保存到文件
    report_file_path = os.path.join("reports", "hackernews_report.md")
    with open(report_file_path, 'w', encoding='utf-8') as file:
        file.write(f"# Hacker News 报告\n\n{report}")
    
    LOG.info(f"报告已生成并保存到 {report_file_path}")

def main():
    # 创建 LLM 和 Hacker News 客户端实例
    llm = LLM()
    hackernews_client = HackerNewsClient()

    # 提示词文件路径
    prompt_file_path = "prompts/hackernews_prompt.txt"

    # 生成 Hacker News 报告
    generate_hackernews_report(hackernews_client, llm, prompt_file_path)

if __name__ == "__main__":
    main()