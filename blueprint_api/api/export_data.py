import pandas as pd
from flask import jsonify, request
from psycopg.sql import SQL
from psycopg.rows import dict_row

from db import connection


def export_data_sql():
    shift = request.args.get('lag_num', 0)

    with connection() as conn:
        cur = conn.cursor(row_factory=dict_row)
        #sql_select_row = ('SELECT rep_dt, delta, deltalag FROM table1_view')
        sql_select_row = (
            SQL('SELECT rep_dt, delta, LAG(delta, {}) '
                'OVER (ORDER BY rep_dt) deltalag FROM table1').format(shift))
        cur.execute(sql_select_row)
        response = cur.fetchall()
    return jsonify(response)


def export_data_pandas():
    shift = request.args.get('lag_num', 0)

    with connection() as conn:
        df = pd.read_sql('SELECT rep_dt, delta FROM table1', con=conn)
    df = df.sort_values(by=['rep_dt'])
    df['deltalag'] = df['delta'].shift(int(shift), fill_value='None')
    return jsonify(df.to_dict(orient='records'))
