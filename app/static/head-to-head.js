var selectOne = document.getElementById("firstTeam")
var selectTwo = document.getElementById("secondTeam")

// master data set
const teams = []
const url = "/teams"

async function getTeams() {
    const response = await fetch(url);
    const data = await response.json();
    data.forEach((team) => teams.push({
        // This has to be a string to make the html work
        value: String(team.id),
        text: team.name
        }));
}

function createOptions(select){

    select.innerHTML = ""

    teams.forEach(team => {
        var opt = new Option(team.text, team.value)
        select.append(opt); 
    });
}

function checkDuplicates(){
    document.getElementById("firstTeam").addEventListener("change", e => {
        const selectedOptionOne = e.target.selectedOption;
    })
    document.getElementById("secondTeam").addEventListener("change", e => {
        const selectedOptionTwo = e.target.selectedOption;
    })
}

function validateForm() {
  let x = selectOne.value;
  let y = selectTwo.value;
  if (x == y) {
    alert("Please pick two teams.");
    return false;
  }
} 

// initialise page with values populated from database
async function init() {
    await getTeams()
    createOptions(selectOne)
    createOptions(selectTwo)
}


init()