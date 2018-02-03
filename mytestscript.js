var results = document.getElementsByClassName("bs-docs-section");
var temp = document.getElementsByClassName("starter-template");
for (var i = 0; results.length; i++) {
    //Create the new content to be added
    var newDiv = document.createElement("div"); 
    var newContent = document.createTextNode("Hi there and greetings!"); 
    
    var parentDiv = results[i].parentNode;
    newDiv.appendChild(newContent);  
    // add the newly created element and its content into the DOM  
    parentDiv.insertBefore(newDiv, results[i]);
}