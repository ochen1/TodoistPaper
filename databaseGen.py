#!/usr/bin/python3.8
from json import dump
from os import getenv
from googletrans import Translator

from todoist import TodoistAPI
from time import time, sleep
from time import strptime, mktime
from json import load as loadJSON
from json import dump as dumpJSON
from json.decoder import JSONDecodeError

from argParse import argparse
from datetimeParser import parse_timedelta

api = TodoistAPI()
api.user.login(getenv("EMAIL"), getenv("PASSWORD"))
# api.sync()

translator = Translator()


def translate2zh(text):
    return translator.translate(text, src='en', dest='zh-CN').text


def getRet():
    with open('database.json', 'r') as f:
        return loadJSON(f)


def todoistitem2dict(item):
    for check_principle in [item['date_completed']]:
        if check_principle:
            if time() - int(mktime(strptime(check_principle, "%Y-%m-%dT%H:%M:%SZ"))) > 86400:
                return None
    content, flags, arguments = argparse(item['content'])
    time_required = None
    if 'time' in arguments:
        time_required = parse_timedelta(arguments['time'])
    computer_time_required = None
    if 'screen' in arguments:
        computer_time_required = parse_timedelta(arguments['screen'])
    i_dict = {
        'name': content,
        'name-zh': translate2zh(content),
        'author': item['added_by_uid'],
        'written': ' '.join(item['date_added'].rstrip('Z').split('T')),
        'due': ' '.join(item['due']['date'].rstrip('Z').split('T')) if item['due'] is not None else item['due'],
        'priority': item['priority'],
        'parent-project': item['project_id'],
        'done': False if item['date_completed'] is None else True,
        'date_completed': ' '.join(item['date_completed'].rstrip('Z').split('T')) if item['date_completed'] is not
                                                                                     None else item['date_completed'],
        'time_required': time_required,
        'computer_time_required': computer_time_required
    }
    return i_dict


def update():
    try:
        with open('database.json', 'r') as f:
            if time() - loadJSON(f)['last_update'] < 1000:
                return getRet()
    except (FileNotFoundError, JSONDecodeError, KeyError):
        pass
    api.sync()

    od = dict()
    with open("database.json", 'w') as f:
        # Collaborators
        od['users'] = list()
        for collaborator in api.state['collaborators']:
            od['users'].append(
                f"{collaborator['full_name']} "
                f"<{collaborator['email']}> "
                f"(Todoist User #{collaborator['id']})"
            )
        # Projects
        od['projects'] = dict()
        for project in api.state['projects']:
            od['projects'][project['id']] = project['name']
        # Tasks
        od['items'] = list()
        for item in api.state['items']:
            od['items'].append(
                todoistitem2dict(item)
            )
        # Completed Tasks
        for project_id in [project['id'] for project in api.state['projects']]:
            for item in api.items.get_completed(project_id):
                od['items'].append(
                    todoistitem2dict(item)
                )
        od['items'] = list(filter(lambda filter_item: filter_item is not None, od['items']))
        od['meta'] = {
            'users-count': len(od['users']),
            'tasks-count': len(od['items'])
        }
        od['last_update'] = int(time())
        dumpJSON(od, f)
    return getRet()


if __name__ == '__main__':
    try:
        while True:
            update()
            print("Updated.")
            sleep(3600 - (time() % 3600))
    except KeyboardInterrupt:
        print()
