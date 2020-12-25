import requests
import time
import config
from bs4 import BeautifulSoup
import jira_info
import telegram_auth

new_offset = None
user_data = []
massiv_zayvok = []
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


def check_message():
    global new_offset
    telegram_auth.greet_bot.get_updates(new_offset)

    last_update = telegram_auth.greet_bot.get_last_update()
    if last_update:
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        # last_chat_name = last_update['message']['chat']['first_name']

        new_offset = last_update_id + 1
        user_message_data = [{'chat_id': last_chat_id,
                              'text': last_chat_text}]
        return user_message_data
    else:
        None


def get_cookie(username_user_ad, password_user_ad):
    url = 'https://intra.s7.aero/apiLogin/login'
    login = username_user_ad
    password = password_user_ad
    data = {
        'username': login,
        'password': password,
    }
    HEADERS = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    }
    r = requests.post(url, headers=HEADERS, json=data)
    x = r.json()
    if r.status_code == 200:
        m = x['cookies']
        return m['s7_jwt_refresh']
    else:
        return None


def login_and_password():
    login = ''
    password = ''
    message_data_user = check_message()
    if message_data_user is not None:
        for message_text in message_data_user:
            if message_text['text'] == '/auth':
                telegram_auth.greet_bot.send_message(message_text['chat_id'], 'Укажи свой логин')
                message_data_user_login = check_message()
                for login_user in message_data_user_login:
                    login = login_user['text']
                telegram_auth.greet_bot.send_message(message_text['chat_id'], 'Укажи свой пароль')
                message_data_user_login = check_message()
                for password_user in message_data_user_login:
                    password = password_user['text']

                l = get_cookie(login, password)
                if l is not None:
                    user_data.append({'user_id': message_text['chat_id'],
                                      'login_user': login,
                                      'password_user': password,
                                      'cookie': l
                                      })
                else:
                    telegram_auth.greet_bot.send_message(message_text['chat_id'], 'Неверно указан логин или пароль')
            elif message_text['text'] == '/stop':
                for delete_data in user_data:
                    if delete_data[message_text['chat_id']] == user_data['user_id']:
                        user_data.remove(delete_data)
                    else: continue
            else:
                continue


def get_suz(cookie, login, password):
    url = 'https://intra.s7.aero/itsd?widget=app%2Fgrid'
    HEADERS = {
        'Content-Type': 'application/json',
        'Accept - Language': 'ru - RU, ru; q = 0.8, en - US; q = 0.5, en; q = 0.3',
        'Accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
        'Cookie': 's7_jwt_refresh=' + cookie,
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
    request = requests.post(url, headers=HEADERS, json=params1)
    response = request.json()
    suz_messages = ['']
    message_error = None
    jira_data = jira_info.jira_info(login, password)
    try:
        for item in response['data']['items']:
            processor = html_parser(item['processor'])
            suz_messages.append(f"Номер заявки: {item['$key']} \n"
                                f"Текст заявки: {item['title']} \n"
                                f"Ссылка на заявку: https://intra.s7.aero{item['$url']}\n"
                                f"Обработчик: {processor}\n\n"
                                )
        for jira in jira_data:
            suz_messages.append(jira)
    except Exception as error:
        message_error = f'возникла ошибка: {error}'
    return suz_messages or message_error


def html_parser(proc):
    soup = BeautifulSoup(proc, 'html.parser')
    l = ''
    ds = ''
    try:
        l = soup.a.get_text()
    except:
        ds = soup.get_text()
    return l or ds


def diff_request():
    s1 = ['']
    s2 = ['']
    while True:
        login_and_password()
        if user_data:
            for user_data_one in user_data:
                s2 = get_suz(user_data_one['cookie'], user_data_one['login_user'], user_data_one['password_user'])
                if set(s1) == set(s2):
                    print('Изменений нет')
                    time.sleep(10)
                else:
                    for s3 in list(set(s1 + s2)):
                        if s3 in s1:
                            pass
                        else:
                            telegram_auth.greet_bot.send_message(user_data_one['user_id'], s3)
                            massiv_zayvok.append({
                                'text': s3,
                                'id': user_data_one['user_id']
                            })
                            s1.append(s3)
                    diff = list(set(s1) ^ set(s2))
                    for item in diff:
                        change_telegram_message(item, user_data_one['user_id'])
                        s1.remove(item)
        else:
            print('Нет данных')
            time.sleep(10)


def change_telegram_message(r, user_id):
    for msg in massiv_zayvok:
        if set(msg['text']) == set(r):
            print(msg['id'])
            telegram_auth.greet_bot.delete_telegram(msg['id'], user_id)
            massiv_zayvok.remove(msg)
            break


if __name__ == '__main__':
    diff_request()
