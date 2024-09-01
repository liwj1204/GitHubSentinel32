import os
import json
from openai import OpenAI  # 导入OpenAI库用于访问GPT模型
from logger import LOG  # 导入日志模块

class LLM:
    def __init__(self):
        # 创建一个OpenAI客户端实例
        self.client = OpenAI()

    def generate_daily_report(self, markdown_content, system_prompt=None, dry_run=False):
        # 使用指定的系统提示词，如果没有指定则使用默认的提示词
        if not system_prompt:
            with open("prompts/report_prompt.txt", "r", encoding='utf-8') as file:
                system_prompt = file.read()

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": markdown_content},
        ]

        if dry_run:
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                json.dump(messages, f, indent=4, ensure_ascii=False)
            LOG.debug("Prompt已保存到 daily_progress/prompt.txt")

            return "DRY RUN"

        LOG.info("使用 GPT 模型开始生成报告。")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            LOG.debug("GPT response: {}", response)
            return response.choices[0].message.content
        except Exception as e:
            LOG.error(f"生成报告时发生错误：{e}")
            raise