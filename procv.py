import os
import time
import pandas as pd


# saldo_cols = ["cpf", "saldo", "liberado"]
# contato_cols = ["cpf", "telefone", "nome"]

# Set global static variables
DATE = time.strftime('%d %m %Y')
HOUR = time.strftime('%H %M %S')
CWD = os.getcwd()
FOLDERS = ["used", "results", ]
FORMATS = ["csv", "xlsx", "xls", ]
USED = os.path.join(CWD, FOLDERS[0])
RESULTS = os.path.join(CWD, FOLDERS[1])


def find_tables(path=CWD, formats=FORMATS):
    """Find tables in the current working directory"""
    # Get all files in CWD
    files = os.listdir(path)

    # print("\nFiles found:")
    # for f in files:
    #     print(f)
    # print("\n")

    # Create empty list for tables
    saldo_tables = []
    contato_tables = []

    # Iterate through files
    for f in files:
        try:
            # Split file name and format
            f_name, f_format = f.split(".")
        except ValueError:
            continue
        
        # Check if file is a table
        if not f_format in formats:
            continue

        print(f)
        # Append file to tables
        if f_name.lower().startswith("saldo"):
            if f_format == "csv":
                df = pd.read_csv(f)
            elif f_format == "xlsx" or f_format == "xls":
                df = pd.read_excel(f)
            saldo_tables.append(df)
        elif f_name.lower().startswith("contato"):
            if f_format == "csv":
                df = pd.read_csv(f)
            elif f_format == "xlsx" or f_format == "xls":
                df = pd.read_excel(f)
            contato_tables.append(df)
        
    if not len(saldo_tables): 
        print(f"\nNo BANCO tables found\n")
    
    if not len(contato_tables):
        print(f"\nNo CONTATO tables found\n")
                

    # Return tables
    return saldo_tables, contato_tables


def create_dfs(saldos:list[pd.DataFrame], contatos:list[pd.DataFrame]):
    saldo_cols = ["cpf", "saldo", "liberado"]
    contato_cols = ["cpf", "telefone", "nome"]
    saldos_df = pd.DataFrame(columns=saldo_cols)
    contatos_df = pd.DataFrame(columns=contato_cols)
    
    for s in saldos:
        # Concatenate the entire DataFrame along columns
        saldos_df = pd.concat([saldos_df, s], axis=0, ignore_index=True)
    for c in contatos:
        # Concatenate the entire DataFrame along columns
        contatos_df = pd.concat([contatos_df, c], axis=0, ignore_index=True)

    """
    # Create file name
    f_name_s = f"S {DATE} {HOUR}.xlsx"
    f_name_c = f"C {DATE} {HOUR}.xlsx"
    # Write table
    saldos_df.to_excel(f_name_s, index=False)
    contatos_df.to_excel(f_name_c, index=False)
    """
    # print(type(saldos_df), type(contatos_df))
    return saldos_df, contatos_df

# print(find_tables())

def table_drop_duplicates(df_list:list[pd.DataFrame],
                    keep="first",
                    ignore_index=True,
                    subset=["cpf"],
                    inplace=False,
                    ):
    """Drop duplicates from a list of DataFrames"""
    for df in df_list:
        df = df.drop_duplicates(subset=subset,
                                keep=keep,
                                ignore_index=ignore_index,
                                inplace=inplace,
                                )
    
    return df_list


def table_dropna(df_list:list[pd.DataFrame], how="any", axis=0):
    """Drop NaN values from a list of DataFrames"""
    for df in df_list:
        df = df.dropna(how=how, axis=axis)
    
    return df_list


# Function to convert non-numeric values to NaN and keep numeric values
def to_numeric_with_commas(value):
    value = str(value)
    try:
        # Try converting the value to float
        float(value.replace('.', '').replace(',', '.'))
        # print(value)
        return value
    except (ValueError, AttributeError):
        # If conversion fails, return NaN
        return pd.NA
    

def fix_tables(saldos, contatos):
    """Fix tables"""
    v = 5
    p = False # Print tables in the process of fixing

    # if p:
    print("\nSALDO ORIGINAL")
    print(len(saldos["cpf"]))
    print("Saldo head:")
    print(saldos.head(v))
    print("Saldo foot:")
    print(saldos.tail(v))

    saldos, contatos = table_dropna([saldos, contatos])

    if p:
        print("\nSALDO DROPNA")
        print(len(saldos["cpf"]))
        print("Saldo head:")
        print(saldos.head(v))
        print("Saldo foot:")
        print(saldos.tail(v))
    
    saldos, contatos = table_drop_duplicates([saldos, contatos])

    if p:
        print("\nSALDO DUPLICATES")
        print(len(saldos["cpf"]))
        print("Saldo head:")
        print(saldos.head(v))
        print("Saldo foot:")
        print(saldos.tail(v))
    
    # print("\n LIBERADO")
    # print(saldos["liberado"].head())
    saldos['liberado'] = saldos['liberado'].apply(to_numeric_with_commas)
    # print(saldos["liberado"].head())
    # print("\n")
    saldos = saldos.dropna(subset=["liberado"])

    if p:
        print("\nSALDO APPLY LIBERADO")
        print(len(saldos["cpf"]))
        print("Saldo head:")
        print(saldos.head(v))
        print("Saldo foot:")
        print(saldos.tail(v))

    return saldos, contatos


def procv(saldos:pd.DataFrame, contatos:pd.DataFrame):
    """Apply procv to the tables"""

    # Columns in the desired order
    match_cols = ["cpf", "nome", "telefone", "saldo", "liberado"]

    # Print the saldos and contatos DataFrames before merging
    print("\nSaldos DataFrame PROCV:")
    print(saldos.head())
    print("Contatos DataFrame:")
    print(contatos.head())
    print("\n")
    # Merge DataFrames based on the "cpf" column and select columns in the specified order
    match = pd.merge(saldos, contatos, on="cpf", how="left")[match_cols]
    match = match.drop_duplicates(keep="first",ignore_index=True,subset=["cpf"],inplace=False)

    """
    # Saldo: cpf, saldo, liberado
    s_cpf = saldos["cpf"]
    s_saldo = saldos["saldo"]
    s_liberado = saldos["liberado"]

    # Contato: cpf, telefone, nome
    c_cpf = contatos["cpf"]
    c_telefone = contatos["telefone"]
    c_nome = contatos["nome"]
    """
    return match


def create_folders():
    """Create folder to store used tables"""
    for f in [USED, RESULTS]:    
        create_dir(f)
    
    # Create folder for current date
    f_name = f"{DATE} {HOUR}"
    create_dir(
        current_folder := os.path.join(USED, f_name)
        )
    
    return current_folder


def create_dir(folder):
    # Check if folder exists'
    if not os.path.exists(folder):
        # Create folder
        os.mkdir(folder)


def move_tables(tables:list, folder:str):
    """Move tables to the used folder"""
    # Move tables
    for t in tables:
        os.rename(
            os.path.join(CWD, t),
            os.path.join(folder, t)
        )


def create_result(match:pd.DataFrame, folder:str):
    """Create result table"""

    # Create file name
    f_name = f"RESULTADO {DATE} {HOUR}.xlsx"

    # Create file path
    f_path = os.path.join(folder, f_name)

    # Write table
    match.to_excel(f_path, index=False)

    print("\nRESULTADO:")
    print(match.head(7))
    print("...          ....            ....")
    print(match.tail(7))
    print("\n")



def main():
    print("Starting...")
    print("\n")
    saldos_l, contatos_l = find_tables()
    print("\n")
    if not len(saldos_l) or not len(contatos_l):
        print("No tables found")
        return
    
    saldos, contatos = create_dfs(saldos_l, contatos_l)
    # Print the saldos and contatos DataFrames before merging
    # Fix tables
    saldos, contatos = fix_tables(saldos, contatos)

    print("\nSaldos DataFrame FIX:")
    print(saldos.head())
    print("Contatos DataFrame:")
    print(contatos.head())
    print("\n")
    match = procv(saldos, contatos)
    current_folder = create_folders()
    
    tables_found = []
    for f in os.listdir(CWD):
        try:
            # Split file name and format
            f_name, f_format = f.split(".")
        except ValueError:
            continue
        
        # Check if file is a table
        if not f_format in FORMATS:
            continue
        else:
            tables_found.append(f)

    move_tables(tables_found, current_folder)
    create_result(match, RESULTS)


if __name__ == "__main__":
    main()
