from twitter import *
import glob
import json
import os.path

ACCESS_TOKEN = '191860718-fpqRdf0CuS0PEYvBf9RnaMlLK4CpW4tA3C56NArU'
ACCESS_SECRET = '3Ss0wnXbbarBgxpyMYBPQjs6HN63YOeINf4Q2f9UnTSha'
CONSUMER_KEY = 'xXkrmDZthbLB9OoGfTxGj1xVl'
CONSUMER_SECRET = 'IgWE22j8hGI9JwdtjWNFQMYjSVf5tVNoE5U21SE2StdBMJRwKt'
t = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET), retry=True)

list_of_my_twitter_friends = t.friends.list(screen_name="vlk83", skip_status=True, count=200)['users']

# создаем директорию для хранения данных
if not os.path.exists('lists_of_user_friends'):
    os.mkdir('lists_of_user_friends')

# отмечаем среди друзей тех, кто не занимается 'масс-фолловингом'
# взял за основу число Данбара (в среднем = 150)
list_of_tagged_friends = []
for friend_ in list_of_my_twitter_friends:
    if 0 < friend_['friends_count'] <= 150:
        list_of_tagged_friends.append(friend_['screen_name'])

# создаем список для уже сохраненных данных о друзьях
fullnames_in_lists_of_user_friends = glob.glob('lists_of_user_friends/*')
shortnames_in_lists_of_user_friends = []
for fullname in fullnames_in_lists_of_user_friends:
    shortname = fullname.replace('lists_of_user_friends\\', '').replace('_friends_list.json', '')
    shortnames_in_lists_of_user_friends.append(shortname)

# создаем частотный словарь, для друзей наших друзей
dict_of_tagged_friends_friends = {}
for tagged_friend in list_of_tagged_friends:
    # если данных о друге ещё нет, то создаем новый файл для хранения списка его друзей
    if tagged_friend not in shortnames_in_lists_of_user_friends:
        filename = str(tagged_friend + '_friends_list.json')
        with open(os.path.join('lists_of_user_friends', filename), 'w', encoding='utf8') as f:
            tagged_friend = t.friends.list(screen_name=tagged_friend, skip_status=True, count=200)['users']
            list_of_user_friends = []
            for tagged_friend_friend in tagged_friend:
                list_of_user_friends.append(tagged_friend_friend['screen_name'])
                if tagged_friend_friend['screen_name'] in dict_of_tagged_friends_friends:
                    value = dict_of_tagged_friends_friends[tagged_friend_friend['screen_name']]
                    dict_of_tagged_friends_friends[tagged_friend_friend['screen_name']] = value + 1
                else:
                    dict_of_tagged_friends_friends[tagged_friend_friend['screen_name']] = 1
            json.dump(list_of_user_friends, f)
    # если данные уже есть, то просто читаем json-файл
    else:
        filename = str(tagged_friend + '_friends_list.json')
        with open(os.path.join('lists_of_user_friends', filename), 'r', encoding='utf8') as f:
            tagged_friend = json.load(f)
            for tagged_friend_friend in tagged_friend:
                if tagged_friend_friend in dict_of_tagged_friends_friends:
                    value = dict_of_tagged_friends_friends[tagged_friend_friend]
                    dict_of_tagged_friends_friends[tagged_friend_friend] = value + 1
                else:
                    dict_of_tagged_friends_friends[tagged_friend_friend] = 1

print('Список твиттер-аккаунтов, отсортированных по популярности у ваших друзей:\n')
for screen_name, count in sorted(dict_of_tagged_friends_friends.items(), key=lambda x: x[1], reverse=True):
    if count > 1:
        print(screen_name, count)
