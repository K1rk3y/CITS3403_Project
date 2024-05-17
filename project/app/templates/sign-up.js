function selectRole(role) {
    var dropdownButton = document.getElementById('dropdownMenuButton');
    dropdownButton.textContent = role;
    document.getElementById('role').value = role;
    dropdownButton.setAttribute('aria-expanded', 'false');
    dropdownButton.nextElementSibling.style.display = 'none';
}

document.getElementById('dropdownMenuButton').addEventListener('click', function() {
    var content = this.nextElementSibling;
    var expanded = this.getAttribute('aria-expanded') === 'true';
    content.style.display = expanded ? 'none' : 'block';
    this.setAttribute('aria-expanded', !expanded);
});

window.addEventListener('click', function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.querySelectorAll('.dropdown-content');
        dropdowns.forEach(function(dropdown) {
            if (dropdown.style.display === 'block') {
                dropdown.previousElementSibling.setAttribute('aria-expanded', 'false');
                dropdown.style.display = 'none';
            }
        });
    }
}, true);
