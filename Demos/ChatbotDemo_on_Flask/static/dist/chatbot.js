$( document ).ready(function(){
    $("#send").click(function(){
        var inputSTR = $("#userInput").val();
        if (inputSTR == ""){
            alert("say something, will you?")
        }
        else{
            $("#invisibleForm").append("<div class='inputLog'>Chatbot: "+inputSTR+"</div>")
            $("#messages").append("<div class='inputLog'>Human: "+inputSTR+"</div>")
        }
    });
});