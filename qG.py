import matplotlib.pyplot as plt

def calculate_emv(strategies):
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
    return emv_results

def calculate_evpi(strategies, emv_results):
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

def calculate_evsi(strategies, base_probabilities, test_results):
    print("\n----------EVSI results----------\n")
    P_Theta = test_results["P(Theta/Y)"] * base_probabilities["P(Y)"] + test_results["P(Theta/X)"] * base_probabilities["P(X)"]
    P_I = test_results["P(I/Y)"] * base_probabilities["P(Y)"] + test_results["P(I/X)"] * base_probabilities["P(X)"]
    P_A = test_results["P(A/Y)"] * base_probabilities["P(Y)"] + test_results["P(A/X)"] * base_probabilities["P(X)"]

    # Calculate posterior probabilities using Bayes' theorem
    posterior = {
        "P(Y/Theta)": (test_results["P(Theta/Y)"] * base_probabilities["P(Y)"]) / P_Theta,
        "P(X/Theta)": (test_results["P(Theta/X)"] * base_probabilities["P(X)"]) / P_Theta,
        "P(Y/I)": (test_results["P(I/Y)"] * base_probabilities["P(Y)"]) / P_I,
        "P(X/I)": (test_results["P(I/X)"] * base_probabilities["P(X)"]) / P_I,
        "P(Y/A)": (test_results["P(A/Y)"] * base_probabilities["P(Y)"]) / P_A,
        "P(X/A)": (test_results["P(A/X)"] * base_probabilities["P(X)"]) / P_A,
    }

    # Now calculate EVSI for each category
    for category, options in strategies.items():

        # We need to calculate EMV for each possible test result (Θ, I, A)
        emv_test_results = {"Theta": {}, "I": {}, "A": {}}

        # For each test result, calculate the best EMV using posterior probabilities
        for test_result in ["Theta", "I", "A"]:
            # Get the posterior probabilities for this test result
            p_Y = posterior[f"P(Y/{test_result})"]
            p_X = posterior[f"P(X/{test_result})"]

            # Calculate EMV for each option under these probabilities
            for name, data in options.items():
                # Assuming the first result in 'results' is for Y and second for X
                # (You may need to adjust this based on your actual data structure)
                payoff_Y = data["results"][0][1] - data["cost"]
                payoff_X = data["results"][1][1] - data["cost"]

                emv = p_Y * payoff_Y + p_X * payoff_X
                emv_test_results[test_result][name] = emv

        # Find the best option for each test result
        best_emv_per_test_result = {
            "Theta": max(emv_test_results["Theta"].values()),
            "I": max(emv_test_results["I"].values()),
            "A": max(emv_test_results["A"].values())
        }

        # Calculate EVSI
        EVSI = (P_Theta * best_emv_per_test_result["Theta"] +
                P_I * best_emv_per_test_result["I"] +
                P_A * best_emv_per_test_result["A"]) - max(emv_results[category].values())

        print(f"{category}: EVSI = {EVSI:.2f}€")


def sensitivity_analysis(strategies):
    print("\n----------Sensitivity Analysis (±10% on highest probability)----------\n")
    deltas = [-0.1, 0.1]
    for delta in deltas:
        print(f"\n>>> Change in highest probability: {delta * 100:+.0f}%\n")
        for category, options in strategies.items():
            print(f"Category: {category}")
            for name, data in options.items():
                original_results = data["results"]
                cost = data["cost"]
                results = [(p, v) for p, v in original_results]
                max_idx = max(range(len(results)), key=lambda i: results[i][0])
                max_prob = results[max_idx][0]
                new_max_prob = min(max_prob * (1 + delta), 1.0)
                remaining_prob = 1.0 - new_max_prob
                other_total = sum(results[i][0] for i in range(len(results)) if i != max_idx)
                new_results = []
                for i in range(len(results)):
                    if i == max_idx:
                        new_results.append((new_max_prob, results[i][1]))
                    else:
                        new_p = remaining_prob * (results[i][0] / other_total) if other_total > 0 else 0
                        new_results.append((new_p, results[i][1]))
                new_expected_value = sum(p * v for p, v in new_results)
                new_emv = new_expected_value - cost
                print(f"{name}: Adjusted EMV = {new_emv:.2f}€")

def plot_sensitivity(base_emv, results):
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)
    fig.suptitle('EMV Sensitivity Analysis: Impact of Probability Changes', fontsize=16, y=0.98)
    styles = {
        "Marketing": {
            "Επιθετικό": {'color': '#1f77b4', 'marker': 'o', 'linestyle': '-', 'markersize': 8},
            "Μέτριο": {'color': '#ff7f0e', 'marker': 's', 'linestyle': '--', 'markersize': 8},
            "Συντηρητικό": {'color': '#2ca02c', 'marker': '^', 'linestyle': ':', 'markersize': 8}
        },
        "Investment": {
            "Υψηλό": {'color': '#d62728', 'marker': 'o', 'linestyle': '-', 'markersize': 8},
            "Χαμηλό": {'color': '#9467bd', 'marker': 's', 'linestyle': '--', 'markersize': 8}
        },
        "Supply": {
            "Ακριβά υλικά": {'color': '#8c564b', 'marker': 'o', 'linestyle': '-', 'markersize': 8},
            "Φτηνά υλικά": {'color': '#e377c2', 'marker': 's', 'linestyle': '--', 'markersize': 8}
        }
    }
    x_points = [0, 1]
    x_labels = ['Base Case', 'Adjusted']
    for row, change in enumerate(["-10%", "+10%"]):
        for col, category in enumerate(["Marketing", "Investment", "Supply"]):
            ax = axes[row, col]
            options = results[change][category]
            all_values = list(base_emv[category].values()) + list(options.values())
            y_min = min(all_values) - 0.1 * abs(min(all_values))
            y_max = max(all_values) + 0.1 * abs(max(all_values))
            for name, adj_emv in options.items():
                base = base_emv[category][name]
                style = styles[category][name]
                ax.plot(x_points, [base, adj_emv], label=name, linewidth=2.5,
                        marker=style['marker'], linestyle=style['linestyle'],
                        color=style['color'], markersize=style['markersize'])
                ax.text(0, base, f' {base:,.0f}€ ', ha='right', va='center',
                        fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
                ax.text(1, adj_emv, f' {adj_emv:,.0f}€ ', ha='left', va='center',
                        fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
            ax.set_title(f'{category} Strategy\n{change} Probability Change', pad=12, fontsize=12)
            ax.set_xticks(x_points)
            ax.set_xticklabels(x_labels, fontsize=11)
            ax.set_ylabel('EMV (€)', fontsize=11)
            ax.grid(True, linestyle=':', alpha=0.7)
            ax.legend(loc='upper left', fontsize=10)
            ax.set_ylim(y_min, y_max)
            if y_min < 0:
                ax.axhline(0, color='black', linewidth=0.8, linestyle='-', alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
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

    base_probabilities = {
        "P(Y)": 0.4,
        "P(X)": 0.6
    }

    test_results = {
        "P(Theta/Y)": 0.50,  # Probability of Positive test given Y
        "P(I/Y)": 0.25,  # Probability of Inconclusive given Y
        "P(A/Y)": 0.25,  # Probability of Negative given Y
        "P(Theta/X)": 0.20,  # Probability of Positive test given X
        "P(I/X)": 0.25,  # Probability of Inconclusive given X
        "P(A/X)": 0.55   # Probability of Negative given X
    }

    base_emv = {
        "Marketing": {"Επιθετικό": 96000, "Μέτριο": 52000, "Συντηρητικό": 51500},
        "Investment": {"Υψηλό": 66000, "Χαμηλό": -8000},
        "Supply": {"Ακριβά υλικά": 57500, "Φτηνά υλικά": 60000}
    }

    results = {
        "-10%": {
            "Marketing": {"Επιθετικό": 87900, "Μέτριο": 47800, "Συντηρητικό": 47975},
            "Investment": {"Υψηλό": 53400, "Χαμηλό": -12200},
            "Supply": {"Ακριβά υλικά": 48750, "Φτηνά υλικά": 53000}
        },
        "+10%": {
            "Marketing": {"Επιθετικό": 104100, "Μέτριο": 56200, "Συντηρητικό": 55025},
            "Investment": {"Υψηλό": 78600, "Χαμηλό": -3800},
            "Supply": {"Ακριβά υλικά": 66250, "Φτηνά υλικά": 67000}
        }
    }

    emv_results = calculate_emv(strategies)
    calculate_evpi(strategies, emv_results)
    calculate_evsi(strategies, base_probabilities, test_results)
    sensitivity_analysis(strategies)
    plot_sensitivity(base_emv, results)
