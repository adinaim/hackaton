from crud import (
    create_data,
    read_data,
    retrieve_data,
    delete_data,
    update_data,
    clear_data,
    sort_by_price,
    sort_by_status,
    purchase
)



def interface():
    """
    Interface of the app. It is called in the main module to run the program
    """
    while True:
        operation = str(input("""
            Выберите операцию, которую хотите совершить:
                1. Create - создать новый товар
                2. Read - получить список всех товаров
                3. Retrieve - получить подробную информацию по определнному товару
                4. Delete - удалить товар
                5. Clear - очистить список
                6. Update - обновить товар
                7. Search by price - отфильтровать товары по цене
                8. Search by selling status - отфильтровать товары по статусу продажи
                9. Purchase - купить товар
                10. Exit - выйти из программы

        """)).strip().lower()

        if operation == '1' or operation == 'create':
            create_data()
        elif operation == '2' or operation == 'read':
            for item in read_data():
                print('-' * 140)
                print(item)
                print('-' * 140)
        elif operation == '3' or operation == 'retrieve':
            print(f'\nВаши данные: {retrieve_data()}\n')
        elif operation == '4' or operation == 'delete':
            delete_data()
        elif operation == '5' or operation == 'clear':
            clear_data()
        elif operation == '6' or operation == 'update':
            update_data()
        elif operation == '7' or operation == 'search by price':
            print(sort_by_price())
        elif operation == '8' or operation == 'search by status':
            print(sort_by_status())
        elif operation == '9' or operation == 'purchase':
            purchase()
        elif operation ==  '10' or operation == 'exit':
            print('Всего доброго!\n')
            break
        else:
            print('Такой операции не существует. Проверьте правильность ввода.')
            continue



# if __name__ == '__main__':
interface()