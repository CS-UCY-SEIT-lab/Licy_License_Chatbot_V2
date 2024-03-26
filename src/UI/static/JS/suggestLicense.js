var keywords ={
    "permit": [
        "commercial-use",
        "modifications",
        "distribution",
        "private-use",
        "sublicensing",
        "patent-use",
        "trademark-use",
    ],
    "require": [
        "include-copyright",
        "disclose-source",
        "document-changes",
        "network-use-diclose",
        "same-license",
    ],
    "offer": ["liability", "warranty"]
}
var htmlCode = ""
Object.entries(keywords).forEach(([key, values]) => {
    htmlCode +=`<tr>`
    htmlCode += `<td class="text-nowrap text-center p-3" >Permissions</td>`
    htmlCode += `<td class="text-nowrap text-center p-3" >${key}</td>`
    htmlCode += `<td class="text-nowrap text-center p-3" >Don't ${key}</td>`
    htmlCode += `<td class="text-nowrap text-center p-3" >Don't Care</td>`
    htmlCode +=`</tr>`
    for (let value of values) {
        htmlCode+='<tr>'
        htmlCode+=`<td class="text-nowrap" >${value}</td>`
        htmlCode+=`<td class="text-nowrap text-center positive-mark"></td>`
        htmlCode+=`<td class="text-nowrap text-center negative-mark"></td>`
        htmlCode+=`<td class="text-nowrap text-center neutral-mark"></td>`
        console.log(value);
        htmlCode+="</tr>"
    }

});
positive_elements=document.getElementsByClassName("positive-mark");
negative_elements=document.getElementsByClassName("negative-mark");
neutral_elements=document.getElementsByClassName("neutral-mark");
document.getElementById("table-element").insertAdjacentHTML('beforeend', htmlCode);

for (let element of positive_elements){
    element.addEventListener("click",function(){
    var siblings = Array.from(element.parentNode.children);
    siblings.shift();
    // Filter out the selected element from the siblings
    var siblingsWithoutSelected = siblings.filter(function(selectedElement) {
    return element !== selectedElement;
  });

  siblingsWithoutSelected.forEach(function(element) {
    firstChild= element.firstChild;
    if (firstChild !== null){
        element.removeChild(firstChild);
    }
  });

  element.innerHTML=`<img src="../images/check-mark.svg" alt="">`

    })
    
}

for (let element of negative_elements){
    element.addEventListener("click",function(){
    var siblings = Array.from(element.parentNode.children);
    siblings.shift();
    // Filter out the selected element from the siblings
    var siblingsWithoutSelected = siblings.filter(function(selectedElement) {
    return element !== selectedElement;
  });

  siblingsWithoutSelected.forEach(function(element) {
    firstChild= element.firstChild;
    if (firstChild !== null){
        element.removeChild(firstChild);
    }
  });

  element.innerHTML=`<img src="../images/cross-mark.svg" alt="">`

    })
    
}
for (let element of neutral_elements){
    element.addEventListener("click",function(){
    var siblings = Array.from(element.parentNode.children);
    // Filter out the selected element from the siblings
    siblings.shift();
    var siblingsWithoutSelected = siblings.filter(function(selectedElement) {
    return element !== selectedElement;
  });

  siblingsWithoutSelected.forEach(function(element) {
    firstChild= element.firstChild;
    if (firstChild !== null){
        element.removeChild(firstChild);
    }
  });

  element.innerHTML=`<img src="../images/neutral-mark.svg" alt="">`

    })
    
}
