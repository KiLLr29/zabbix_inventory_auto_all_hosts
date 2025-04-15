import csv
from pyzabbix import ZabbixAPI
from config import ZABBIX_URL, ZABBIX_USER, ZABBIX_PASSWORD

def export_unique_tags_to_csv(zapi):
    """
    Экспорт уникальных тегов для хостов и элементов в два отдельных CSV-файла.
    """
    try:
        # Получение всех хостов с тегами
        hosts = zapi.host.get(
            output=["hostid", "host"],
            selectTags="extend",
            selectItems=["itemid", "name", "key_", "tags"]
        )

        # Словари для хранения уникальных тегов
        unique_host_tags = {}
        unique_item_tags = {}

        for host in hosts:
            host_id = host["hostid"]
            host_name = host["host"]
            host_tags = host["tags"]

            # Добавление уникальных тегов хоста
            for tag in host_tags:
                tag_key = f"{tag['tag']}={tag['value']}"
                if tag_key not in unique_host_tags:
                    unique_host_tags[tag_key] = {
                        "Host ID": host_id,
                        "Host Name": host_name,
                        "Tag": tag["tag"],
                        "Value": tag["value"]
                    }

            # Добавление уникальных тегов элементов (items)
            for item in host["items"]:
                item_id = item["itemid"]
                item_name = item["name"]
                item_key = item["key_"]
                item_tags = item.get("tags", [])

                for tag in item_tags:
                    tag_key = f"{tag['tag']}={tag['value']}"
                    if tag_key not in unique_item_tags:
                        unique_item_tags[tag_key] = {
                            "Item ID": item_id,
                            "Item Name": item_name,
                            "Item Key": item_key,
                            "Tag": tag["tag"],
                            "Value": tag["value"]
                        }

        # Запись уникальных тегов хостов в CSV
        write_to_csv(unique_host_tags.values(), "zabbix_host_tags.csv", ["Host ID", "Host Name", "Tag", "Value"])

        # Запись уникальных тегов элементов в CSV
        write_to_csv(unique_item_tags.values(), "zabbix_item_tags.csv", ["Item ID", "Item Name", "Item Key", "Tag", "Value"])

    except Exception as e:
        print(f"Ошибка при экспорте данных: {e}")

def write_to_csv(data, filename, fieldnames):
    """
    Запись данных в CSV-файл.
    """
    if data:
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        print(f"Данные успешно экспортированы в файл: {filename}")
    else:
        print(f"Нет данных для экспорта в файл: {filename}")

def main():
    # Инициализация API
    try:
        zapi = ZabbixAPI(ZABBIX_URL)
        zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)
        print(f"Успешно подключено к Zabbix API: {zapi.api_version()}")
    except Exception as e:
        print(f"Ошибка подключения к Zabbix API: {e}")
        return

    # Выполнение экспорта
    export_unique_tags_to_csv(zapi)

if __name__ == "__main__":
    main()