from molecule_3d import Chem_API 
import streamlit as st

st.title("Plot Your Own Compound!")

compound_name = st.sidebar.text_input('Name of compound', 'Fructose')

compound = Chem_API(compound_name, 'name')

st.plotly_chart(compound.plot_3d())
st.write("You can expand the above compound to full screen using the arrows above the legend.")

st.dataframe(compound.atomic_df())


# compound.plot_3d()