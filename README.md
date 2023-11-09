# PROCV?

### This program grab the cpfs and concatenate the values of the other columns to a single file.

*This is a program to solve a very specific problem in my daily routine at my current job.
We have this files with contacts and a program to validate some data, then I made this to simplify the usage of excel.*

***With the result, we can visualize the info off a client in one file with almost no work required.***

## HOW TO USE:

- You need to set both files (in one of those formats: .csv, .xls, .xlsx) (Can be different formats, but in this range)
- File names **must to be** "contato" for contacts and "saldo" for the other.
- **saldo column names:** ["cpf", "saldo", "liberado"]
- **contato column names:** ["cpf", "telefone", "nome"]
- With the files in place, just run procv.exe or procv.py and its done

#### WHERE THE FILES GO?

- the excel files go in the same folder as the procv.py or procv.exe

#### After the execution, what I do?

- Inside of /used will be created a new file with the time of execution in the name
- Inside of /result will be the file with the result of course.

**RESULT FORMAT:** .xlsx
**RESULT COLS:** ["cpf", "nome", "telefone", "saldo", "liberado"]
