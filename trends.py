import json
import csv
from csv import reader
import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def json():
    directory = "/Users/sanjay/Desktop/CODE/Python/youtube_data_analysis/data/data.json"
    f = open(directory)
    data = json.load(f)
    # dict_keys(['kind', 'etag', 'items'])
    kind = data["kind"]
    etag = data["etag"]
    items = data["items"]
    json_data = zip(kind, etag, items)
    f.close()
    return json_data


class Video(object):
    def __init__(self, data):
        self.video_id = data[0]
        self.trending_date = data[1]
        self.title = data[2]
        self.channel_title = data[3]
        self.tags = data[6]
        self.views = data[7]
        self.likes = data[8]
        self.dislikes = data[9]
        self.comment_count = data[10]
        self.comments_disabled = data[12]
        self.ratings_disabled = data[13]
        self.description = data[15]


def read_csv():
    with open('data/data.csv', 'r') as file:
        data = dict()
        csv = reader(file)
        count = 0
        for row in csv:
            if (row[0] != 'video_id'):
                data[count] = Video(row)
                count += 1
        return data


def list_iter(attribute, temp):
    for entry in temp:
        if f"{attribute}" in entry:
            return f"{attributeA}"


def dict_iter(attribute, temp):
    for entry in temp.keys():
        if f"{attribute}" in entry:
            return f"{attributeA}"


def string_checker(attribute, temp):
    if f"{attribute}" in temp:
        return f"{attribute}"


def str_to_func(attribute, vid):
    funCall = {
        'video_id': vid.video_id,
        'trending_date': vid.trending_date,
        'title': vid.title,
        'channel_title': vid.channel_title,
        'tags': vid.tags,
        'views': vid.views,
        'likes': vid.likes,
        'dislikes': vid.dislikes,
        'comment_count': vid.comment_count,
        'comments_disabled': vid.comments_disabled,
        'ratings_disabled': vid.ratings_disabled,
        'description': vid.description,
    }
    return funCall.get(attribute)


def iterator(data, sentiments):
    ret_a = {}
    ret_b = {}
    for key in data.keys():
        ran = False
        for class_attribute in filter(lambda a: not a.startswith('__'),
                                      dir(data[key])):
            video_attributes = str_to_func(class_attribute, data[key])
            if type(video_attributes) == str:
                for sm in sentiments:
                    if ran == False and string_checker(
                            sm, video_attributes) != None:
                        ret_a[key] = data[key]
                        ran = True
            elif type(video_attributes) == list:
                print('NO NEED')
                for sm in sentiments:
                    if ran == False and list_iter(sm,
                                                  video_attributes) != None:
                        ret_a[key] = data[key]
                        ran = True
            elif type(video_attributes) == dict:
                print('NO NEED')
                for sm in sentiments:
                    if ran == False and dict_iter(sm,
                                                  video_attributes) != None:
                        ret_a[key] = data[key]
                        ran = True
        if ran == False:
            ret_b[key] = data[key]
    return ret_a, ret_b


def avg(A):
    avg_likes = 0
    avg_dislikes = 0
    avg_views = 0
    avg_comment_count = 0
    for key in A.keys():
        avg_likes += int(A[key].likes)
        avg_dislikes += int(A[key].dislikes)
        avg_views += int(A[key].views)
        avg_comment_count += int(A[key].comment_count)
    avg_likes = int(avg_likes / len(A.values()))
    avg_dislikes = int(avg_dislikes / len(A.values()))
    avg_views = int(avg_views / len(A.values()))
    avg_comment_count = int(avg_comment_count / len(A.values()))
    return [avg_likes, avg_dislikes, avg_views, avg_comment_count]


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            '{}'.format(height),
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset
            textcoords="offset points",
            ha='center',
            va='bottom')


def bar_graph(A, B, topic):
    A_averaged = avg(A)
    B_averaged = avg(B)
    labels = ["avg_likes", "avg_dislikes", "avg_views", "avg_numOfComments"]
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, A_averaged, width, label=topic)
    rects2 = ax.bar(x + width / 2, B_averaged, width, label=f'Non-{topic}')
    ax.set_ylabel('Number of Users')
    ax.set_title(f'{topic} vs. Non-{topic} Video stats')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    autolabel(rects1, ax)
    autolabel(rects2, ax)
    fig.tight_layout()
    plt.show()


def basic_plots(data):
    temp_likes = 0
    temp_views = 0
    views_total = list()
    likes_total = list()
    print('ran A')
    n = 10
    count = 0
    for key in data.keys():
        count += 1
        if count == n:
            count = 0
            temp_likes += int(data[key].likes)
            temp_views += int(data[key].views)
            views_total.append(temp_likes / n)
            likes_total.append(temp_views / n)

    plt.plot(views_total, likes_total)
    plt.show()
    print('ran B')


if __name__ == '__main__':
    data = read_csv()
    #print(len(data))
    #sports: Bar graph
    sport_sentiments = [
        'sport', 'Sport', 'soccer', 'football', 'golf', 'tennis', 'badminton',
        'swimming', 'nascar', 'baseball', 'lacrosse', 'cycling', 'boxing',
        'fencing', 'judo', 'karate', 'wrestling'
    ]

    sport, non_sport = iterator(data, sport_sentiments)
    bar_graph(sport, non_sport, "Sport")
    #basic_plots(data)
    print('RAN C')
