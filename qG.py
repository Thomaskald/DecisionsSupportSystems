# Data definition
import numpy as np

strategies = {
    "Marketing":{
        "Επιθετικό":{
            "cost": 70000,
            "results": [(0.6, 220000), (0.3, 100000), (0.1, 40000)]
        },
        "Μέτριο":{
            "cost": 40000,
            "results": [(0.6, 120000), (0.3, 60000), (0.1, 20000)]
        },
        "Συντηρητικό":{
            "cost": 25000,
            "results": [(0.6, 100000), (0.3, 50000), (0.1, 15000)]
        }
    },
    "Investment":{
        "Υψηλό":{
            "cost": 100000,
            "results": [(0.6, 250000), (0.4, 40000)]
        },
        "Χαμηλό":{
            "cost": 30000,
            "results": [(0.6, 50000), (0.4, -20000)]
        }
    },
    "Supply":{
        "Ακριβά υλικά":{
            "cost": 70000,
            "results": [(0.7, 165000), (0.3, 40000)]
        },
        "Φτηνά υλικά":{
            "cost": 30000,
            "results": [(0.7, 120000), (0.3, 20000)]
        }
    }
}

emv_results = {}
print("\n----------EMV results----------\n")

for category, options in strategies.items():
    print(category)
    emv_results[category] = {}
    for name, data in options.items():
        expected_value = sum(prob * result for prob, result in data["results"])
        emv = expected_value - data["cost"]
        emv_results[category][name] = emv
        print(f"{name}: EMV = {emv:.2f}€")

evpi_results = {}
print("\n----------EVPI results----------\n")

for category, options in strategies.items():
    print(f"Κατηγορία: {category}")
    strategy_names = list(options.keys())
    payoff_matrix = []
    probabilities = [prob for prob, _ in list(options.values())[0]["results"]]

    for name in strategy_names:
        strategy = options[name]
        net_results = [result - strategy["cost"] for prob, result in strategy["results"]]
        payoff_matrix.append(net_results)

    payoff_matrix = np.array(payoff_matrix)

    # Υπολογισμός EVwPI
    best_per_scenario = np.max(payoff_matrix, axis=0)
    evwpi = np.dot(probabilities, best_per_scenario)

    # Ανάκτηση μέγιστου EMV από τα υπολογισμένα emv_results
    best_emv = max(emv_results[category].values())

    # Υπολογισμός EVPI
    evpi = evwpi - best_emv

    print(f"  ➤ EVwPI = {evwpi:.2f}€")
    print(f"  ➤ Max EMV = {best_emv:.2f}€")
    print(f"  ➤ EVPI = {evpi:.2f}€")
    print("-" * 40)