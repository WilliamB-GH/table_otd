var selectOne = document.getElementById("firstTeam")
var selectTwo = document.getElementById("secondTeam")

function validateForm() {
  let x = selectOne.value;
  let y = selectTwo.value;
  if (x == y) {
    alert("Please pick two teams.");
    return false;
  }
  else if (x == "" || y == ""){
    alert("Please pick two teams.");
    return false; 
  }
} 