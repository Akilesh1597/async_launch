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


async def countdown(name, start, delay, color, depends_on=None, dependents=None):
    dependents = dependents or []
    depends_on = depends_on or []
    for dep_task in depends_on:
        print('{}: waiting for parent'.format(name))
        await dep_task
        print('{}: waiting for parent over'.format(name))
    colored_print('countdown {} delayed by {} seconds'.format(name, delay), color)
    await sleep(delay)
    for i in range(start, 0, -1):
        colored_print('countdown {}: {}'.format(name, i), color)
        await sleep(1)
    for dep_task in dependents:
        print('{}: notifyiing waiting dependents'.format(name))
        dep_task.set_result((name, start, color,))
    return (name, start, color)


def liftoff(future):
    colored_print('{}: liftoff...'.format(future.result()[0]), future.result()[2])

def complete(future):
    colored_print('{}: countdown to {} complete.'.format(*future.result()[:2]), future.result()[2])


async def monitor_tasks(*tasks):
    while any([not task.done() for task in tasks]):
        print('Some tasks still pending...')
        await sleep(1)
    print('all tasks done...')


def schedule_countdowns(*countdowns):
    tasks = []
    B_future = loop.create_future()
    A_future = loop.create_future()
    for name, count, color in countdowns:
        if name == 'A':
            task = loop.create_task(countdown(name, count, random(), color, depends_on=[B_future], dependents=[A_future]))
        elif name == 'B':
            task = loop.create_task(countdown(name, count, random(), color, depends_on=[A_future], dependents=[B_future]))
        else:
            task = loop.create_task(countdown(name, count, random(), color))
        task.add_done_callback(complete)
        task.add_done_callback(liftoff)
        tasks.append(task)
    return tasks


if __name__ == '__main__':
    start = datetime.datetime.now()
    print('starting all tasks at {}'.format(start))
    loop.run_until_complete(monitor_tasks(*schedule_countdowns(*COUNTDOWNS)))
    end = datetime.datetime.now()
    print('ending all tasks at {}'.format(end))
    print('total {}'.format((end-start).total_seconds()))
