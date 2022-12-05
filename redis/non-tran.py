#!/usr/bin/env python3

import redis
import threading
import random

def user_amount_key(user):
    return "{0}:amount".format(user)

def bank_transfer(conn, user_from, user_to, amount):
    user_from_amount_key = user_amount_key(user_from)

    balance_from = int(conn.get(user_from_amount_key) or "0")
    new_balance = balance_from - amount;
    if new_balance < 0:
        return
    conn.set(user_from_amount_key, new_balance)
    conn.incrby(user_amount_key(user_to), amount)

def transfer_loop(conn, user_from, user_to):
    for i in range(100):
        amt = random.randint(1, 99)
        bank_transfer(conn, user_from, user_to, amt)

if __name__ == '__main__':
    conn = redis.Redis()
    user_a_amount_key = user_amount_key('user-a')
    user_b_amount_key = user_amount_key('user-b')
    conn.set(user_a_amount_key, 200)
    conn.set(user_b_amount_key, 200)
    thread_a = threading.Thread(target = lambda: transfer_loop(conn, 'user-a', 'user-b'))
    thread_b = threading.Thread(target = lambda: transfer_loop(conn, 'user-b', 'user-a'))
    thread_a.start()
    thread_b.start()
    thread_a.join()
    thread_b.join()
    print("User a balance: {0}".format(conn.get(user_a_amount_key)))
    print("User b balance: {0}".format(conn.get(user_b_amount_key)))

