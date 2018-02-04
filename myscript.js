var results = document.getElementsByClassName("st");
var btncss = "color:green";
var textcss = "color:red";
for (let i = 0; i < results.length; i++) {
    //Create the new content to be added
    let newDiv = document.createElement("div");
    newDiv.async = true;
    let btn = document.createElement("BUTTON");
    btn.style.cssText = btncss;//change css of all the buttons
    let t = document.createTextNode(">>");
    btn.appendChild(t);

    //Grab the parent div so we can insert within the same place
    let parentDiv = results[i].parentNode;
    newDiv.appendChild(btn);

    let serverUrl = "https://safe-island-38827.herokuapp.com/data";
    let targetUrl = "https://en.wikipedia.org/wiki/Adam_Conover";
    let query = serverUrl + '?url=' + encodeURIComponent(targetUrl);
    fetch(query).then(result => {
        result.text().then(result => {
            console.log('current index i = ' + i);
            console.log(result);
            let summary = document.createTextNode(result);
            newDiv.appendChild(summary);
            newDiv.style.cssText = textcss;//change the css of all the text
            // add the newly created element and its content into the DOM
            //nextSibiling helps put the code AFTER results[i]
            parentDiv.insertBefore(newDiv, results[i].nextSibling);
        })
    }).catch(error => {
        console.log(error)
    })
}