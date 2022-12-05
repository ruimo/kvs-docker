#!/usr/bin/env python3

from cassandra.cluster import Cluster

def create_keyspace(cluster):
    session = cluster.connect()
    session.execute("CREATE KEYSPACE IF NOT EXISTS my_keyspace WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };")

def create_table(session):
    session.execute("""
      CREATE TABLE IF NOT EXISTS my_keyspace.user (
        last_name text, first_name text, title text,
        PRIMARY KEY (last_name, first_name)
      )
    """)

if __name__ == '__main__':
    cluster = Cluster(['localhost'])
    try:
        create_keyspace(cluster)
        
        session = cluster.connect('my_keyspace')
        create_table(session)

        session.execute("INSERT INTO my_keyspace.user (first_name, last_name, title) VALUES ('Bill', 'Nguyen', 'Mr.')")
        session.execute("INSERT INTO my_keyspace.user (first_name, last_name, title) VALUES ('Bill', 'Pugh', 'Mr.')")
        pstmt = session.prepare("SELECT * FROM my_keyspace.user WHERE first_name=? AND last_name=?").bind(['Bill', 'Pugh'])
        rows = session.execute(pstmt)
        for row in rows:
            print(row.first_name, row.last_name, row.title)
    finally:
        cluster.shutdown()
