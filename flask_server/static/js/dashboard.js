// Husk å bruke 'defer' i linkingen i HTML slik siden er lastet før js filen kjører.

graphs.load();
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

const canvas = document.getElementById("powerConsumptionGraph").querySelector("canvas");
const ctx = canvas.getContext("2d");
setInterval(()=>{
    graphs.drawChart(canvas, ctx, [0,1,2,3,4,5], [5,3,-2,6,1,3], true, 30);
}, 1000)

// Dynamically resize graph after container
window.addEventListener( 'resize', onWindowResize, false );
function onWindowResize(){
    let innerPadding = 12;
    let container = document.getElementById("powerConsumptionGraph");
    refHeight = container.clientHeight;
    refWidth = container.clientWidth - (innerPadding*2); // sets width of graph canvas

    let cnvs = container.querySelector("canvas");
    cnvs.width = refWidth;
    //cnvs.height = refHeight;

    // resize hybel
    let hybel = document.getElementById("hybel");
    let roomData = document.getElementById("roomData");

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

// Run once:
updateRoomTables(); // run once to init
onWindowResize(); // run once to style graph