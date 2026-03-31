from main import CurrencyRates
from controllers import CurrencyRatesCRUD, ViewController


def main():
    c_r = CurrencyRates(['USD', 'EUR', 'GBP'])
    
    if not c_r.update_rates():
        print("Не удалось обновить курсы валют")
        return

    crud = CurrencyRatesCRUD(c_r)
    
    if not crud.create():
        print("Не удалось записать данные в БД")
        return

    view = ViewController(c_r)
    print(view())

    crud.close()

if __name__ == "__main__":
    main()