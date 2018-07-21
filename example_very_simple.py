import datetime
from random import random
import asyncio
from asyncio import sleep
from termcolor import colored
from time import sleep as sleep_no_async


loop = asyncio.get_event_loop()
COUNTDOWNS = (('A', 4, 'red'), ('B', 5, 'green'), ('C', 10, 'blue'))


def colored_print(text, color):
    print(colored(text, color, attrs=['bold']))


async def countdown(name, start, delay, color):
    colored_print('countdown {} delayed by {} seconds'.format(name, delay), color)
    sleep(delay)
    for i in range(start, 0, -1):
        colored_print('countdown {}: {}'.format(name, i), color)
        sleep(1)
    colored_print('{}: liftoff...'.format(name), color)
    colored_print('{}: countdown to {} complete.'.format(name, start), color)


async def monitor_tasks(*tasks):
    while any([not task.done() for task in tasks]):
        print('Some tasks still pending...')
        await sleep(1)
    print('all tasks done...')


def schedule_countdowns(*countdowns):
    tasks = []
    for name, count, color in countdowns:
        task = loop.create_task(countdown(name, count, random(), color))
        tasks.append(task)
    return tasks


if __name__ == '__main__':
    start = datetime.datetime.now()
    print('starting all tasks at {}'.format(start))
    #loop.run_until_complete(asyncio.gather(*schedule_countdowns(*COUNTDOWNS)))
    loop.run_until_complete(monitor_tasks(*schedule_countdowns(*COUNTDOWNS)))
    end = datetime.datetime.now()
    print('ending all tasks at {}'.format(end))
    print('total {}'.format((end-start).total_seconds()))
