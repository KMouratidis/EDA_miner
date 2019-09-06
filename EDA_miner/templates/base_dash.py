# TODO: Convert this to HTML when finished with the changes
# TODO: Night-mode. It should be 1) a script that adds a "night-mode"
#       class to the EVERY element of the page and 2) a CSS overwriting
#       every element's colors to the night mode.

dash_appstring = """
<!DOCTYPE html>
<html>
    <head>

        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-143785705-1"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'UA-143785705-1');
        </script>


        <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/react-dom@15.4.2/dist/react-dom.min.js"></script>
    
        <link rel="stylesheet" type="text/css"
            href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" />
        <link rel="stylesheet" type="text/css"
            href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" />
        <link rel="stylesheet" type="text/css"
            href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.bundle.min.js" />
    
        <link rel="stylesheet" type="text/css" 
              href="https://use.fontawesome.com/releases/v5.8.1/css/all.css">
        <link rel="stylesheet" type="text/css" 
              href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        
        <link rel="stylesheet" type="text/css"
            href="/static/css/10_plotly_base.css" />
        <link rel="stylesheet" type="text/css"
            href="/static/css/20_site-wide_dash.css" />
        <link rel="stylesheet" type="text/css"
            href="/static/css/navbar.css" />
        <link rel="stylesheet" type="text/css"
            href="/static/css/viz_app.css" />
        <link rel="stylesheet" type="text/css"
            href="/static/css/model_app.css" />
        <link rel="stylesheet" type="text/css"
            href="/static/css/docs_app.css" />
            
        {%metas%}    
        {%favicon%}
        {%css%}

        <title>EDA Miner</title>
    
    </head>
    
    <body>

<!--   SIDEBAR     -->
        <div style="height: 100%">
            <div id="sidenav" class="sidenav">

                <img src="/static/images/y2d.png" id="app_logo"></img>
                
                <a class="closebtn" id="closebtn" 
                        onclick="closeNav()">
                    <i class="fas fa-times">
                    </i>        
                </a>
    
                <a href="/" class="nav_links">
                    <i class="fas fa-home">
                        <span>Home</span>
                    </i>
                </a>
                <a href="/data/" class="nav_links">
                    <i class="fas fa-database">
                        <span> Data</span>
                    </i>
                </a>
                <a href="/visualization/" class="nav_links">
                    <i class="fas fa-eye">
                        <span>Visualization</span>
                    </i>
                </a>
                <a href="/modeling/" class="nav_links">
                    <i class="fas fa-laptop-code">
                        <span>Modeling</span>
                    </i>
                </a>
                
                <div id="accordion">
                    <a data-toggle="collapse" data-target="#collapseOne"
                        aria-expanded="true" aria-controls="collapseOne"
                         class="nav_links"  id="headingOne">
                        <i class="fas fa-caret-square-down">
                            <span>External links</span>
                        </i>
                    </a>
                    
                    <div id="collapseOne" class="collapse show" 
                        aria-labelledby="headingOne" data-parent="#accordion">
                        
                        <div>
                            <a href="https://github.com/KMouratidis/EDA_miner_public" 
                                class="nav_links2">
                                <i class="fab fa-github">
                                    <span class="fas"> GitHub repo </span>
                                </i>
                            </a>
                            <a href="https://dash.plot.ly/" class="nav_links2">
                                <i class="fas fa-link">
                                    <span class="fas"> Dash docs </span>
                                </i>
                            </a>
                            <a href="/docs" class="nav_links2">
                                <i class="fas fa-link">
                                    <span class="fas"> Our docs </span>
                                </i>
                            </a>
                            
                            
                        </div>
                    </div>
                    
                </div>

            </div>
            



<!--   DASH APP     -->

            <span onclick="openNav()" class="open_menu" id="open_menu">
                <i class="fas fa-angle-double-right"></i>
            </span>

            <div id="dash_content" class="app0">
                        
                {%app_entry%}
            </div>
        </div>


<!--   OTHER STUFF     -->

        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}


            <script src="/static/navbar_interactivity.js"></script>


        </footer>
    </body>
</html>
"""