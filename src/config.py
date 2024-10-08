import json
import os

class Config:
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        # 尝试从环境变量获取配置或使用 config.json 文件中的配置作为回退
        with open('config.json', 'r') as f:
            config = json.load(f)
            
            # 使用环境变量或配置文件的 GitHub Token
            self.github_token = os.getenv('GITHUB_TOKEN')
            self.api_key = os.getenv('OPENAI_API_KEY')


            # 如果环境变量中没有GitHub Token，则从配置文件中读取
            if not self.github_token:
                self.github_token = config.get('github_token')
            if not self.api_key:
                self.api_key = config.get('api_key')

            # 初始化电子邮件设置
            self.email = config.get('email', {})
            # 使用环境变量或配置文件中的电子邮件密码
            self.email['password'] = os.getenv('EMAIL_PASSWORD', self.email.get('password', ''))

            self.subscriptions_file = config.get('subscriptions_file')
            # 默认每天执行
            self.freq_days = config.get('github_progress_frequency_days', 1)
            # 默认早上8点更新 (操作系统默认时区是 UTC +0，08点刚好对应北京时间凌晨12点)
            self.exec_time = config.get('github_progress_execution_time', "08:00") 
            # 加载 LLM 相关配置
            llm_config = config.get('llm', {})
            self.llm_model_type = llm_config.get('model_type', 'openai')
            self.openai_model_name = llm_config.get('openai_model_name', 'gpt-4o-mini')
            self.ollama_model_name = llm_config.get('ollama_model_name', 'llama3')
            self.ollama_api_url = llm_config.get('ollama_api_url', 'http://localhost:11434/api/chat')
            
