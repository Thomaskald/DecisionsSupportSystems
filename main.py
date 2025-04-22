import numpy as np


def calculate_weights(matrix):
    """Υπολογισμός βαρών με μέσο όρο κανονικοποιημένων στηλών"""
    normalized = matrix / matrix.sum(axis=0)
    return normalized.mean(axis=1)


def calculate_cr(matrix):
    """Υπολογισμός Consistency Ratio με βελτιωμένη ακρίβεια"""
    n = matrix.shape[0]
    if n <= 2: return 0.0  # Για πίνακες μικρότερους από 3x3

    weights = calculate_weights(matrix)
    weighted_sum = np.dot(matrix, weights)
    lambda_max = np.mean(weighted_sum / weights)

    CI = (lambda_max - n) / (n - 1)
    RI = {3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}.get(n, 0.58)
    CR = CI / RI if RI != 0 else 0.0

    return CR


def ahp_analysis():
    # 1. Ιεραρχία κριτηρίων
    criteria = ['Οικονομικά θέματα', 'Απόδοση', 'Κοινωνική αποδοχή']
    subcriteria = {
        'Οικονομικά θέματα': ['Κόστος ανάπτυξης', 'Κόστος συντήρησης'],
        'Απόδοση': ['Αξιοπιστία', 'Ταχύτητα', 'Ασφάλεια δεδομένων'],
        'Κοινωνική αποδοχή': ['Συμβατότητα', 'Ευχρηστία']
    }
    alternatives = ['Ιστοσελίδα', 'Mobile εφαρμογή', 'Κεντρικό σύστημα']

    # 2. Πίνακες σύγκρισης (συνεπείς τιμές)
    # Κριτήρια
    criteria_matrix = np.array([
        [1, 1 / 3, 1 / 2],
        [3, 1, 2],
        [2, 1 / 2, 1]
    ])

    # Υποκριτήρια
    economic_matrix = np.array([[1, 1 / 2], [2, 1]])
    performance_matrix = np.array([[1, 2, 4], [1 / 2, 1, 2], [1 / 4, 1 / 2, 1]])
    social_matrix = np.array([[1, 3], [1 / 3, 1]])

    # Εναλλακτικές
    dev_cost_matrix = np.array([[1, 1 / 2, 1 / 3], [2, 1, 1 / 2], [3, 2, 1]])
    maint_cost_matrix = np.array([[1, 1 / 3, 1 / 5], [3, 1, 1 / 2], [5, 2, 1]])
    reliability_matrix = np.array([[1, 2, 3], [1 / 2, 1, 2], [1 / 3, 1 / 2, 1]])
    speed_matrix = np.array([[1, 1 / 2, 1 / 3], [2, 1, 1 / 2], [3, 2, 1]])
    security_matrix = np.array([[1, 3, 5], [1 / 3, 1, 2], [1 / 5, 1 / 2, 1]])
    compat_matrix = np.array([[1, 2, 3], [1 / 2, 1, 2], [1 / 3, 1 / 2, 1]])
    usability_matrix = np.array([[1, 1 / 3, 1 / 5], [3, 1, 1 / 2], [5, 2, 1]])

    # 3. Υπολογισμοί
    # Κριτήρια
    criteria_weights = calculate_weights(criteria_matrix)
    cr_criteria = calculate_cr(criteria_matrix)

    # Υποκριτήρια
    economic_weights = calculate_weights(economic_matrix)
    performance_weights = calculate_weights(performance_matrix)
    social_weights = calculate_weights(social_matrix)

    cr_economic = calculate_cr(economic_matrix)
    cr_performance = calculate_cr(performance_matrix)
    cr_social = calculate_cr(social_matrix)

    # Εναλλακτικές
    dev_cost_weights = calculate_weights(dev_cost_matrix)
    maint_cost_weights = calculate_weights(maint_cost_matrix)
    reliability_weights = calculate_weights(reliability_matrix)
    speed_weights = calculate_weights(speed_matrix)
    security_weights = calculate_weights(security_matrix)
    compat_weights = calculate_weights(compat_matrix)
    usability_weights = calculate_weights(usability_matrix)

    # 4. Τελική βαθμολογία εναλλακτικών
    alternative_scores = np.zeros(3)
    for i in range(3):
        # Οικονομικά
        economic = criteria_weights[0] * (
                    economic_weights[0] * dev_cost_weights[i] + economic_weights[1] * maint_cost_weights[i])
        # Απόδοση
        performance = criteria_weights[1] * (performance_weights[0] * reliability_weights[i] +
                                             performance_weights[1] * speed_weights[i] +
                                             performance_weights[2] * security_weights[i])
        # Κοινωνικά
        social = criteria_weights[2] * (
                    social_weights[0] * compat_weights[i] + social_weights[1] * usability_weights[i])

        alternative_scores[i] = economic + performance + social

    # 5. Εμφάνιση αποτελεσμάτων
    print("ΑΝΑΛΥΣΗ AHP ΓΙΑ ΨΗΦΙΑΚΕΣ ΠΛΑΤΦΟΡΜΕΣ ΕΣΥ\n")

    print("1. ΒΑΡΗ ΚΡΙΤΗΡΙΩΝ:")
    for crit, weight in zip(criteria, criteria_weights):
        print(f"{crit}: {weight:.4f}")
    print(f"\nConsistency Ratio (CR): {cr_criteria:.4f} ({'Συνεπής' if cr_criteria < 0.1 else 'Μη συνεπής'})")

    print("\n2. ΒΑΡΗ ΥΠΟΚΡΙΤΗΡΙΩΝ:")
    print("Οικονομικά θέματα:")
    for sub, weight in zip(subcriteria['Οικονομικά θέματα'], economic_weights):
        print(f"  {sub}: {weight:.4f}")
    print(f"  CR: {cr_economic:.4f}")

    print("\nΑπόδοση:")
    for sub, weight in zip(subcriteria['Απόδοση'], performance_weights):
        print(f"  {sub}: {weight:.4f}")
    print(f"  CR: {cr_performance:.4f}")

    print("\nΚοινωνική αποδοχή:")
    for sub, weight in zip(subcriteria['Κοινωνική αποδοχή'], social_weights):
        print(f"  {sub}: {weight:.4f}")
    print(f"  CR: {cr_social:.4f}")

    print("\n3. ΤΕΛΙΚΗ ΒΑΘΜΟΛΟΓΙΑ ΕΝΑΛΛΑΚΤΙΚΩΝ:")
    ranked = sorted(zip(alternatives, alternative_scores), key=lambda x: -x[1])
    for i, (alt, score) in enumerate(ranked, 1):
        print(f"{i}. {alt}: {score:.4f}")


if __name__ == "__main__":
    ahp_analysis()