var initMessage = 'Chatbot (雅口): 您好，我是機器人「雅口」，我可以幫您找到合適看診科別。您哪裡不舒服嗎？';

$(document).ready(function(){
    $('#chatbotMessage').empty();
    receiveMessage(initMessage);

    $(document).on('click', "#chatbotSenderBtn", function(e) {
        var inputText = $('#chatbotSenderText').val();
        if (inputText != '') {
            setSenderIcon(true);
            sendMessage(inputText);
            $.post({
                url: "ask",
                data: {"inputSTR": inputText},
                success: function(resp) {
                    console.log(resp);
                    receiveMessage(resp);
                    setSenderIcon(false);
                }
            });
            $('#chatbotSenderText').val('');
        }
    });
});

function setSenderIcon(isSending) {
    $('#chatbotSenderIcon').removeClass();
    if (isSending) {
        var classStr = 'fa fa-spinner fa-lg fa-spin fa-fw';
        setSenderBtn(true);
    } else {
        var classStr = 'fa fa-paper-plane-o fa-lg';
        setSenderBtn(false);
    }
    $('#chatbotSenderIcon').addClass(classStr);
}

function setSenderBtn(disabled) {
    $('#chatbotSenderBtn').prop('disabled', disabled);
}

function sendMessage(message) {
    var messageText =
        '<div class="row d-flex justify-content-end">'
        + '<div class="col-10">'
        + '<div class="alert alert-primary float-right">'
        + message
        + '</div>'
        + '</div>'
        + '</div>';
    addMessage(messageText);
}

function receiveMessage(message) {
    var messageText =
        '<div class="row">'
        + '<div class="col-10">'
        + '<div class="alert alert-success d-inline-block">'
        + message
        + '</div>'
        + '</div>'
        + '</div>';
    addMessage(messageText);
}

function addMessage(message) {
    $('#chatbotMessage').append(message);
    $('#chatbotMessage').scrollTop($('#chatbotMessage')[0].scrollHeight);
}