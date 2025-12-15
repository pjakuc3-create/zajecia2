import streamlit as st

# --- Inicjalizacja Magazynu ---
# Używamy st.session_state, aby zachować stan listy towarów
# po ponownym uruchomieniu aplikacji przez Streamlit.
if 'magazyn' not in st.session_state:
    st.session_state.magazyn = ["Kawa", "Herbata", "Cukier"]

# --- Funkcje Magazynu ---

def dodaj_towar(nazwa):
    """Dodaje towar do listy magazynu."""
    if nazwa and nazwa not in st.session_state.magazyn:
        st.session_state.magazyn.append(nazwa)
        st.success(f"Dodano towar: **{nazwa}**")
    elif nazwa in st.session_state.magazyn:
        st.warning(f"Towar **{nazwa}** już istnieje w magazynie.")
    else:
        st.error("Nazwa towaru nie może być pusta.")

def usun_towar(nazwa):
    """Usuwa towar z listy magazynu."""
    if nazwa in st.session_state.magazyn:
        st.session_state.magazyn.remove(nazwa)
        st.success(f"Usunięto towar: **{nazwa}**")
    else:
        st.error(f"Nie znaleziono towaru: **{nazwa}** w magazynie.")

# --- Interfejs Użytkownika Streamlit ---

st.title("📦 Prosty Magazyn Towarów")

# Kolumny dla głównej zawartości i "ciastka"
col1, col2 = st.columns([3, 1])

with col1:
    st.header("Zarządzanie Stanem")

    # --- Dodawanie Towaru ---
    st.subheader("➕ Dodaj Nowy Towar")
    nowy_towar = st.text_input("Wprowadź nazwę towaru do dodania:", key="input_dodaj")
    if st.button("Dodaj", use_container_width=True):
        dodaj_towar(nowy_towar)
        # Czyszczenie pola tekstowego po dodaniu
        st.session_state.input_dodaj = ""


    # --- Usuwanie Towaru ---
    st.subheader("➖ Usuń Towar")
    
    if st.session_state.magazyn:
        towar_do_usuniecia = st.selectbox(
            "Wybierz towar do usunięcia:",
            options=st.session_state.magazyn,
            key="select_usun"
        )
        if st.button("Usuń Wybrany Towar", use_container_width=True):
            usun_towar(towar_do_usuniecia)
            # Wymuszenie odświeżenia, aby zaktualizować selectbox
            st.rerun() 
    else:
        st.info("Magazyn jest pusty. Nie ma czego usuwać.")


    # --- Aktualny Stan Magazynu ---
    st.subheader("Aktualny Stan Magazynu")
    if st.session_state.magazyn:
        st.dataframe({
            'Lp.': range(1, len(st.session_state.magazyn) + 1),
            'Nazwa Towaru': st.session_state.magazyn
        }, hide_index=True, use_container_width=True)
    else:
        st.info("Magazyn jest obecnie pusty.")

with col2:
    st.header("Boczny Akcent")
    st.markdown("---")
    st.write("🍪 **Ciastko Dnia!**")
    st.markdown("---")
