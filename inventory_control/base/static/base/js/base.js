jQuery(function() {
    const currentLocation = location.pathname;
    const $menuItems = $(".nav-link");

    $.each($menuItems, (_, menu) => {
        const $menu = $(menu);

        if ($menu.attr("href") === currentLocation) {
            $menu.attr("class", "nav-link active");
        } else {
            $menu.attr("class", "nav-link link-dark");
        }
    });

    // Habilitar os toats de notificação
    $(".toast").toast("show");
});