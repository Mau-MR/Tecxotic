const navs = document.querySelectorAll(".rightside > .rightside__task > li");
if (navs != "") {
    console.log(navs)
}
navs.forEach((nav) => {

    nav.addEventListener("click", (e) => {
        document.querySelector(".nav-tab.active").classList.remove("active");
        nav.classList.add("active");

        console.log("click")
        document.querySelector('div[data-view-active="true"]').setAttribute("data-view-active", false);
        console.log(nav)

        const nav_view = nav.getAttribute("data-view-name");
        console.log(nav_view);
        document.querySelector(`.${nav_view}`).setAttribute("data-view-active", true);

    });
});