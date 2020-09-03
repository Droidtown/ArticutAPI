$(document).ready(function() {
    $(document).on('input', '#smartHomeMsg', function() {
        if ($('#smartHomeMsg').val() == "") {
            $('#smartHomeBtn').attr('disabled', true);
        } else {
            $('#smartHomeBtn').attr('disabled', false);
        }
    });
    
    $('#smartHomeMsg').keypress(function(e) {
        var key = e.which;
        if (key == 13) // the enter key code
        {
            $('#smartHomeBtn').trigger('click');
            return false;
        }
    });

    $(document).on('click', '#smartHomeBtn', function() {
        var msg = $('#smartHomeMsg').val();
        if (msg == "") return false;

        showMask(true);
        $.post({
            url: "msg",
            data: {"msg": msg},
            success: function(resp) {
                $('#smartHomeMsg').val("");
                showMask(false);
                switch (resp.type) {
                    case "msg":
                        return appendMsg(resp.msg);
                    case "command":
                        return showCommand(resp.msg, resp.command);
                    case "question":
                        return showQuestion(resp.msg, resp.command);
                    default:
                        return unknown();
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                showMask(false);
            }
        });
    });
});

function appendMsg(msg) {
    if (msg == "") return false;

    $('.card-body').append('\
                    <div class="row">\
                        <div class="col-auto">\
                            <div class="alert alert-primary" role="alert">\
                                ' + msg + '\
                            </div>\
                        </div>\
                    </div>');
    scrollBottom();

    return true;
}

function showCommand(msg, commandList) {
    if (msg == "") return false;
    if (commandList.length == 0) return false;

    var tempStr = '\
                    <div class="row">\
                        <div class="col-auto">\
                            <div class="alert alert-primary" role="alert">\
                                ' + msg + '\
                            </div>\
                        </div>\
                    </div>\
                    <div class="row question mb-3">';
    for (var i=0; i<commandList.length; i++) {
        tempStr += '\
                        <div class="col">\
                            <button class="btn btn-success btn-lg btn-block" onclick="doCommand(\'' + commandList[i]["command"] + '\', \'' + commandList[i]["value"] +  '\')">' + commandList[i]["text"] + '</button>\
                        </div>';
    }
    tempStr += '\
                    </div>';

    $('.card-body').append(tempStr);
    scrollBottom();

    return true;
}

function showQuestion(msg, command) {
    if (msg == "") return false;
    if (Object.keys(command).length == 0) return false;

    var tempStr = '\
                    <div class="row">\
                        <div class="col-auto">\
                            <div class="alert alert-primary" role="alert">\
                                ' + msg + '\
                            </div>\
                        </div>\
                    </div>\
                    <div class="row question mb-3">\
                        <div class="col">\
                            <button class="btn btn-success btn-lg btn-block" onclick="doCommand(\'' + command["command"] + '\', \'' + command["value"] +  '\')">是</button>\
                        </div>\
                        <div class="col">\
                            <button class="btn btn-danger btn-lg btn-block" onclick="response()">否</button>\
                        </div>\
                    </div>';

    $('.card-body').append(tempStr);
    scrollBottom();

    return true;
}

function doCommand(command, value) {
    if (command == "") return false;
    if (value == "") return false;

    showMask(true);
    $.post({
        url: "command",
        data: {
            "command": command,
            "value": value
        },
        success: function(resp) {
            $('.question').remove();
            if (resp.type == "msg") {
                showMask(false);
                return appendMsg(resp.msg);
            } else {
                showMask(false);
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            showMask(false);
        }
    });
}

function response() {
    $('.question').remove();
    appendMsg("沒問題。");
}

function unknown() {
    return appendMsg("對不起，小三不太了懂您的意思 ...");
}

function scrollBottom() {
    $('.card-body').animate({scrollTop: $('.card-body')[0].scrollHeight}, 500);
}

function showMask(flag) {
    if (flag) {
        $('#mask').css('display', 'block');
    } else {
        setTimeout(function() {
            $('#mask').css('display', 'none');
        }, 500);
    }
}