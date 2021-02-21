import requests
import os
import sys
import time

cwd = os.getcwd()
splits = cwd.split(os.sep)
splits.pop()
parent_path = '/'.join(splits)
sys.path.append(parent_path)
from base import base_bs, base_requests
from sql.BaseTableTool import BaseTableTool


class DouBanDatabaseTool(BaseTableTool):
    def check_comment_by_cid(self, cid):
        comments = self.select_comment_cid(cid)
        return len(comments) > 0

    def select_comment_cid(self, cid):
        table = 'comments'
        return self.select(table, where='cid=' + cid)

    def insert_comment(self, comment_obj):
        result = False
        # "cid"
        # "product_id"
        # "uid"
        # "content"
        # "rating"
        # "user_name"
        sql_str = '''insert into comments
                                (cid, product_id, uid, content, rating, user_name)
                                values
                                (:st_cid, :st_product_id, :st_uid,:st_content,:st_rating,:st_user_name )
                                '''
        # ts = math.floor(time.time())
        try:
            self.cursor.execute(sql_str, {
                'st_cid': comment_obj['cid'],
                'st_product_id': comment_obj['product_id'],
                'st_uid': comment_obj['uid'],
                'st_content': comment_obj['content'],
                'st_rating': comment_obj['rating'],
                'st_user_name': comment_obj['user_name'],
            })
            self.connection.commit()
            result = True
        except Exception as e:
            print('insert to table error : ', e)
            print(comment_obj)
        return result


def get_page_url(movie_id, start, limit):
    host = 'movie.douban.com'
    return 'https://{0}/subject/{1}/comments?start={2}&limit={3}&status=P&sort=new_score'.format(
        host,
        movie_id,
        start,
        limit
    )


def get_comment_rating(rate_str):
    rat = rate_str[7:9]
    # print('get common rating {0}, {1}'.format(rate_str, rat))
    return int(rat)


def get_user_id_from_url(user_url):
    str_list = user_url.split('/')
    size = len(str_list)
    # print('split list = ', str_list)
    return str_list[size - 2]


def parse_comments_of_page_url(movie_id, url):
    cookie = '__utmv=30149280.9430; gr_user_id=5c21482c-80a0-4b49-9282-15ead6410b42; _vwo_uuid_v2=D9A27CFD7695F5B756A774684F344A8E7|b6db148c463da0a1a9c9eba1c1379670; ll="118282"; bid=qRpP_orYXPA; __utmc=30149280; __utmz=30149280.1613705430.14.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; ap_v=0,6.0; _pk_ref.100001.4cf6=["","",1613731017,"https://www.douban.com/"]; _pk_ses.100001.4cf6=*; __utma=30149280.1878159750.1575353804.1613729127.1613731018.17; __utmt=1; __utmb=30149280.1.10.1613731018; dbcl2="94304536:kKumSIYYR4A"; ck=gdyb; _pk_id.100001.4cf6=caa8e6c212507330.1583305918.4.1613731043.1613729166.; __utma=223695111.2020287006.1583305918.1613729127.1613731043.5; __utmb=223695111.0.10.1613731043; __utmz=223695111.1613731043.5.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0'
    result = base_requests.base_request(url, {'Cookie': cookie})
    comment_list = []
    max_count = 0
    error = False

    if result is not None:
        # print(len(result))
        html_obj = base_bs.get_bs_parse_result(result)
        comments = html_obj.find_all('div', {'class': 'comment-item'})

        try:
            count_tag = html_obj.find('ul', {'class': 'fleft CommentTabs'})
            count_span = count_tag.find('span')
            count_text = count_span.getText()
            max_count = int(count_text[3:(len(count_text) - 1)])
        except Exception as e:
            print('count exception ', e)
            print('count exception ', result)
            max_count = -1

        try:
            for commentItem in comments:
                comment_span = commentItem.find('span', {'class': 'short'})
                comment = comment_span.getText()
                rate_span = commentItem.find('span', {'class': 'rating'})

                rating = None
                if rate_span is not None:
                    rat_str = rate_span['class']
                    rating = get_comment_rating(rat_str[0])

                cid = commentItem['data-cid']
                user_tag = commentItem.find('div', {'class': 'avatar'})

                uid = ''
                user_name = ''

                if user_tag is not None:
                    user_url = user_tag.a['href']
                    uid = get_user_id_from_url(user_url)
                    user_name = user_tag.a['title']
                # print(cid)
                # print('user url = {}'.format(user_url))

                obj = {
                    'cid': cid,
                    'content': comment,
                    'rating': rating,
                    'user_name': user_name,
                    'product_id': movie_id,
                    'uid': uid,
                }
                comment_list.append(obj)
                # print(obj)
        except Exception as e:
            error = True
            print('comment item exception ', e)
            print('comment item exception ', result)

    return {'comment_list': comment_list, 'max_count': max_count, 'error': error}


def insert_comment_list_to_database(db_tool: DouBanDatabaseTool, comment_list):
    for comment_obj in comment_list:
        comment_id = comment_obj['cid']
        comment_exist = db_tool.check_comment_by_cid(comment_id)
        if comment_exist is not True:
            db_tool.insert_comment(comment_obj)


def fetch_movie_comments():
    db_path = './database/douban.db'
    movie_id = '34841067'
    start = 200
    limit = 20
    db_tool = DouBanDatabaseTool(db_path)
    db_tool.start_connect()

    url = get_page_url(movie_id, start, limit)
    data = parse_comments_of_page_url(movie_id, url)
    comment_list = data['comment_list']
    count = data['max_count']
    # print(len(comment_list))

    while start < count or count < 0:
        insert_comment_list_to_database(db_tool, comment_list)
        time.sleep(1)
        if count > 0:
            start += limit
        print('fetch start = ', start)
        url = get_page_url(movie_id, start, limit)
        data = parse_comments_of_page_url(movie_id, url)
        if data['error'] is True:
            break
        else:
            comment_list = data['comment_list']

    db_tool.close_connection()


def check_comment_cid(cid):
    db_path = './database/douban.db'
    db_tool = DouBanDatabaseTool(db_path)
    db_tool.start_connect()

    exist = db_tool.check_comment_by_cid(cid)
    print(exist)

    db_tool.close_connection()


if __name__ == "__main__":
    fetch_movie_comments()
    # check_comment_cid('2734723812')
