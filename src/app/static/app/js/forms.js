// Restrict Elites to marathon

let routeDropdown = document.querySelector("#id_route")
let categoryDropdown = document.querySelector("#id_category")

categoryDropdown.onchange = () => {
    if (categoryDropdown.value == 1){
        routeDropdown.value = 1
    }
}

routeDropdown.onchange = () => {
    if (routeDropdown.value == 2){
        categoryDropdown.value = 0
    }
}