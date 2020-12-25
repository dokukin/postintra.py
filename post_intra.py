import requests
import time
import config

URL = 'https://intra.s7.aero/itsr/request/index'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 '
                  'Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9 '
}

'''def get_authentification(login, password):
    data = {
        'yform_site_login_form': '1',
        'LoginForm[username]': login,
        'LoginForm[password]': password,
        'LoginForm[rememberMe]': '0',
        'submit': 'Войти'
    }
    s = requests.session()
    s.post('https://intra.s7.aero/site/login', data=data)
    return s'''


def get_suz(m):
    url = 'https://intra.s7.aero/itsd?widget=app%2Fgrid'
    HEADERS = {
        'Content-Type': 'application/json',
        'Accept - Language': 'ru - RU, ru; q = 0.8, en - US; q = 0.5, en; q = 0.3',
        'Accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
        'Cookie': 's7_jwt_refresh=' + m['s7_jwt_refresh'],
    }
    params1 = {
        "config": {}, "pagination": {"pageSize": 50, "currentPage": 1},
        "sort": [{"name": "status", "order": False}, {"name": "waiting_time", "order": False},
                 {"name": "when_to_end", "order": False}, {"name": "when_touched", "order": True}],
        "filters": {
            "model": {"$scenario": "search", "filter_group": "assigned_to_group", "filter_processors_group": [],
                      "filter_ignore_waiting": True, "filter_service_type": [], "date_column": None, "date_start": None,
                      "date_end": None, "source": None, "type": None, "priority": None, "show_closed": False,
                      "with_mail": False, "search_text": None, "sticker": None, "filter_processor": None,
                      "filter_sd_module": None, "company": None, "city": None, "with_childs": None, "has_files": None,
                      "sla_failed": None, "ignore_sla": None, "access_sd_failed": None, "vip": None,
                      "filter_mass_request": None, "assessment_type": None, "agency": None, "trash": False,
                      "filter_has_errors": False, "filter_rework": False, "id": "", "applicant": None, "title": None,
                      "status": None, "processor": None}}
    }
    # r = m.get(url, headers=HEADERS, params=params)
    request = requests.post(url, headers=HEADERS, json=params1)
    response = request.json()
    # print(len(l['data']['items']))
    suz_messages = []
    try:
        for item in response['data']['items']:
            suz_messages.append(f"Номер заявки: {item['$key']} \n"
                                f"Текст заявки: {item['title']} \n"
                                f"Ссылка на заявку: https://intra.s7.aero{item['$url']}\n\n"
                                )
    except Exception as error:
        message_error = f'возникла ошибка: {error}'
    # for k in range(len(l['data']['items'])):
    #     suz.append({
    #         'Номер заявки': (l['data']['items'][k]['$key']),
    #         'Текст заявки': (l['data']['items'][k]['title']),
    #         'В работе на группе': (l['data']['items'][k]['processor'])
    #     })

    return suz_messages or message_error


def diff_request():
    s1 = []
    while True:
        s2 = parse()
        if s1 == s2:
            print('Изменений нет')
            time.sleep(10)
        else:
            # return_delete = list(set(list(set(s1) ^ set(s2))) & set(s1))
            # delete_telegram(return_delete)
            for s3 in list(set(s1 + s2)):
                if s3 in s1:
                    pass
                else:
                    send_telegram(s3)
                    s1.append(s3)




# def diff_request():
#     s1 = [1, 2, 3]
#     s2 = [1, 2, 4]
#     if s1 == s2:
#         print('Изменений нет')
#     else:
#         print('На удаление: ' + str(list(set(list(set(s1) ^ set(s2))) & set(s1))))
#         for s3 in list(set(s1 + s2)):
#             if s3 in s1:
#                 pass
#             else:
#                 print(s3)
#                 s1.append(s3)


def get_cookie():
    login_user = 'a.dokukin'
    # password_user = input('Введите пароль :')
    password_user = 'Ri$$adm1n!'
    url = 'https://intra.s7.aero/apiLogin/login'
    data = {
        'username': login_user,
        'password': password_user,
    }
    HEADERS = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    }
    r = requests.post(url, headers=HEADERS, json=data)
    x = r.json()
    m = x['cookies']
    return m


l = get_cookie()


def parse():
    return get_suz(l)


def send_telegram(text: str):
    token = config.token
    url = "https://api.telegram.org/bot"
    channel_id = "-1001483076999"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })
    m = r.json()
    m['result']['message_id']
    if r.status_code != 200:
        raise Exception("post_text error")
massiv_zayvok - []
def change_telegram_message(r, add):
    if add == 0:
        massiv_zayvok.append


# def delete_telegram(text: str):
#     token = config.token
#     url = "https://api.telegram.org/bot"
#     channel_id = "-1001483076999"
#     url += token
#     method = url + "/deleteMessage"
#
#     r = requests.post(method, data={
#         "chat_id": channel_id,
#         "text": text
#     })

    if r.status_code != 200:
        raise Exception("post_text error")


diff_request()
