import pandas as pd

cols = ["saldo_lib", "cpf", "saldo"]
df = pd.DataFrame(columns=cols)

cpfs = ["111.111.111-11", "222.222.222-22", "333.333.333-33", "444.444.444-44", "555.555.555-55"]
saldos = [1000, 2000, 3000, 4000, 5000]
saldos_lib = [700, 1000, 2000, 3000, 4000]

for i in range(len(cpfs)):
    df.loc[i] = [saldos_lib[i], cpfs[i], saldos[i]]

df.to_excel("banco2.xlsx", index=False)
