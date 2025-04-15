from pyzabbix import ZabbixAPI
import sys
from config import ZABBIX_URL, ZABBIX_USER, ZABBIX_PASSWORD

def set_host_inventory_mode(zapi, host_id, mode):
    """
    Установка режима инвентаризации для хоста.
    mode: 0 - Disabled, 1 - Manual, 2 - Automatic
    """
    try:
        result = zapi.host.update(hostid=host_id, inventory_mode=mode)
        print(f"Режим инвентаризации установлен для хоста ID {host_id}: {result}")
    except Exception as e:
        print(f"Ошибка при обновлении режима инвентаризации для хоста ID {host_id}: {e}")

def get_host_id_by_name(zapi, host_name):
    """Получение ID хоста по его имени."""
    try:
        hosts = zapi.host.get(filter={"host": host_name}, output=["hostid"])
        if not hosts:
            raise Exception(f"Хост с именем '{host_name}' не найден")
        return hosts[0]["hostid"]
    except Exception as e:
        print(f"Ошибка при поиске хоста: {e}")
        sys.exit(1)

def main():
    # Инициализация API
    try:
        zapi = ZabbixAPI(ZABBIX_URL)
        zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)
        print(f"Успешно подключено к Zabbix API: {zapi.api_version()}")
    except Exception as e:
        print(f"Ошибка подключения к Zabbix API: {e}")
        sys.exit(1)

    # Режим работы: один хост или все хосты
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        # Обработка всех хостов
        try:
            hosts = zapi.host.get(output=["hostid", "host"])
            for host in hosts:
                host_id = host["hostid"]
                host_name = host["host"]
                print(f"Обновление инвентаризации для хоста: {host_name} (ID: {host_id})")
                set_host_inventory_mode(zapi, host_id, mode=2)  # Automatic
        except Exception as e:
            print(f"Ошибка при обработке хостов: {e}")
    else:
        # Обработка одного хоста
        host_name = "test-se-dtc-worker07"
        try:
            host_id = get_host_id_by_name(zapi, host_name)
            print(f"Найден хост '{host_name}' с ID: {host_id}")
            set_host_inventory_mode(zapi, host_id, mode=2)  # Automatic
        except Exception as e:
            print(f"Ошибка при обработке хоста: {e}")


if __name__ == "__main__":
    main()