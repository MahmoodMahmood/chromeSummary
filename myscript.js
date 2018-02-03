var results = document.getElementsByClassName("st");
for (var i = 0; results.length; i++) {
    //Create the new content to be added
    var newDiv = document.createElement("div"); 
    var newContent = document.createTextNode("Hi there and greetings!"); 
    
    //Grab the parent div so we can insert within the same place
    var parentDiv = results[i].parentNode;
    newDiv.appendChild(newContent);  
    // add the newly created element and its content into the DOM
    //nextSibiling helps put the code AFTER results[i]  
    parentDiv.insertBefore(newDiv, results[i].nextSibling);
}