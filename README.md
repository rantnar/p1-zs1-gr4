# p1-zs1-gr4 - Obliczanie różnic kursowych.

## Wymagania

- Python 3.6 lub nowszy
- pip

## Instalacja

1. Sklonuj repozytorium do lokalnego katalogu.
2. Przejdź do katalogu projektu.
3. Zainstaluj wymagane pakiety za pomocą pip:

```sh
pip install -r requirements.txt
```
## Uruchamianie
```sh
python main-rich.py
```
### Wyjście z programu
W tej chwili z programu wychodzimy zamykając terminal, albo wysyłając sygnał SIGINT ```CTRL+C```

### Szkielet pliku JSON, który reprezentuje fakturę
```json
[{
  "invoice_number": "string",
  "value": "number",
  "currency": "string",
  "issue_date": "string (format YYYY-MM-DD)",
  "payments": [
    {
      "date": "string (format YYYY-MM-DD)",
      "value": "number"
    }
    // Może być więcej obiektów płatności
  ]
}]
```
### Użytkownicy windows muszą upewnić się, że mają zainstalowany pip, oraz znajduje się on w PATH. Rozwiązaniem może być instalacja python wprost z Microsoft Store.
