# Data definition

strategies = {
    "Marketing":{
        "Επιθετικό":{
            "cost": 70000,
            "results": [(0.6, 220000), (0.3, 100000), (0.1, 40000)]
        },
        "Μέτριο":{
            "cost": 40000,
            "results": [(0.4, 120000), (0.4, 60000), (0.2, 20000)]
        },
        "Συντηρητικό":{
            "cost": 25000,
            "results": [(0.2, 100000), (0.5, 50000), (0.3, 15000)]
        }
    },
    "Investment":{
        "Υψηλό":{
            "cost": 100000,
            "results": [(0.6, 250000), (0.4, 40000)]
        },
        "Χαμηλό":{
            "cost": 30000,
            "results": [(0.4, 50000), (0.6, -20000)]
        }
    },
    "Supply":{
        "Ακριβά υλικά":{
            "cost": 70000,
            "results": [(0.7, 165000), (0.3, 40000)]
        },
        "Φτηνά υλικά":{
            "cost": 30000,
            "results": [(0.4, 120000), (0.6, 20000)]
        }
    }
}

emv_results = {}

for category, options in strategies.items():
    print(category)
    emv_results[category] = {}
    for name, data in options.items():
        expected_value = sum(prob * result for prob, result in data["results"])
        emv = expected_value - data["cost"]
        emv_results[category][name] = emv
        print(f"{name}: EMV = {emv:.2f}€")