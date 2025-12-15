import streamlit as st

# --- Inicjalizacja Magazynu (Lista przechowująca nazwy towarów) ---
# Używamy st.session_state do utrzymania stanu (listy) pomiędzy interakcjami.
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = ["Kawa", "Herbata", "Czekolada"]

# --- Funkcje Logiki Magazynu ---

def dodaj_towar(nazwa):
    """Dodaje towar do listy magazynu."""
    if nazwa and nazwa not in st.session_state.magazyn:
        st.session_state.magazyn.append(nazwa)
        st.success(f"Dodano: **{nazwa}**")
    elif nazwa in st.session_state.magazyn:
        st.warning(f"Towar **{nazwa}** jest już w magazynie.")
    else:
        st.error("Nazwa towaru nie może być pusta.")

def usun_towar(nazwa):
    """Usuwa towar z listy magazynu."""
    try:
        st.session_state.magazyn.remove(nazwa)
        st.success(f"Usunięto: **{nazwa}**")
    except ValueError:
        st.warning(f"Nie znaleziono towaru o nazwie: **{nazwa}**")

# --- Interfejs Użytkownika Streamlit ---

st.title("📦 Prosty Magazyn (Streamlit + Lista)")
st.caption("Dane są przechowywane tylko w sesji, bez zapisu do pliku.")

## Sekcja 1: Wyświetlanie Stanu Magazynu
st.header("Aktualny Stan Magazynu")

if st.session_state.magazyn:
    # Wyświetlenie listy jako numerowanej listy Markdown
    magazyn_str = "\n".join([f"* {item}" for item in st.session_state.magazyn])
    st.markdown(magazyn_str)
else:
    st.info("Magazyn jest pusty.")

st.markdown("---")

## Sekcja 2: Dodawanie Towaru
st.header("➕ Dodaj Towar")
# Używamy formy Streamlit, aby przycisk wywoływał funkcję po kliknięciu
with st.form("dodaj_form"):
    nowy_towar = st.text_input("Nazwa nowego towaru:", key="input_dodaj")
    # Formularz wymaga przycisku submit
    dodaj_przycisk = st.form_submit_button("Dodaj do Magazynu")
    
    if dodaj_przycisk:
        dodaj_towar(nowy_towar)


## Sekcja 3: Usuwanie Towaru
st.header("➖ Usuń Towar")

if st.session_state.magazyn:
    # Użycie st.selectbox pozwala na łatwy wybór spośród istniejących towarów
    towar_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia:",
        st.session_state.magazyn,
        key="select_usun"
    )
    
    # Przycisk, który wywoła funkcję usuwania
    if st.button("Usuń Wybrany Towar"):
        usun_towar(towar_do_usuniecia)
else:
    st.info("Brak towarów do usunięcia.")
