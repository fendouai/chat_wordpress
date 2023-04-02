# encoding:utf-8
import pprint
import time
from wp_post import wp_post
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import taxonomies
import openai

# 换成你的 key
openai.api_key = "sk-chat_wordpress"
domain_name = ""
user_name = ""
password = ""
client = Client(domain_name + "/xmlrpc.php", domain_name, password)
categories = client.call(taxonomies.GetTerms('category', {"search": "Uncategorized"}))
pack = [categories[0], ]

def get_chatgpt(openai, task, content):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": task + content}
        ]
    )
    time.sleep(10)
    return completion.choices[0].message["content"]



def get_keywords(openai, content):
    return get_chatgpt(openai,  content," 的知识包括哪些方面，以逗号分隔")


def get_description(openai, content):
    return get_chatgpt(openai, "写一篇文章详细介绍一下如何使用：", content)


def get_title(openai, content):
    return get_chatgpt(openai, "一句话介绍一下如何使用：", content)


def content_fission(openai, post_seed):
    title = get_title(openai, post_seed)
    content = get_description(openai, post_seed)
    result = wp_post(client, title, content, pack)
    print(result)
    keywords_str = get_keywords(openai, content)
    print(keywords_str)
    if "," in keywords_str:
        keywords = keywords_str.split(",")
    else:
        keywords = keywords_str.split("、")
    print(keywords)
    for k in keywords[1:5]:
        print(k)
        content_fission(openai, k)


if __name__ == '__main__':
    post_seed = "chat_wordpress"
    #content_fission(openai, post_seed)
    title = get_title(openai, post_seed)
    content = get_description(openai, post_seed)
    result = wp_post(client, title, content, pack)
    print(result)
