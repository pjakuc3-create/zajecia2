import streamlit as st
import sqlite3
import os

# --- Konfiguracja Bazy Danych ---
DB_FILE = 'magazyn.db'
# Sprawdzenie, czy plik bazy danych istnieje, i utworzenie tabeli, jeśli to konieczne
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Utworzenie tabeli 'towary'
    cursor.execute("""
        CREATE TABLE towary (
            id INTEGER PRIMARY NULL,
            nazwa TEXT NOT NULL UNIQUE
        )
    """)
    # Dodanie początkowych danych
    cursor.execute("INSERT INTO towary (nazwa) VALUES (?)", ("Kawa",))
    cursor.execute("INSERT INTO towary (nazwa) VALUES (?)", ("Herbata",))
    cursor.execute("INSERT INTO towary (nazwa) VALUES (?)", ("Cukier",))
    conn.commit()
    conn.close()

# --- Funkcje Bazy Danych ---

def get_db_connection():
    """Tworzy i zwraca połączenie z bazą danych."""
    # Używamy st.cache_resource, aby połączenie było buforowane i wielokrotnie wykorzystywane
    # podczas przeładowań aplikacji, ale było bezpieczne dla Streamlit.
    return sqlite3.connect(DB_FILE)

def pobierz_towary():
    """Pobiera wszystkie towary z bazy danych."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nazwa FROM towary ORDER BY nazwa")
    # Zwraca listę nazw towarów
    return [row[0] for row in cursor.fetchall()]

def dodaj_towar(nazwa):
    """Dodaje towar do bazy danych."""
    nazwa = nazwa.strip()
    if not nazwa:
        st.error("Nazwa towaru nie może być pusta.")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Dodanie nowego towaru
        cursor.execute("INSERT INTO towary (nazwa) VALUES (?)", (nazwa,))
        conn.commit()
        st.success(f"Dodano towar: **{nazwa}**")
        # Ponowne uruchomienie aplikacji, aby odświeżyć interfejs
        st.rerun() 
    except sqlite3.IntegrityError:
        # Wyjątek w przypadku, gdy nazwa towaru już istnieje (constraint UNIQUE)
        st.warning(f"Towar **{nazwa}** już istnieje w magazynie.")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas dodawania towaru: {e}")

def usun_towar(nazwa):
    """Usuwa towar z bazy danych."""
    if not nazwa:
        st.error("Nie wybrano towaru do usunięcia.")
        return
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Usunięcie towaru
        cursor.execute("DELETE FROM towary WHERE nazwa = ?", (nazwa,))
        conn.commit()
        if cursor.rowcount > 0:
            st.success(f"Usunięto towar: **{nazwa}**")
            # Ponowne uruchomienie aplikacji, aby odświeżyć interfejs
            st.rerun() 
        else:
            st.error(f"Nie znaleziono towaru: **{nazwa}** w magazynie.")
    except Exception as e:
        st.error(f"Wystąpił błąd podczas usuwania towaru: {e}")

# --- Interfejs Użytkownika Streamlit ---

# Pobieranie aktualnego stanu magazynu z bazy danych
magazyn_list = pobierz_towary() 

st.title("📦 Prosty Magazyn Towarów - Wersja DB")

# Kolumny dla głównej zawartości i "ciastka"
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Zarządzanie Stanem")

    # --- Dodawanie Towaru ---
    st.subheader("➕ Dodaj Nowy Towar")
    # Używamy key="input_dodaj" w st.session_state, aby pole mogło być wyczyszczone
    nowy_towar = st.text_input("Wprowadź nazwę towaru do dodania:", key="input_dodaj")
    if st.button("Dodaj", key="btn_dodaj", use_container_width=True):
        dodaj_towar(nowy_towar)
        # Czyszczenie pola tekstowego po dodaniu
        st.session_state.input_dodaj = ""


    # --- Usuwanie Towaru ---
    st.subheader("➖ Usuń Towar")
    
    if magazyn_list:
        towar_do_usuniecia = st.selectbox(
            "Wybierz towar do usunięcia:",
            options=magazyn_list,
            key="select_usun"
        )
        if st.button("Usuń Wybrany Towar", key="btn_usun", use_container_width=True):
            usun_towar(towar_do_usuniecia)
            # st.rerun() jest już wywoływane w funkcji usun_towar
    else:
        st.info("Magazyn jest pusty. Nie ma czego usuwać.")


    # --- Aktualny Stan Magazynu ---
    st.subheader("Aktualny Stan Magazynu")
    if magazyn_list:
        st.dataframe({
            'Lp.': range(1, len(magazyn_list) + 1),
            'Nazwa Towaru': magazyn_list
        }, hide_index=True, use_container_width=True)
    else:
        st.info("Magazyn jest obecnie pusty.")

with col2:
    st.header("Boczny Akcent")
    st.markdown("---")
    st.write("💾 **Trwałe Zapisywanie!**")
    st.markdown("---")
