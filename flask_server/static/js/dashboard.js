// Husk å bruke 'defer' i linkingen i HTML slik siden er lastet før js filen kjører.
let roomData = document.getElementById("roomData")
let table = roomData.querySelector("table");

// Denne dataen må byttes ut med data fra CoT / Raspberry Pi Serveren
const rooms = [{name: "Hybel 1", people: 0, kwh: 9.4}, {name: "Hybel 2", people: 0}, {name: "Hybel 3", people: 1}, {name: "Hybel 4", people: 0}, {name: "Hybel 5", people: 0}, 
                {name: "Bad", people: 1}, {name: "Kjøkken", people: 2}, {name: "Trappegang", people: 0}]

let updateRoomTables = () => {
    // Looper over hvert rom og legger til data
    try{
        let rows = "";
        for(let i = 0; i < rooms.length; i++){
            let room = rooms[i]
            rows = `<tr>`;
            rows += `<td>${room.name ? room.name : "-"}</td>`
            rows += `<td>${room.people ? room.people : 0}</td>`
            rows += `<td>${room.kwh ? room.kwh : 0}</td>`
            rows += `</tr>`;
            table.innerHTML += rows;
        }
    }catch(err){
        alert("Room table update failed!");
        console.log(err);
        return err;
    }
}

/*
    ONCHANGE TABLE:
    Run 'updateTableStyle
*/

onTableChange = () => {
    let roomData = document.getElementById("roomData");
    console.log(roomData);
    let table = roomData.querySelector("table");
    loop1: for(let i = 1; i < table.children.length; i++){ // starts at 1 to skip the header
        let attributes = table.children[i].querySelector("tr").children;
        parseFloat(attributes[1].innerText) > 0 ? attributes[1].style.color = "white" : attributes[1].style.color = "gray";
    }
}

setInterval( async ()=>{
    //graphs.drawChart(canvas, ctx, [0,1,2,3,4,5], [5,3,-2,6,1,3], true, 30);
    getWeatherData();
}, 60000)

url = 'http://localhost:5000'

getWeatherData = async ()=>{
    let res = await fetch(url+'/api/forecast')
    let json = await res.json()
    console.log(json)
    return json // returns weather data
}


// Dynamically resize graph after container
window.addEventListener( 'resize', onWindowResize, false );
function onWindowResize(){
    /*
    let innerPadding = 12;
    let container = document.getElementById("powerChart");
    refHeight = container.clientHeight;
    refWidth = container.clientWidth - (innerPadding*2); // sets width of graph canvas

    let cnvs = document.getElementById("realTime"); // grabs real-time graph and sets its size equal to powerChart
    cnvs.width = refWidth;
    */
    //cnvs.height = refHeight;

    // resize hybel
    let hybel = document.getElementById("hybel");
    let roomData = document.getElementById("roomData");

    // Hybel dynamisk sizing
    hybel.style.height = `${roomData.clientHeight}px`
    hybel.querySelector("#kitchen").style.height = `${hybel.clientHeight / 3}px`
    hybel.querySelector("#commonroom").style.height = `${hybel.clientHeight / 3}px`
    hybel.querySelector("#kitchen").style.height = `${hybel.clientHeight / 3}px`
    hybel.querySelector("#entrance").style.height = `${hybel.clientHeight / 3}px`
    hybel.querySelector("#bathroom").style.height = `${hybel.clientHeight / 3}px`
    hybel.querySelector("#sleep1").style.height = `${hybel.clientHeight / 3}px`
    hybel.querySelector("#sleep2").style.height = `${hybel.clientHeight / 3 - 24}px`
    hybel.querySelector("#sleep3").style.height = `${hybel.clientHeight / 3 - 24}px`
    hybel.querySelector("#sleep4").style.height = `${hybel.clientHeight / 3 - 24}px`
    hybel.querySelector("#sleep5").style.height = `${hybel.clientHeight / 3 - 24}px`
    hybel.querySelector("#sleep6").style.height = `${hybel.clientHeight / 3}px`

}

/* Chartjs */

// labels are x-axis (time)
// data is y-axis (Kwh used)
const kwhGenerated = [12,10,7,16,20,22,24]
const kwhUsed = [65, 59, 80, 81, 56, 55, 40]
const labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
const data = {
  labels: labels,
  datasets: [
    {
        label: 'Solkraft',
        data: kwhGenerated,
        fill: true,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
        backgroundColor: 'rgba(75, 192, 192, 0.493)',
      },
    {
    label: 'Strømforbruk',
    data: kwhUsed,
    fill: true,
    borderColor: 'rgb(236, 129, 7)',
    tension: 0.1,
    backgroundColor: 'rgba(146, 80, 5, 0.5)',
  },
]
};

var ctx2 = document.getElementById('powerChart').getContext('2d');
var myChart = new Chart(ctx2, {
    type: 'line',
    data: data,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

const kwhGeneratedLive = [90,91,90,92,94,95,94]
const kwhUsedLive = [11.1, 11.1, 11.2, 11.0, 11.0, 10.9, 11]
const labelsLive = ["11:01:01", "11:01:02", "11:01:03", "11:01:04", "11:01:05", "11:01:06", "11:01:07", "11:01:08"]
const datart = {
  labels: labelsLive,
  datasets: [
    {
        label: 'Strømforbruk',
        data: kwhUsedLive,
        fill: true,
        borderColor: 'rgb(236, 129, 7)',
        tension: 0.1,
        backgroundColor: 'rgba(146, 80, 5, 0.5)',
      },
    {
        label: 'Solkraft',
        data: kwhGeneratedLive,
        fill: true,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
        backgroundColor: 'rgba(75, 192, 192, 0.493)',
      },
]
};

var ctx = document.getElementById('realTime').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: datart,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});


// Run once after everything has loaded:
updateRoomTables(); // run once to init
onWindowResize(); // run once to style graph
onTableChange();
getWeatherData();