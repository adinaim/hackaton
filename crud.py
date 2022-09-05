import json
from settings import DB
from datetime import datetime
from json.decoder import JSONDecodeError


"""
почему список сбрасывается
"""

def read_data():
    """
    Shows information about all items in the shop
    """
    with open(DB) as file:
        try:
            python_data = json.load(file)
            if python_data != []:
                return python_data
            else:
                return ('Список товаров пуст')
        except JSONDecodeError:
            return []


# ascii

def create_data():
    """
    Creates a new item in the list
    """
    id_ = datetime.now().strftime('%H%M%S')
    try:
        data = {
            'id': id_,
            'title': input('Введите название товара: '),
            'price': int(input('Введите цену: ')),
            'creation_date': datetime.now().strftime('%d.%m.%y %H:%M'),
            'description': input('Введите описание товара: '),
            'selling_status': 'Продается'
        }
    except ValueError:
        print('Неправильный ввод. Повторите попытку')
        data = {
            'id': id_,
            'title': input('Введите название: '),
            'price': int(input('Введите цену: ')),
            'description': input('Введите описание: '),
            'selling_status': 'Продается',
            'creation_date': datetime.now().strftime('%d.%m.%y %H:%M')
        }
    json_data: list = read_data()
    json_data.append(data)
    with open(DB, 'w') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)



# почему 2 раза отрабатывает
def available_id():
    """
    Shows available ids and is called in the check_id() function 
    """
    json_data = read_data()
    if json_data != []:
        try:
            global list_of_keys
            list_of_keys = []
            global item
            for item in json_data:
                list_of_keys.append(item['id'])
            print(f'Доступные id:{list_of_keys}')
            return True
        except JSONDecodeError:
            return 'Список товаров пуст!'
    elif json_data == []:
            return []


# почему 2 раза отрабатывает
def check_id():
    """
    Checks if an id is in the list
    """
    if available_id() == True:
        # available_id()
        global id_
        id_ = input('Введите id: ')
        # print(json_data)
        if id_ in list_of_keys:
            print('1')
            return True
        else:
            print('2')
            return False
    else:
        return []



def retrieve_data():
    """
    Retrieves an item from the database by id
    """
    if check_id() == []:
        print('Список товаров пуст')
    else:
        while check_id() == False:
            print(f'ID {id_} нет в списке. Проверьте правильность ввода')
            continue
        else:
            json_data = read_data()
            for item in json_data:
                if item['id'] == id_:
                    print(f'\nВаши данные: {item}\n')



def update_data():
    """
    Updates info about items
    """
    if check_id() == []:
        print('Список пуст. Обновлять нечего')
    else:
        while check_id() == False:
            print(f'{id_} нет в списке. Проверьте правильность ввода')
            continue
        else:
            json_data = read_data()
            for item in json_data:
                if item['id'] == id_:
                    item['title'] = input('Введите новое название: ') or item['title']
                    try:
                        item['price'] = int(input('Введите новую цену: '))
                        item['description'] = input('Введите новое описание: ') or item['description']
                    except ValueError:
                        item['price'] = item['price']
                        item['description'] = input('Введите новое описание: ') or item['description']
                    finally:
                        print('-' * 150 + f'\nДанные товара обновлены:\n{item}')
                    with open(DB, 'w+') as file:
                        for item in json_data:
                            if item['id'] == id_:
                                item.update({'update_date': str(datetime.now().strftime('%d.%m.%y %H:%M'))})
                                json.dump(json_data, file, indent=4, ensure_ascii=False)




def delete_data():
    """
    Deletes items from the list by id
    """
    if check_id() == []:
        print('Список пуст. Удалять нечего')
    while check_id() == False:
        print(f'{id_} нет в списке. Проверьте правильность ввода')
        continue
    else:
        json_data = read_data()
        for item in json_data:
            if item['id'] == id_:
                json_data.remove(item)
                print(f'\n{id_} удален из списка\n')
                with open(DB, 'w') as file:
                    json.dump(json_data, file, indent=4, ensure_ascii=False)
                return True



def clear_data():
    with open(DB, 'w+') as file:
        try:
            python_data = json.load(file)
            python_data.clear()
        except JSONDecodeError:
            return []
        finally:
            print('Список товаров пуст')



# как сделать так, чтобы либо минимальная, либо максимальная цена была
def sort_by_price():
    json_data = read_data()
    if json_data == []:
        print('Список пуст. Сортировать нечего')
        return []
    else:
        prices = []
        for item in json_data:
            prices.append(item['price'])
        print(f'Диапазон цен: {min(prices)} - {max(prices)}.')
        try:
            min_price = int(input('Введите минимальную цену: ')) or 0
            max_price = int(input('Введите максимальную цену: ')) or max(prices)
        except ValueError:
            print('Некорректно введена цена. Проверьте правильность ввода')
            min_price = 0
            max_price = max(prices)
        price_list = list([item for item in json_data if max_price >= item['price'] and min_price <= item['price']])
        for item in price_list:
            print('\nТовары, удовлетворяющие вашим пожеланиям: ')
            print('-' * 140)
            print(item)
            print('-' * 140)

            


# если список пустой
def sold_or_not():
    json_data = read_data()
    if json_data == []:
        print('Список пуст. Сортировать нечего')
    else:
        try:
            wanted_status = str(input('Какие товары вы хотите посмотреть: 1 - продается, 2 - продано: ')).strip().lower()
            if wanted_status == '1' or wanted_status =='продается':
                return list([item for item in json_data if item['selling_status'] == 'Продается'])
            elif wanted_status == '2' or wanted_status =='продано':
                return list([item for item in json_data if item['selling_status'] == 'Продано'])
            else:
                raise ValueError('Неправильно введены данные. Повторите попытку')
            return True
        except ValueError:
            wanted_status = str(input('Какие товары вы хотите посмотреть: 1 - продается, 2 - продано: ')).strip().lower()
            if wanted_status == '1' or wanted_status =='продается':
                return list([item for item in json_data if item['selling_status'] == 'Продается'])
            elif wanted_status == '2' or wanted_status =='продано':
                return list([item for item in json_data if item['selling_status'] == 'Продано'])


# почему два раза запрашивает
# есл список пустой
def sort_by_status():
    while not sold_or_not() is None:
        sold_or_not()
        break
    else:
        print('Товаров, удовлетворяющих параметрам вашего поиска, нет.')


# почему после выводится непонятный список, почму стирает базу
# есл список пустой
def purchase():
    json_data = read_data()
    for item in json_data:
        if item['selling_status'] == 'Продано':
            raise ValueError('Данный товар уже продан')
        else:
            # try:
                while check_id() == False:
                    print(f'{id_} нет в списке. Проверьте правильность ввода')
                    continue
                else:
                    item['selling_status'] = 'Продано'
                    with open(DB) as file:
                        json.dump(item, file, indent=4, ensure_ascii=False)
                    print('Поздравляем с покупкой')
                # except ValueError:    # что надо здесь прописать на самом деле
                #     while check_id() == False:
                #         print(f'{id_} нет в списке. Проверьте правильность ввода')
                #         continue
                #     else:
                #         obj['selling_status'] = 'Продано'
                #         json.dump(obj, file, indent=4)
                #         print('Поздравляем с покупкой')