import requests
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

class Chem_API():

    elements = pd.read_csv('Periodic Table.csv').set_index('Atomic_Number')
    elements_dict = elements.to_dict()

    atom_names = elements_dict['Name']
    atom_weights = elements_dict['Atomic_Mass']

    def __init__(self, name, data_type):
        self.name = name    
        self.data_type = data_type

    # Searches PUG API for compound and return JSON file
    def get_conformers(self):
        if self.data_type == 'SMILES':
            response = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{self.name}/conformers/json')
        else:
            response = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{self.name}/conformers/json')
        
        json_conformers = response.json()
        conformer_id = json_conformers['InformationList']['Information'][0]['ConformerID'][0]
        CID = json_conformers['InformationList']['Information'][0]['CID']
        return conformer_id, CID
    
    # Grabs conformer_id number from JSON and searches again to get 3d version in JSON
    def get_atoms_json(self):
        conformer_id = self.get_conformers()[0]
        response = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/conformers/{conformer_id}/json')
        json_file_3d = response.json()
        return json_file_3d
    
    # Create DataFrame with all these specs
    def atomic_df(self):
        json_file_3d = self.get_atoms_json()
        coordinates = json_file_3d['PC_Compounds'][0]['coords'][0]

        # Create DataFrame with all these specs
        compound_atoms = pd.DataFrame(columns=['ID', 'Atom', 'Size',
        'X Coord', 'Y Coord', 'Z Coord'])

        compound_atoms['ID'] = coordinates['aid']
        compound_atoms['Atom'] = json_file_3d['PC_Compounds'][0]['atoms']['element']
        compound_atoms['Size'] = compound_atoms['Atom'].replace(self.atom_weights)
        compound_atoms['Atom'] = compound_atoms['Atom'].replace(self.atom_names)
        compound_atoms['X Coord'] = coordinates['conformers'][0]['x']
        compound_atoms['Y Coord'] = coordinates['conformers'][0]['y']
        compound_atoms['Z Coord'] = coordinates['conformers'][0]['z']

        compound_atoms = compound_atoms.set_index('ID')

        return compound_atoms

    # Grabs CID from conformer file and pulls up additional information such as SMILES
    def get_SMILES(self):
        CID = self.get_conformers()[1]
        response = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{CID}/json')
        more_info = response.json()
        compound_SMILES = more_info['PC_Compounds'][0]['props'][18]['value']['sval']
        return compound_SMILES

    # Get coordinates for one axis
    def bond_coordinates(self, axis):
        json_file_3d = self.get_atoms_json()
        compound = self.atomic_df()

        bond_pairs = json_file_3d['PC_Compounds'][0]['bonds']
        df = pd.DataFrame({'bond1': bond_pairs['aid1'], 'bond2':bond_pairs['aid2']})
        bond_pairs_df = df.copy()

        df['coord1'] = df.bond1.map(compound[axis])
        df['coord2'] = df.bond2.map(compound[axis])

        coord_list = [[df.coord1[i], df.coord2[i], None] for i in range(df.shape[0])]
        coord_list = [item for sublist in coord_list for item in sublist]

        return coord_list, bond_pairs_df
    
    # Combine all axes coordinates into dataframe
    def bonds_coord_combined(self):
        X_list = self.bond_coordinates('X Coord')[0]
        Y_list = self.bond_coordinates('Y Coord')[0]
        Z_list = self.bond_coordinates('Z Coord')[0]

        bonds = pd.DataFrame({'X_coords': X_list, 'Y_coords': Y_list, 'Z_coords': Z_list})

        return bonds
    
    # 3D Graph of molecule with a tight layout
    def plot_3d(self):
        compound = self.atomic_df()
        bonds = self.bonds_coord_combined()

        trace1 = px.scatter_3d(compound, 
                            x='X Coord', 
                            y='Y Coord', 
                            z='Z Coord',
                            color='Atom', 
                            size='Size', 
                            size_max=50, 
                            opacity=1,
                            custom_data=['X Coord', 'Y Coord', 'Z Coord', 'Atom', 'Size'])

        trace2 = px.line_3d(bonds, x='X_coords', y='Y_coords', z='Z_coords', 
                            color_discrete_sequence=['black'])

        labels = '<b>Atom Name</b>: %{customdata[3]}<br>' + \
                 '<b>Atom Weight</b>: %{customdata[4]}<br>' + \
                 '<b>X Coord</b>: %{customdata[0]}<br>' + \
                 '<b>Y Coord</b>: %{customdata[1]}<br>' + \
                 '<b>Z Coord</b>: %{customdata[2]}<br>'

        trace1.update_traces(hovertemplate=labels)

        trace2.update_traces(hovertemplate = None, 
                             hoverinfo = "skip", 
                             line=dict(width=10))

        fig=go.Figure(data=trace1.data + trace2.data)

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=30),
                          #title=f'{self.name.capitalize()} 3D Plot',
                          width=700, height=700)
        return fig

