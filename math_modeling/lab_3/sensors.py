def get_sensor_data(power_on=True, cooling=True, noise=False, ice=False):
    """
    Имитация сигналов датчиков холодильника
    """
    return {
        "power_on": power_on,
        "cooling": cooling,
        "noise": noise,
        "ice": ice
    }
