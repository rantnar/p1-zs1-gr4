
# Dokumentacja techniczna

## Spis treści
1. [Opis ogólny](#opis-ogólny)
-  [Instrukcje obsługi programu pomocniczego](#instrukcje_obsługi_programu_pomocniczego)
2. [Funkcje](#funkcje)
   - [Funkcja `get_cached_data(currency, date)`](#get_cached_data)
   - [Funkcja `get_data_from_api(currency, date)`](#get_data_from_api)
   - [Funkcja `save_data_to_cache(currency, date, rate)`](#save_data_to_cache)
   - [Funkcja `get_exchange_rate_for_date(currency, date)`](#get_exchange_rate_for_date)
   - [Funkcja `get_exchange_rate(currency, date_issue, date_payment)`](#get_exchange_rate)
   - [Funkcja `calculate_exchange_rate_difference(invoice_amount, currency, date_issue, date_payment)`](#calculate_exchange_rate_difference)
   - [Funkcja `save_invoice_data(invoice_data, file_path='data.json')`](#save_invoice_data)
   - [Funkcja `save_single_invoice_to_file(invoice_data)`](#save_single_invoice_to_file)
   - [Funkcja `validate_invoice_number(existing_invoices)`](#validate_invoice_number)
   - [Funkcja `validate_value()`](#validate_value)
   - [Funkcja `validate_currency()`](#validate_currency)
   - [Funkcja `validate_date(prompt, earliest_date=None)`](#validate_date)
   - [Funkcja `validate_payment_value()`](#validate_payment_value)
   - [Funkcja `get_invoice_data()`](#get_invoice_data)
   - [Funkcja `format_invoice_to_display(invoice)`](#format_invoice_to_display)
   - [Funkcja `display_results(invoices)`](#display_results)
   - [Funkcja `process_invoice(invoice_data)`](#process_invoice)
   - [Funkcja `print_error(msg)`](#print_error)
   - [Funkcja `print_warning(msg)`](#print_warning)
   - [Funkcja `validate_database(data, required_keys=None)`](#validate_database)
   - [Funkcja `run_interactive_mode()`](#run_interactive_mode)
   - [Funkcja `run_batch_mode()`](#run_batch_mode)
   - [Funkcja `display_menu()`](#display_menu)
   - [Funkcja `exit_program()`](#exit_program)
   - [Funkcja `main()`](#main)
3. [Przykłady użycia programu i formatu pliku](#przykłady-użycia-programu-i-formatu-pliku)
4. [Informacje końcowe](#informacje-końcowe)

## Opis ogólny

Program służy do obliczania różnic kursowych walut oraz zarządzania danymi faktur. Pozwala użytkownikowi wprowadzać dane faktur interaktywnie lub za pomocą pliku wsadowego, a następnie wyświetlać wyniki w czytelnej formie.

Funkcje programu obejmują:

1. **Walidacja danych faktur**: Funkcja `validate_database()` służy do sprawdzania poprawności kluczy w danych faktur, zapewniając kompletność i poprawność danych przed ich przetworzeniem.

2. **Tryb interaktywny**: Funkcja `run_interactive_mode()` umożliwia użytkownikowi wprowadzanie danych faktur w trybie interaktywnym, gdzie każdy krok jest wykonywany w czasie rzeczywistym.

3. **Tryb wsadowy**: Funkcja `run_batch_mode()` umożliwia użytkownikowi wczytywanie danych faktur z pliku wsadowego, co pozwala na przetwarzanie danych faktur w trybie wsadowym.

4. **Formatowanie danych faktur do wyświetlenia**: Funkcja `format_invoice_to_display()` formatuje dane faktur do czytelnej prezentacji, wyświetlając kursy walut, różnice kursowe oraz status płatności.

5. **Wyświetlanie wyników**: Funkcja `display_results()` prezentuje wyniki obliczeń w czytelnej formie tabelarycznej, zawierającej informacje o numerze faktury, walucie, wartości, kursach walut, różnicach kursowych oraz statusie płatności.

6. **Obsługa błędów**: Program zawiera mechanizmy obsługi błędów, które informują użytkownika o ewentualnych problemach podczas wprowadzania danych lub przetwarzania faktur.

Program został zaprojektowany w sposób umożliwiający łatwe zarządzanie danymi faktur oraz wygodne przeglądanie wyników obliczeń, co sprawia, że jest użytecznym narzędziem dla osób zajmujących się obsługą finansową oraz analizą kursów walut.

Oto dokumentacja techniczna dla instrukcji obsługi programu pomocniczego:

### Instrukcje obsługi programu pomocniczego

Po uruchomieniu programu, możesz skorzystać z opcji "-h" lub "--help", aby uzyskać instrukcje dotyczące użytkowania. Poniżej znajdziesz opis instrukcji:

1. **Wprowadź dane, gdy zostaniesz o to poproszony:**
   - Program może poprosić Cię o wprowadzenie danych, które są niezbędne do wykonania określonych operacji.

2. **Postępuj zgodnie z wyświetlanymi komunikatami:**
   - Program będzie wyświetlać komunikaty dotyczące kolejnych kroków lub informacje zwrotne dotyczące przeprowadzanych operacji. Postępuj zgodnie z nimi, aby korzystać z programu efektywnie.

3. **Program zamyka się przy użyciu skrótu ctrl+c:**
   - Aby zakończyć działanie programu, możesz użyć standardowego skrótu klawiszowego "Ctrl+C", który spowoduje jego zakończenie.

4. **Pliki pojedynczych faktur są przechowywane w folderze "data/nr faktury.json":**
   - Program przechowuje pliki pojedynczych faktur w folderze o nazwie "data", gdzie każda faktura ma swój własny plik JSON o nazwie zgodnej z jej numerem.

5. **Główna baza danych to plik "data.json":**
   - Główne dane programu przechowywane są w pliku o nazwie "data.json", który zawiera informacje o fakturach oraz inne istotne dane.

6. **W razie problemów z uruchomieniem proszę przeczytać plik README.md:**
   - W przypadku problemów z uruchomieniem programu lub potrzeby uzyskania dodatkowych informacji, zaleca się zapoznanie się z plikiem README.md, który zawiera informacje dotyczące konfiguracji i uruchomienia programu.


## Funkcje


### Funkcja `get_cached_data(currency, date)`

Opis:
- Odczytuje dane z pliku 'cache.json' dla danej waluty i daty, zwracając je, jeśli istnieją.

Argumenty:
- `currency`: (str) Kod waluty, dla której pobierane są dane.
- `date`: (str) Data w formacie 'YYYY-MM-DD', dla której pobierane są dane.

Zwracane wartości:
- `data`: (dict or None) Dane kursowe dla podanej waluty i daty, jeśli istnieją w pamięci podręcznej, w przeciwnym razie None.

### Funkcja `get_data_from_api(currency, date)`

Opis:
- Pobiera dane z API Narodowego Banku Polskiego (NBP) dla podanej waluty i daty, próbując do 7 dni wstecz, zwracając kurs średni waluty z danego dnia.

Argumenty:
- `currency`: (str) Kod waluty, dla której pobierane są dane.
- `date`: (str) Data w formacie 'YYYY-MM-DD', dla której pobierane są dane.

Zwracane wartości:
- `mid`: (float) Średni kurs wymiany waluty dla podanej daty.

### Funkcja `save_data_to_cache(currency, date, rate)`

Opis:
- Zapisuje dane do pamięci podręcznej (cache) w pliku JSON dla podanej waluty, daty i kursu.

Argumenty:
- `currency`: (str) Kod waluty, dla której zapisywane są dane.
- `date`: (str) Data w formacie 'YYYY-MM-DD', dla której zapisywane są dane.
- `rate`: (float) Kurs wymiany waluty dla podanej daty.

Zwracane wartości:
- Brak.

### Funkcja `get_exchange_rate_for_date(currency, date)`

Opis:
- Pobiera kurs wymiany waluty dla podanej daty z pamięci podręcznej lub z API NBP, a następnie zapisuje go do pamięci podręcznej.

Argumenty:
- `currency`: (str) Kod waluty, dla której pobierany jest kurs wymiany.
- `date`: (str) Data w formacie 'YYYY-MM-DD', dla której pobierany jest kurs wymiany.

Zwracane wartości:
- `rate`: (float) Kurs wymiany waluty dla podanej daty.

Oto dokumentacja techniczna dla każdej z funkcji:

### Funkcja `get_exchange_rate(currency, date_issue, date_payment)`

Opis:
- Pobiera kurs wymiany waluty dla podanych dat daty emisji i daty płatności. Jeśli waluta to PLN, zwraca kursy 1:1. W przeciwnym razie pobiera kursy dla daty emisji i daty płatności.

Argumenty:
- `currency`: (str) Kod waluty, dla której pobierany jest kurs wymiany.
- `date_issue`: (str) Data emisji faktury w formacie 'YYYY-MM-DD'.
- `date_payment`: (str) Data płatności faktury w formacie 'YYYY-MM-DD'.

Zwracane wartości:
- `issue_rate`: (float) Kurs wymiany waluty dla daty emisji.
- `payment_rate`: (float) Kurs wymiany waluty dla daty płatności.

### Funkcja `calculate_exchange_rate_difference(invoice_amount, currency, date_issue, date_payment)`

Opis:
- Funkcja obliczająca różnicę kursową na podstawie podanych parametrów, zwraca różnicę kursową.

Argumenty:
- `invoice_amount`: (str) Kwota faktury.
- `currency`: (str) Kod waluty faktury.
- `date_issue`: (str) Data emisji faktury w formacie 'YYYY-MM-DD'.
- `date_payment`: (str) Data płatności faktury w formacie 'YYYY-MM-DD'.

Zwracane wartości:
- `exchange_rate_difference`: (float) Różnica kursowa pomiędzy datami emisji i płatności faktury.

### Funkcja `save_invoice_data(invoice_data, file_path='data.json')`

Opis:
- Funkcja zapisująca dane faktury do pliku JSON.

Argumenty:
- `invoice_data`: (dict) Dane faktury do zapisania.
- `file_path`: (str) Ścieżka do pliku JSON, domyślnie 'data.json'.

Zwracane wartości:
- Brak.

### Funkcja `save_single_invoice_to_file(invoice_data)`

Opis:
- Funkcja zapisująca dane faktury do pojedynczego pliku JSON.

Argumenty:
- `invoice_data`: (dict) Dane faktury do zapisania.

Zwracane wartości:
- Brak.

### Funkcja `validate_invoice_number(existing_invoices)`

Opis:
- Funkcja walidująca numer faktury, zwraca poprawny numer faktury.

Argumenty:
- `existing_invoices`: (list) Lista istniejących faktur.

Zwracane wartości:
- `invoice_number`: (str) Poprawny numer faktury.

### Funkcja `validate_value()`

Opis:
- Funkcja walidująca wartość faktury, zwraca poprawną wartość faktury.

Argumenty:
- Brak.

Zwracane wartości:
- `value`: (float) Poprawna wartość faktury.

Oto dokumentacja techniczna dla nowych funkcji:

### Funkcja `validate_currency()`

Opis:
- Funkcja walidująca walutę, zwraca poprawną walutę.

Argumenty:
- Brak.

Zwracane wartości:
- `currency`: (str) Poprawny kod waluty.

### Funkcja `validate_date(prompt, earliest_date=None)`

Opis:
- Waliduje datę wprowadzoną przez użytkownika w formacie YYYY-MM-DD.

Argumenty:
- `prompt`: (str) Komunikat wyświetlany użytkownikowi, proszący o wprowadzenie daty.
- `earliest_date` (opcjonalny): (str) Najwcześniejsza akceptowalna data. Jeśli podana, data wprowadzona przez użytkownika nie może być wcześniejsza niż `earliest_date`.

Zwracane wartości:
- `date`: (datetime) Data w formacie datetime.

### Funkcja `validate_payment_value()`

Opis:
- Waliduje kwotę płatności wprowadzoną przez użytkownika.

Argumenty:
- Brak.

Zwracane wartości:
- `payment_value`: (float) Kwota płatności jako wartość float.

### Funkcja `get_invoice_data()`

Opis:
- Funkcja pobierająca dane faktury od użytkownika, zwraca słownik z danymi faktury.

Argumenty:
- Brak.

Zwracane wartości:
- `invoice_data`: (dict) Słownik zawierający dane faktury.

Oto dokumentacja techniczna dla nowych funkcji:

### Funkcja `format_invoice_to_display(invoice)`

Opis:
- Formatuje dane faktury do wyświetlenia.

Argumenty:
- `invoice`: (dict) Słownik zawierający dane faktury.

Zwracane wartości:
- `issue_rate`: (float) Kurs waluty na dzień wystawienia faktury.
- `payment_dates_rates`: (list) Lista dat płatności wraz z kursami walut.
- `differences`: (list) Lista różnic między kursami walut.
- `payment_status`: (str) Status płatności (NADPŁATA, NIEDOPŁATA, OK).
- `payment_status_value`: (float) Wartość statusu płatności.
- `total_difference_str`: (str) Łączna różnica między kursami walut.

### Funkcja `display_results(invoices)`

Opis:
- Funkcja wyświetlająca wyniki w tabeli.

Argumenty:
- `invoices`: (list) Lista faktur do wyświetlenia.

Zwracane wartości:
- Brak.

### Funkcja `process_invoice(invoice_data)`

Opis:
- Przetwarza dane faktury, oblicza różnice kursów walut i zwraca wyniki.

Argumenty:
- `invoice_data`: (dict) Słownik zawierający dane faktury.

Zwracane wartości:
- `total_payments`: (float) Suma płatności.
- `results`: (list) Lista krotek zawierających wyniki dla każdej płatności.

### Funkcja `print_error(msg)`

Opis:
- Funkcja wyświetlająca komunikat o błędzie.

Argumenty:
- `msg`: (str) Komunikat błędu.

Zwracane wartości:
- Brak.

### Funkcja `print_warning(msg)`

Opis:
- Funkcja wyświetlająca komunikat o ostrzeżeniu.

Argumenty:
- `msg`: (str) Komunikat ostrzeżenia.

Zwracane wartości:
- Brak.

Oto dokumentacja techniczna dla nowych funkcji:

### Funkcja `validate_database(data, required_keys=None)`

Opis:
- Waliduje klucze w danych faktury.

Argumenty:
- `data`: (list) Lista słowników zawierających dane faktur.
- `required_keys`: (list) Lista kluczy wymaganych w danych faktury. Domyślnie to: ['invoice_number', 'value', 'currency', 'issue_date', 'payments'].

Zwracane wartości:
- `missing_keys`: (list) Lista kluczy brakujących w danych faktury.

### Funkcja `run_interactive_mode()`

Opis:
- Funkcja uruchamiająca tryb interaktywny.

Argumenty:
- Brak.

Zwracane wartości:
- Brak.

### Funkcja `run_batch_mode()`

Opis:
- Funkcja uruchamiająca tryb wsadowy.

Argumenty:
- Brak.

Zwracane wartości:
- Brak.

### Funkcja `display_menu()`

Opis:
- Funkcja wyświetlająca menu wyboru trybu pracy.

Argumenty:
- Brak.

Zwracane wartości:
- Brak.

### Funkcja `exit_program()`

Opis:
- Funkcja kończąca działanie programu.

Argumenty:
- Brak.

Zwracane wartości:
- Brak.

### Funkcja `main()`

Opis:
- Funkcja główna programu.

Argumenty:
- Brak.

Zwracane wartości:
- Brak.


### Przykłady użycia programu i formatu pliku

Dokumentacja zawiera przykłady użycia programu, które pomagają użytkownikom zrozumieć, jak korzystać z jego funkcji w praktyce. Każdy przykład jest szczegółowo opisany i zawiera kroki niezbędne do wykonania określonych zadań za pomocą programu.

Na przykład, aby obliczyć różnicę kursową dla konkretnej faktury, użytkownik może użyć funkcji `calculate_exchange_rate_difference()` podając numer faktury, wartość, walutę, datę wystawienia oraz datę płatności. Poniżej przedstawiony jest przykład użycia tej funkcji:

```python
invoice_amount = 1000.00  # Wartość faktury
currency = 'USD'          # Waluta
date_issue = '2023-05-15' # Data wystawienia faktury
date_payment = '2023-06-01'  # Data płatności

difference = calculate_exchange_rate_difference(invoice_amount, currency, date_issue, date_payment)
print(f"Różnica kursowa dla faktury wynosi: {difference} PLN")
```

Ponadto, dokumentacja przedstawia format pliku danych wejściowych lub wyjściowych, który jest akceptowany lub generowany przez program. Poprawne zrozumienie tego formatu jest kluczowe dla prawidłowego korzystania z programu oraz przetwarzania danych zgodnie z jego oczekiwaniami.

Przykład użycia programu oraz format pliku są prezentowane w sposób przejrzysty i zrozumiały, aby umożliwić użytkownikom szybkie i efektywne wykorzystanie programu do rozwiązywania konkretnych problemów.


## Informacje końcowe

1. Autorzy: Łukasz Kuliński 52725, Katarzyna Lisiecka 54163, Kacper Lewicki 54162, Zuzanna Kroczak 52718, Oskar Krzysztofek 52720
2. Wsparcie mentorskie: mgr inż. Łukasz Łuczak
3. Historia zmian: https://github.com/rantnar/p1-zs1-gr4/graphs/contributors