from molecule_3d import Chem_API 
import streamlit as st

st.markdown('''
# 3D Compound Visualization

Being able to visualize a compound is essential for understanding how a molecule functions. This simple tool will show the molecule's bonds and coordinates for a typical orientation of a molecule. 

This project uses the [PubChem API](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) to obtain the cooridinates for any of the 114 million compounds listed in it's database. 

Watch for additional features in the near future!
 ''')

compound_name = st.text_input('Enter in the name of a compound:', 'Fructose')

compound = Chem_API(compound_name, 'name')

tab1, tab2 = st.tabs(["Chart", "Data"])

with tab1.container():
    st.header(f'{compound.name.capitalize()} Plot')
    st.markdown("_Go full-screen using the arrows above the legend._")

    with st.spinner("Your molecule is loading..."):
        st.plotly_chart(compound.plot_3d(), use_container_width=True)

with tab2.container():
    st.header(f'{compound.name.capitalize()} Data')
    with st.spinner("Your molecule is loading..."):
        st.dataframe(compound.atomic_df())