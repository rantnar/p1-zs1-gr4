#Importy bibliotek
import requests
import json
# from questionary import Prompt, print_error
# from questionary import console
from datetime import datetime
import re
import traceback
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
#Inicializacja konsoli
console = Console()

def get_cached_data(currency, date):
    try:
        with open('cache.json', 'r') as file:
            data = json.load(file)
            if currency in data and date in data[currency]:
                return data[currency][date]
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return None

def get_data_from_api(currency, date):
    try:
        response = requests.get(f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date}/?format=json")
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise Exception("Błąd HTTP: {}. Brak danych dla podanej daty.".format(errh))
    except requests.exceptions.ConnectionError as errc:
        raise Exception("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        raise Exception("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        raise Exception("Something went wrong",err)

    data = response.json()
    return data["rates"][0]["mid"]

def save_data_to_cache(currency, date, rate):
    try:
        with open('cache.json', 'r') as file:
            cache_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        cache_data = {}

    if currency not in cache_data:
        cache_data[currency] = {}
    cache_data[currency][date] = rate

    with open('cache.json', 'w') as file:
        json.dump(cache_data, file)

def get_exchange_rate_for_date(currency, date):
    cached_data = get_cached_data(currency, date)
    if cached_data is not None:
        return cached_data

    rate = get_data_from_api(currency, date)
    save_data_to_cache(currency, date, rate)

    return rate

def get_exchange_rate(currency, date_issue, date_payment):
    if currency.upper() == 'PLN':
        return 1, 1
    issue_rate = get_exchange_rate_for_date(currency, date_issue)
    payment_rate = issue_rate if date_issue == date_payment else get_exchange_rate_for_date(currency, date_payment)
    return issue_rate, payment_rate

def calculate_exchange_rate_difference(invoice_amount, currency, date_issue, date_payment):
    #Funkcja obliczająca różnicę kursową na podstawie podanych parametrów, zwraza różnicę kursową.

    issue_rate, payment_rate = get_exchange_rate(currency, date_issue, date_payment)

    #Zmienna invoice_amount jest typu string, konwersja na float jest wymagana do poprawnego działania funkcji.
    invoice_amount = float(invoice_amount)
    
    amount_in_pln_issue = invoice_amount * issue_rate
    amount_in_pln_payment = invoice_amount * payment_rate
    return amount_in_pln_payment - amount_in_pln_issue

def save_invoice_data(invoice_data, file_path='data.json'):
    #Funkcja zapisująca dane faktury do pliku JSON.
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []
    data.append(invoice_data)
    with open(file_path, 'w') as file:
        json.dump(data, file)

def validate_invoice_number(existing_invoices):
    #Funkcja walidująca numer faktury, zwraca poprawny numer faktury.
    invoice_number = Prompt.ask("Nr. faktury: ")
    while not re.match(r"^[a-zA-Z0-9-/]+$", invoice_number) or any(invoice['invoice_number'] == invoice_number for invoice in existing_invoices):
        invoice_number = Prompt.ask("Nieprawidłowy numer faktury lub numer faktury już istnieje. Wprowadź ponownie: ")
    return invoice_number

def validate_value():
    #Funkcja walidująca wartość faktury, zwraca poprawną wartość faktury.
    value = Prompt.ask("Wartość faktury: ")
    while True:
        try:
            return float(value)
        except ValueError:
            value = Prompt.ask("Nieprawidłowa wartość faktury. Wprowadź ponownie: ")

def validate_currency():
    #Funkcja walidująca walutę, zwraca poprawną walutę.
    currency = Prompt.ask("Waluta(EUR, USD, GBP, PLN): ")
    while currency not in ['EUR', 'USD', 'GBP', 'PLN']:
        currency = Prompt.ask("Nieprawidłowa waluta. Dozwolone waluty to EUR, USD, GBP i PLN. Wprowadź ponownie: ")
    return currency

def validate_date(prompt_message, earliest_date=None):
    #Funkcja walidująca datę, zwraca poprawną datę.
    date_str = Prompt.ask(prompt_message)
    while True:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if earliest_date and date < earliest_date:
                raise ValueError
            return date_str
        except ValueError:
            date_str = Prompt.ask("Nieprawidłowa data. Wprowadź ponownie: ")

def get_invoice_data():
    #Funkcja pobierająca dane faktury od użytkownika, zwraca słownik z danymi faktury.
    invoice_data = {}

    with open('data.json', 'r') as file:
        existing_invoices = json.load(file)

    invoice_data['invoice_number'] = validate_invoice_number(existing_invoices)
    invoice_data['value'] = validate_value()
    invoice_data['currency'] = validate_currency()
    invoice_data['issue_date'] = validate_date("Data wystawienia (YYYY-MM-DD): ")
    invoice_data['payment_date'] = validate_date("Data zapłaty (YYYY-MM-DD): ", datetime.strptime(invoice_data['issue_date'], '%Y-%m-%d'))

    return invoice_data
    
def display_results(invoices):
    #Funkcja wyświetlająca wyniki w tabeli.
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Numer faktury")
    table.add_column("Kurs waluty w dniu wystawienia faktury")
    table.add_column("Kurs waluty w dniu płatności")
    table.add_column("Różnica kursowa wynosi")

    for invoice in invoices:
        #Pętla przetwarzająca dane faktury i dodająca wyniki do tabeli.
        issue_rate, payment_rate, difference = process_invoice(invoice)
        if issue_rate is not None and payment_rate is not None and difference is not None:
            difference_str = str(round(difference, 2)) + " PLN"
            if difference > 0:
                difference_str = f"[red]{difference_str}[/red]"
            else:
                difference_str = f"[green]{difference_str}[/green]"
            table.add_row(str(invoice['invoice_number']), str(issue_rate), str(payment_rate), difference_str)
        else:
            print_error("Błąd przetwarzania faktury. Pominięto wynik.\n")
    console.print(table)

def print_error(msg):
    #Funkcja wyświetlająca komunikat o błędzie.
    console.print(msg, style="bold red")

def process_invoice(invoice_data):
    #Funkcja przetwarzająca dane faktury, zwraca kursy walut w dniu wystawienia i płatności faktury oraz różnicę kursową.
    currency = invoice_data['currency']
    issue_date = invoice_data['issue_date']
    payment_date = invoice_data['payment_date']
    value = invoice_data['value']
    try:
        issue_rate, payment_rate = get_exchange_rate(currency, issue_date, payment_date)
        if issue_rate is None or payment_rate is None:
            print_error("Nie udało się pobrać kursów walut. Spróbuj ponownie.\n")
            return None, None, None
        difference = calculate_exchange_rate_difference(value, currency, issue_date, payment_date)
        return issue_rate, payment_rate, difference
    except Exception as e:
        print_error(f"Wystąpił błąd: {e}")
        return None, None, None   

def run_interactive_mode():
    #Funkcja uruchamiająca tryb interaktywny.
    while True:
        invoice_data = get_invoice_data()
        if invoice_data is None:
            continue
        while True:
            correct_input = Prompt.ask("Czy poprawnie wprowadziłeś dane? (t/n) ")
            if correct_input.lower() == 't':
                save_invoice_data(invoice_data)
                display_results([invoice_data]) 
                break
        continue_input = Prompt.ask("Czy chcesz wprowadzić kolejną płatność? (t/n) ")
        if continue_input.lower() != 't':
            break

def run_batch_mode():
    # Funkcja uruchamiająca tryb wsadowy.
    while True:
        file_path = Prompt.ask("Podaj ścieżkę do pliku z danymi: ")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                display_results(data)
                break  # Przerywa pętlę, jeśli plik został wczytany poprawnie
        except FileNotFoundError:
            print_error("Plik nie został znaleziony. Podaj poprawną ścieżkę.")
        except json.JSONDecodeError:
            print_error("Nieprawidłowy format pliku JSON. Podaj poprawny plik.")
        except ValueError as e:
            print_error(str(e))

    console.input("Naciśnij Enter, aby kontynuować...\n")
    
def main():
    #Funkcja główna programu. Wyświetla menu wyboru trybu pracy.
    console.print("Witaj w programie do obliczania różnic kursowych!\n")
    console.print("Wybierz tryb pracy:\n")
    console.print("1. Tryb interaktywny\n")
    console.print("2. Tryb wsadowy\n")

    mode = Prompt.ask("Wybór: ")
    while mode not in ["1", "2"]:
        mode = Prompt.ask("Nieprawidłowy wybór. Wprowadź ponownie: ")

    if mode == "1":
        run_interactive_mode()
    elif mode == "2":
        run_batch_mode()

if __name__ == '__main__':
    #Wywołanie funkcji głównej programu.
    try:
        main()
    except Exception:
        console.print("Wystąpił błąd:")
        console.print(traceback.format_exc())

