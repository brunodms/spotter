document.addEventListener('DOMContentLoaded', function () {
    const dock = document.querySelector('.search-dock');
    if (!dock) return;

    const tabs = dock.querySelectorAll('.search-dock__tab');
    const input = dock.querySelector('#search-especialidade');

    tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
            tabs.forEach(function (t) { t.classList.remove('is-active'); });
            tab.classList.add('is-active');
            if (input) {
                input.value = tab.dataset.value;
            }
        });
    });
});
