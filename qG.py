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

    probabilities = [p for p, r in next(iter(options.values()))["results"]]

    payoffs_per_state = []
    for i in range(len(probabilities)):
        payoffs_state_i = []
        for name, data in options.items():
            payoff = data["results"][i][1] - data["cost"]
            payoffs_state_i.append(payoff)
        payoffs_per_state.append(payoffs_state_i)

    max_payoffs_per_state = [max(payoffs) for payoffs in payoffs_per_state]

    Evwpi = sum(p * payoff for p, payoff in zip(probabilities, max_payoffs_per_state))

    max_emv = max(emv_results[category].values())

    EVPI = Evwpi - max_emv

    print(f"{category}: EVPI = {EVPI:.2f}€")