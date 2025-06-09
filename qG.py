# Data definition
import matplotlib.pyplot as plt

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

# EMV
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


# EVPI
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
#
# # EVSI
# outcomes = ["Θετικό", "Αρνητικό"]
# test_probabilities = {
#     "Marketing": np.array([
#         [0.8, 0.2],  # P(Θετικό|High)
#         [0.5, 0.5],  # P(Θετικό|Medium)
#         [0.2, 0.8]   # P(Θετικό|Low)
#     ]),
#     "Investment": np.array([
#         [0.7, 0.3],  # P(Θετικό|High)
#         [0.4, 0.6],  # P(Θετικό|Low)
#     ]),
#     "Supply": np.array([
#         [0.9, 0.1],  # P(Θετικό|High)
#         [0.3, 0.7],  # P(Θετικό|Low)
#     ])
# }
#
# print("\n----------EVSI results----------\n")
#
# for category, likelihood in test_probabilities.items():
#     # Πιθανότητες καταστάσεων (a priori)
#     prior_probs = [p for p, r in next(iter(strategies[category].values()))["results"]]
#
#     # Υπολογισμός συνολικής πιθανότητας κάθε test outcome
#     test_probs = np.dot(prior_probs, likelihood)  # vector με πιθανότητες test outcomes
#
#     # Υπολογισμός a-posteriori πιθανοτήτων για κάθε αποτέλεσμα
#     posterior_probs = (likelihood.T * prior_probs).T / test_probs
#
#     evsi_sum = 0
#     for i, test_outcome_prob in enumerate(test_probs):
#         post_probs = posterior_probs[:, i]
#         max_emv_post = float('-inf')
#
#         # Υπολογισμός νέου EMV για κάθε επιλογή με a-posteriori πιθανότητες
#         for name, data in strategies[category].items():
#             expected_value_post = sum(post_probs[j] * data["results"][j][1] for j in range(len(post_probs)))
#             emv_post = expected_value_post - data["cost"]
#             if emv_post > max_emv_post:
#                 max_emv_post = emv_post
#
#         evsi_sum += test_outcome_prob * max_emv_post
#
#     best_emv = max(emv_results[category].values())
#     evsi = evsi_sum - best_emv
#
#     print(f"{category}: EVSI = {evsi:.2f}€")

    # SENSITIVITY ANALYSIS ±10% on highest probability
print("\n----------Sensitivity Analysis (±10% on highest probability)----------\n")

deltas = [-0.1, 0.1]

for delta in deltas:
    print(f"\n>>> Change in highest probability: {delta * 100:+.0f}%\n")
    for category, options in strategies.items():
        print(f"Category: {category}")
        best_option = None
        best_emv = float('-inf')

        for name, data in options.items():
            original_results = data["results"]
            cost = data["cost"]

            # Copy results
            results = [(p, v) for p, v in original_results]
            max_idx = max(range(len(results)), key=lambda i: results[i][0])
            max_prob = results[max_idx][0]

            # Adjust max probability
            new_max_prob = max_prob * (1 + delta)
            if new_max_prob > 1:
                new_max_prob = 1.0
            remaining_prob = 1.0 - new_max_prob

            # Adjust other probabilities proportionally
            other_total = sum(results[i][0] for i in range(len(results)) if i != max_idx)
            new_results = []
            for i in range(len(results)):
                if i == max_idx:
                    new_results.append((new_max_prob, results[i][1]))
                else:
                    if other_total > 0:
                        new_p = remaining_prob * (results[i][0] / other_total)
                    else:
                        new_p = 0
                    new_results.append((new_p, results[i][1]))

            # Check total probability
            prob_sum = sum(p for p, _ in new_results)
            if abs(prob_sum - 1.0) > 0.0001:
                print(f"⚠️ WARNING: Probabilities do not sum to 1 in {name} (sum = {prob_sum:.4f})")

            # Calculate new EMV
            new_expected_value = sum(p * v for p, v in new_results)
            new_emv = new_expected_value - cost
            print(f"{name}: Adjusted EMV = {new_emv:.2f}€")

            if new_emv > best_emv:
                best_emv = new_emv
                best_option = name

        print(f"--> Best Option: {best_option} with EMV = {best_emv:.2f}€\n")

import matplotlib.pyplot as plt
import numpy as np

# Prepare the probability variation range (similar to your example image)
prob_range = np.linspace(0.15, 0.95, 9)  # 0.15 to 0.95 in 9 steps

# Create 6 subplots (2 rows, 3 columns)
fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.suptitle('Sensitivity Analysis of EMV (Varying Highest Probability)', fontsize=16)

for i, category in enumerate(strategies.keys()):
    for j, delta in enumerate([-0.1, 0.1]):  # -10% and +10% variations
        ax = axes[j, i]

        # Get all options for this category
        option_names = list(strategies[category].keys())

        # Prepare to store all EMV curves
        emv_curves = {name: [] for name in option_names}

        # Vary the probability and calculate EMV for each option
        for base_prob in prob_range:
            for name in option_names:
                data = strategies[category][name]
                original_results = data["results"]
                cost = data["cost"]

                # Find the highest probability outcome
                max_idx = max(range(len(original_results)),
                              key=lambda k: original_results[k][0])
                max_prob = original_results[max_idx][0]

                # Adjust the max probability (but keep it between 0 and 1)
                new_max_prob = max(0, min(1, base_prob))
                remaining_prob = 1.0 - new_max_prob

                # Adjust other probabilities proportionally
                other_total = sum(original_results[k][0]
                                  for k in range(len(original_results)) if k != max_idx)
                new_results = []
                for k in range(len(original_results)):
                    if k == max_idx:
                        new_results.append((new_max_prob, original_results[k][1]))
                    else:
                        if other_total > 0:
                            new_p = remaining_prob * (original_results[k][0] / other_total)
                        else:
                            new_p = 0
                        new_results.append((new_p, original_results[k][1]))

                # Calculate EMV
                new_expected_value = sum(p * v for p, v in new_results)
                new_emv = new_expected_value - cost
                emv_curves[name].append(new_emv)

        # Plot all curves for this category and delta
        for name in option_names:
            ax.plot(prob_range, emv_curves[name], marker='o', label=name)

        ax.set_title(f'{category} - {"+" if delta > 0 else ""}{delta * 100:.0f}% Change')
        ax.set_xlabel('Adjusted Probability')
        ax.set_ylabel('EMV (€)')
        ax.legend()
        ax.grid(True)

plt.tight_layout()
plt.show()