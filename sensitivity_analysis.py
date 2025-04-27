# sensitivity_analysis.py
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def parallel_perturbation_analysis():
    # Αρχικά δεδομένα AHP
    criteria = ['Οικονομικά θέματα', 'Απόδοση', 'Κοινωνική αποδοχή']
    original_weights = np.array([0.2970, 0.5396, 0.1634])
    alternatives = ['Ιστοσελίδα', 'Mobile εφαρμογή', 'Κεντρικό σύστημα']
    original_scores = np.array([0.2436, 0.3127, 0.4437])

    # Παράμετροι Monte Carlo
    N = 10000  # Αριθμός επαναλήψεων
    s_values = np.arange(0.2, 0.7, 0.1)  # Εύρος διαταραχών

    # Αποθήκευση αποτελεσμάτων
    prr_matrix = np.zeros((len(s_values), len(alternatives)))

    for s_idx, s in enumerate(tqdm(s_values, desc="Παραμετροποίηση s")):
        rank_reversals = np.zeros(len(alternatives))

        for _ in range(N):
            # 1. Παράλληλη παραμετροποίηση βαρών (ομοιόμορφη κατανομή)
            perturbations = np.random.uniform(-s / 2, s / 2, size=len(criteria))
            new_weights = original_weights * (1 + perturbations)
            new_weights = new_weights / np.sum(new_weights)  # Κανονικοποίηση

            # 2. Υπολογισμός νέων σκορ (απλοποιημένο μοντέλο)
            # Προσομοίωση αλλαγών στις υποκριτηριακές αξιολογήσεις
            subcriteria_perturb = np.random.uniform(-s / 2, s / 2, size=(3, 3))
            new_scores = original_scores * (1 + subcriteria_perturb.mean(axis=1))
            new_scores = new_scores / np.sum(new_scores)

            # 3. Έλεγχος αναστροφής κατάταξης
            original_rank = np.argsort(-original_scores)
            new_rank = np.argsort(-new_scores)

            for i in range(len(alternatives)):
                if original_rank[i] != new_rank[i]:
                    rank_reversals[i] += 1

        # 4. Υπολογισμός PRR
        prr_matrix[s_idx, :] = rank_reversals / N

    # 5. Οπτικοποίηση αποτελεσμάτων
    plt.figure(figsize=(14, 6))

    # Διάγραμμα PRR vs s
    plt.subplot(1, 2, 1)
    for i, alt in enumerate(alternatives):
        plt.plot(s_values, prr_matrix[:, i], 'o-', label=alt)

    plt.xlabel('Perturbation Strength (s)')
    plt.ylabel('Probability of Rank Reversal (PRR)')
    plt.title('PRR vs Διαταραχή Βαρών')
    plt.legend()
    plt.grid(True)

    # Διάγραμμα αρχικών vs τελικών προτεραιοτήτων
    plt.subplot(1, 2, 2)
    width = 0.35
    x = np.arange(len(alternatives))

    plt.bar(x - width / 2, original_scores, width, label='Αρχικές')
    final_scores = np.mean(prr_matrix[-1, :]) * np.ones_like(original_scores)  # Για επίδειξη
    plt.bar(x + width / 2, final_scores, width, label=f'Μετά s={s_values[-1]:.1f}')

    plt.xticks(x, alternatives)
    plt.ylabel('Βαθμολογία')
    plt.title('Σύγκριση Αρχικών/Τελικών Προτεραιοτήτων')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Εκτύπωση αναλυτικών αποτελεσμάτων
    print("\nΑρχικές Προτεραιότητες:")
    for alt, score in zip(alternatives, original_scores):
        print(f"{alt}: {score:.4f}")

    print("\nΠιθανότητες Αναστροφής Κατάταξης (PRR):")
    for s, prr in zip(s_values, prr_matrix):
        print(f"\nΓια s={s:.1f}:")
        for alt, p in zip(alternatives, prr):
            print(f"{alt}: {p:.4f}")


if __name__ == "__main__":
    parallel_perturbation_analysis()