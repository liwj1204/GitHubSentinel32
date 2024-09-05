import os
import requests
import json
from openai import OpenAI  # 导入OpenAI库用于访问GPT模型
from logger import LOG  # 导入日志模块

class LLM:
    def __init__(self,config):
        # 创建一个OpenAI客户端实例
        self.config = config
        print("api_key================================"+config.api_key)
        self.model = config.llm_model_type.lower()  # 获取模型类型并转换为小写
        if self.model == 'openai':
            self.client = OpenAI(
                #302.AI后台-API超市-API列表 生成的API KEY
                api_key=self.config.api_key,
                #302.AI的base-url
                base_url="https://api.302.ai/v1"
            )
        elif self.model == 'ollama':
            self.api_url = config.ollama_api_url  # 设置Ollama API的URL
            
        else:
            raise ValueError(f"Unsupported model type: {self.model}")  # 如果模型类型不支持，抛出错误
        # 从TXT文件加载提示信息
        with open("prompts/report_prompt.txt", "r", encoding='utf-8') as file:
            self.system_prompt = file.read()
        
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

        # 根据选择的模型调用相应的生成报告方法
        if self.model == "openai":
            return self._generate_report_openai(messages)
        elif self.model == "ollama":
            return self._generate_report_ollama(messages)
        else:
            raise ValueError(f"Unsupported model type: {self.model}")



    def _generate_report_openai(self, messages):

        LOG.info("使用 OPENAI GPT 模型开始生成报告。")
        
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
    
    def _generate_report_ollama(self, messages):

        LOG.info("使用 Ollama GPT 模型开始生成报告。"+self.config.ollama_model_name)
        
        try:
            payload={
                "model": self.config.ollama_model_name,
                "messages": messages,
                "stream": False
            }
            response = requests.post(self.api_url, json=payload)    
            response_data=response.json()

            LOG.debug("Ollma response: {}", response_data)
            messages_content = response_data.get('message', {}).get('content',None)
            if messages_content:
                return messages_content
            else:
                LOG.error("Ollama response content is empty.")
                raise Exception("Ollama response content is empty.")
            
        except Exception as e:
            LOG.error(f"生成报告时发生错误：{e}")
            raise
        
if __name__ == '__main__':
    from config import Config  # 导入配置管理类
    config = Config()
    llm = LLM(config)

    markdown_content="""
# Progress for langchain-ai/langchain (2024-08-20 to 2024-08-21)


## Issues Closed in the Last 1 Days
- partners/chroma: release 0.1.3 #25599
- docs: few-shot conceptual guide #25596
- docs: update examples in api ref #25589
"""

    report = llm.generate_daily_report(markdown_content, dry_run=False)
    print(report)