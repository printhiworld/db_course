import requests


def get_data():
    vacancies = []

    url = f"https://api.hh.ru/vacancies"
    response = requests.get(url).json()['items']
    for i in response:
        company = i.get("employer", {}).get("name", "-")
        salary_from = i.get("salary", "0")['from']
        vacancy = {
            "name": i.get("name", "-"),
            "salary": salary_from,
            "url": i.get("alternate_url", "-"),
            "company": company
        }

        if vacancies == []:
            vacancies.append({
                    "company_name": company,
                    "vacancies": [vacancy]
                })
            continue

        for vac in vacancies:
            if vac["company_name"] == company:
                vac["vacancies"].append(vacancy)

            else:
                vacancies.append({
                    "company_name": company,
                    "vacancies": [vacancy]
                })

    return vacancies
