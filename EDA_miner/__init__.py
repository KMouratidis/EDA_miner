"""
Welcome to EDA Miner!

Usage walk-through:
We strive to create a simple and intuitive interface. The app is meant to \
be run in a central server and accessed via web, but can of course be run \
locally, too.

Upon visiting the page you will be directed to the "Data View" tab where \
you upload your own datasets, connect to APIs, or view the data you have \
uploaded. When viewing your data, each API displays data in different \
ways, although actually using those data is not yet implemented (May 2019).

As soon as you have uploaded a dataset, the other two tabs become \
functional. The first stop would be the "Explore & Visualize" tab. \
Here you will find options to plot your data; each sub-tab contains \
a different class of visualizations.
    - Exploratory analysis: contains all the 2D graphs, including \
                            matplotlib-generated pairplots.
    - Key performance indicators: currently implements only a baseline \
                                  graph, but we plan to implement \
                                  functionality so you can create your \
                                  own KPIs, and we want to add additional \
                                  analysis tools.
    - 3D graphs: currently only plots 3D scatterplots.
    - Network graphs: use Cytoscape.js to create graph/network \
                      visualizations, allowing various layout choices.
    - Text visualizations: currently only allow for creating simple word \
                           clouds (from given text), but plans for further \
                           integration and more visualizations include \
                           word vector visualization.
    - PDF report: allows you to create reports using the figures you \
                  plot in the other tabs (using the "export graph \
                  config" buttons) and add custom text, headers, titles.


Finally, in the "Analyze & Predict" tab you are able to use your \
data to train Machine Learning models. The Model builder can be \
used to create more advanced pipelines (including defining your own \
features). The default steps are to first define the model fully \
(or some features may not work), then go over every node you want to \
customize and change its node options, and when you're done export the \
model ("convert to model" button). Finally, head over to the "Pipelines \
trainer" tab, select and train your model. If you want to run simpler \
models, there are additional tabs with the most common types of problems.


Project structure:
    Contributors wanting to familiarize themselves with the project \
    structure can take a look at the contributor guidelines \
    (https://github.com/KMouratidis/EDA_miner_public/wiki/Style-guide-and-contributor-guidelines). \
    You can also go through all the files and read the module docstrings \
    that have rough guidelines about contributions. In the Python \
    spirit, feel free to completely ignore them.
"""