
// Most of the below is done with the aid of AI, specifically to avoid using frameworks
// I manually debugged issues as they came up, specifically by implementing the async
// work and the init function.

const available = document.getElementById("available")
const selected = document.getElementById("selected")
const filter = document.getElementById("filter")

// Master data set
const teams = []
const url = "/teams"

async function getTeams() {
    const response = await fetch(url);
    const data = await response.json();
    data.forEach((team) => teams.push({
        // This has to be a string
        value: String(team.id),
        text: team.name
        }));
}

// Selected values
const selectedValues = new Set()

async function render() {

    const term = filter.value.toLowerCase()

    available.innerHTML = ""
    selected.innerHTML = ""

    teams.forEach(team => {

        const opt = new Option(team.text, team.value)

        if (selectedValues.has(team.value)) {

            const opt = new Option(team.text, team.value, true, true)
            selected.appendChild(opt)

        } else {

            if (team.text.toLowerCase().includes(term)) {
                available.appendChild(opt)
            }
        }
    })
}



// Move values from available to selected
function moveToSelected() {

    [...available.selectedOptions].forEach(opt => {
        selectedValues.add(opt.value)
    })

    render()
}

// Move values from selected to available
function moveToAvailable() {

    [...selected.selectedOptions].forEach(opt => {
        selectedValues.delete(opt.value)
    })

    render()
}

// Move all teams from selected back to available
function removeAll() {

    selectedValues.clear()
    render()
}

// Initialise page with values populated from database
async function init() {
    await getTeams()
    render()
}

document.getElementById("add").onclick = moveToSelected
document.getElementById("remove").onclick = moveToAvailable
document.getElementById("removeAll").onclick = removeAll

available.ondblclick = moveToSelected
selected.ondblclick = moveToAvailable

filter.addEventListener("input", render)

init()