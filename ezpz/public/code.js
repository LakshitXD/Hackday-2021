
function compile(){

    var inputTA = document.getElementById("inputArea");
var xd = document.getElementById("xd").contentWindow.document;
xd.open();
xd.writeln(inputTA.value);}
