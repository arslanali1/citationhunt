#!/usr/bin/env python

import os
import sys
_upper_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
if _upper_dir not in sys.path:
    sys.path.append(_upper_dir)

import chdb
import handlers.database as database

def update_intersections():
    chdb.copy_tables_to_scratch([
        ('intersections', 'SELECT * FROM %s WHERE expiration > NOW()'),
        ('articles_intersections',
            ('SELECT * FROM %s WHERE article_id IN ' +
            '(SELECT page_id FROM articles)')),
    ])
    def update_snippets_links(cursor):
        cursor.execute('SELECT id FROM intersections')
        database.populate_snippets_links(cursor,
            intersection_ids = (row[0] for row in cursor))
    chdb.init_scratch_db().execute_with_retry(update_snippets_links)
    # delete empty intersections. should this surface an error to the user
    # instead?
    chdb.init_scratch_db().execute_with_retry_s(
        '''DELETE FROM intersections WHERE id NOT IN (
            SELECT inter_id FROM articles_intersections)''')

if __name__ == '__main__':
    update_intersections()
