# Contributor guidelines

As you are probably aware, this project is almost entirely written in Dash, Python. There are very few Javascript snippets here and there, and there are also some custom Dash components made with React. For CSS this project uses part of Dash's defaults, some Bootstrap, and of course some custom sheets. 

## Table of contents

* [Learning resources](#learning-resources)
* [Style guide recommendations](#style-guide-recommendations)
* [General info on project structure](#general-info-on-project-structure)
* [General info on contributions](#general-info-on-contributions)
  * [Contributions for visualizations](#contributions-for-visualizations)
  * Contributions for databases

## Learning resources

* Basics: To write Dash, you just need a basic knowledge of HTML. It is probably impossible to contribute without first going over the The [Dash docs](https://dash.plot.ly/), which are also the best place to start your reading. Going through their tutorial, and then taking a quick look on each component library listed should get you up to speed with what you need to know about callbacks, the main feature of Dash, and more. 
* Visualizations: Dash steps on the shoulders of plotly for its visualizations, so if you are interested in working on visualizations take a look at the [Plotly docs](https://plot.ly/python/) page, and/or at [D3.js for Dash](https://dash.plot.ly/d3-react-components) from the Dash docs. 
* Custom components / React: If you're a JS wiz with a react spellbook, then we love you a bit more (you can design your own components!). You can start working with custom components, and React, Javascript. Take a quick look at what these Dash docs page say: [React for Python Developers](https://dash.plot.ly/react-for-python-developers), and [Writing your own components](https://dash.plot.ly/plugins).
* Machine Learning: There are hundreds of material out there and we won't go over them here but familiriaty with sklearn and its programmatic API is strongly desired (see [Quickstart](https://scikit-learn.org/stable/tutorial/basic/tutorial.html), [User guide](https://scikit-learn.org/stable/user_guide.html), [API reference](https://scikit-learn.org/stable/modules/classes.html), [Developers guide](https://scikit-learn.org/stable/developers/index.html), especially the [Estimators](https://scikit-learn.org/stable/developers/contributing.html#estimators) chapter). 

## Style guide recommendations

You need to write at least somewhat pythonic code. A few good starting points are: [PEP-8](https://www.python.org/dev/peps/pep-0008/) and [The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/style/). Also take a quick look at [this quick discussion](https://docs.python-guide.org/writing/structure/) about project structure (mentioned again later).

Regarding imports, consider this a personal peculiarity but it seems far easier to find stuff when they are in a particular order, with a line separating each category: 
1. Import the core Dash libraries (e.g. `dash`, `dcc`, `html`, `daq`, dash_table`)
2. Import other Dash components including any custom (e.g. `visdcc`, `dash_rnd`)
3. Import modules from the app: first `server.app`, then other high-level modules, then anything else ordered by depth.
4. Import any other libraries necessary.

<details>
  <summary>Example</summary>

```from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import visdcc

from server import app
from utils import cleanup, r
from menus import SideBar, MainMenu, landing_page
from apps import data_view, exploration_view
from apps.exploration_tabs import KPIs

from functools import partial
import pandas as pd
```
</details>

**Naming is extremely important.** Use plural for lists (e.g. `traces = [scatter]`) and singular with optional numbering for sole items (e.g. `trace1 = scatter`). Edit away others' work if necessary, and feel free to suggest more rules that will help us keep our sanity.

## General info on project structure

This project spans multiple files and directories. Although our efforts have been geared towards packing logical units together, the nesting that resulted seems less than ideal and we may restructure it a bit. There are multiple ways to get acquainted with said folder structure. Visiting the `/images` folder you will find `eda_miner_callback_chain.html` which is the Dash-rendered graph showing every function in the project (also found as images, divided over several screenshots). Another way is to look directly at the `directory_tree.png`, (made with the linux `tree` command).

It is extremely likely that after these you will still want an explainer; don't worry, even I spent much time searching around for the right file, more than I want to admit (and if you're awesome at structuring python projects... `;D`). The rough idea is as follows:
- Top level modules define the overall app including some utils; probably not the place to start playing.
- `/assets` is the place to go if you feel like adding some custom JS/CSS or storing your images
- `/apps/` is the place where the main logic happens. Each tab (top-level/level-1 menu) has its own:
  - `something_view.py` file which renders the main layout (level-2 menu). This simply delegates to the appropriate sub-module.
  - `something` package (folder), which defines the content for each choice of the level-2 menu.
    - The layout of the content div is defined here, usually a few dropdowns including any potential output (usually graphs, tables, ML stuff, or their placeholders)
    - A callback delegating the final call to your results (e.g. the actual rendering of the graphs)
    - Any other folder with package-specific utilities

We are not yet too keen on having this structure, but one with less modules feels slightly off as well considering the direction we want to take. Suggestion on this end are also welcome.

## General info on contributions

**Almost everything here is a soft suggestion, not hard requirement. If you're confident in your coding, don't pay too much attention to these guidelines, do your thing.**

For now, modules in the top level of the app should probably not be modified. For other modules, there are docstrings with a few more words on whether work is encouraged in those modules. Do note:  *Any and every contribution is welcome*; those modules are just marked as such to notify beginners to be cautious, or they merely mark areas where we think improvements are needed - and easy to implement. Each module has its own guidelines (see `Notes to others` section at the top), which are there to give you a gereral idea of what you could do. **Advanced users can safely ignore all that. If you want to contribute but don't know where to start, find issues marked with `good first issue`.**  If you have some standalone code that works but don't know where that fits into the project, open an issue or a pull request. A few examples:
- Stylistic elements (UI/UX, CSS, themes, graph coloring)
- API integrations, data gathering & handling
- Machine Learning Algorithms (classes with a sklearn-like API: `.fit`, `.predict`, `.transform`)

### Contributions for visualizations

Dash graphs are mainly done in plotly, and we don't promise much for other libraries (but fire away anyway!). We have tried our hands at using matplotlib which somewhat works (plotly has some integration). D3 visualizations should also be possible and are welcome. If you want to wrap some JS library as a collection of React components then that is great as well. You will also probably find discussions about integrating Dash with other visualization tools (such as for folium, e.g. [here](https://community.plot.ly/t/folium-maps-and-dash/6956) and [here](https://community.plot.ly/t/dash-and-folium-integration/5772)).

### Contributions for databases

TBW...

