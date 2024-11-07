document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('liveSearchForm');
    const searchResults = document.getElementById('searchResults');
    const searchInput = document.getElementById('searchInput');
    let typingTimeout; // Variable for timeout

    // Listen for clicks outside the search results or input field to hide the results
    document.addEventListener('click', handleClickOutsideSearch);

    // Prevent closing search results when clicking inside the input field
    searchInput.addEventListener('click', (event) => event.stopPropagation());

    // Listen for input changes and debounce the requests
    searchInput.addEventListener('input', handleSearchInput);

    // Handle form submit
    form.addEventListener('submit', handleFormSubmit);

    // Function to handle clicks outside the search results and input
    function handleClickOutsideSearch(event) {
        if (!searchResults.contains(event.target) && event.target !== searchInput) {
            hideSearchResults();
        }
    }

    // Function to handle input change and debounce the request
    function handleSearchInput() {
        const query = searchInput.value;
        
        // If the field is empty, immediately hide the results
        if (!query) {
            hideSearchResults();
            return;
        }
    
        // If the field is not empty, add a delay before sending the request
        clearTimeout(typingTimeout);
    
        typingTimeout = setTimeout(() => {
            fetchSearchResults(query);
        }, 1000); // 1 second delay after user stops typing
    }
    

    // Function to handle form submission (for initial search or pressing Enter)
    function handleFormSubmit(event) {
        event.preventDefault();
        const query = form.querySelector('input[name="q"]').value;
        fetchSearchResults(query);
    }

    // Function to fetch search results from the server
    function fetchSearchResults(query) {
        const url = form.getAttribute('data-url');
        const searchParams = new URLSearchParams({ q: query });

        fetch(`${url}?${searchParams.toString()}`, { method: 'GET', headers: { 'Content-Type': 'application/json' } })
            .then(response => response.json())
            .then(data => renderSearchResults(data))
            .catch(error => renderError(error));
    }

    // Function to render search results
    function renderSearchResults(data) {
        searchResults.innerHTML = ''; // Clear existing results

        // Render products by category
        if (Object.keys(data.results.products).length > 0) {
            for (const [category, products] of Object.entries(data.results.products)) {
                searchResults.innerHTML += renderCategory(category, products, 'Продукты:');
            }
        }

        // Render bouquets by category
        if (Object.keys(data.results.bouquets).length > 0) {
            for (const [category, bouquets] of Object.entries(data.results.bouquets)) {
                searchResults.innerHTML += renderCategory(category, bouquets, 'Букеты:');
            }
        }

        // No results found
        if (Object.keys(data.results.products).length === 0 && Object.keys(data.results.bouquets).length === 0) {
            searchResults.innerHTML = `<p class="text-muted m-2">${gettext('Нет результатов')}<i class="bi bi-emoji-frown ms-2"></i></p>`;
        }

        searchResults.style.display = 'block'; // Show search results
    }

    // Function to render a category (products or bouquets)
    function renderCategory(category, items, title) {
        const itemsHtml = items.map(item => 
            `<div><i class="bi bi-search"></i><a href="${item.url}" class="text-dark">${item.name}</a></div>`
        ).join('');
        return `<h3 class="text-dark">${title} ${category}</h3><div class="d-flex flex-column align-items-start">${itemsHtml}</div>`;
    }

    // Function to render error message
    function renderError(error) {
        console.error('Error:', error);
        searchResults.innerHTML = `<p class="text-danger m-2">${gettext('Ошибка при поиске')}<i class="bi bi-emoji-frown ms-2"></i></p>`;
        searchResults.style.display = 'block';
    }

    // Function to hide search results
    function hideSearchResults() {
        searchResults.style.display = 'none';
        searchResults.innerHTML = ''; // Clear results
    }
});
