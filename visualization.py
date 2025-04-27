import matplotlib.pyplot as plt
import seaborn as sns


def show_visualizations():
    # Δεδομένα από την ανάλυση AHP
    criteria = ['Οικονομικά θέματα', 'Απόδοση', 'Κοινωνική αποδοχή']
    criteria_weights = [0.2970, 0.5396, 0.1634]

    subcriteria = {
        'Οικονομικά θέματα': ['Κόστος ανάπτυξης', 'Κόστος συντήρησης'],
        'Απόδοση': ['Αξιοπιστία', 'Ταχύτητα', 'Ασφάλεια δεδομένων'],
        'Κοινωνική αποδοχή': ['Συμβατότητα', 'Ευχρηστία']
    }
    subcriteria_weights = {
        'Οικονομικά θέματα': [0.3333, 0.6667],
        'Απόδοση': [0.5714, 0.2857, 0.1429],
        'Κοινωνική αποδοχή': [0.7500, 0.2500]
    }

    alternatives = ['Ιστοσελίδα', 'Mobile εφαρμογή', 'Κεντρικό σύστημα']
    alternative_scores = [0.2436, 0.3127, 0.4437]

    # 1. Ιεραρχική δομή (Matplotlib)
    plt.figure(figsize=(15, 6))
    plt.title('Ιεραρχική Δομή Απόφασης AHP')

    # Ορισμός θέσεων
    levels = {
        'Αναβάθμιση ΕΣΥ': (0, 2),
        'Οικονομικά θέματα': (-2, 1),
        'Απόδοση': (0, 1),
        'Κοινωνική αποδοχή': (2, 1),
        'Κόστος ανάπτυξης': (-2.5, 0),
        'Κόστος συντήρησης': (-1.5, 0),
        'Αξιοπιστία': (-0.5, 0),
        'Ταχύτητα': (0, 0),
        'Ασφάλεια δεδομένων': (0.5, 0),
        'Συμβατότητα': (1.5, 0),
        'Ευχρηστία': (2.5, 0),
        'Ιστοσελίδα': (-1.5, -1),
        'Εφαρμογή': (0, -1),
        'Κεντρικό σύστημα': (1.5, -1)
    }

    # Συνδέσεις
    connections = [
        ('Αναβάθμιση ΕΣΥ', 'Οικονομικά θέματα'),
        ('Αναβάθμιση ΕΣΥ', 'Απόδοση'),
        ('Αναβάθμιση ΕΣΥ', 'Κοινωνική αποδοχή'),
        ('Οικονομικά θέματα', 'Κόστος ανάπτυξης'),
        ('Οικονομικά θέματα', 'Κόστος συντήρησης'),
        ('Απόδοση', 'Αξιοπιστία'),
        ('Απόδοση', 'Ταχύτητα'),
        ('Απόδοση', 'Ασφάλεια δεδομένων'),
        ('Κοινωνική αποδοχή', 'Συμβατότητα'),
        ('Κοινωνική αποδοχή', 'Ευχρηστία'),
        ('Κόστος ανάπτυξης', 'Ιστοσελίδα'),
        ('Κόστος συντήρησης', 'Ιστοσελίδα'),
        ('Αξιοπιστία', 'Ιστοσελίδα'),
        ('Ταχύτητα', 'Ιστοσελίδα'),
        ('Ασφάλεια δεδομένων', 'Ιστοσελίδα'),
        ('Συμβατότητα', 'Ιστοσελίδα'),
        ('Ευχρηστία', 'Ιστοσελίδα'),
        ('Κόστος ανάπτυξης', 'Εφαρμογή'),
        ('Κόστος συντήρησης', 'Εφαρμογή'),
        ('Αξιοπιστία', 'Εφαρμογή'),
        ('Ταχύτητα', 'Εφαρμογή'),
        ('Ασφάλεια δεδομένων', 'Εφαρμογή'),
        ('Συμβατότητα', 'Εφαρμογή'),
        ('Ευχρηστία', 'Εφαρμογή'),
        ('Κόστος ανάπτυξης', 'Κεντρικό σύστημα'),
        ('Κόστος συντήρησης', 'Κεντρικό σύστημα'),
        ('Αξιοπιστία', 'Κεντρικό σύστημα'),
        ('Ταχύτητα', 'Κεντρικό σύστημα'),
        ('Ασφάλεια δεδομένων', 'Κεντρικό σύστημα'),
        ('Συμβατότητα', 'Κεντρικό σύστημα'),
        ('Ευχρηστία', 'Κεντρικό σύστημα')
    ]

    for start, end in connections:
        xs = [levels[start][0], levels[end][0]]
        ys = [levels[start][1], levels[end][1]]
        plt.plot(xs, ys, 'b-', lw=1.5)

    for node, (x, y) in levels.items():
        plt.text(x, y, node, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.5'))

    plt.axis('off')
    plt.tight_layout()
    plt.show()

    # 2. Βάρη κριτηρίων (Pie Chart)
    plt.pie(criteria_weights, labels=criteria, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    plt.title('Κατανομή Βαρών Κριτηρίων')
    plt.show()

    # 3. Βάρη υποκριτηρίων (Bar Plots)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Βάρη Υποκριτηρίων ανά Κριτήριο')

    colors = sns.color_palette('pastel')
    for ax, (criterion, subs), color in zip(axes, subcriteria.items(), colors):
        weights = subcriteria_weights[criterion]
        sns.barplot(x=subs, y=weights, ax=ax, palette=[color, color])
        ax.set_title(criterion)
        ax.set_ylim(0, 1)
        for p in ax.patches:
            ax.annotate(f"{p.get_height():.2f}",
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 5),
                        textcoords='offset points')

    plt.tight_layout()
    plt.show()

    # 4. Τελική κατάταξη (Plotly Interactive)

    plt.figure(figsize=(8, 6))
    sns.barplot(x=alternatives, y=alternative_scores, palette="Blues_d")

    plt.title('Τελική Κατάταξη Εναλλακτικών Λύσεων')
    plt.xlabel('Εναλλακτικές Λύσεις')
    plt.ylabel('Βαθμολογία')
    for i, v in enumerate(alternative_scores):
        plt.text(i, v + 0.01, f'{v:.2%}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()




if __name__ == "__main__":

    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'DejaVu Sans'
    show_visualizations()