import os
from faker import Faker
from hashfunclab1 import preimage_1, preimage_2, collision_1, collision_2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

output_dir = "results"
os.makedirs(output_dir, exist_ok=True)

fake = Faker('uk_UA')

name = "Сергєєв Андрій Андрійович"
num_runs = 100
results = {
    "Preimage_1": [],
    "Preimage_2": [],
    "Collision_1": [],
    "Collision_2": []
}

for i in range(num_runs):
    msg1 = fake.text(max_nb_chars=150) + " " + name
    msg2 = fake.text(max_nb_chars=150) + " " + name

    if i == 0:
        file_path = os.path.join(output_dir, "output30.txt")
        log_file = open(file_path, "w", encoding="utf-8")
        res_pi1 = preimage_1(msg1, printmsg=True, fi=log_file)
        res_pi2 = preimage_2(msg1, printmsg=True, fi=log_file)
        res_col1 = collision_1(msg2, printmsg=True, fi=log_file)
        res_col2 = collision_2(msg2, printmsg=True, fi=log_file)
        log_file.close()
    else:
        res_pi1 = preimage_1(msg1, printmsg=False)
        res_pi2 = preimage_2(msg1, printmsg=False)
        res_col1 = collision_1(msg2, printmsg=False)
        res_col2 = collision_2(msg2, printmsg=False)
    
    results["Preimage_1"].append(res_pi1)
    results["Preimage_2"].append(res_pi2)
    results["Collision_1"].append(res_col1)
    results["Collision_2"].append(res_col2)
    
    if (i + 1) % 10 == 0:
        print(f"Виконано {i + 1}/{num_runs} ітерацій...")


df = pd.DataFrame(results)
df.index.name = "Запуск №"
df.index += 1

print("\n--- Таблиця результатів ---")
print(df.to_string())
print("-" * 50)

print("\n--- Статистична оцінка складності атак ---")

stats_data = []
for attack_name, data in results.items():
    data_array = np.array(data)
    mean_val = np.mean(data_array)
    var_val = np.var(data_array, ddof=1)
    
    sem = stats.sem(data_array)
    ci = stats.t.interval(0.95, len(data_array)-1, loc=mean_val, scale=sem)
    
    stats_data.append({
        "Атака": attack_name,
        "Середнє (Mean)": mean_val,
        "Дисперсія (Var)": var_val,
        "Довірчий інтервал (95%)": f"({ci[0]:.2f}, {ci[1]:.2f})"
    })
    
df_stats = pd.DataFrame(stats_data)
print(df_stats.to_string(index=False))

excel_path = os.path.join(output_dir, "attack_results.xlsx")
with pd.ExcelWriter(excel_path) as writer:
    df.to_excel(writer, sheet_name="Data")
    df_stats.to_excel(writer, sheet_name="Statistics", index=False)
print(f"\nДані успішно збережено в Excel: {excel_path}")


fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Розподіл складності атак (кількість ітерацій для успіху)', fontsize=16)

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

for ax, (attack_name, data), color in zip(axes.flatten(), results.items(), colors):
    ax.hist(data, bins=20, color=color, alpha=0.7, edgecolor='black')
    ax.set_title(attack_name, fontsize=12)
    ax.set_xlabel('Кількість згенерованих повідомлень')
    ax.set_ylabel('Кількість атак')
    
    mean_val = np.mean(data)
    ax.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Середнє: {mean_val:.0f}')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    fig_single, ax_single = plt.subplots(figsize=(8, 6))
    ax_single.hist(data, bins=20, color=color, alpha=0.7, edgecolor='black')
    ax_single.set_title(attack_name, fontsize=14)
    ax_single.set_xlabel('Кількість згенерованих повідомлень')
    ax_single.set_ylabel('Кількість атак')
    ax_single.axvline(mean_val, color='red', linestyle='dashed', linewidth=2, label=f'Середнє: {mean_val:.0f}')
    ax_single.legend()
    ax_single.grid(axis='y', alpha=0.3)
    
    image_path = os.path.join(output_dir, f"{attack_name}.png")
    fig_single.savefig(image_path, bbox_inches='tight')
    plt.close(fig_single)

print(f"Гістограми успішно збережено в папку '{output_dir}'.")
