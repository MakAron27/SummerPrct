import json
from collections import Counter
import re

def analyze_logs(file_path):
    """
    Анализирует лог-файл.
    Оптимизация: используем Counter вместо вложенных циклов.
    """
    
    ip_counter = Counter()
    status_counter = Counter()
    url_counter = Counter()
    
    # Читаем файл построчно (экономит память при больших логах)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.split()
            if len(parts) < 9:
                continue  # Пропускаем кривые строки
            
            ip = parts[0]
            status = parts[8]  # Код ответа
            
            # Достаем URL из кавычек
            match = re.search(r'"(GET|POST|PUT|DELETE) ([^"]+)"', line)
            url = match.group(2) if match else "unknown"
            
            # Считаем
            ip_counter[ip] += 1
            status_counter[status] += 1
            url_counter[url] += 1
    
    # Формируем результат
    result = {
        "total_requests": sum(ip_counter.values()),
        "top_ips": ip_counter.most_common(5),
        "status_distribution": dict(status_counter),
        "top_urls": url_counter.most_common(5)
    }
    
    # Сохраняем в JSON
    with open("stats.json", "w", encoding="utf-8") as out_file:
        json.dump(result, out_file, indent=2, ensure_ascii=False)
    
    return result

if __name__ == "__main__":
    print("Запускаю анализ логов...")
    stats = analyze_logs("test_log.txt")
    
    print("=" * 40)
    print("РЕЗУЛЬТАТ АНАЛИЗА")
    print("=" * 40)
    print(f"Всего запросов: {stats['total_requests']}")
    print("\nТоп-5 IP:")
    for ip, count in stats['top_ips']:
        print(f"  {ip} -> {count} раз(а)")
    print("\nРаспределение статусов:")
    for status, count in stats['status_distribution'].items():
        print(f"  {status} -> {count}")