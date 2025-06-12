from config.db import pgsqlConn, sql
import json

class repoSQL:
    def __init__(self, table_name, columns):
        self.table_name = table_name
        self.columns = columns

    def get_all(self, limit=15):
        try:
            cur = pgsqlConn.cursor()
            stmt = sql.SQL('SELECT CAST(row_to_json(row) as text) FROM (SELECT {} FROM {} LIMIT %s) row;').format(
                sql.SQL(',').join(map(sql.Identifier, self.columns)),
                sql.Identifier(self.table_name)
            )
            cur.execute(stmt, (limit,))
            data = cur.fetchall()
            cur.close()
            return [json.loads(row[0]) for row in data]
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_by_id(self, record_id):
        try:
            cur = pgsqlConn.cursor()
            stmt = sql.SQL('SELECT CAST(row_to_json(row) as text) FROM (SELECT {} FROM {} WHERE id = %s) row;').format(
                sql.SQL(',').join(map(sql.Identifier, self.columns)),
                sql.Identifier(self.table_name)
            )
            cur.execute(stmt, (record_id,))
            data = cur.fetchall()
            cur.close()
            return [json.loads(row[0]) for row in data]
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_by_conditions(self, conditions=None):
        try:
            cur = pgsqlConn.cursor()

            select_part = sql.SQL(',').join(map(sql.Identifier, self.columns))

            if conditions:
                where_clauses = [
                    sql.SQL("{} = %s").format(sql.Identifier(col))
                    for col in conditions.keys()
                ]
                where_part = sql.SQL(' AND ').join(where_clauses)
                query = sql.SQL('SELECT CAST(row_to_json(row) as text) FROM (SELECT {} FROM {} WHERE {}) row;').format(
                    select_part,
                    sql.Identifier(self.table_name),
                    where_part
                )
                cur.execute(query, tuple(conditions.values()))
            else:
                query = sql.SQL('SELECT CAST(row_to_json(row) as text) FROM (SELECT {} FROM {}) row;').format(
                    select_part,
                    sql.Identifier(self.table_name)
                )
                cur.execute(query)

            data = cur.fetchall()
            cur.close()
            return [json.loads(row[0]) for row in data]
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_by_between(self, conditions=None, date_range_conditions=None):
        try:
            cur = pgsqlConn.cursor()
            select_part = sql.SQL(',').join(map(sql.Identifier, self.columns))

            where_clauses = []
            params = []

            if conditions:
                for col, val in conditions.items():
                    where_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(col)))
                    params.append(val)

            if date_range_conditions:
                for col, (start_date, end_date) in date_range_conditions.items():
                    where_clauses.append(
                        sql.SQL("{} BETWEEN %s AND %s").format(sql.Identifier(col))
                    )
                    params.extend([start_date, end_date])

            if where_clauses:
                where_part = sql.SQL(' AND ').join(where_clauses)
                query = sql.SQL('SELECT CAST(row_to_json(row) as text) FROM (SELECT {} FROM {} WHERE {}) row;').format(
                    select_part,
                    sql.Identifier(self.table_name),
                    where_part
                )
                cur.execute(query, tuple(params))
            else:
                query = sql.SQL('SELECT CAST(row_to_json(row) as text) FROM (SELECT {} FROM {}) row;').format(
                    select_part,
                    sql.Identifier(self.table_name)
                )
                cur.execute(query)

            data = cur.fetchall()
            cur.close()
            return [json.loads(row[0]) for row in data]
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_with_joins(self, joins, select_columns=None, conditions=None):
        try:
            cur = pgsqlConn.cursor()

            if not select_columns:
                select_part = sql.SQL('*')
            else:
                select_part = sql.SQL(',').join(
                    sql.SQL("{}.{}").format(
                        sql.Identifier(col.split('.')[0]),
                        sql.Identifier(col.split('.')[1])
                    ) for col in select_columns
                )

            join_parts = []
            for join in joins:
                join_conditions = [
                    sql.SQL("{}.{} = {}.{}").format(
                        sql.Identifier(src_col.split('.')[0]),
                        sql.Identifier(src_col.split('.')[1]),
                        sql.Identifier(dst_col.split('.')[0]),
                        sql.Identifier(dst_col.split('.')[1])
                    ) for src_col, dst_col in join['on'].items()
                ]
                join_parts.append(
                    sql.SQL("INNER JOIN {} ON {}").format(
                        sql.Identifier(join['table']),
                        sql.SQL(' AND ').join(join_conditions)
                    )
                )

            where_part = sql.SQL('')
            params = []
            if conditions:
                where_clauses = [
                    sql.SQL("{}.{} = %s").format(
                        sql.Identifier(col.split('.')[0]),
                        sql.Identifier(col.split('.')[1]))
                    for col in conditions.keys()
                ]
                where_part = sql.SQL('WHERE {}').format(
                    sql.SQL(' AND ').join(where_clauses)
                )
                params = list(conditions.values())

            query = sql.SQL("""
                SELECT CAST(row_to_json(row) as text)
                FROM (
                    SELECT {} FROM {} {} {}
                ) row
            """).format(
                select_part,
                sql.Identifier(self.table_name),
                sql.SQL(' ').join(join_parts),
                where_part
            )

            cur.execute(query, params)
            data = cur.fetchall()
            cur.close()
            return [json.loads(row[0]) for row in data]
        except Exception as e:
            print(f"Error: {e}")
            return None

    def insert(self, data):
        try:
            cur = pgsqlConn.cursor()
            columns = list(data.keys())
            values = tuple(data[col] for col in columns)
            stmt = sql.SQL("INSERT INTO {} ({}) VALUES ({}) RETURNING id").format(
                sql.Identifier(self.table_name),
                sql.SQL(',').join(map(sql.Identifier, columns)),
                sql.SQL(',').join(sql.Placeholder() * len(columns))
            )
            cur.execute(stmt, values)
            inserted_id = int(cur.fetchone()[0])
            pgsqlConn.commit()
            cur.close()
            return inserted_id
        except Exception as e:
            print(f"Error: {e}")
            return None

    def update(self, record_id, data):
        try:
            cur = pgsqlConn.cursor()
            set_clause = sql.SQL(',').join(
                sql.SQL('{} = {}').format(sql.Identifier(col), sql.Placeholder()) for col in data.keys()
            )
            stmt = sql.SQL("UPDATE {} SET {} WHERE id = %s").format(
                sql.Identifier(self.table_name),
                set_clause
            )
            values = tuple(data[col] for col in data.keys()) + (record_id,)
            cur.execute(stmt, values)
            pgsqlConn.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def delete(self, record_id):
        try:
            cur = pgsqlConn.cursor()
            stmt = sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(self.table_name))
            cur.execute(stmt, (record_id,))
            pgsqlConn.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False