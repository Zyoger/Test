import pandas as pd

meters = pd.read_csv("Показания.csv", sep=";")
meters["Апрель-Май"] = meters["Май"] - meters["Апрель"]
meters["Май-Июнь"] = meters["Июнь"] - meters["Май"]
meters.to_csv("Потребление.csv", index=False, sep=";")

consumption = pd.read_csv("Потребление.csv", sep=";")
consumption["Сумма по квартирам"] = consumption["Апрель-Май"] + consumption["Май-Июнь"]
house_count = pd.pivot_table(consumption[consumption["№ Квартиры"] > 0], values="Сумма по квартирам",
                             index=["Улица", "№ дома"], aggfunc="sum", sort=False)
common_house_counter = pd.pivot_table(consumption[consumption["№ Квартиры"] == 0], values="Сумма по квартирам",
                                      index=["Улица", "№ дома"], aggfunc="sum", sort=False)
house_count["Домовой счетчик"] = common_house_counter["Сумма по квартирам"]

house_count.loc[house_count["Сумма по квартирам"] == house_count["Домовой счетчик"], "Статус показаний"] = "Верно"
house_count.loc[house_count["Сумма по квартирам"] != house_count["Домовой счетчик"], "Статус показаний"] = " Не верно"
print(house_count)
