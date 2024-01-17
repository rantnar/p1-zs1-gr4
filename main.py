import requests
import json
from datetime import datetime

def get_exchange_rate(date, currency):
    # Tutaj pobieramy kurs waluty z API NBP
    pass

def calculate_exchange_rate_difference(invoice_date, payment_date, currency):
    # Tutaj obliczamy różnicę kursową
    pass

def save_data_to_file(data, filename):
    # Tutaj zapisujemy dane do pliku
    pass

def get_invoice_data():
    # Tutaj zbieramy dane o fakturach od użytkownika lub z pliku
    pass

def get_payment_data():
    # Tutaj zbieramy dane o płatnościach od użytkownika lub z pliku
    pass

def calculate_exchange_rate_difference_for_all_invoices(invoices, payments):
    # Tutaj obliczamy różnice kursowe dla wszystkich faktur na podstawie danych o płatnościach
    pass

def display_results(results):
    # Tutaj wyświetlamy wyniki obliczeń
    pass

def run_interactive_mode():
    # Tutaj uruchamiamy program w trybie interaktywnym, gdzie użytkownik wprowadza dane bezpośrednio
    pass

def run_batch_mode():
    # Tutaj uruchamiamy program w trybie wsadowym, gdzie dane są pobierane z pliku
    pass

def main():
    # Tutaj decydujemy, czy uruchomić program w trybie interaktywnym czy wsadowym
    pass

if __name__ == '__main__':
    main()