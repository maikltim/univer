from state_machine import FridgeStateMachine
from expert_system import diagnose
from sensors import get_sensor_data

def main():
    fridge = FridgeStateMachine()

    tests = [
        get_sensor_data(power_on=False),
        get_sensor_data(power_on=True, cooling=False),
        get_sensor_data(power_on=True, cooling=True, noise=True),
        get_sensor_data(power_on=True, cooling=True, ice=True),
        get_sensor_data()
    ]

    for i, data in enumerate(tests, 1):
        state = fridge.update(data)
        result = diagnose(state)

        print(f"Эксперимент {i}")
        print(f"Состояние: {state}")
        print(f"Диагноз: {result}")
        print("-" * 40)

if __name__ == "__main__":
    main()
