import matplotlib.pyplot as plt
import numpy as np

def calculate_emv(strategies):
    emv_results = {}
    print("\nEMV results\n")
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
    print("\nEVPI results\n")
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
    print("\nEVSI results\n")

    # Probabilities for test outcomes
    P_Theta = test_results["P(Theta/Y)"] * base_probabilities["P(Y)"] + test_results["P(Theta/X)"] * base_probabilities["P(X)"]
    P_I = test_results["P(I/Y)"] * base_probabilities["P(Y)"] + test_results["P(I/X)"] * base_probabilities["P(X)"]
    P_A = test_results["P(A/Y)"] * base_probabilities["P(Y)"] + test_results["P(A/X)"] * base_probabilities["P(X)"]

    posterior = {
        "P(Y/Theta)": (test_results["P(Theta/Y)"] * base_probabilities["P(Y)"]) / P_Theta,
        "P(X/Theta)": (test_results["P(Theta/X)"] * base_probabilities["P(X)"]) / P_Theta,
        "P(Y/I)": (test_results["P(I/Y)"] * base_probabilities["P(Y)"]) / P_I,
        "P(X/I)": (test_results["P(I/X)"] * base_probabilities["P(X)"]) / P_I,
        "P(Y/A)": (test_results["P(A/Y)"] * base_probabilities["P(Y)"]) / P_A,
        "P(X/A)": (test_results["P(A/X)"] * base_probabilities["P(X)"]) / P_A,
    }

    # EVSI for each category
    for category, options in strategies.items():

        # EMV for each test result
        emv_test_results = {"Theta": {}, "I": {}, "A": {}}

        # For each test result, calculate the best EMV using posterior probabilities
        for test_result in ["Theta", "I", "A"]:
            p_Y = posterior[f"P(Y/{test_result})"]
            p_X = posterior[f"P(X/{test_result})"]

            for name, data in options.items():
                payoff_Y = data["results"][0][1] - data["cost"]
                payoff_X = data["results"][1][1] - data["cost"]
                # Updated EMV
                emv = p_Y * payoff_Y + p_X * payoff_X
                emv_test_results[test_result][name] = emv

        # Find best option for each test result
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


def sensitivity_analysis(strategies, base_prob, variations=[-0.10, 0, +0.10]):
    print("\nSensitivity Analysis\n")
    for category, options in strategies.items():
        print(f"\n{category}")
        original_p = base_prob["P(Y)"]
        for variation in variations:
            new_p = original_p + (variation * original_p)
            new_p_X = 1 - new_p
            print(f"\nP(Y) = {new_p:.2f}, P(X) = {new_p_X:.2f}")

            best_emv = -float('inf')
            best_strategy = None

            for name, data in options.items():
                # Calculate EMV with new probabilities
                payoff_Y = data["results"][0][1] - data["cost"]
                payoff_X = data["results"][1][1] - data["cost"]
                emv = new_p * payoff_Y + new_p_X * payoff_X

                print(f"{name}: EMV = {emv:.2f}€")

                if emv > best_emv:
                    best_emv = emv
                    best_strategy = name

            print(f"→ Best strategy: {best_strategy} (EMV = {best_emv:.2f}€)")


def plot_sensitivity_results(strategies, base_prob):
    # Probability range +-10%
    p_Y_values = np.linspace(base_prob["P(Y)"] * 0.9,
                             base_prob["P(Y)"] * 1.1,
                             100)

    # Create a figure for each category
    for category, options in strategies.items():
        plt.figure(figsize=(10, 6))

        # Calculate EMV for each strategy across P(Y) range
        for strategy_name, data in options.items():
            emvs = []
            for p_Y in p_Y_values:
                p_X = 1 - p_Y
                payoff_Y = data["results"][0][1] - data["cost"]
                payoff_X = data["results"][1][1] - data["cost"]
                emv = p_Y * payoff_Y + p_X * payoff_X
                emvs.append(emv)

            # Plot the strategy's EMV curve
            plt.plot(p_Y_values, emvs,
                     label=strategy_name,
                     linewidth=2)

        # Format the plot
        plt.title(f"Sensitivity Analysis: {category}")
        plt.xlabel("Probability")
        plt.ylabel("EMV")
        plt.axvline(x=base_prob["P(Y)"], color='gray', linestyle='--',
                    label='Base Probability')
        plt.grid(True)
        plt.legend()
        plt.show()

if __name__ == '__main__':
    strategies = {
        "Marketing":{
            "Επιθετικό":{
                "cost": 70000,
                "results": [(0.6, 220000), (0.4, 100000)]
            },
            "Μέτριο":{
                "cost": 40000,
                "results": [(0.6, 120000), (0.4, 60000)]
            },
            "Συντηρητικό":{
                "cost": 25000,
                "results": [(0.6, 100000), (0.4, 50000)]
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
                "results": [(0.6, 165000), (0.4, 40000)]
            },
            "Φτηνά υλικά":{
                "cost": 30000,
                "results": [(0.6, 120000), (0.4, 20000)]
            }
        }
    }

    base_probabilities = {
        "P(Y)": 0.6,
        "P(X)": 0.4
    }

    test_results = {
        "P(Theta/Y)": 0.50,
        "P(I/Y)": 0.25,
        "P(A/Y)": 0.25,
        "P(Theta/X)": 0.20,
        "P(I/X)": 0.25,
        "P(A/X)": 0.55
    }

    emv_results = calculate_emv(strategies)
    calculate_evpi(strategies, emv_results)
    calculate_evsi(strategies, base_probabilities, test_results)
    base_prob = {"P(Y)": 0.6, "P(X)": 0.4}
    sensitivity_analysis(strategies, base_prob)
    plot_sensitivity_results(strategies, base_prob)