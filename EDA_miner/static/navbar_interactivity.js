/* These can be defined here because they exist on page creation,
   but open_menu2, closebtn2, sidenav2 are created in Dash, after
   the page loads */
var dash_content = document.getElementById("dash_content");
var sidenav = document.getElementById("sidenav");
var closebtn = document.getElementById("closebtn");
var open_menu = document.getElementById("open_menu");

/* Set the width of the side navigation to 200px and the left margin
of the page content to 250px */
function openNav() {
    dash_content.style.marginLeft = "220px";
    sidenav.style.width = "220px";
    open_menu.style.display = "none";
    document.getElementById("open_menu2").style.opacity = "1";

    setTimeout(function(){
        window.dispatchEvent(new Event("resize"))
    }, 500);
}

/* Set the width of the side navigation to 0 and the left margin
of the page content to 0 */
function closeNav() {
    dash_content.style.marginLeft = "0";
    sidenav.style.width = "0";
    open_menu.style.display = "inline-block";
    document.getElementById("open_menu2").style.opacity = "0";

    setTimeout(function(){
        window.dispatchEvent(new Event("resize"))
    }, 500);
}

/* Set the width of the side navigation to 250px and the left
margin of the page content to 250px */
function openNav2() {
    dash_content.style.marginLeft = "470px";
    closebtn.style.display = "none";
    document.getElementById("sidenav2").style.width = "250px";
    document.getElementById("open_menu2").style.opacity = "0";

    setTimeout(function(){
        window.dispatchEvent(new Event("resize"))
    }, 500);
}

/* Set the width of the side navigation to 0 and the left margin
of the page content to 0 */
function closeNav2() {
    dash_content.style.marginLeft = "220px";
    closebtn.style.display = "inline-block";
    document.getElementById("sidenav2").style.width = "0";
    document.getElementById("open_menu2").style.opacity = "1";

    setTimeout(function(){
        window.dispatchEvent(new Event("resize"))
    }, 500);
}
