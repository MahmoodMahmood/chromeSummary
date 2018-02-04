var results = document.getElementsByClassName("rc");
var btncss = "color:white;background-color:green;border-width:2px;border-color:#d3d3d3";
var textcss = "color:black;background-color:#d3d3d3;display:none";
for (let i = 0; i < results.length; i++) {
    //Create the new content to be added
    let newDiv = document.createElement("div");
    newDiv.async = true;
    let btn = document.createElement("BUTTON");
    btn.style.cssText = btncss;//change css of all the buttons
    let t = document.createTextNode(">>");
    btn.appendChild(t);
    btn.setAttribute("id","butt" + i);
    btn.onclick=function(){
        let butN = btn.getAttribute("id").substr(4);
        console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"+butN);
        let targetS=document.getElementById("summary" + butN);
        //targetS.style.display = "inline-block";
        
        if (targetS.style.display == "inline-block"){
           targetS.style.display = "none"
        }
        else
            targetS.style.display = "inline-block"
            
    }
    //Grab the parent div so we can insert within the same place
    //let parentDiv = results[i].parentNode;
    let child = results[i].getElementsByTagName("a")[0];
    console.log(child.getAttribute("href"));
    let targetUrl = child.getAttribute("href");
    //let linkOuterDiv = parentDiv.getElementsByClassName("f kv _SWb");
    //let linkDiv = results[i].previousSibling.getElementsByClassName("_Rm");
    //console.log("link is: " + linkDiv.textContent);
    newDiv.appendChild(btn);

    let serverUrl = "https://safe-island-38827.herokuapp.com/data";
    //let targetUrl = "https://en.wikipedia.org/wiki/Adam_Conover";
    let query = serverUrl + '?url=' + encodeURIComponent(targetUrl);
    fetch(query).then(result => {
        result.text().then(result => {
            console.log('current index i = ' + i);
            console.log(result);
            let summary = document.createElement("div");
            summary.innerHTML = result;
            summary.setAttribute("id","summary"+i);
            newDiv.appendChild(summary);
            summary.style.cssText = textcss;//change the css of all the text 
            // add the newly created element and its content into the DOM
            //nextSibiling helps put the code AFTER results[i]
            //parentDiv.insertBefore(newDiv, results[i].nextSibling);
            results[i].appendChild(newDiv);
        })
    }).catch(error => {
        console.log(error)
    })
}
