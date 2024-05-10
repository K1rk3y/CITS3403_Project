const charactersList = document.getElementById('charactersList');
const searchBar = document.getElementById('searchBar');
let hpCharacters = [];

searchBar.addEventListener('keyup', (e) => {
    const searchString = e.target.value.toLowerCase();

    const filteredCharacters = hpCharacters.filter((character) => {
        return (
            character.title.toLowerCase().includes(searchString) ||
            character.course.toLowerCase().includes(searchString) ||
            character.cuisine.toLowerCase().includes(searchString) ||
            character.mainIngredient.toLowerCase().includes(searchString) 


        );
    });
    displayCharacters(filteredCharacters);
});

const loadCharacters = async () => {
    try {
        const res = await fetch('https://api.sampleapis.com/recipes/recipes');
        hpCharacters = await res.json();
        displayCharacters(hpCharacters);
    } catch (err) {
        console.error(err);
    }
};

const displayCharacters = (characters) => {
    const htmlString = characters
        .map((character) => {
            return `
            <li class="character">
                <h3>${character.title}</h3>
                <p>Course: ${character.course}</p>
                <p>Cuisine: ${character.cuisine}</p>
                <p>Main Ingredient: ${character.mainIngredient}</p>
            </li>
        `;
        })
        .join('');
    charactersList.innerHTML = htmlString;
};

loadCharacters();
