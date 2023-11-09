from procv import fix_tables
import pandas as pd

cols = ["cpf", "liberado"]
cpfs = "1 2 2 3 3 3 4 4 4 4 5 5 5 5 5 6 6 6 6 6 6 7 7 7 7 7 7 7 8 8 8 8 8 8 8 8 9 9 9 9 9 9 9 9 9 10 10 10 11 11 11 12 12 12".split()
liberados = "1000 hsbdcsjhbd 3000 4000,40 5000 ahwgdjgi 7000,70 8000,80 9000,90 10000,100 sdf 12000,120 13000,130 14000,140 15000,150 16000,160 17000,170 18000,180 19000,190 20000,200 21000,210 22000,220 23000,230 24000,240 25000,250 26000,260 27000,270 28000,280 29000,290 30000,300 31000,310 32000,320 33000,330 34000,340 35000,350 36000,360 37000,370 38000,380 39000,390 40000,400 41000,410 42000,420 43000,430 44000,440 45000,450 46000,460 47000,470 48000,480 49000,490 50000,500 51000,510 52000,520 53000,530 54000,540".split()
print(len(cpfs), len(liberados))

d = {
    cols[0]: cpfs,
    cols[1]: liberados
}

saldos = pd.DataFrame(data=d)
# print(type(saldos))
fix_tables(saldos, saldos)