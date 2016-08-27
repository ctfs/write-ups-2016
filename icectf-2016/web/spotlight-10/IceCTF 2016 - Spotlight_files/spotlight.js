/*
 * TODO: Remove debug log
 */

// Load the canvas context
console.log("DEBUG: Loading canvas context...");
var canvas = document.getElementById('myCanvas');
var context = canvas.getContext('2d');

// Make the canvas fill the screen
console.log("DEBUG: Adjusting canvas size...");
context.canvas.width  = window.innerWidth;
context.canvas.height = window.innerHeight;

// Mouse listener
console.log("DEBUG: Adding mouse listener...");
canvas.addEventListener('mousemove', function(evt) {
    spotlight(canvas, getMousePos(canvas, evt));
}, false);

console.log("DEBUG: Initializing spotlight sequence...");
function spotlight(canvas, coord) {
    // Load up the context
    var context = canvas.getContext('2d');

    // Clear the canvas
    context.clearRect(0,0,canvas.width, canvas.height);

    // Turn off the lights! Mwuhahaha >:3
    context.fillRect(0,0,window.innerWidth,window.innerHeight);

    // Scatter around red herrings
    context.font = "20px Arial";
    context.fillText("Not here.",width(45),height(60));
    context.fillText("Keep looking...",width(80),height(20));
    context.fillText(":c",width(20),height(30));
    context.fillText("Look closer!",width(75),height(80));
    context.fillText("Almost there!",width(60),height(10));
    context.fillText("Howdy!",width(10),height(90));
    context.fillText("Closer...",width(30),height(80));
    context.fillText("FLAG AHOY!!!!!!!!1",width(80),height(95));

    // Turn on the flash light
    var grd = context.createRadialGradient(
        coord.x, coord.y,  75,
        coord.x, coord.y,  50);
    grd.addColorStop(0,'rgba(255,255,255,0)');
    grd.addColorStop(1,'rgba(255,255,255,.7)');

    context.fillStyle=grd;
}

console.log("DEBUG: IceCTF{5tup1d_d3v5_w1th_th31r_l095}");

console.log("DEBUG: Loading up helper functions...");
console.log("DEBUG:     * getMousePos(canvas, evt)");
function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        x:  evt.clientX - rect.left,
        y:  evt.clientY - rect.top
    };
}

// Calculate height percenteges
console.log("DEBUG:     * height(perc)");
function height(perc)
{
    var h = window.innerHeight;
    return h * (perc / 100);
}

// Calculate width percenteges
console.log("DEBUG:     * width(perc)");
function width(perc)
{
    var w = window.innerWidth;
    return w * (perc / 100);
}
console.log("DEBUG: Done.");

console.log("DEBUG: Ready for blast off!");
