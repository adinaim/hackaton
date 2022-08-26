import json
from settings import DB
from datetime import datetime
from json.decoder import JSONDecodeError



def read_data():
    """
    Shows information about all items in the shop
    """
    with open(DB) as file:
        try:
            return json.load(file)
        except JSONDecodeError:
            return []



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
        json_data: list = read_data()
        json_data.append(data)
        with open(DB, 'w') as f:
            json.dump(json_data, f, indent=4)
    except ValueError:
        print('Неправильно введены данные. Проверьте правильность и повторите попытку')
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
            json.dump(json_data, file, indent=4)




def available_id():
    """
    Shows available ids and is called in the functions that request an id from a user
    """
    with open(DB, 'r') as file:
        file.seek(0)
        python_data = json.load(file)
        list_of_keys = []
        for item in python_data:
            list_of_keys.append(item['id'])
        print(f'Доступные id:{list_of_keys}')



def check_id():
    """
    Shows ids of available items and checks if an id is in the list
    """
    available_id()
    global id_
    id_ = input('Введите id: ')
    global data
    data = read_data()
    global obj
    for obj in data:
        if obj['id'] == id_:
            return True
    else:
        return False



def retrieve_data():
    """
    Retrieves an item from the database by id
    """
    while check_id() == False:
        print(f'{id_} нет в списке. Проверьте правильность ввода')
        continue
    else:
        return obj



def update_data():
    """
    Updates info about items
    """
    while check_id() == False:
        print(f'{id_} нет в списке. Проверьте правильность ввода')
        continue
    else:
        try:
            obj['title'] = input('Введите новое название: ') or obj['title']
            obj['price'] = int(input('Введите новую цену: ')) or obj['price']
            obj['description'] = input('Введите новое описание: ') or obj['description']
        except (ValueError, JSONDecodeError):
            print('Введите правильную цену')
            obj['price'] = obj['price']
            obj['description'] = input('Введите новое описание: ') or obj['description']
        finally:
            print('-' * 80 + f'\nДанные товара обновлены:\n{obj}')
        with open(DB, 'w+') as file:
            python_data = json.load(file)
            for item in python_data:
                if obj['id'] == id_:
                    update_date = {'update_date': datetime.now().strftime('%d.%m.%y %H:%M')}
                    item.update(update_date)
            json.dump(data, file, indent=4)



def delete_data():
    """
    Deletes items from the list by id
    """
    while check_id() == False:
        print(f'{id_} нет в списке. Проверьте правильность ввода')
        continue
    else:
        data.remove(obj)
        print(f'\n{id_} удален из списка\n')
        with open(DB, 'w') as file:
            json.dump(data, file, indent=4)
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



def sort_by_price():
    with open(DB, 'r') as file:
        python_data = json.load(file)
        prices = []
        for item in python_data:
            prices.append(item['price'])
        print(f'Диапазон цен: {min(prices)} - {max(prices)}.')
        try:
            min_price = int(input('Введите минимальную цену: ')) or 0
            max_price = int(input('Введите максимальную цену: ')) or max(prices)
            print(list([item for item in python_data if max_price >= item['price'] and min_price <= item['price']]))
        except ValueError:
            print('Некорректно введена цена. Проверьте правильность ввода')
            min_price = 0
            max_price = max(prices)
            for item in python_data:
                print(list([item for item in python_data if max_price >= item['price'] and min_price <= item['price']]))



def sold_or_not():
    try:
        with open(DB, 'r') as file:
            python_data = json.load(file)
            wanted_status = str(input('Какие товары вы хотите посмотреть: 1 - продается, 2 - продано: ')).strip().lower()
            if wanted_status == '1' or wanted_status =='продается':
                print(list([item for item in python_data if item['selling_status'] == 'Продается']))
            elif wanted_status == '2' or wanted_status =='продано':
                print(list([item for item in python_data if item['selling_status'] == 'Продано']))
            else:
                raise ValueError('Неправильно введены данные. Повторите попытку')
            return True
    except ValueError:
        if wanted_status == '1' or wanted_status =='продается':
            return [item for item in python_data if item['selling_status'] == 'Продается']
        elif wanted_status == '2' or wanted_status =='продано':
            return [item for item in python_data if item['selling_status'] == 'Продано']
        else:
            raise ValueError
            return True



def sort_by_status():
    if not sold_or_not() is None:
        sold_or_not()
    else:
        print('Товаров, удовлетворяющих параметрам вашего поиска, нет.')



def purchase():
    with open(DB) as file:
        python_data = json.load(file)
        for obj in python_data:
            if obj['selling_status'] == 'Продано':
                raise ValueError('Данный товар уже продан')
            try:
                while check_id() == False:
                    print(f'{id_} нет в списке. Проверьте правильность ввода')
                    continue
                else:
                    obj['selling_status'] = 'Продано'
                    with open(DB, 'w+') as file:
                        selling_status = {'selling_status': 'Продано'}
                        obj.update(selling_status)
                        print('Поздравляем с покупкой')
            except ValueError:
                while check_id() == False:
                    print(f'{id_} нет в списке. Проверьте правильность ввода')
                    continue
                else:
                    selling_status = {'selling_status': 'Продано'}
                    obj.update(selling_status)
                    with open(DB, 'w+') as file:
                        json.dump(data, file)
                        print('Поздравляем с покупкой')