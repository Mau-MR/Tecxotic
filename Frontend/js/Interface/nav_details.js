const navs = document.querySelectorAll(".rightside > .rightside__task > li");

navs.forEach((nav) => {

    nav.addEventListener("click", (e) => {
        document.querySelector(".nav-tab.active").classList.remove("active");
        nav.classList.add("active");

        document.querySelector('div[data-view-active="true"]').setAttribute("data-view-active", false);

        const nav_view = nav.getAttribute("data-view-name");
 
        document.querySelector(`.${nav_view}`).setAttribute("data-view-active", true);

    });
});

