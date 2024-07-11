import streamlit as st

def display_filtered_weapons(filtered_weapons):
    for weapon in filtered_weapons.iterrows():
        with st.expander(f"{weapon[1]['name']} - Click to expand"):
            st.image(weapon[1]['image'], caption=weapon[1]['name'], use_column_width=True)
            st.markdown(f"**Description:** {weapon[1]['description']}")
            st.text(f"Weight: {weapon[1]['weight']}")
            st.text(f"Phy Damage: {weapon[1]['Phy']}")

def display_filtered_armors(filtered_armors):
    for armor in filtered_armors.iterrows():
        with st.expander(f"{armor[1]['name']} - Click to expand"):
            st.image(armor[1]['image'], caption=armor[1]['name'], use_column_width=True)
            st.markdown(f"**Description:** {armor[1]['description']}")
            st.text(f"Weight: {armor[1]['weight']}")
            st.text(f"Phy Defense: {armor[1]['Phy']}")