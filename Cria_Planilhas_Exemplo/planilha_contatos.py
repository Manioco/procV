import pandas as pd

cols = ["cpf", "nome", "telefone"]
df = pd.DataFrame(columns=cols)

nomes = ["João", "Maria", "José", "Pedro", "Ana"]
telefones = ["99999-1111", "99999-2222", "99999-3333", "99999-4444", "99999-5555"]
cpfs = ["111.111.111-11", "222.222.222-22", "333.333.333-33", "444.444.444-44", "555.555.555-55"]

for i in range(len(nomes)):
    df.loc[i] = [cpfs[i], nomes[i], telefones[i]]

df.to_excel("contatos2.xlsx", index=False)
