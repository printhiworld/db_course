import psycopg2
from hh import get_data


class DBManager:
    def __init__(self, host, database, user, password):
        self.data = get_data()
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cur = self.conn.cursor()

    def create_tables(self):
        company_table = """CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200) UNIQUE,
                count INTEGER)"""
        vacancy_table = """CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(200),
                salary INTEGER,
                url VARCHAR(200),
                company_id INTEGER REFERENCES companies(id))"""
        self.cur.execute(company_table)
        self.cur.execute(vacancy_table)
        self.conn.commit()

    def add_company_data(self):
        for company in self.data:
            name = company['company_name']
            count = len(company['vacancies'])
            self.cur.execute('''
            INSERT INTO companies (name, count) VALUES (%s, %s);
            ''', (name, count))
        self.conn.commit()

    def add_vacancy_data(self):
        for company in self.data:
            for vacancy in company['vacancies']:
                name = vacancy['name']
                salary = vacancy['salary']
                url = vacancy['url']
                comp = vacancy['company']
                self.cur.execute(f'''
                SELECT id FROM companies WHERE name = %s''', (comp,))
                ci = self.cur.fetchall()
                self.cur.execute('''
                INSERT INTO vacancies (name, salary, url, company_id) VALUES (%s, %s, %s, %s);
                ''', (name, salary, url, ci[0]))
                self.conn.commit()

    def drop_table(self):
        self.cur.execute('''DROP TABLE companies, vacancies''')

    def get_company_and_vacancies_count(self):
        self.cur.execute('''
        SELECT name, count FROM companies''')
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute(f'''
        SELECT * FROM vacancies''')
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute(f'''
        SELECT AVG(salary) FROM vacancies''')
        return self.cur.fetchone()

    def get_vacancies_with_keyword(self, filter):
        self.cur.execute("""
        SELECT * FROM vacancies WHERE vacancies.name LIKE %s
        """, ('%' + filter + '%',))
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        avg = self.get_avg_salary()
        self.cur.execute("""
        SELECT * FROM vacancies WHERE vacancies.salary > %s
        """, (round(avg[0]),))
        return self.cur.fetchall()

    def close_connection(self):
        self.cur.close()
        self.conn.close()



