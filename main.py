from db_manager import DBManager

def interaction():
    dbm = DBManager('host', 'database', 'user', 'password')
    dbm.drop_table()
    dbm.create_tables()
    dbm.add_company_data()
    dbm.add_vacancy_data()

    while True:
        print('1) список всех компаний и количество вакансий в каждой компании')
        print('2) подробный список вакансий')
        print('3) средняя зарплата по вакансиям')
        print('4) вакансии с зарплатой выше средней')
        print('5) вакансии с ключевым словом')
        print('Ведите любой символ чтобы выйти')
        action = input()
        if action == '1':
            count = dbm.get_company_and_vacancies_count()
            for i in count:
                print(i)
        elif action == '2':
            vacancies = dbm.get_all_vacancies()
            for vacancy in vacancies:
                print(vacancy)
        elif action == '5':
            print('Введите ключевые слова для поиска')
            filter = input()
            vacancies = dbm.get_vacancies_with_keyword(filter)
            for vacancy in vacancies:
                print(vacancy)
        elif action == '4':
            vacancies = dbm.get_vacancies_with_higher_salary()
            for vacancy in vacancies:
                print(vacancy)
        elif action == '3':
            vacancies = dbm.get_avg_salary()
            print(vacancies[0])
        else:
            dbm.close_connection()
            break

if __name__ == "__main__":
    interaction()