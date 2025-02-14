def get_pc_configuration(purpose, budget, brand):
    rules = {
        ("Игры", "до 50 тыс.", "Intel"): "Intel i3-12100F, GTX 1650, 16GB RAM, SSD 512GB",
        ("Игры", "50-100 тыс.", "Intel"): "Intel i5-12400F, RTX 3060, 16GB RAM, SSD 1TB",
        ("Игры", "до 50 тыс.", "AMD"): "Ryzen 5 5500, RX 6500XT, 16GB RAM, SSD 512GB",
        ("Игры", "50-100 тыс.", "AMD"): "Ryzen 5 5600X, RTX 3060, 16GB RAM, SSD 1TB",
        
        ("Офис", "до 50 тыс.", "Intel"): "Intel i3-10105, 8GB RAM, SSD 256GB",
        ("Офис", "до 50 тыс.", "AMD"): "Ryzen 3 4100, 8GB RAM, SSD 256GB",
        
        ("Графика", "50-100 тыс.", "Intel"): "Intel i7-12700F, RTX 3060Ti, 32GB RAM, SSD 1TB",
        ("Графика", "50-100 тыс.", "AMD"): "Ryzen 7 5800X, RTX 3060Ti, 32GB RAM, SSD 1TB",
        
        ("Программирование", "до 50 тыс.", "Intel"): "Intel i5-11400, 16GB RAM, SSD 512GB",
        ("Программирование", "50-100 тыс.", "AMD"): "Ryzen 5 5600X, 32GB RAM, SSD 1TB",
    }
    
    return rules.get((purpose, budget, brand), "Нет подходящей конфигурации в базе")

# Ввод данных
purpose = input("Для чего нужен ПК? (Игры/Офис/Графика/Программирование): ")
budget = input("Какой бюджет? (до 50 тыс./50-100 тыс./свыше 100 тыс.): ")
brand = input("Предпочитаемый бренд (Intel/AMD): ")

# Вывод результата
config = get_pc_configuration(purpose, budget, brand)
print("Рекомендуемая конфигурация:", config)