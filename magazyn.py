import streamlit as st
from st_supabase_connection import SupabaseConnection

# --- Konfiguracja połączenia ---
# Dane (URL i Key) powinny znaleźć się w .streamlit/secrets.toml
conn = st.connection("supabase", type=SupabaseConnection)

# --- Funkcje Magazynu (Operacje na DB) ---

def pobierz_magazyn():
    """Pobiera wszystkie towary z bazy danych."""
    res = conn.table("produkty").select("nazwa").execute()
    return [item['nazwa'] for item in res.data]

def dodaj_towar(nazwa):
    """Dodaje towar do bazy Supabase."""
    obecny_magazyn = pobierz_magazyn()
    if nazwa and nazwa not in obecny_magazyn:
        conn.table("produkty").insert({"nazwa": nazwa}).execute()
        st.success(f"Dodano towar: **{nazwa}**")
        st.rerun()
    elif nazwa in obecny_magazyn:
        st.warning(f"Towar **{nazwa}** już istnieje w bazie.")
    else:
        st.error("Nazwa towaru nie może być pusta.")

def usun_towar(nazwa):
    """Usuwa towar z bazy Supabase."""
    conn.table("produkty").delete().eq("nazwa", nazwa).execute()
    st.success(f"Usunięto towar: **{nazwa}**")
    st.rerun()

# --- Interfejs Użytkownika Streamlit ---

st.title("📦 Magazyn zintegrowany z Supabase")

# Pobranie aktualnych danych z bazy
lista_towarow = pobierz_magazyn()

col1, col2 = st.columns([3, 1])

with col1:
    st.header("Zarządzanie Stanem")

    # --- Dodawanie Towaru ---
    st.subheader("➕ Dodaj Nowy Towar")
    nowy_towar = st.text_input("Wprowadź nazwę towaru:", key="input_dodaj")
    if st.button("Dodaj do Bazy", use_container_width=True):
        dodaj_towar(nowy_towar)

    # --- Usuwanie Towaru ---
    st.subheader("➖ Usuń Towar")
    if lista_towarow:
        towar_do_usuniecia = st.selectbox(
            "Wybierz towar do usunięcia:",
            options=lista_towarow,
            key="select_usun"
        )
        if st.button("Usuń z Bazy", use_container_width=True):
            usun_towar(towar_do_usuniecia)
    else:
        st.info("Baza danych jest pusta.")

    # --- Aktualny Stan Magazynu ---
    st.subheader("Aktualny Stan (Live z Supabase)")
    if lista_towarow:
        st.dataframe({
            'Lp.': range(1, len(lista_towarow) + 1),
            'Nazwa Towaru': lista_towarow
        }, hide_index=True, use_container_width=True)
    else:
        st.info("Brak danych do wyświetlenia.")

with col2:
    st.header("Status")
    st.markdown("---")
    st.write("✅ Połączono z Supabase")
    if st.button("Odśwież dane"):
        st.rerun()
