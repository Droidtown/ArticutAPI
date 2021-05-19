< script src = "//ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js" > < /script> <
    script >
    var articutResult = null;
$(document).ready(function() {
    alert('Demo 開始！ Articut\'s indexWithPOS');
    // 取得 Articut 的斷詞結果
    doArticut('蔡英文到宜蘭低調拜訪林義雄', ['get_person']);
});

function doArticut(text) {
    $.post({
        url: "https://api.droidtown.co/Articut/API/",
        dataType: "json",
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify({
            "username": "",
            "api_key": "",
            "input_str": text
        }),
        success: function(response) {
            if (response.status) {
                articutResult = response;
                $("#result_pos").text(articutResult.result_pos);
                // 將 Articut 的斷詞結果送入 /Addons 取得「人名列表」。
                doArticutAddons(articutResult.result_pos, true);
                doArticutAddons(articutResult.result_pos, false);
            }
        }
    });
}

function doArticutAddons(resultPos, indexWithPos) {
    $.post({
        url: "https://api.droidtown.co/Articut/Addons/",
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify({
            "username": "", //您註冊時的 email。若留空，則會使用每日 1 萬字的公用帳號。
            "api_key": "", //您完成付費後取得的 apikey 值。若留空，則會使用每日 1 萬字的公用帳號。
            "result_pos": resultPos,
            "func": ['get_person'], //這裡以「取得人名」為例
            "index_with_pos": indexWithPos //index_with_pos 的預設值為 true
        }),
        success: function(response) {
            if (response.status) {
                $("#indexWithPOS_" + indexWithPos).text(response.results.person_list);
            }
        }
    });
} <
/script>
<!-- edit your html here -->
<
h3 > < div > POS Result: < /div></h
3 >
    <
    div id = "result_pos" > < /div><br> <
    h3 > < div > 取得人名列表 < /div></h
3 >
    <
    h4 > < div > indexWithPOS = True(預設值) < /div></h
4 >
    <
    div id = "indexWithPOS_true" > < /div> <
    h4 > < div > indexWithPOS = False < /div></h
4 >
    <
    div id = "indexWithPOS_false" > < /div>