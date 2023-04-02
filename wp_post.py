#encoding:utf-8
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost,EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc import WordPressPost
import json


def wp_post(client,title,content,tags):
        post = WordPressPost()
        post.title = title
        post.content = content
        post.terms = tags

        post.id=client.call(NewPost(post))

        # whoops, I forgot to publish it!
        post.post_status = 'publish'
        post.custom_fields = []
        result=client.call(EditPost(post.id,post))
        return result


def wp_post_custom_field(client,title,content,custom_field):
        post = WordPressPost()
        post.title = title
        post.content = content
        post.custom_fields = []
        post.custom_fields.append(custom_field)
        post.id=client.call(NewPost(post))

        # whoops, I forgot to publish it!
        #post.post_status = 'publish'
        post.post_status = 'private'
        post.custom_fields = []
        result=client.call(EditPost(post.id,post))
        return result

if __name__=='__main__':
        domain_name=""
        user_name=""
        password=""
        client = Client(domain_name+"/xmlrpc.php",domain_name ,password )
        categories = client.call(taxonomies.GetTerms('category', {"search": "Uncategorized"}))
        title = 'chat_wordpress'
        content = '''have a try https://github.com/fendouai/chat_wordpress'''
        result=wp_post(client,title,content,categories)
        print(result)