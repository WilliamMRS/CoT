
/*options = {
	ctx: ctx, text: "Hi", x: 100, y: 100, fillstyle: "Red", font: "18px Arial"
}*/

const graphs = 
{
	load: function(){
		console.log("graphs loaded..");
	},
	drawText: function (options){
		options.ctx.font = options.font;//18px Arialp
		options.ctx.fillStyle = options.fillstyle; //"black"
		options.ctx.textAlign = "middle";
		options.ctx.fillText(options.text, options.x, options.y);
	},
	/*options = {
   	 ctx: ctx, xCentre: 100, yCentre: 100, radius: 10, color: "Black",
	}*/
	drawCircle: function (options) {
		options.ctx.beginPath();
		options.ctx.strokeStyle = options.color;
		options.ctx.arc(options.xCentre, options.yCentre, options.radius, 0, 2 * Math.PI);
		options.ctx.stroke();
	},
	/*options = {
    ctx: ctx, x: 100, y: 100, size: 10, color: "Black",
	}*/
	drawFilledCircle: function (options) {
		options.ctx.beginPath();
		options.ctx.strokeStyle = options.color;
		options.ctx.fillStyle = options.color;
		options.ctx.moveTo(options.x, options.y);
		options.ctx.arc(options.x, options.y, options.size, 0, 2 * Math.PI);
		options.ctx.fill();
	},
	/*options = {
    ctx: ctx, x: 100, y: 100, height: 10, width: 10, color: "Black", lineWidth: 2,
}*/
	drawSquare: function (options) {
		options.ctx.beginPath();
		options.ctx.strokeStyle = options.color;
		options.ctx.lineWidth = options.lineWidth;
		options.ctx.moveTo(options.x, options.y);
		options.ctx.lineTo(options.x + options.width, options.y);
		options.ctx.lineTo(options.x + options.width, options.y + options.height);
		options.ctx.lineTo(options.x, options.y + options.height);
		options.ctx.lineTo(options.x, options.y);
		options.ctx.stroke();
	},

	/*options = {
		ctx: ctx, x: 100, y: 100, height: 10, width: 10, color: "Black",
	}*/
	drawFilledSquare: function (options) {
		options.ctx.beginPath();
		options.ctx.fillStyle = options.color;
		options.ctx.moveTo(options.x, options.y);
		options.ctx.lineTo(options.x + options.width, options.y);
		options.ctx.lineTo(options.x + options.width, options.y - options.height);
		options.ctx.lineTo(options.x, options.y - options.height);
		options.ctx.lineTo(options.x, options.y);
		options.ctx.fill();
	},

	/*options = {
		ctx: ctx, x: 100, y: 100, height: 10, width: 10, color: "Black", linewidth: 2,
	}*/
	drawTriangle: function (options) {
		options.ctx.beginPath();
		options.ctx.strokeStyle = options.color;
		options.ctx.lineWidth = options.linewidth;
		options.ctx.moveTo(options.x, options.y);
		options.ctx.lineTo(options.x + options.width, options.y);
		options.ctx.lineTo(options.x + options.width, options.y - options.height);
		options.ctx.lineTo(options.x, options.y);
		options.ctx.stroke();
	},

	/*options = {
		ctx: ctx, x: 100, y: 100, height: 10, width: 10, color: "Black"
	}*/
	drawFilledTriangle: function (options) {
		options.ctx.beginPath();
		options.ctx.fillStyle = options.color;
		options.ctx.moveTo(options.x, options.y);
		options.ctx.lineTo(options.x + options.width, options.y);
		options.ctx.lineTo(options.x + options.width, options.y + options.height);
		options.ctx.lineTo(options.x, options.y);
		options.ctx.fill();
	},

	/*options = {
		ctx: ctx, x: 100, y: 100, radius: 5, color: "Black", linewidth: 2, count: 5
	}*/
	drawFilledPoly: function (options) {
		ctx.beginPath();
		ctx.moveTo(options.x + options.radius * Math.cos(0), options.y + options.radius * Math.sin(0));
		ctx.strokeStyle = options.color;
		ctx.lineWidth = options.linewidth;
		for (i = 1; i <= options.count; i += 1) {
			ctx.lineTo(options.x + options.radius * Math.cos(i * 2 * Math.PI / options.count), options.y + options.radius * Math.sin(i * 2 * Math.PI / options.count));
		}
		ctx.stroke();
	},

	/*
		Hvordan å importere bilder til bruk i canvas:

		<img src="myImage.png" alt="" style = "display: none;">
		myImage = document.getElementById('myImage.png');
		ctx.drawImage(myImage, x, y);
	*/
	drawRotatedImage: function(x, y, obj, angle){
		ctx.translate(x + obj.width/2, y + obj.height/2);
		ctx.rotate(angle * Math.PI/180);
		ctx.drawImage(obj, -obj.width/2, -obj.height/2);
		ctx.rotate(- angle * Math.PI/180);
		ctx.translate(-x - obj.width/2, - y - obj.height/2);
	},

	/*
	drawPolyline DOC:
		x: [data for x axis]
		y: [data for y axis]
		cvx: [spacing between each datapoint in x pixels]
		cvy: start y of graph
		colour: what color is the graph
		yScale: The relevant scale of the project. Often use the same value as used in other programs utilizing the canvas.

	*/
	drawPolyline: function (canvas, ctx, x, y, cvx, zeroInTheMiddle, colour, yScale, lineWidth) { // canvas object, canvas context2d, x data, y data, x spacing, is zero in the middle?, color, Scale of graph, widht of graph line
		let yPoint
		let xPoint
		let width = canvas.width;
		let yOffset
		let xOffset

		ctx.beginPath();
		ctx.strokeStyle = colour;
		ctx.lineWidth = lineWidth;
		let xStart = (canvas.width);
		if(zeroInTheMiddle)
			yOffset = canvas.height/2
		xOffset = cvx/2 // offset x from the walls

		ctx.moveTo(xStart, y[y.length] + yOffset); // Moves to the right of the canvas

		// Draw the last value of the array first
		for (let i = y.length; i > 0; i -= 1) { // Starts at the furthermost index
			if(y[i] === null){ // If y value is 'null' move further, but don't draw anything.
				ctx.moveTo(xOffset + (cvx * i), yOffset) // move along
			}else{
				yPoint = yOffset - (y[i] * yScale); // Decides yPoint, using '-' because the canvas is 0 at the top
				xPoint = xOffset + (cvx * i) // uses '-' here as well, as the graph starts from the furthermost right and draws to the left.
				ctx.lineTo(xPoint, yPoint);
			}
		}
		ctx.stroke();
	},

	drawHorizontalLines: function (canvas, ctx, step, colour, lineWidth){
		ctx.beginPath();
		ctx.strokeStyle = colour;
		ctx.lineWidth = lineWidth;
		
		for (let i = 0; i <= canvas.height/step; i += 1) { // moves once per x/step
			ctx.moveTo(0, (canvas.height/step)*i);
			ctx.lineTo(canvas.width, (canvas.height/step)*i);
		}
		ctx.stroke();
	},

	drawVerticalLines: function (canvas, ctx, step, colour, lineWidth, dataPointsCount){
		ctx.beginPath();
		ctx.strokeStyle = colour;
		ctx.lineWidth = lineWidth;
		for (let i = 0; i <= dataPointsCount; i += 1*step) { // moves once per y/step
			ctx.moveTo((canvas.width/dataPointsCount)*i, 0);
			ctx.lineTo((canvas.width/dataPointsCount)*i, canvas.height);
		}
		ctx.stroke();
	},

	drawVerticalValues: function (canvas, ctx, cvx, step, colour, size, yScale, isZeroCenter){
		let maxVal;
		if(isZeroCenter)
			maxVal = canvas.height/2/yScale
		for (let i = 0; i <= canvas.height/step; i += 1) { // moves once per y/step
			let text = (maxVal-((maxVal/step)*i)).toFixed(0)
			drawText({ctx: ctx, text: text, x: cvx, y: (maxVal/step)*i*yScale+(size/2), fillstyle: colour, font: size.toString() + "px Arial"})
		}
	},

	drawHorizontalValues: function (canvas, ctx, step, yOffset, colour, size, scale, timesteps, dataPointsCount){
		let dateObj = new Date();
		let text = ""
		for (let i = 0; i < dataPointsCount; i += 1*step) { // moves once per y/step
			dateObj = new Date(timesteps[i]);
			let hours = dateObj.getHours();
			let minutes = dateObj.getMinutes()
			if(hours < 10)
				hours = "0"+hours.toString()
			if(minutes < 10)
				minutes = "0"+minutes.toString()

			text = `${hours}:${minutes}`
			drawText({ctx: ctx, text: text, x: (canvas.width/dataPointsCount)*i, y: canvas.height - yOffset, fillstyle: colour, font: size.toString() + "px Arial"})
		}
	},

	/* CHARTING TOOLS 
	
		canvas is canvas html object
		ctx is canvas.getContext("2d")
		x is array of x values
		y is array of y values
		midZero is a boolen. If true, the graph is drawn with 0 as the centerline
		dataPointsCount are the amount of datapoints to be graphed
	
	*/
	drawChart: function (canvas, ctx, x, y, midZero, dataPointsCount) {
		let max = 0
		let min = 0
		for(let i = 0; i < y.length; i++){
			if(y[i] > max)
				max = y[i]
			if(y[i] < min)
				min = y[i]
		}
		let range
			if(min > 0)
				range = max - min
			else
				range = max + Math.abs(min)
		if(dataPointsCount)
			range = range*2
		let scale
		if(range > 0)
			scale = (canvas.height/(range*1.1)) // If scale is 1, the y values will be charted with equal to canvas.height. *1.1 is there to make some room
		else
			scale = 1

		ctx.clearRect(0, 0, canvas.width, canvas.height);
		this.drawHorizontalLines(canvas, ctx, 10, '#bab8b7', 0.25)
		this.drawVerticalLines(canvas, ctx, 50, '#bab8b7', 0.25, dataPointsCount)
		try{
			if(x[0]){
				this.drawVerticalValues(canvas, ctx, 15, 5, "white", 10, scale, midZero);
				this.drawHorizontalValues(canvas, ctx, 50, 15, "white", 10, scale, x, dataPointsCount);
				let spacingBetweenEachPoint = canvas.width/dataPointsCount
				this.drawPolyline(canvas, ctx, x, y, spacingBetweenEachPoint, 50, 'red', scale, 2)
			}
		}catch(err){
			console.log(err)
		}
		this.drawSquare({ ctx: ctx, x: 0, y: 0, height: canvas.height, width: canvas.width, color: "#4cd137", lineWidth: 2, })
	},

	/*
	drawColumnChart DOC:
	{
		ctx: ctx,
		canvas: myCanvas,
		xData: [1,2,3,4,5,6],
		yData: [10,30,20,10,20,30],
		cvx: "the spacing between the columns" 25,
		cvy: "Bottom left corner y coord" 250,
		number: "how many columns to display" 6,
		widthPx: "the width of the columns" 1,
		yScale: "scaling of the height of the columns" 1,
		barColor: "DarkBlue",
		textColor: "Red"
	}
	*/
	drawColumnChart: function (options) {
		let i, yPixel;
		options.number = options.number - 1;
		
		for (i = 0; i <= options.number; i = i + 1) {
			yPixel = options.yData[i] * options.yScale;
			drawFilledSquare({
				ctx: options.ctx,
				x: 10 + options.cvx * i,
				y: options.cvy,
				height: yPixel,
				width: options.widthPx,
				color: options.barColor
			});
			drawText({
				ctx: options.ctx,
				text: options.yData[i],
				x: options.widthPx/2 + options.cvx * i,
				y: options.cvy - 15 - yPixel,
				fillstyle: options.textColor,
				font: "18px Arial"
			});
		}
	},

	drawPieChart: function (ctx, canvas, data, colors) {
		let lastend = 0;
		let total = 0;

		for (let e = 0; e < data.length; e += 1) {
			total += data[e];
		}

		for (let i = 0; i < data.length; i += 1) {
			ctx.fillStyle = colors[i];
			ctx.beginPath();
			ctx.moveTo(canvas.width / 2, canvas.height / 2);
			// Arc Parameters: x, y, radius, startingAngle (radians), endingAngle (radians), antiClockwise (boolean)
			ctx.arc(canvas.width / 2, canvas.height / 2, canvas.height / 2, lastend, lastend + (Math.PI * 2 * (data[i] / total)), false);
			ctx.lineTo(canvas.width / 2, canvas.height / 2);
			ctx.fill();
			lastend += Math.PI * 2 * (data[i] / total);
			console.log(colors[i]);
		}
	}
}