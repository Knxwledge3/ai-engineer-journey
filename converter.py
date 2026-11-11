USD_RATE = 447 
EUR_RATE = 500
text = input("Cумма в тенге: ")
try:
    amount = float(text)
except ValueError:
    print("Нужно ввести число")
if amount < 0:
    print("Сумма не может быть отрицательной")
    exit()
currency = input("Во что конвертировать (USD / EUR): ")
if currency =="USD":
    result = amount / USD_RATE
elif currency == "EUR":
    result = amount / EUR_RATE
else:
    print("Такой валюты нет")
    exit()
print(f"{amount} тенге = {round(result, 2)} {currency}")