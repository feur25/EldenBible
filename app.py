import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import EldenRingGraph

class AppLoading:
    def __init__(self):
        self.load_data()

    def load_game(self):
        return EldenRingGraph.EldenRing(self.ammos, self.armors, self.ashes, self.incantations, self.sorceries, self.talismans, self.classes, self.npcs, self.weapons, self.spirits, self.creatures, self.bosses, self.df, self.boss_names, self.output_armor)
    
    def load_data(self):
        self.ammos = pd.read_csv('./data/ammos.csv')
        self.armors = pd.read_csv('./data/armors.csv')
        self.ashes = pd.read_csv('./data/ashes.csv')
        self.incantations = pd.read_csv('./data/incantations.csv')
        self.sorceries = pd.read_csv('./data/sorceries.csv')
        self.talismans = pd.read_csv('./data/talismans.csv')
        self.classes = pd.read_csv('./data/classes.csv')
        self.npcs = pd.read_csv('./data/npcs.csv')
        self.weapons = pd.read_csv('./data/weapons.csv')
        self.spirits = pd.read_csv('./data/spirits.csv')
        self.creatures = pd.read_csv('./data/creatures.csv')
        self.bosses = pd.read_csv('./data/bosses.csv')
        self.df = pd.read_csv("./data/elden_ring_weapon.csv")
        self.output_armor = pd.read_csv('./data/output_ammor.csv')

        self.boss_names = {
            'ACH00': 'Elden Ring',
            'ACH01': 'Elden Lord',
            'ACH02': 'Age of the Stars',
            'ACH03': 'Lord of Frenzied Flame',
            'ACH04': 'Shardbearer Godrick',
            'ACH05': 'Shardbearer Radahn',
            'ACH06': 'Shardbearer Morgott',
            'ACH07': 'Shardbearer Rykard',
            'ACH08': 'Shardbearer Malenia',
            'ACH09': 'Shardbearer Mohg',
            'ACH10': 'Maliketh the Black Blade',
            'ACH11': 'Hoarah Loux, Warrior',
            'ACH12': 'Dragonlord Placidusax',
            'ACH13': 'God-Slaying Armament',
            'ACH18': 'Rennala, Queen of the Full Moon',
            'ACH19': 'Lichdragon Fortissax',
            'ACH20': 'Godskin Duo',
            'ACH21': 'Fire Giant',
            'ACH22': 'Dragonkin Soldier of Nokstella',
            'ACH23': 'Regal Ancestor Spirit',
            'ACH24': 'Valiant Gargoyles',
            'ACH25': 'Margit, the Fell Omen',
            'ACH26': 'Red Wolf of Radagon',
            'ACH27': 'Godskin Noble',
            'ACH28': 'Magma Wyrm Makar',
            'ACH29': 'Godfrey, First Elden Lord',
            'ACH30': 'Mohg, the Omen',
            'ACH31': 'Mimic Tear',
            'ACH32': 'Loretta, Knight of the Haligtree',
            'ACH33': 'Astel, Naturalborn of the Void',
            'ACH34': 'Leonine Misbegotten',
            'ACH35': 'Royal Knight Loretta',
            'ACH36': 'Elemer of the Briar',
            'ACH37': 'Ancestor Spirit',
            'ACH38': 'Commander Niall',
            'ACH40': 'Great Rune',
            'ACH41': 'Erdtree Aflame'
        }

        game = self.load_game()
        self.df = game.replaceZero()

        self.average_physical_damage, self.average_magic_damage, self.average_holy_damage = game.groupByType()

        def load_css(file_path):
            with open(file_path) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        load_css('./css/styles.css')

    

class SteamlitWebSite:
    def __init__(self):
        self.run()
    
    def run(self):
        self.display_app()

    def display_app(self):
        app_loader = AppLoading()
        game = app_loader.load_game()
        with st.sidebar:
            selected = option_menu(
                "Elden Bible",
                ["Introduction", "Statistiques", "Elden Vanilla", "Ending"],
                icons=["info-circle", "bar-chart", "book", "pause"],
                menu_icon="cast",
                default_index=0,
            )

        if selected == "Introduction":
            st.header("Elden Ring")
            st.markdown("""
            Welcome to the Elden Ring Data Visualization Application! This app allows you to explore various statistics and features of items, weapons, incantations, and much more in the game Elden Ring.

            Use the sections below to navigate through the interactive visualizations. The goal of this site is to help you make potentially game-changing decisions regarding your equipment, as well as to discover the challenges that await you. We hope to inspire you to dive into or re-engage with this fantastic universe that belongs to the magnificent Souls family. Elden Ring, with its complex narrative structure and richly detailed world, offers an unparalleled gaming experience.

            Join our community! Experience the intensity of combat, learn enemy patterns, and challenge the bosses until you emerge victorious. Elden Ring is not just a game; it is an adventure where every victory, big or small, is a personal triumph. By immersing yourself in this world, you will become part of a large family of passionate players. Come to rage, learn, and master the challenges that await you.

            Here are some features of this application:
            - Data Exploration: Detailed analysis of the statistics of weapons, armor, and other equipment
            - Interactive Visualizations: Graphs and charts that help you understand the strengths and weaknesses of each item.
            - Equipment Comparison: Tools to compare different items and optimize your build.
            - Game Guides: Tips and strategies to defeat the toughest bosses and progress efficiently in the game.

            Whether you are a new player or a veteran, this application is designed to enrich your gaming experience. We wish you the best of luck in your adventure and hope you find these tools useful in becoming a true Elden Lord!
            """)

        elif selected == "Statistiques":
            stats_selected = st.selectbox(
                "Select a statistic to view",
                ["Average Damage by Weapon Type", "Weight vs Physical Damage", "Boss Elden Ring", "Dlc Content"]
            )

            if stats_selected == "Average Damage by Weapon Type":
                st.title("Average Damage by Weapon Type")
                st.subheader("Choose Damage Category:")
                damage_category = st.radio("Select Damage Category", ["Physical", "Magic", "Holy"])

                if damage_category == "Physical":
                    st.header("Top 5 Weapons - Physical Damage")
                    app_loader.weapons['Phy'] = app_loader.weapons['attack'].apply(lambda x: next((d['amount'] for d in eval(x) if d['name'] == 'Phy'), 0))
                    top_weapons = app_loader.weapons.sort_values(by='Phy', ascending=False).head(5)
                elif damage_category == "Magic":
                    st.header("Top 5 Weapons - Magic Damage")
                    app_loader.weapons['Mag'] = app_loader.weapons['attack'].apply(lambda x: next((d['amount'] for d in eval(x) if d['name'] == 'Mag'), 0))
                    top_weapons = app_loader.weapons.sort_values(by='Mag', ascending=False).head(5)
                elif damage_category == "Holy":
                    st.header("Top 5 Weapons - Holy Damage")
                    app_loader.weapons['Hol'] = app_loader.weapons['attack'].apply(lambda x: next((d['amount'] for d in eval(x) if d['name'] == 'Holy'), 0))
                    top_weapons = app_loader.weapons.sort_values(by='Hol', ascending=False).head(5)

                cols = st.columns(5)
                for i, weapon in enumerate(top_weapons.iterrows()):
                    with cols[i]:
                        st.image(weapon[1]['image'], caption=weapon[1]['name'])
                        st.text(weapon[1]['category'])

                search_term = st.sidebar.text_input("Weapon name to search")
                if search_term:
                    weapon_results = game.search_item(app_loader.weapons, search_term)
                    if not weapon_results.empty:
                        st.subheader(f"Weapons matching '{search_term}':")
                        for index, weapon in weapon_results.iterrows():
                            st.image(weapon['image'], caption=weapon['name'])
                            st.text(weapon['category'])
                    else:
                        st.write("No weapons found matching that name.")

                game.plot_interactive_weapon_details(app_loader.average_physical_damage, app_loader.average_magic_damage, app_loader.average_holy_damage)

            elif stats_selected == "Weight vs Physical Damage":
                st.header("Weapons Weight")
                weapons_df = pd.read_csv('./data/weapons.csv')
                top_heavy_weapons = weapons_df.nlargest(5, 'weight')

                if len(top_heavy_weapons) < 5:
                    st.error("Not enough weapons data to display top 5 heaviest weapons.")
                else:
                    cols = st.columns(5)
                    for i in range(5): 
                        with cols[i]:
                            if i < len(top_heavy_weapons):
                                st.image(top_heavy_weapons.iloc[i]['image'], caption=top_heavy_weapons.iloc[i]['name'])
                                st.text(f"Weight: {top_heavy_weapons.iloc[i]['weight']}")

                st.header("Weight vs Physical Damage")
                game.scatter_plot()

            elif stats_selected == "Boss Elden Ring":
                st.header("Boss Elden Ring")
                st.subheader("Bosses spécifiques")
                specific_bosses = ['Lichdragon Fortissax', 'Dragonlord Placidusax', 'Mohg, the Omen', 'Shardbearer Malenia']
                filtered_bosses = app_loader.bosses[app_loader.bosses['name'].isin(specific_bosses)]
                cols = st.columns(len(specific_bosses))

                image_width = 250
                image_height = 200

                for col, (_, boss) in zip(cols, filtered_bosses.iterrows()):
                    if pd.notna(boss['image']):
                        with col:
                            st.markdown(f'<img src="{boss["image"]}" alt="{boss["name"]}" style="width: {image_width}px; height: {image_height}px;">', unsafe_allow_html=True)
                            st.text(boss['region'])

                search_term = st.sidebar.text_input("Nom du boss à rechercher")
                if search_term:
                    boss_results = app_loader.bosses[app_loader.bosses['name'].str.contains(search_term, case=False, na=False)]
                    if not boss_results.empty:
                        st.subheader(f"Bosses correspondant à '{search_term}':")
                        search_cols = st.columns(len(specific_bosses))
                        for col, (_, boss) in zip(search_cols, boss_results.iterrows()):
                            if pd.notna(boss['image']):
                                with col:
                                    st.markdown(f'<img src="{boss["image"]}" alt="{boss["name"]}" style="width: {image_width}px; height: {image_height}px;">', unsafe_allow_html=True)
                                    st.text(boss['region'])
                    else:
                        st.write("Aucun boss trouvé avec ce nom.")

                game.barre_plot_boss()

            elif stats_selected == "Dlc Content":
                video_url_2 = "https://static.bandainamcoent.eu/video/eldenring-kf-01-animated-new.webm"
                st.markdown(f"""
                    <video width="750" height="450" autoplay loop>
                        <source src="{video_url_2}" type="video/webm">
                        Your browser does not support the video tag.
                    </video>
                """, unsafe_allow_html=True)

                st.subheader("Armor Statistics")
                game.barre_plot_armor('Chest')
                game.barre_plot_armor('Hands')
                game.barre_plot_armor('Head')
                game.barre_plot_armor('Legs')

                video_url_1 = "https://www.youtube.com/embed/qLZenOn7WUo"
                st.markdown(f"""
                    <iframe width="750" height="450" src="{video_url_1}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                """, unsafe_allow_html=True)

        elif selected == "Elden Vanilla":
            st.header("Elden Vanilla")
            vanilla_selected = st.selectbox(
                "Select a category",
                ["Weapons", "Armor", "Incantation", "Spell", "Npc"]
            )

            if vanilla_selected == "Weapons":
                st.header("All Weapons")
                game.weapons['Phy'] = game.weapons['attack'].apply(lambda x: next((d['amount'] for d in eval(x) if d['name'] == 'Phy'), 0))

                search_term = st.sidebar.text_input("Search by Weapon Name")
                min_weight = st.sidebar.number_input("Minimum Weight", value=0)
                max_weight = st.sidebar.number_input("Maximum Weight", value=100)
                min_damage = st.sidebar.number_input("Minimum Physical Damage", value=0)

                filtered_weapons = game.weapons.copy()

                if search_term:
                    filtered_weapons = game.search_item(filtered_weapons, search_term)

                filtered_weapons = filtered_weapons[(filtered_weapons['weight'] >= min_weight) & (filtered_weapons['weight'] <= max_weight)]
                filtered_weapons = filtered_weapons[filtered_weapons['Phy'] >= min_damage]

                cols = st.columns(3)
                for weapon in filtered_weapons.iterrows():
                    with cols[filtered_weapons.index.get_loc(weapon[0]) % 3]: 
                        st.image(weapon[1]['image'], caption=weapon[1]['name'], use_column_width=True)
                        with st.expander("description", expanded=False):
                            st.markdown(f"**Description:** {weapon[1]['description']}")
                            st.text(f"Weight: {weapon[1]['weight']}")
                            st.text(f"Phy Damage: {weapon[1]['Phy']}")

            if vanilla_selected == "Armor":
                st.header("All Armors")
                game.armors['Phy'] = game.armors['dmgNegation'].apply(lambda x: next((d['amount'] for d in eval(x) if d['name'] == 'Phy'), 0))

                search_term = st.sidebar.text_input("Search by Armor Name")
                min_weight = st.sidebar.number_input("Minimum Weight", value=0)
                max_weight = st.sidebar.number_input("Maximum Weight", value=100)
                min_phy = st.sidebar.number_input("Minimum Physical Defense", value=0)

                game.armors['image'] = game.armors['image'].astype(str)

                filtered_armors = game.armors.copy()

                if search_term:
                    filtered_armors = game.search_item(filtered_armors, search_term)

                filtered_armors = filtered_armors[(filtered_armors['weight'] >= min_weight) & (filtered_armors['weight'] <= max_weight)]
                filtered_armors = filtered_armors[filtered_armors['Phy'] >= min_phy]

                cols = st.columns(3)
                for armor in filtered_armors.iterrows():
                    with cols[filtered_armors.index.get_loc(armor[0]) % 3]: 
                        if pd.notna(armor[1]['image']):
                            st.image(armor[1]['image'], caption=armor[1]['name'], use_column_width=True)
                            with st.expander("description", expanded=False):
                                st.markdown(f"**Description:** {armor[1]['description']}")
                                st.text(f"Weight: {armor[1]['weight']}")
                                st.text(f"Phy Defense: {armor[1]['Phy']}")
                        else:
                            st.text("Image not available")


            elif vanilla_selected == "Incantation":
                st.header("Incantation")
                pass

            elif vanilla_selected == "Spell":
                st.header("Spell")
                pass

            elif vanilla_selected == "Npc":
                st.header("Npc")
                pass

        if selected == "Ending":
            st.markdown(
                """
                <div class="video-background">
                    <iframe src="https://www.youtube.com/embed/GV2fGyTrYx8?autoplay=1&loop=1&playlist=GV2fGyTrYx8&controls=0&disablekb=1&modestbranding=1&showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                </div>
                <div style="position: relative; z-index: 1; color: white;">
                    <h1 style="text-align: center; margin-top: 50vh;">Merci d'avoir utilisé l'application de visualisation des données de Elden Ring !</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    SteamlitWebSite()