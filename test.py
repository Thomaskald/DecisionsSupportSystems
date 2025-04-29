import numpy as np
import random

# === AHP Functions ===

def calculate_weights(matrix):
    normalized = matrix / matrix.sum(axis=0)
    return normalized.mean(axis=1)

def calculate_cr(matrix):
    n = matrix.shape[0]
    if n <= 2: return 0.0
    weights = calculate_weights(matrix)
    weighted_sum = np.dot(matrix, weights)
    l_max = np.mean(weighted_sum / weights)
    CI = (l_max - n) / (n - 1)
    RI = {3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}.get(n, 0.58)
    return CI / RI if RI != 0 else 0.0

def generate_random_matrix(size=3):
    saaty_scale = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    matrix = np.ones((size, size))
    for i in range(size):
        for j in range(i + 1, size):
            val = random.choice(saaty_scale)
            matrix[i][j] = val
            matrix[j][i] = 1 / val
    return matrix

def generate_consistent_matrix(size):
    while True:
        m = generate_random_matrix(size)
        if calculate_cr(m) < 0.1:
            return m

# === AHP per Specialist ===

def ahp_for_expert():
    # Generate all matrices
    matrices = {
        "criteria": generate_consistent_matrix(3),
        "economic": generate_consistent_matrix(2),
        "performance": generate_consistent_matrix(3),
        "social": generate_consistent_matrix(2),
        "dev_cost": generate_consistent_matrix(3),
        "maint_cost": generate_consistent_matrix(3),
        "reliability": generate_consistent_matrix(3),
        "speed": generate_consistent_matrix(3),
        "security": generate_consistent_matrix(3),
        "compat": generate_consistent_matrix(3),
        "usability": generate_consistent_matrix(3)
    }

    # Calculate weights and CR
    weights = {k: calculate_weights(m) for k, m in matrices.items()}
    crs = {k: calculate_cr(m) for k, m in matrices.items()}

    # Compute final alternative scores
    criteria_weights = weights["criteria"]
    economic_weights = weights["economic"]
    performance_weights = weights["performance"]
    social_weights = weights["social"]

    alternative_scores = np.zeros(3)
    for i in range(3):
        economic = criteria_weights[0] * (
            economic_weights[0] * weights["dev_cost"][i] +
            economic_weights[1] * weights["maint_cost"][i]
        )
        performance = criteria_weights[1] * (
            performance_weights[0] * weights["reliability"][i] +
            performance_weights[1] * weights["speed"][i] +
            performance_weights[2] * weights["security"][i]
        )
        social = criteria_weights[2] * (
            social_weights[0] * weights["compat"][i] +
            social_weights[1] * weights["usability"][i]
        )
        alternative_scores[i] = economic + performance + social

    return {
        "weights": weights,
        "crs": crs,
        "scores": alternative_scores
    }

# === Run for Multiple Experts ===

def ahp_multi_expert(n_experts=10):
    all_results = []

    for i in range(n_experts):
        print(f"\n========== ΕΙΔΙΚΟΣ {i + 1} ==========\n")
        result = ahp_for_expert()
        weights = result["weights"]
        crs = result["crs"]
        scores = result["scores"]
        all_results.append(result)

        # Labels
        criteria = ['Οικονομικά θέματα', 'Απόδοση', 'Κοινωνική αποδοχή']
        economic_sub = ['Κόστος ανάπτυξης', 'Κόστος συντήρησης']
        performance_sub = ['Αξιοπιστία', 'Ταχύτητα', 'Ασφάλεια δεδομένων']
        social_sub = ['Συμβατότητα', 'Ευχρηστία']
        alternatives = ['Ιστοσελίδα', 'Mobile εφαρμογή', 'Κεντρικό σύστημα']

        # Print results per expert
        print("1. ΒΑΡΗ ΚΡΙΤΗΡΙΩΝ:")
        for c, w in zip(criteria, weights["criteria"]):
            print(f"{c}: {w:.4f}")
        print(f"CR: {crs['criteria']:.4f}")

        print("\n2. ΒΑΡΗ ΥΠΟΚΡΙΤΗΡΙΩΝ:")
        print("Οικονομικά θέματα:")
        for s, w in zip(economic_sub, weights["economic"]):
            print(f"{s}: {w:.4f}")
        print(f"CR: {crs['economic']:.4f}")

        print("\nΑπόδοση:")
        for s, w in zip(performance_sub, weights["performance"]):
            print(f"{s}: {w:.4f}")
        print(f"CR: {crs['performance']:.4f}")

        print("\nΚοινωνική αποδοχή:")
        for s, w in zip(social_sub, weights["social"]):
            print(f"{s}: {w:.4f}")
        print(f"CR: {crs['social']:.4f}")

        print("\n3. ΤΕΛΙΚΗ ΒΑΘΜΟΛΟΓΙΑ ΕΝΑΛΛΑΚΤΙΚΩΝ:")
        for alt, score in zip(alternatives, scores):
            print(f"{alt}: {score:.4f}")

    # === Averages ===
    print("\n========== ΜΕΣΟΙ ΟΡΟΙ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ==========\n")
    avg_criteria = np.mean([r["weights"]["criteria"] for r in all_results], axis=0)
    avg_economic = np.mean([r["weights"]["economic"] for r in all_results], axis=0)
    avg_performance = np.mean([r["weights"]["performance"] for r in all_results], axis=0)
    avg_social = np.mean([r["weights"]["social"] for r in all_results], axis=0)
    avg_scores = np.mean([r["scores"] for r in all_results], axis=0)

    print("1. ΜΕΣΟΙ ΟΡΟΙ ΒΑΡΩΝ ΚΡΙΤΗΡΙΩΝ:")
    for c, w in zip(criteria, avg_criteria):
        print(f"{c}: {w:.4f}")

    print("\n2. ΜΕΣΟΙ ΟΡΟΙ ΥΠΟΚΡΙΤΗΡΙΩΝ:")
    print("Οικονομικά θέματα:")
    for s, w in zip(economic_sub, avg_economic):
        print(f"{s}: {w:.4f}")

    print("\nΑπόδοση:")
    for s, w in zip(performance_sub, avg_performance):
        print(f"{s}: {w:.4f}")

    print("\nΚοινωνική αποδοχή:")
    for s, w in zip(social_sub, avg_social):
        print(f"{s}: {w:.4f}")

    print("\n3. ΜΕΣΟΙ ΟΡΟΙ ΒΑΘΜΟΛΟΓΙΩΝ ΕΝΑΛΛΑΚΤΙΚΩΝ:")
    for alt, score in zip(alternatives, avg_scores):
        print(f"{alt}: {score:.4f}")

# Run the full analysis
if __name__ == "__main__":
    ahp_multi_expert(n_experts=10)
