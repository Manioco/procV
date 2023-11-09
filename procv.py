import os
import time
import pandas as pd


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
    return create_dfs(saldo_tables, contato_tables)


def create_dfs(saldos:list[pd.DataFrame], contatos:list[pd.DataFrame]):
    saldo_cols = ["cpf", "saldo", "liberado"]
    contato_cols = ["cpf", "telefone", "nome"]
    saldos_df = pd.DataFrame(columns=saldo_cols)
    contatos_df = pd.DataFrame(columns=contato_cols)
    
    for s in saldos:
        # Find each column
        cpf = s["cpf"]
        saldo = s["saldo"]
        nome = s["liberado"]

        # concat
        saldos_df = pd.concat([saldos_df, cpf, saldo, nome], axis=1)
    
    for c in contatos:
        # Find each column
        cpf = c["cpf"]
        telefone = c["telefone"]
        nome = c["nome"]

        # concat
        contatos_df = pd.concat([contatos_df, cpf, telefone, nome], axis=1)

    return saldos_df, contatos_df

# print(find_tables())


def procv(saldo:pd.DataFrame, contato:pd.DataFrame):
    """Apply procv to the tables"""

    match_cols = ["cpf", "nome", "telefone", "saldo", "liberado"]
    match = pd.DataFrame(columns=match_cols)

    # Merge tables
    match = pd.merge(saldo, contato, on="cpf", how="left")

    # Drop duplicates
    match.drop_duplicates(subset="cpf", keep="first", inplace=True)

    # Drop columns
    match.drop(columns=["Nome_x", "Nome_y"], inplace=True)

    # Rename columns
    match.rename(columns={"cpf":"cpf", "saldo":"saldo", "telefone":"telefone"}, inplace=True)

    # Return merged table
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

    # Create excel writer
    writer = pd.ExcelWriter(f_path)

    # Write table
    match.to_excel(writer, index=False)

    # Save file
    writer.save()


def main():
    print("Starting...")
    print("\n")
    saldos, contatos = find_tables()
    print("\n")
    if not len(saldos) or not len(contatos):
        print("No tables found")
        return
    
    match = procv(saldos, contatos)
    current_folder = create_folders()
    move_tables([saldos, contatos], current_folder)
    create_result(match, RESULTS)


if __name__ == "__main__":
    main()
