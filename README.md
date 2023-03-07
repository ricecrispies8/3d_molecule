# 3D Molecule Plotting App

This Streamlit app allows you to plot 3D molecular structures and visualize their properties. The app uses the Pug Rest API, an third-party molecule libary created by PubChem, to generate the molecular structures and plot them using Plotly.

## Getting Started

There are no prerequisites needed to run the app. Simply navigate to [the app](https://3d-molecule.streamlit.app/) and follow the prompts.

*Note: Only covalently bonded molecules will work with this app. Ionic bonds cannot be plotted (as of this version). This means some common compounds such as salts will not work currently as there are no bond distances to place into the plot.*

## Using the App

To use the app, enter in a favorite molecule name. Common names and IUPAC names are acceptable. The app will automatically generate a 3D plot of the molecule, which you can manipulate using the mouse. All atoms are plotted and visualized according to size.

The 3D conformation is NOT an average of all conformations, but just the first conformation listed in the Pug Rest API.
