# Contributor guidelines

As you are probably aware, this project is almost entirely written in Dash, Python. There are very few Javascript snippets here and there, and there are also some custom Dash components made with React. For CSS this project uses part of Dash's defaults, some Bootstrap, and of course some custom sheets. 

## Table of contents

* [Learning resources](#learning-resources)
* [Style guide recommendations](#style-guide-recommendations)
* [General info on project structure](#general-info-on-project-structure)
* [General info on contributions](#general-info-on-contributions)
  * [Contributions for code quality](#contributions-for-code-quality)
  * [Contributions for visualizations](#contributions-for-visualizations)
  * [Contributions for data](#contributions-for-data)
  * [Contributions for modeling](#contributions-for-modeling)
  * [Contributions for deployment and scaling](#contributions-for-deployment-and-scaling)
* [List of contributors](#list-of-contributors)

## Learning resources

* Basics: To write Dash, you just need a basic knowledge of HTML. It is probably impossible to contribute without first going over the The [Dash docs](https://dash.plot.ly/), which are also the best place to start your reading. Going through their tutorial, and then taking a quick look on each component library listed should get you up to speed with what you need to know about callbacks, the main feature of Dash, and more. 
* Visualizations: Dash steps on the shoulders of plotly for its visualizations, so if you are interested in working on visualizations take a look at the [Plotly docs](https://plot.ly/python/) page, and/or at [D3.js for Dash](https://dash.plot.ly/d3-react-components) from the Dash docs. 
* Custom components / React: If you're a JS wiz with a react spellbook, then we love you a bit more (you can design your own components!). You can start working with custom components, and React, Javascript. Take a quick look at what these Dash docs page say: [React for Python Developers](https://dash.plot.ly/react-for-python-developers), and [Writing your own components](https://dash.plot.ly/plugins).
* Machine Learning: There are hundreds of material out there and we won't go over them here but familiriaty with sklearn and its programmatic API is strongly desired (see [Quickstart](https://scikit-learn.org/stable/tutorial/basic/tutorial.html), [User guide](https://scikit-learn.org/stable/user_guide.html), [API reference](https://scikit-learn.org/stable/modules/classes.html), [Developers guide](https://scikit-learn.org/stable/developers/index.html), especially the [Estimators](https://scikit-learn.org/stable/developers/contributing.html#estimators) chapter). 

## Style guide recommendations

You need to write at least somewhat pythonic code. A few good starting points are: [PEP-8](https://www.python.org/dev/peps/pep-0008/) and [The Hitchhiker's Guide to Python](https://docs.python-guide.org/writing/style/). Also take a quick look at [this quick discussion](https://docs.python-guide.org/writing/structure/) about project structure (mentioned again later).

Regarding imports, it seems to me far easier to find stuff when they are in a particular order, with a line separating each category: 
1. The core Dash libraries (e.g. `dash`, `dcc`, `html`, `daq`, `dash_table`) and other Dash components including any custom (e.g. `visdcc`, `dash_rnd`)
2. Import modules from the app: first `server.app`, then other high-level modules, then anything else ordered however you like.
3. Import any other libraries necessary, ordered by fancy points.

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

import turtle
from functools import partial
import pandas as pd
```
</details>

**Naming is extremely important.** Use plural for lists (e.g. `traces = [scatter]`) and singular with optional numbering for sole items (e.g. `trace1 = scatter`). Edit away others' work if necessary, and feel free to suggest more rules that will help us keep our sanity. Also, if you find some names weird, flame the author hard and suggest alternatives.

## General info on project structure

The older project structure was a mess, but I hope the new one (post v0.3, aka 19th August 2019) is much cleaner. The app is structured as a main Flask app (responsible for user management, mainly) which connects various other Flask and Dash apps at the WSGI level with Werkzeug's [DispatcherMiddleware](https://werkzeug.palletsprojects.com/en/0.15.x/middleware/dispatcher/). If you want to add a new app all you need to do is follow the instruction in the `wsgi.py` file (i.e. register the flask extensions and give it a URL path). 

You can get acquainted with the project by looking at `/docs` after starting the app, or (equivalently) reading the module and package docstrings. Another way is by visiting the `/images` folder where you will find an old version of `eda_miner_callback_chain.html` which was the Dash-rendered graph showing every function in the project (also found as images, divided over several screenshots) on `v0.2`. Another way is to look directly at the `directory_tree.png`, (made with the linux `tree` command).

It is extremely likely that after these you will still want an explainer; don't worry, anyone working on the project will be more than happy to help you (see Contact section). Anyhow, here is the rough idea:
- Top level modules define the overall app (Flask server, models, forms, flask extensions) including some utils; probably not the place to start playing.
- `/static` and `/templates/` are the place to go if you feel like adding some custom JS/CSS (or HTML for the main Flask app) or storing your images.
- App folders; these are (almost-)standalone applications in either Dash/Flask (maybe Django?). If you want to create an extension that does something more elaborate or separate than existing apps, or just want to add your pre-existing Dash/Flask apps, you create a new directory and do it (remember to visit `wsgi.py`!). Here are a three of them:
  - `data`: This Dash app contains all the logic for the user to handle data, be it uploading data or fetching them from an API. It also detects a data schema following some heuristics, and allows the user to edit it. Found at `/data`, and needs login.
    - Contents of each app are largely up to you. We will soon release a "mini-app" template with more detailed instruction so you can use that as a reference.
    - Current apps usually include a `server.py` (Dash config & definition) and an `app.py` (index page) file as well as different python files for each sub-page (we usually use tabs as a navigation method, feel free to deviate). 
  - `docs` is a standalone app that parses the rest of the python codebase as strings, extracts docstrings and automatically creates an API reference page found at `/docs` (no login required).
  - `google_analytics` is a REST API built with Flask and runs completely independently of the main Flask server. It was initially created as a separate "micro-service" because of an incompatibility with the libraries that we used but that is no longer the case. Still, we decided to keep it mainly for demonstration purposes. Go over to `/data/data_utils/api_layouts` to see how `GAnalyticsAPI` interacts with it.

Suggestion on project structure are also welcome.

## General info on contributions

**Almost everything here is a soft suggestion, not a hard requirement. If you're confident in your coding, don't pay too much attention to these guidelines.**
> Do the thing <br>
> -Varrick, inventor, businessman, rebel.

For now, modules in the top level of the app should probably not be modified, unless you're an experienced dev (optionally with Flask knowledge). For other modules, there are docstrings with a few more words on whether work is encouraged in those modules. Do note:  *Any and every contribution is welcome*; those modules are just marked as such to notify beginners to be cautious, or they merely mark areas where we think improvements are needed most - and are easy to implement. Each module as well as each package has its own guidelines (see `Notes to others` section of each), which are there to give you a gereral idea of what you could do. That said, docstrings are somewhat outdated as of this writing (19th August 2019).

**Advanced users can safely ignore all that. If you want to contribute but don't know where to start, find issues marked with `good first issue` in GitHub Issues.**  If you have some standalone code that works but don't know where that fits into the project, open an issue or a pull request. A few examples:
- Stylistic elements (UI/UX, CSS, themes, graph coloring)
- API integrations, data gathering & handling
- Machine Learning Algorithms (classes with a sklearn-like API: `.fit`, `.predict`, `.transform`)
- Custom React components (e.g. resize-n-drag).

Also, if you have suggestions open an issue with a "feature request" tag. A few suggestions on good (and potentially easy) contributions that are really needed (and not mentioned below):
- Writing function/class/module docstrings
- Writing tutorials on the usage of the app
- Writing tutorials for helping other contributors
- Writing (unit-)tests
- Benchmarking (parts or all of the app, libraries, other tools used)

### Contributions for code quality

With v0.3 I tried quite a lot to improve code quality; that is to make everything more readable, with more/better comments and docstrings, cleaner and visually appealing, as well as make it simpler for new contributors to do their thing. I believe I did well (not perfect) with `/data/apis` where you have clear instructions on how to make a new API connection, and then the rest is handled for you. I probably didn't help with `/visualization`. I know I failed super hard with `/modeling/model_builder`; a few times it made me want to cry (thank you, *pizza*, for the emotional support!). **Helping here is HUGELY APPRECIATED**. Really. If you are a brave soul and attempt it, do not hesitate to spam and flame me with questions till I cry.

### Contributions for visualization

Dash graphs are mainly done in plotly, and we don't promise much for other libraries (but fire away anyway!). We have tried our hands at using matplotlib which somewhat works (plotly has some integration). D3 visualizations should also be possible and are welcome. If you want to wrap some JS library as a collection of React components then that is great as well. You will also probably find discussions about integrating Dash with other visualization tools (such as for folium, e.g. [here](https://community.plot.ly/t/folium-maps-and-dash/6956) and [here](https://community.plot.ly/t/dash-and-folium-integration/5772)).

Visualization is currently handled by the `/visualization` app. It is split across 6 modules but might be trimmed in the future. These modules are (and some ideas on what can be done):
- ChartMaker: Handling basic 2D and 3D visualizations which are built using individual traces, much like a poor man's ripoff of [Plotly's Online Graph Maker](https://plot.ly/create/#/). Other modules (e.g. maps, kpis) might be integrated here.
- KPIs: Handling... KPIs! Currently it only calculates a simple Baseline (without any sort of filtering). You could augment the baseline by adding filters (e.g. for promo dates), or new KPIs, or even allow users to create their own.
- Maps: Currently only two types of maps are supported, choropleths, geoscatters (and a combination), and "lines on map", all from Plotly. You could add more, or provide more options, even mapping functionality with/from other libraries and providers.
- Networks: Very basic network/graph visualizations. Currently it has trouble handling more than a couple hundred nodes so that is one possible way to contribute. Also, styles and interactivity for the cytoscape graph. You might also want to try integration with networkx or other libraries.
- Text visualizations: For now it only handles a simple wordcloud. Feel free to add additional visualizations, but do leave word-vector visualizations for later (or use very small models) since increasing server boot time is an issue.
- DashboardMaker: Create your own dashboards, Power BI style. Not quite, because the drag-and-resize is not yet complete, and a lot of stuff still need to be done; so that's your cue, React wizs ;)

### Contributions for data

Everyone needs data to work with, and currently there are two ways ways to get data: the user can upload a file, or we can connect to their account somewhere and fetch data via an API. After that, the user should be able to inspect and edit both the data and the inferred schema. Here are a few suggestions on what you could do:
- Connections to APIs: Currently only 6 connections to APIs are supported (Google Analytics, Google Drive / Spreadsheets, Twitter, Quandl, Spotify, and Reddit). For these connections, we only access a very limited subset of what their APIs offer (e.g. only playlists for Spotify), so this is one thing you can work on. If you want to customize the API connections or create a new one, you need to subclass `APIConnection` from `/data/data_utils/api_layouts.py`. Basically it needs two Dash layouts (giving credentials, and getting data after successful authentication), a (potentially dummy) method to prettily display fetched results, a `connect` method (to connect to the API), and a `fetch_data` method to actually get the data and save it as a `pandas.DataFrame` (use the inherited `save_data_and_schema`).
- Uploading data: A simple box where the user can drag-n-drop files (or click/navigate/open) to upload. A few things can be done here like adding supported for different filetypes (currently only csv, json, xls/x, and feather are supported), or handling large file uploads (see also [Dash Resumable Upload](https://community.plot.ly/t/show-and-tell-dash-resumable-upload/9519)).
- Schema inference: Responsible for detecting the data types of the various columns, using (currently) heuristics. You can improve the heuristics, create a better interface for viewing the data (e.g. with pagination), or other (?).
- View data: A Dash DataTable for inspecting the data. Potential improvements here include handling pagination, editting better (e.g. save edits), and schema-relevant operations (e.g. categorical columns svisualizationshould have a dropdown). 
- **New features**:
  - Ability to connect datasets with a schema, like in SQL.
  - Concatenate datasets (columns/rows).
  - Permanent storage of data fetched from APIs, e.g. by concatenating previous results. This is important.
  - Query the data with an SQL-like syntax (with or without a front-end GUI) or natural language (text2sql).
  - Create new columns/features using formulas. Spreadsheets can handle it, so why not us too? *This used to be part of the FeatureMaker class in the ModelBuilder but was removed for convenience*.

### Contributions for modeling

This app is responsible for training Machine Learning (Data Mining, Business Intelligence, Statistics, whatever) models. If you want to train a simple model, the `single_model.py` module handles that case, but if you want something more complex then you would have to go to the `model_builder.py`, define a custom pipeline, and switch over to `pipelines.py` to train it. Each is accessible by selecting its respective tab.
- Single model: A simple GUI with few dropdowns to select dataset and variables, and a div with tabs for showing the various result types (currently 2: text metrics like accuracy, confusion matrix, MSE, and graphical results).
- Model Builder: Using `dash-cytoscape` we use graph nodes to represent the various "estimators" (using sklearn language). Every model class **MUST** conform to the sklearn API (fit, predict, transform). You can add new models/classes (see `/modeling/models/pipeline_classes.py`). If you are brave enough, you can try converting cytoscape graphs to models (see `/modeling/models/graph_structures.py`) and/or creating pipelines from them (see `/modeling/models/pipeline_creator.py`) as well as training them (see `/modeling/pipelines.py`).

### Contributions for deployment and scaling

Up to now, deployment has not been that much of a concern because I was mostly handling it on my own. However, as the app grows and is tied to other services (Redis, google_analytics, some other SQL soon?) we will need a better way to handle this. Currently I'm working a bit on a `docker-compose` script, especially since docker seems the best way to package and set-up the whole project. 

The idea behind splitting up the various apps was due to two reasons: allowing for easier addition of new apps (which was achieved), and allowing each app to scale independently (which is currently not done at all). Connecting Flask and Dash apps at the WSGI level is easy and allows for the `login_manager` and other extensions to be connected easily. It is possible that connecting these extensions does not need all apps to be under the same server, but I simply don't know about that stuff and will look into them later on. If not, then each app will have to be separable and get its own url and connected via another dispatcher / proxy (e.g. see [Werkzeug's HTTP Proxy](https://werkzeug.palletsprojects.com/en/0.15.x/middleware/http_proxy/)). If you have other suggestions, or know a way to pass user session / information in a secure way across Dash/Flask apps, those would be **extremely welcome** as well.

Scaling and performance are issues I didn't concern myself with so far, at least not much. Since v0.3 some early attempts have been made in improving performance:
- Instead of loading datasets from Redis every time we need to create options according to dataset columns, we load the data schema which is a small dict growing only according to number of columns. The same principle applies to other parts where data copying has decreased.
- Caching (memoization) and expiration for Redis data were added to a lot of API calls, and will probably be added to a lot more.
That said, a lot of performance upgrades can still be done, including overall scaling. Here are some ideas:
- Some plotly visualizations can benefit from either using OpenGL or performing aggregations in Python before plotting. This lessens the burden both for internet bandwidth and the browser, at the potential cost of graphing precision. For more than a few hundred/thousand data points these are probably worth it.
- The pre-v0.2 application could be scaled by simply creating more containers. This can be done now, too, but it would be a waste (and the user database would need some extra handling). Instead, each app should be scaled on its own (see previous paragraph).
- Currently CI/CD is lacking. I am using a custom Python script to copy files, create docs, run tests, update coverage, and remove non-public code from the private version (as of 19th August 2019 there is no such code: the login has been just integrated, export to PDF has been dropped completely). Integration with TravisCI and other tools exist but are at an early stage. I will be looking into this a bit more over the coming months, as well as tools like Ansible and Jenkins. If you know about these, do lend a hand or tips.
- Deployment: I used to have it deployed on an old computer of mine but now it is deployed on Amazon (pre-v0.2), sponsored by Prof. Ioannis Magnisalis ([website](http://magnio.tech/)). Neither of us look hard enough into this; a different Amazon service may be more fitting, or a combination of them. Reach out to either of us for suggestions or details.

### List of contributors

<details>
<summary>Notice</summary>
I try to keep them in alphabetical order, edit if you notice inconsistencies! Also, note that most contributions are not visible in the public version of the repository.
</details>

- **Active** (as of 19th August 2019):
  - **Gkoustilis George**, promotion, and asking tough questions.
  - **Magnisalis Ioannis**, oversight of the project, including academic and implementation guidance.
  - **Mouratidis Kostas**, everything related to code.
  - **Tentsoglidis Iordanis**, mostly the theoretical part, and university promotion.
- **Past**:
  - **Katrilakas George**, mostly the theoretical part, and a bit on treemaps.
  - **Timamopoulos Chris**, mostly the theoretical part, and a bit on 3D scatteroplot.
  - **Tsichli Vaso**, most of the graphs, a bit on model fitting reporting, LOTS of suggestions for the interface. Patient receiver of my spam.
