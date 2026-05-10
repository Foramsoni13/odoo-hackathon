import re

with open('templates/home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the control bar buttons to be `<select>`
new_controls = '''    <select class="ctrl-btn" id="groupBy">
      <option value="">Group by</option>
      <option value="upcoming">Status: Upcoming</option>
      <option value="planned">Status: Planned</option>
      <option value="ongoing">Status: Ongoing</option>
    </select>
    <select class="ctrl-btn" id="filterBy">
      <option value="">Filter Category</option>
      <option value="all">All</option>
      <option value="romantic">Romantic</option>
      <option value="scenic">Scenic</option>
      <option value="luxury">Luxury</option>
      <option value="adventure">Adventure</option>
    </select>
    <select class="ctrl-btn" id="sortBy">
      <option value="">Sort by...</option>
      <option value="price_asc">Price: Low to High</option>
      <option value="price_desc">Price: High to Low</option>
    </select>'''

html = re.sub(
    r'<button class="ctrl-btn">Group by ▾</button>\s*<button class="ctrl-btn">Filter ▾</button>\s*<button class="ctrl-btn">Sort by\.\.\. ▾</button>',
    new_controls,
    html
)

# 2. Add data- attributes to cards for easy JS sorting/filtering

# Top Regional Selections (destinations)
# Venice
html = html.replace('<div class="dest-card">', '<div class="dest-card" data-name="Venice Italy" data-price="70000" data-cat="romantic" data-type="dest">', 1)
# Santorini
html = html.replace('<div class="dest-card">', '<div class="dest-card" data-name="Santorini Greece" data-price="95000" data-cat="scenic" data-type="dest">', 1)
# Dubai
html = html.replace('<div class="dest-card">', '<div class="dest-card" data-name="Dubai UAE" data-price="60000" data-cat="luxury" data-type="dest">', 1)
# Rio
html = html.replace('<div class="dest-card">', '<div class="dest-card" data-name="Rio de Janeiro Brazil" data-price="78000" data-cat="adventure" data-type="dest">', 1)

# Previous Trips (trips)
# Bali
html = html.replace('<div class="trip-card">', '<div class="trip-card" data-name="Bali Indonesia" data-price="95000" data-status="upcoming" data-type="trip">', 1)
# Paris
html = html.replace('<div class="trip-card">', '<div class="trip-card" data-name="Paris France" data-price="225000" data-status="planned" data-type="trip">', 1)
# Tokyo
html = html.replace('<div class="trip-card">', '<div class="trip-card" data-name="Tokyo Japan" data-price="250000" data-status="ongoing" data-type="trip">', 1)

# 3. Add Script for Filtering and Sorting
script = '''
<!-- FILTER AND SORT LOGIC -->
<script>
document.addEventListener("DOMContentLoaded", function() {
    const searchBox = document.getElementById("searchBox");
    const groupBy = document.getElementById("groupBy");
    const filterBy = document.getElementById("filterBy");
    const sortBy = document.getElementById("sortBy");

    function applyFilters() {
        const query = searchBox.value.toLowerCase();
        const group = groupBy.value;
        const filter = filterBy.value;
        
        // Destinations
        const destGrid = document.querySelector(".dest-grid");
        let destCards = Array.from(destGrid.querySelectorAll(".dest-card"));
        
        destCards.forEach(card => {
            const name = card.getAttribute("data-name").toLowerCase();
            const cat = card.getAttribute("data-cat");
            
            let show = name.includes(query);
            if (filter && filter !== "all" && cat !== filter) show = false;
            if (group) show = false; // "Group by" status only applies to trips, hide destinations if grouping by status
            
            card.style.display = show ? "" : "none";
        });
        
        // Trips
        const tripsGrid = document.querySelector(".trips-grid");
        let tripCards = Array.from(tripsGrid.querySelectorAll(".trip-card"));
        
        tripCards.forEach(card => {
            const name = card.getAttribute("data-name").toLowerCase();
            const status = card.getAttribute("data-status");
            
            let show = name.includes(query);
            if (group && status !== group) show = false;
            if (filter && filter !== "all") show = false; // Filter category only applies to destinations
            
            card.style.display = show ? "" : "none";
        });
        
        // Sorting
        const sortVal = sortBy.value;
        if (sortVal) {
            // Sort Destinations
            destCards.sort((a, b) => {
                let pa = parseInt(a.getAttribute("data-price"));
                let pb = parseInt(b.getAttribute("data-price"));
                return sortVal === "price_asc" ? pa - pb : pb - pa;
            });
            destCards.forEach(card => destGrid.appendChild(card));
            
            // Sort Trips
            tripCards.sort((a, b) => {
                let pa = parseInt(a.getAttribute("data-price"));
                let pb = parseInt(b.getAttribute("data-price"));
                return sortVal === "price_asc" ? pa - pb : pb - pa;
            });
            tripCards.forEach(card => tripsGrid.appendChild(card));
        }
    }

    searchBox.addEventListener("input", applyFilters);
    groupBy.addEventListener("change", applyFilters);
    filterBy.addEventListener("change", applyFilters);
    sortBy.addEventListener("change", applyFilters);
});
</script>
</body>
'''
html = html.replace('</body>', script)

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Added workable functionality to home.html')
