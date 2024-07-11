import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import json

class EldenRing:

    def __init__(self, ammos, armors, ashes, incantations, sorceries, talismans, classes, npcs, weapons, spirits, creatures, bosses, df, bosses_names, output_armor):
        self.ammos = ammos
        self.armors = armors
        self.ashes = ashes
        self.incantations = incantations
        self.sorceries = sorceries
        self.talismans = talismans
        self.classes = classes
        self.npcs = npcs
        self.weapons = weapons
        self.spirits = spirits
        self.creatures = creatures
        self.bosses = bosses
        self.df = df
        self.bosses_names = bosses_names
        self.output_armor = output_armor

    @staticmethod
    def search_item(items, name):
        return items[items['name'] == name]
        
    def plot_interactive_weapon_weight(self):
        self.weapons['customdata'] = self.weapons['name'] + ' - ' + self.weapons['category']

        fig = px.bar(self.weapons, x='name', y='weight', hover_data=['customdata'], title='Weapons')

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font_color='white',
            title=dict(text='Weapons', font=dict(color='white'))
        )

        fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)', font_color='white')

        fig.update_traces(hovertemplate='<b>Name:</b> %{customdata}<br><b>Weight:</b> %{y}<extra></extra>')

        fig.update_xaxes(title=dict(text='Name', font=dict(color='white')))
        fig.update_yaxes(title=dict(text='Weight', font=dict(color='white')))

        st.plotly_chart(fig)

    def replaceZero(self):
        self.df = self.df.replace('-', 0)
        self.df['Phy'] = self.df['Phy'].astype(float)
        self.df['Mag'] = self.df['Mag'].astype(float)
        self.df['Hol'] = self.df['Hol'].astype(float)
        return self.df
    
    def groupByType(self):
        try:
            if all(col in self.df.columns for col in ['Type', 'Phy', 'Mag', 'Hol']):
                average_physical_damage = self.df.groupby('Type')['Phy'].mean().reset_index()
                average_magic_damage = self.df.groupby('Type')['Mag'].mean().reset_index()
                average_holy_damage = self.df.groupby('Type')['Hol'].mean().reset_index()
                return average_physical_damage, average_magic_damage, average_holy_damage
            else:
                st.warning("Some required columns are missing in filtered data.")
                return None, None, None
        except KeyError as e:
            st.error(f"Column error: {e}")
            return None, None, None

    def barre_plot_boss(self):
        df_achievements = pd.read_csv('./data/steam_api_data.csv')

        df_achievements['ID'] = df_achievements['ID'].map(self.bosses_names)

        if 'Margit, the Fell Omen' not in df_achievements['ID'].values:
            raise ValueError("Le nom 'Margit, the Fell Omen' n'a pas été trouvé dans le DataFrame après le mapping des noms.")

        df_achievements.sort_values(by='Percent', inplace=True)

        margit_percent = df_achievements.loc[df_achievements['ID'] == 'Margit, the Fell Omen', 'Percent'].values[0]
        df_achievements['Normalized Percent'] = df_achievements['Percent'] / margit_percent * 100

        subplot = make_subplots(rows=1, cols=2, subplot_titles=("Raw Percentage", "Percentages normalized to Margit"))

        colors = {
            'Elden Ring': 'purple',
            'Elden Lord': 'blue',
            'Age of the Stars': 'green',
            'Lord of Frenzied Flame': 'orange'
        }

        subplot.add_trace(go.Bar(
            x=df_achievements['Percent'],
            y=df_achievements['ID'],
            text=df_achievements['Percent'].round(2).astype(str) + '%',
            textposition='inside',
            orientation='h',
            marker_color=[colors.get(boss, 'darkcyan') for boss in df_achievements['ID']], 
            opacity=0.8,
        ), row=1, col=1)

        subplot.add_trace(go.Bar(
            x=df_achievements['Normalized Percent'],
            y=df_achievements['ID'],
            text=df_achievements['Normalized Percent'].round(2).astype(str) + '%',
            textposition='inside',
            orientation='h',
            marker_color=[colors.get(boss, 'darkcyan') for boss in df_achievements['ID']], 
            opacity=0.8,
        ), row=1, col=2)

        subplot.update_layout(
            title=dict(text='Boss Achievements Completed', font=dict(color='white')),
            xaxis_title=dict(text='Percentages (%)', font=dict(color='white')),
            yaxis_title=dict(text='Boss Name', font=dict(color='white')),
            bargap=0.1,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            height=1000,
            width=2400,
            showlegend=False
        )

        subplot.update_xaxes(showgrid=False, zeroline=False)
        subplot.update_yaxes(showgrid=False, zeroline=False)
        st.plotly_chart(subplot)

    def plot_interactive_weapon_details(self, ph, mg, hl):
        average_damage = pd.concat([ph['Type'], ph['Phy'], mg['Mag'], hl['Hol']], axis=1)
        average_damage.columns = ['Type', 'Physical', 'Magic', 'Holy']

        average_damage['data'] = average_damage.apply(lambda row: f"Physical: {row['Physical']}<br>Magic: {row['Magic']}<br>Holy: {row['Holy']}", axis=1)
        
        fig = px.bar(average_damage, x='Type', y=['Physical', 'Magic', 'Holy'], barmode='group', hover_data=['data'])

        fig.update_traces(text=average_damage['Type'], textposition='outside')

        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        fig.update_layout(font_color='white')
        
        fig.update_layout(
            title=dict(text='Average Damage by Weapon Type', font=dict(color='white')),
            xaxis_title=dict(text='Weapon Type', font=dict(color='white')),
            yaxis_title=dict(text='Average Damage', font=dict(color='white')),
            legend_title=dict(text='Damage Type', font=dict(color='white'))
        )

        st.plotly_chart(fig)

    def scatter_plot(self):
        self.df['Name'] = self.df['Name'].str.strip()

        sorted_data = self.df.sort_values(by='Phy', ascending=False)

        fig = px.scatter(sorted_data, x='Wgt', y='Phy', color='Type', hover_data=['Name', 'Wgt', 'Phy', 'Mag', 'Hol', 'Type'])

        fig.update_traces(marker=dict(size=12))

        fig.update_layout(
            title=dict(text='Weight vs Physical Damage', font=dict(color='white')),
            xaxis_title=dict(text='Weight', font=dict(color='white')),
            yaxis_title=dict(text='Physical Damage', font=dict(color='white')),
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font_color='white'
        )

        fig.update_layout(clickmode='event+select')

        selected_point = st.selectbox("Select an item to display details", sorted_data['Name'])

        selected_item = sorted_data[sorted_data['Name'] == selected_point].iloc[0]

        st.write(f"Selected item: {selected_item['Name']} - Weight: {selected_item['Wgt']} - Physical Damage: {selected_item['Phy']}")

        selected_weapon = self.weapons[self.weapons['name'] == selected_item['Name']].iloc[0]
        st.image(selected_weapon['image'], caption=selected_weapon['name'])

        st.plotly_chart(fig)

    def incantation_plot(self):
        fig = px.bar(self.incantations, x='name', y='cost', title='Incantations')

        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
        fig.update_layout(font_color='white')

        fig.update_xaxes(title='Name')
        fig.update_yaxes(title='cost')

        st.plotly_chart(fig)
    
    def incantation_plot_requires(self):
        df = pd.DataFrame(columns=['name', 'cost', 'requires', 'requiresIntelligence', 'requiresFaith', 'requiresArcane'])

        list = []

        for name in self.incantations['name']:
            incantation = self.search_item(self.incantations, name)
            requires_value = incantation['requires'].iloc[0]
            requires = json.loads(requires_value.replace("'", '"')) if isinstance(requires_value, str) else []
            cost = incantation['cost'].values[0]

            intelligence_requirement = sum(req['amount'] for req in requires if req['name'] == 'Intelligence') / len(requires) if requires else 0
            faith_requirement = sum(req['amount'] for req in requires if req['name'] == 'Faith') / len(requires) if requires else 0
            arcane_requirement = sum(req['amount'] for req in requires if req['name'] == 'Arcane') / len(requires) if requires else 0

            list.append(pd.DataFrame({'name': [name], 'cost': [cost], 'requires': [requires], 'requiresIntelligence': [intelligence_requirement], 'requiresFaith': [faith_requirement], 'requiresArcane': [arcane_requirement]}))

        df = pd.concat(list)

        fig = px.scatter(df, x='requiresIntelligence', y='cost', title='Incantations', hover_data=['name'])

        fig.add_traces(px.scatter(df, x='requiresIntelligence', y='cost', trendline="ols").data)
        fig.add_traces(px.scatter(df, x='requiresFaith', y='cost', trendline="ols").data)
        fig.add_traces(px.scatter(df, x='requiresArcane', y='cost', trendline="ols").data)

        fig.update_layout(legend_title='Legend', xaxis_title='Requires', yaxis_title='Cost')

        st.plotly_chart(fig)

    def barre_plot_chest_armor(self):
        filtered_df = self.output_armor[self.output_armor['type'] == 'Chest']

        fig = go.Figure()

        stats = ["weight", "phys.def", "vs.std", "vs.slash", "vs.pierce", 
                "magic.def", "fire.def", "light.def", "holy.def", 
                "immunity", "robustness", "focus", "vitality", "poise"]

        colors = ['blue', 'green', 'red', 'purple', 'orange', 'yellow', 
                'cyan', 'magenta', 'lime', 'pink', 'teal', 'lavender', 
                'brown', 'gray']

        for i, stat in enumerate(stats):
            if stat == "robustness":
                color = 'gold'  
            else:
                color = colors[i % len(colors)]
            
            fig.add_trace(go.Bar(
                x=filtered_df['name'],
                y=filtered_df[stat],
                name=stat,
                marker_color=color,
                visible=(stat == "poise"), 
            ))

        fig.update_layout(
            title=dict(text='Statistiques des équipements de type "Chest"', font=dict(color='white')),
            xaxis_title=dict(text='Équipement', font=dict(color='white')),
            yaxis_title=dict(text='Valeur', font=dict(color='white')),
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            height=1500
        )

        buttons = []
        for stat in stats:
            button = dict(
                label=stat,
                method="update",
                args=[{"visible": [stat == s for s in stats]}, {"title": f'Statistiques: {", ".join([s for s in stats if stat == s])}'}]
            )
            buttons.append(button)

        fig.update_layout(
            updatemenus=[
                {
                    'buttons': [
                        {'label': 'Afficher tout', 'method': 'update', 'args': [{'visible': [True] * len(fig.data)}]},
                        {'label': 'Masquer tout', 'method': 'update', 'args': [{'visible': [False] * len(fig.data)}]},
                    ],
                    'direction': 'down',
                    'showactive': True,
                },
            ],
            annotations=[
                dict(
                    x=0.5,
                    y=1.1,
                    xref="paper",
                    yref="paper",
                    text="Chests Statistics:",
                    showarrow=False,
                )
            ],
        )

        for i, stat in enumerate(stats):
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="down",
                        buttons=buttons,
                    ),
                ]
            )

        st.plotly_chart(fig)

    def barre_plot_hands_armor(self):
        filtered_df = self.output_armor[self.output_armor['type'] == 'Hands']

        fig = go.Figure()

        stats = ["weight", "phys.def", "vs.std", "vs.slash", "vs.pierce", 
                "magic.def", "fire.def", "light.def", "holy.def", 
                "immunity", "robustness", "focus", "vitality", "poise"]

        colors = ['blue', 'green', 'red', 'purple', 'orange', 'yellow', 
                'cyan', 'magenta', 'lime', 'pink', 'teal', 'lavender', 
                'brown', 'gray']

        for i, stat in enumerate(stats):
            if stat == "robustness":
                color = 'gold' 
            else:
                color = colors[i % len(colors)]
            
            fig.add_trace(go.Bar(
                x=filtered_df['name'],
                y=filtered_df[stat],
                name=stat,
                marker_color=color,
                visible=(stat == "poise"), 
            ))

        fig.update_layout(
            title=dict(text='Statistiques des équipements de type "Hands"', font=dict(color='white')),
            xaxis_title=dict(text='Équipement', font=dict(color='white')),
            yaxis_title=dict(text='Valeur', font=dict(color='white')),
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            height=1500
        )

        buttons = []
        for stat in stats:
            button = dict(
                label=stat,
                method="update",
                args=[{"visible": [stat == s for s in stats]}, {"title": f'Statistiques: {", ".join([s for s in stats if stat == s])}'}]
            )
            buttons.append(button)

        fig.update_layout(
            updatemenus=[
                {
                    'buttons': [
                        {'label': 'Afficher tout', 'method': 'update', 'args': [{'visible': [True] * len(fig.data)}]},
                        {'label': 'Masquer tout', 'method': 'update', 'args': [{'visible': [False] * len(fig.data)}]},
                    ],
                    'direction': 'down',
                    'showactive': True,
                },
            ],
            annotations=[
                dict(
                    x=0.5,
                    y=1.1,
                    xref="paper",
                    yref="paper",
                    text="Hands Statistics:",
                    showarrow=False,
                )
            ],
        )

        for i, stat in enumerate(stats):
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="down",
                        buttons=buttons,
                    ),
                ]
            )

        st.plotly_chart(fig)


    def barre_plot_head_armor(self):
        filtered_df = self.output_armor[self.output_armor['type'] == 'Head']

        fig = go.Figure()

        stats = ["weight", "phys.def", "vs.std", "vs.slash", "vs.pierce", 
                "magic.def", "fire.def", "light.def", "holy.def", 
                "immunity", "robustness", "focus", "vitality", "poise"]

        colors = ['blue', 'green', 'red', 'purple', 'orange', 'yellow', 
                'cyan', 'magenta', 'lime', 'pink', 'teal', 'lavender', 
                'brown', 'gray']
        
        for i, stat in enumerate(stats):
            if stat == "robustness":
                color = 'gold' 
            else:
                color = colors[i % len(colors)]
            
            fig.add_trace(go.Bar(
                x=filtered_df['name'],
                y=filtered_df[stat],
                name=stat,
                marker_color=color,
                visible=(stat == "poise"), 
            ))

        fig.update_layout(
            title=dict(text='Statistiques des équipements de type "Head"', font=dict(color='white')),
            xaxis_title=dict(text='Équipement', font=dict(color='white')),
            yaxis_title=dict(text='Valeur', font=dict(color='white')),
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            height=1500
        )

        buttons = []
        for stat in stats:
            button = dict(
                label=stat,
                method="update",
                args=[{"visible": [stat == s for s in stats]}, {"title": f'Statistiques: {", ".join([s for s in stats if stat == s])}'}]
            )
            buttons.append(button)

        fig.update_layout(
            updatemenus=[
                {
                    'buttons': [
                        {'label': 'Afficher tout', 'method': 'update', 'args': [{'visible': [True] * len(fig.data)}]},
                        {'label': 'Masquer tout', 'method': 'update', 'args': [{'visible': [False] * len(fig.data)}]},
                    ],
                    'direction': 'down',
                    'showactive': True,
                },
            ],
            annotations=[
                dict(
                    x=0.5,
                    y=1.1,
                    xref="paper",
                    yref="paper",
                    text="Heads Statistics:",
                    showarrow=False,
                )
            ],
        )

        for i, stat in enumerate(stats):
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="down",
                        buttons=buttons,
                    ),
                ]
            )

        st.plotly_chart(fig)

    def barre_plot_legs_armor(self):

        filtered_df = self.output_armor[self.output_armor['type'] == 'Legs']

        fig = go.Figure()

        stats = ["weight", "phys.def", "vs.std", "vs.slash", "vs.pierce", 
                "magic.def", "fire.def", "light.def", "holy.def", 
                "immunity", "robustness", "focus", "vitality", "poise"]

        colors = ['blue', 'green', 'red', 'purple', 'orange', 'yellow', 
                'cyan', 'magenta', 'lime', 'pink', 'teal', 'lavender', 
                'brown', 'gray']

        for i, stat in enumerate(stats):
            if stat == "robustness":
                color = 'gold' 
            else:
                color = colors[i % len(colors)]
            
            fig.add_trace(go.Bar(
                x=filtered_df['name'],
                y=filtered_df[stat],
                name=stat,
                marker_color=color,
                visible=(stat == "poise"),  
            ))

        fig.update_layout(
            title='Statistiques des équipements de type "Legs"',
            xaxis_title='Équipement',
            yaxis_title='Valeur',
            barmode='group', 
        )

        buttons = []
        for stat in stats:
            button = dict(
                label=stat,
                method="update",
                args=[{"visible": [stat == s for s in stats]}, {"title": f'Statistiques: {", ".join([s for s in stats if stat == s])}'}]
            )
            buttons.append(button)

        fig.update_layout(
            updatemenus=[
                {
                    'buttons': [
                        {'label': 'Afficher tout', 'method': 'update', 'args': [{'visible': [True] * len(fig.data)}]},
                        {'label': 'Masquer tout', 'method': 'update', 'args': [{'visible': [False] * len(fig.data)}]},
                    ],
                    'direction': 'down',
                    'showactive': True,
                },
            ],
            annotations=[
                dict(
                    x=0.5,
                    y=1.1,
                    xref="paper",
                    yref="paper",
                    text="Afficher les statistiques:",
                    showarrow=False,
                )
            ],
        )

        for i, stat in enumerate(stats):
            fig.update_layout(
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="down",
                        buttons=buttons,
                    ),
                ]
            )

        st.plotly_chart(fig)

