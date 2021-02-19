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
    result = base_requests.base_request(url)
    comment_list = []
    max_count = 0

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

        for commentItem in comments:
            comment_span = commentItem.find('span', {'class': 'short'})
            if comment_span is None:
                print('comment error: ', commentItem)
                print('comment error: ', comments)
                continue
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
    return {'comment_list': comment_list, 'max_count': max_count}


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
    comment_count = 0

    url = get_page_url(movie_id, start, limit)
    data = parse_comments_of_page_url(movie_id, url)
    comment_list = data['comment_list']
    count = data['max_count']

    while start < count or count < 0:
        insert_comment_list_to_database(db_tool, comment_list)
        time.sleep(1)
        if count > 0:
            start += limit
        print('fetch start = ', start)
        url = get_page_url(movie_id, start, limit)
        data = parse_comments_of_page_url(movie_id, url)
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
