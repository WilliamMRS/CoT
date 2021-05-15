// Husk å bruke 'defer' i linkingen i HTML slik siden er lastet før js filen kjører.
let roomData = document.getElementById("roomData")
let table = roomData.querySelector("table");

// Denne dataen må byttes ut med data fra CoT / Raspberry Pi Serveren
const rooms = [
    {name: "Stue", people: 0, kwh: 0},
    {name: "Kjøkken", people: 0, kwh: 0}, 
    {name: "Bad", people: 0, kwh: 0}, 
    {name: "Hybel 1", people: 1, kwh: 0}, 
    {name: "Hybel 2", people: 1, kwh: 0}, 
    {name: "Hybel 3", people: 1, kwh: 0}, 
    {name: "Hybel 4", people: 1, kwh: 0}, 
    {name: "Hybel 5", people: 1, kwh: 0}, 
    {name: "Hybel 6", people: 1, kwh: 0}
]

let updateRoomTables = async () => {
    // Looper over hvert rom og legger til data
    try{
        let res = await fetch(url+'/api/getOccupants')
        let json = await res.json()
        console.log(json)
        roomData = json[1] // roomdata
        let rows = "";
        let allRows = "";

        for(let i = 0; i < rooms.length; i++){
            let peopleInRoom = 0
            if(i > 2){
                d = roomData[3].split('{')[1].split('}')[0]
                x = d.substr(1, 3)
                peopleInRoom = JSON.parse(x)
            }
            else{
                peopleInRoom = JSON.parse(roomData[0]).length
            }

            let room = rooms[i]
            rows = `<tr>`;
            rows += `<td>${room.name ? room.name : "-"}</td>`
            rows += `<td>${room.people ? room.people : peopleInRoom}</td>`
            rows += `<td>${room.kwh ? room.kwh : 0}</td>`
            rows += `</tr>`;
            allRows += rows
        }
        table.innerHTML = allRows;
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
    for(let i = 1; i < table.children.length; i++){ // starts at 1 to skip the header
        let attributes = table.children[i].querySelector("tr").children;
        parseFloat(attributes[1].innerText) > 0 ? attributes[1].style.color = "white" : attributes[1].style.color = "gray";
    }
}

url = 'http://localhost:5000'

getWeatherData = async ()=>{
    let res = await fetch(url+'/api/forecast')
    let json = await res.json()
    let imgSource = json.symbol_code + ".svg"
    document.getElementById("weatherIcon").src = "/static/weatherIcons/"+ imgSource;
    let weatherData = document.getElementById("weatherData");
    let table = weatherData.querySelector("table");
    let builtHTML = ""
    for(variable in json.variables){
        let prefix = "";
        let value = json.variables[variable].split(":")[1];
        switch(json.variables[variable].split(":")[0]){
            case "air_pressure_at_sea_level":
            prefix = "Trykk";
            break;
            case "air_temperature":
            prefix = "&deg;C";
            value = value.split("celsius")[0]
            break;
            case "cloud_area_fraction":
            prefix = "Skydekke";
            break;
            case "precipitation_amount":
            prefix = "Nedbør";
            break;
            case "relative_humidity":
            prefix = "Fuktighet";
            break;
            case "wind_from_direction":
            prefix = "Vindretning";
            value = value.split("degrees")[0] + "&deg;"
            break;
            case "wind_speed":
            prefix = "Vindhastighet";
            break;
            default:
            prefix = "Ukjent"
            break;
        }
        builtHTML += 
        `<tr>
            <td>${value}</td>
            <td>${prefix}</td>
        </tr>`
    }
    table.innerHTML = builtHTML;

    return json // returns weather data
}

// Dynamically resize graph after container
window.addEventListener( 'resize', onWindowResize, false );
function onWindowResize(){
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

buildPowerChart = async () => {
    // labels are x-axis (time)
    // data is y-axis (Kwh used)

    let res = await fetch(url+'/api/getPowerUsage')
    let json = await res.json()

    let kwhGenerated = json["PvGeneration"]
    let kwhUsed = json["powerUsage"]
    let labels = json["time"]
    let cost = json["costOfPower"]
    let savings = json["solarSavings"]

    for (let i = 0; i < kwhGenerated.length; i++){
        kwhGenerated[i] = kwhGenerated[i][0]
        kwhUsed[i] = kwhUsed[i][0]
        cost[i] = cost[i][0]/100 // looks like this came out as 'øre' per kwh. Divide by 100 for nok
        savings[i] = savings[i][0]
        labels[i] = labels[i][0].split(" ")[1]
    }

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
            }
        ]
    };

    const data2 = {
        labels: labels,
        datasets: [
                {
                    label: 'Kostnad Strøm',
                    data: cost,
                    fill: true,
                    borderColor: 'rgb(180, 0, 70)',
                    tension: 0.1,
                    backgroundColor: 'rgba(180, 0, 70, 0.5)',
                },
                {
                    label: 'Penger Spart av Solar',
                    data: savings,
                    fill: true,
                    borderColor: 'rgb(100, 200, 7)',
                    tension: 0.1,
                    backgroundColor: 'rgba(100, 200, 7, 0.5)',
                },
            ]
        };

    var ctx1 = document.getElementById('costChart').getContext('2d');
    var costChart = new Chart(ctx1, {
        type: 'line',
        data: data2,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

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
}

updatePowerTable = async () => {
    builtHTML = "";


    builtHTML += 
    `<tr>
        <td>${value}</td>
        <td>${prefix}</td>
    </tr>`
    table.innerHTML = builtHTML;
}


// Timepicker 
document.querySelector("#timePickerStart").addEventListener("input", function(e) {
    const reTime = /^([0-1][0-9]|2[0-3]):[0-5][0-9]$/;
    const time = this.value;
    if (reTime.exec(time)) {
      const minute = Number(time.substring(3,5));
      const hour = Number(time.substring(0,2)) % 12 + (minute / 60);
      this.style.backgroundImage = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40'><circle cx='20' cy='20' r='18.5' fill='none' stroke='%23222' stroke-width='3' /><path d='M20,4 20,8 M4,20 8,20 M36,20 32,20 M20,36 20,32' stroke='%23bbb' stroke-width='1' /><circle cx='20' cy='20' r='2' fill='%23222' stroke='%23222' stroke-width='2' /></svg>"), url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40'><path d='M18.5,24.5 19.5,4 20.5,4 21.5,24.5 Z' fill='%23222' style='transform:rotate(${360 * minute / 60}deg); transform-origin: 50% 50%;' /></svg>"), url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40'><path d='M18.5,24.5 19.5,8.5 20.5,8.5 21.5,24.5 Z' style='transform:rotate(${360 * hour / 12}deg); transform-origin: 50% 50%;' /></svg>")`;
    }
  });
document.querySelector("#timePickerEnd").addEventListener("input", function(e) {
    const reTime = /^([0-1][0-9]|2[0-3]):[0-5][0-9]$/;
    const time = this.value;
    if (reTime.exec(time)) {
        const minute = Number(time.substring(3,5));
        const hour = Number(time.substring(0,2)) % 12 + (minute / 60);
        this.style.backgroundImage = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40'><circle cx='20' cy='20' r='18.5' fill='none' stroke='%23222' stroke-width='3' /><path d='M20,4 20,8 M4,20 8,20 M36,20 32,20 M20,36 20,32' stroke='%23bbb' stroke-width='1' /><circle cx='20' cy='20' r='2' fill='%23222' stroke='%23222' stroke-width='2' /></svg>"), url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40'><path d='M18.5,24.5 19.5,4 20.5,4 21.5,24.5 Z' fill='%23222' style='transform:rotate(${360 * minute / 60}deg); transform-origin: 50% 50%;' /></svg>"), url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40'><path d='M18.5,24.5 19.5,8.5 20.5,8.5 21.5,24.5 Z' style='transform:rotate(${360 * hour / 12}deg); transform-origin: 50% 50%;' /></svg>")`;
    }
});

winInit = ()=>{
    // Run once after everything has loaded:
    updateRoomTables(); // run once to init
    onWindowResize(); // run once to style graph
    onTableChange();
    getWeatherData();
    buildPowerChart();
}


setInterval( async ()=>{
    //graphs.drawChart(canvas, ctx, [0,1,2,3,4,5], [5,3,-2,6,1,3], true, 30);
    getWeatherData();
    updateRoomTables();
    //refreshPowerChart();
}, 5000)

window.onload = winInit;