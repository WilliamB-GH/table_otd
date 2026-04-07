var selectOne = document.getElementById("firstTeam")
var selectTwo = document.getElementById("secondTeam")


function validateForm() {
  let x = selectOne.value;
  let y = selectTwo.value;
  var startDate = new Date(document.getElementById("start_date").value);
  var endDate = new Date(document.getElementById("end_date").value);

  if (x == "" || y == "" || x == y){
    alert("Please pick two teams.");
    return false; 
  }
  if (startDate > endDate){
    alert("The end date cannot be earlier than the start date.");
    return false;
  }
  return true;
} 