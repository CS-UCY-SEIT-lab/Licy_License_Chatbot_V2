// $(document).ready(function() {
//     $('#send').click(function() {
//         var message = $('#input').val();
//         $('#input').val('');
//         $('#messages').append('<p><strong>You:</strong> ' + message + '</p>');
//         console.log(message)
//         $.ajax({
//             type: "POST",
//             url: '/ask',
//             contentType: 'application/json',
//             data: JSON.stringify({ user_input: message }),
//             success: function(data) {
//                 $('#messages').append('<p><strong>Bot:</strong> ' + data.message + '</p>');
//             }
//         });
//     });
// });
var answer_counter=1;
var question_counter=1;
var details_object= {};

function getQuestionID(elementID){
    var regex = /(\d+)(?=\D*$)/;

    // Match the last number in the string using the regular expression
    var match = elementID.match(regex);

    // If a match is found, return the last number as an integer
    if (match) {
        return parseInt(match[0]);
    } else {
        // If no match is found, return null or handle it according to your use case
        return null;
    }
}
function startBeginnerTutorial(){
    $.ajax({
        type: "POST",
        url: '/start-tutorial',
        contentType: 'application/json',
        data: JSON.stringify({ type: "Have knowledge"}),
        success: function(data) {
            document.getElementById('messageBox').style.display='none'
            document.getElementById('stop-button').style.display='inline-block'
            displayStartTutorial(data)
        }
    
    });
}
function closePopup(element){
    element.parentNode.firstChild.remove()
    element.parentNode.style.display="none"
}
function displayPopup(content){
    let popup_container=document.createElement( "div" ); 
    popup_container.className="popup-container";
    popup_container.innerHTML=content;

    let popup=document.getElementById("popup")
    popup.prepend(popup_container)
    popup.style.display="block"
}
function displayStartTutorial(data){
    console.log("Data:",data);
    var element=document.getElementById("conversation");
    
    var htmlString=`<div class="chat-block" id="start-tutorial-block">
    <div class="bot-icon-block">
          <div class="bot-icon-text">Bot</div>
          <div class="bot-icon">
            <img class="bot-image" src="/static/images/bot.png" alt="">
          </div>
        </div>
    <div id="question-${question_counter}" class="question-block">${data.question}</div>
    <span class="arrow-icon" id="arrow-icon-${question_counter}"><i class="bi bi-arrow-down-circle-fill dropdown-arrow"></i></span>
    </div>
    <div class="explanation-block" id="explanation-block-${question_counter}">${data.question_explanation}</div>
    <div class="options-block">`;

    

    var options= ""
    for (option of data.options){
        options+=`<button class="option ${data.option_colors[option]}-block" onclick="handleAnswer(this,'${data.option_colors[option]}')">${option}</button>`
    }
    htmlString=htmlString+options;
    element.insertAdjacentHTML('beforeend', htmlString);
    document.querySelector('#arrow-icon-'+question_counter).addEventListener('click', function() {
    handleExplanation(this);
    });
   
    question_element=document.getElementById("question-"+question_counter);
    question_element.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
    question_counter++;
}
function handleStop(){
    $.ajax({
        type: "POST",
        url: '/questionnaire',
        contentType: 'application/json',
        data: JSON.stringify({ answer: "Stop" }),
        success: function(data) {
            document.getElementById("messageBox").style.display="flex"
            document.getElementById("stop-button").style.display="none"
            
            let starting_block=document.getElementById('start-tutorial-block')

            let siblings = [starting_block];

            // Traverse through the siblings using nextSibling
            let sibling = starting_block.nextSibling;
            while (sibling !== null) {
                // Check if the sibling is an element node (nodeType === 1)
                if (sibling.nodeType === 1) {
                    // Add the sibling to the array
                    siblings.push(sibling);
                }
                // Move to the next sibling
                sibling = sibling.nextSibling;
            }

            // Remove each sibling from the DOM
            siblings.forEach(function(sibling) {
                sibling.remove();
            });



            // if (data['finished']){
            //     if(data["type"] == "Beginner")
            //         displaySubset(data.option_license_subsets[element.textContent])
            //     else{
            //         displaySubset(data['current_subset'])
            //     }
            // }
            // else{
            //     displayQuestion(data)
            // }
        }
    
    });
}
function createChatBlock(message,timeout){
        var chatBlock = document.createElement("div");
        chatBlock.classList.add("chat-block");

        // Create bot-icon-block element
        var botIconBlock = document.createElement("div");
        botIconBlock.classList.add("bot-icon-block");

        // Create bot-icon-text element
        var botIconText = document.createElement("div");
        botIconText.classList.add("bot-icon-text");
        botIconText.textContent = "Bot"; // Set text content

        // Create bot-icon element
        var botIcon = document.createElement("div");
        botIcon.classList.add("bot-icon");

        // Create bot-image element
        var botImage = document.createElement("img");
        botImage.classList.add("bot-image");
        botImage.setAttribute("src", "/static/images/bot.png");
        botImage.setAttribute("alt", "A bot icon");

        // Append botImage to bot-icon
        botIcon.appendChild(botImage);

        // Append botIconText and botIcon to botIconBlock
        botIconBlock.appendChild(botIconText);
        botIconBlock.appendChild(botIcon);


        // Create question-block element
        var questionBlock = document.createElement("div");
        questionBlock.classList.add("question-block");
        questionBlock.textContent = message; // Set text content
        
       

        // Create load container element
        var loadContainer = document.createElement("div");
        loadContainer.classList.add("load");

        // Create three progress divs and append them to the load container
        for (var i = 0; i < 3; i++) {
            var progressDiv = document.createElement("div");
            progressDiv.classList.add("progress");
            loadContainer.appendChild(progressDiv);
            
        }

        // Append load container to a parent element (assuming you have a parent element with id "container")
        
        
        // Append botIconBlock and questionBlock to chatBlock
        chatBlock.appendChild(botIconBlock);
        

        
        if(timeout){
            chatBlock.appendChild(loadContainer);
            setTimeout(function() {
                loadContainer.remove();
                chatBlock.appendChild(questionBlock);
                questionBlock.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
                document.getElementById("message-component").style.display="flex"
                
            }, 2000);
        }
        else{
            chatBlock.appendChild(questionBlock);
        }
        document.getElementById("conversation").appendChild(chatBlock);
        chatBlock.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
        return chatBlock
        
}
function displaySubset(subset){
    chatBlock=createChatBlock(subset,false)

    $.ajax({
        type: "POST",
        url: '/retrieve-license-info',
        contentType: 'application/json',
        data: JSON.stringify({ license_ids: subset}),
        success: function(data) {
            
            displayPermissionTable(data)
            addMoreInfoIcon(chatBlock)
        }
    
    });

    
}
function handleAnswer(element,color) {
   
    element.classList.add(color);
   

    var elements = document.getElementsByClassName('option');

// Iterate through the elements and disable onClick
    for (var i = 0; i < elements.length; i++) {
    // Store a reference to the current element
        var currentElement = elements[i];

    // Disable the existing onClick function
        currentElement.removeAttribute('onclick');
    }
    $.ajax({
        type: "POST",
        url: '/questionnaire',
        contentType: 'application/json',
        data: JSON.stringify({ answer: element.textContent }),
        success: function(data) {
            console.log("From Quesstionnaire call:  ",data);
            if (data['finished']){
                if(data["type"] == "Beginner"){
                    if(data.option_license_subsets[element.textContent]["type"]==="text")
                        displaySubset(data.option_license_subsets[element.textContent]["licenses"])
                    else if(data.option_license_subsets[element.textContent]["type"]==="popup"){
                        displayPopup(data.option_license_subsets[element.textContent]["content"])

                    }
                    else if(data.option_license_subsets[element.textContent]["type"]==="tutorial"){
                        startBeginnerTutorial();
                    }
                }
                else{
                    displaySubset(data.current_subset)
                }
            }
            else{
                displayQuestion(data)
            }
        }
    
    });


}
function handleExplanation(element){
    const question_id=getQuestionID(element.id)
    console.log("Explanation block id: ",'explanation-block-'+question_id)
    const explanation_block= document.getElementById('explanation-block-'+question_id);
    if (explanation_block.style.display==='block') {
        explanation_block.style.display='none';
        element.firstChild.className="";
        element.firstChild.classList.add('bi',"bi-arrow-down-circle-fill","dropdown-arrow");
    }
    else{
        explanation_block.style.display='block';
        explanation_block.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
        element.firstChild.className="";
        element.firstChild.classList.add('bi',"bi-arrow-up-circle-fill","dropdown-arrow");
    }   
}
function displayQuestion(data){
    var element=document.getElementById("conversation");
    
    var htmlString=`<div class="chat-block">
    <div class="bot-icon-block">
          <div class="bot-icon-text">Bot</div>
          <div class="bot-icon">
            <img class="bot-image" src="/static/images/bot.png" alt="">
          </div>
        </div>
    <div id="question-${question_counter}" class="question-block">${data.question}</div>
    <span class="arrow-icon" id="arrow-icon-${question_counter}"><i class="bi bi-arrow-down-circle-fill dropdown-arrow"></i></span>
    </div>
    <div class="explanation-block" id="explanation-block-${question_counter}">${data.question_explanation}</div>
    <div class="options-block">`;

    

    var options= ""
    for (option of data.options){
        options+=`<button class="option ${data.option_colors[option]}-block" onclick="handleAnswer(this,'${data.option_colors[option]}')">${option}</button>`
    }
    htmlString=htmlString+options;
    element.insertAdjacentHTML('beforeend', htmlString);
    document.querySelector('#arrow-icon-'+question_counter).addEventListener('click', function() {
    handleExplanation(this);
    });
   
    question_element=document.getElementById("question-"+question_counter);
    question_element.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
    question_counter++;
}
function startTutorial(element){
    if (element.textContent == "Beginner")
        element.classList.add("orange")
    else
        element.classList.add("green")

    let option_buttons=document.querySelectorAll(".option")
    for (option of option_buttons){
        option.removeAttribute("click");
    }
    $.ajax({
        type: "POST",
        url: '/start-tutorial',
        contentType: 'application/json',
        data: JSON.stringify({ type: element.textContent }),
        success: function(data) {
            document.getElementById('messageBox').style.display='none'
            document.getElementById('stop-button').style.display='inline-block'
            displayStartTutorial(data)
        }
    
    });
}
function displayOptions(element,options){
console.log("Options: "+options)
let options_block= `
<div class="options-block">
<button id="beginner-button" class="orange-block option knowledge-level-option" onclick="startTutorial(this)" >${options[0]}</button>
<buttton id="basic-button" class="green-block option knowledge-level-option" onclick="startTutorial(this)">${options[1]}</buttton>
</div>
`;

element.insertAdjacentHTML('beforeend', options_block);
}
function addMoreInfoIcon(container){
    // Create span element
    var moreInfoIconSpan = document.createElement("span");
    moreInfoIconSpan.id = `more-info-${answer_counter}`;
    moreInfoIconSpan.classList.add("more-info-icon-container");

    // Create img element
    var imgElement = document.createElement("img");
    imgElement.setAttribute("src", "/static/images/info-icon.svg");
    imgElement.setAttribute("alt", "");

    // Append img element to span element
    moreInfoIconSpan.appendChild(imgElement);

    moreInfoIconSpan.addEventListener('click',function(){
        let id=moreInfoIconSpan.id;
        let answer_index=id[id.length - 1];
        let element=details_object[answer_index];
        let more_details_component=document.getElementById("more-details-component");
        more_details_component.append(element);
        more_details_component.style.display="block";
        
        

    })

    // Append span element to a parent element (assuming you have a parent element with id "container")
    container.appendChild(moreInfoIconSpan);
    answer_counter++;
}

function displayPermissionTable(info){
    console.log("Data Info",info);
    let license_ids=info.license_ids;
    let license_titles=info.license_titles;
    let license_permissions=info.license_permissions;

    var license_instance = license_permissions[0]
    var allkeys=[...Object.keys(license_instance[0]),...Object.keys(license_instance[1]),...Object.keys(license_instance[2])];
    let element= document.createElement("div")
    element.id=`more-details-content-${answer_counter}`
    var htmlCode=`<div id="header"><h1>Here are some more details about this answer</h1></div><div id="table-container" class="table-responsive"><table class="table table-dark table-striped rounded-3 overflow-hidden">
    <thead><tr><th scope="col" class="text-nowrap text-center p-3">Recommended Licenses</th>`; 
    for (let key of allkeys) {
        htmlCode += `<th scope="col" class="text-nowrap text-center p-3">${key}</th>`;
    }
    htmlCode += `</tr></thead><tbody>`;
    var counter=0;
    
    for (let license of license_permissions) {
        let permissions = Object.values(license[0]);
        let conditions = Object.values(license[1]);
        let limitations = Object.values(license[2]);
        htmlCode+=`<tr>`;
        htmlCode+=`<td class="text-nowrap " >${license_titles[counter]}</td>`
        for (let value of permissions) {
            if(value==1)
                htmlCode+=`<td class="text-center"><img src="static/images/check-mark.svg" alt=""></td>`
            else
                htmlCode+=`<td class="text-center"><img src="static/images/cross-mark.svg" alt=""></td>`
            
        }
        for (let value of conditions) {
            if(value==1)
                htmlCode+=`<td class="text-center"><img src="static/images/check-mark.svg" alt=""></td>`
            else
                htmlCode+=`<td class="text-center"><img src="static/images/cross-mark.svg" alt=""></td>`
            
        }
        for (let value of limitations) {
            if(value==0)
                htmlCode+=`<td class="text-center"><img src="static/images/check-mark.svg" alt=""></td>`
            else
                htmlCode+=`<td class="text-center"><img src="static/images/cross-mark.svg" alt=""></td>`
            
        }
        counter++;
        htmlCode+=`</tr>`;

        
    }
    htmlCode+=`</tbody>
    </table>
    </div>`;
    element.insertAdjacentHTML('beforeend', htmlCode);
    details_object[`${answer_counter}`]=element;
    console.log(details_object)
   
    // document.getElementById("more-details-component").style.display="block";
}
function askChatbot(message){
    $.ajax({
    type: "POST",
    url: '/ask',
    contentType: 'application/json',
    data: JSON.stringify({ user_input: message }),
    success: function(data) {
        console.log("Succeeded response")

        // Create chat-block element
        var chatBlock = document.createElement("div");
        chatBlock.classList.add("chat-block");

        // Create bot-icon-block element
        var botIconBlock = document.createElement("div");
        botIconBlock.classList.add("bot-icon-block");

        // Create bot-icon-text element
        var botIconText = document.createElement("div");
        botIconText.classList.add("bot-icon-text");
        botIconText.textContent = "Bot"; // Set text content

        // Create bot-icon element
        var botIcon = document.createElement("div");
        botIcon.classList.add("bot-icon");

        // Create bot-image element
        var botImage = document.createElement("img");
        botImage.classList.add("bot-image");
        botImage.setAttribute("src", "/static/images/bot.png");
        botImage.setAttribute("alt", "A bot icon");

        // Append botImage to bot-icon
        botIcon.appendChild(botImage);

        // Append botIconText and botIcon to botIconBlock
        botIconBlock.appendChild(botIconText);
        botIconBlock.appendChild(botIcon);


        // Create question-block element
        var questionBlock = document.createElement("div");
        questionBlock.classList.add("question-block");
        questionBlock.textContent = data.message; // Set text content
        
       

        // Create load container element
        var loadContainer = document.createElement("div");
        loadContainer.classList.add("load");

        // Create three progress divs and append them to the load container
        for (var i = 0; i < 3; i++) {
            var progressDiv = document.createElement("div");
            progressDiv.classList.add("progress");
            loadContainer.appendChild(progressDiv);
            
        }

        // Append load container to a parent element (assuming you have a parent element with id "container")
        
        
        // Append botIconBlock and questionBlock to chatBlock
        chatBlock.appendChild(botIconBlock);
        chatBlock.appendChild(loadContainer);
        
        document.getElementById("conversation").appendChild(chatBlock);

        setTimeout(function() {
            loadContainer.remove();
            chatBlock.appendChild(questionBlock);
            console.log(data.info);
            console.log(data.info)
            if (data.info !== null){

                if(data.info.key === "permission_suggested_licenses" || data.info.key=== "license_info"){
                    displayPermissionTable(data.info);
                    addMoreInfoIcon(chatBlock)
                }
                else if(data.info.key === "start-tutorial"){
                    displayOptions(
                        document.getElementById("conversation"),data.info.options);
                    // addMoreInfoIcon(chatBlock)
                }
            }
            console.log("Scroll: ",questionBlock.innerHTML);
            chatBlock.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
            document.getElementById("message-component").style.display="flex"
        }, 2000);

        // Append chatBlock to a parent element (assuming you have a parent element with id "conversation")

    }
});
}
function handleUserInput(){
    document.getElementById("message-component").style.display="none"
    let user_text=document.getElementById("messageInput").value;
    document.getElementById("messageInput").value=""

    // Create chat-block element
    var chatBlock = document.createElement("div");
    chatBlock.classList.add("chat-block");

    // Create user-icon-block element
    var userIconBlock = document.createElement("div");
    userIconBlock.classList.add("user-icon-block");

    // Create user-icon-text element
    var userIconText = document.createElement("div");
    userIconText.classList.add("user-icon-text");
    userIconText.textContent = "You"; // Set text content

    // Create user-icon element
    var userIcon = document.createElement("div");
    userIcon.classList.add("user-icon");

    // Create user-image element
    var userImage = document.createElement("img");
    userImage.classList.add("user-image");
    userImage.setAttribute("src", "/static/images/user2.png");
    userImage.setAttribute("alt", "A user icon");

    // Append userImage to user-icon
    userIcon.appendChild(userImage);

    // Append userIconText and userIcon to userIconBlock
    userIconBlock.appendChild(userIconText);
    userIconBlock.appendChild(userIcon);

    // Create question-block element
    var questionBlock = document.createElement("div");
    questionBlock.classList.add("question-block");
    questionBlock.id=`question-${question_counter}`
    question_counter++;
    questionBlock.textContent = user_text; // Set text content

    // Append userIconBlock and questionBlock to chatBlock
    chatBlock.appendChild(userIconBlock);
    chatBlock.appendChild(questionBlock);

    // Append chatBlock to a parent element (assuming you have a parent element with id "conversation")
    document.getElementById("conversation").appendChild(chatBlock);
    askChatbot(user_text)
}

var send_button=document.getElementById("sendButton");
var cloce_icon= document.getElementById("close-icon").addEventListener("click",function(){
    children=Array.from(this.parentNode.children).filter(item=>item!=this);
    for( child of children){
        child.remove();
    }
    document.getElementById("more-details-component").style.display="none";
})

send_button.addEventListener("click", handleUserInput);
messageInput=document.getElementById("messageInput").addEventListener("keydown", function(event){
    if (event.key === 'Enter') {
        handleUserInput();
      }
});