var url = "https://api.droidtown.co/Articut/API/";

var xhr = new XMLHttpRequest();
xhr.open("POST", url);

xhr.setRequestHeader("Accept", "application/json");
xhr.setRequestHeader("Content-Type", "application/json");

xhr.onreadystatechange = function () {
   if (xhr.readyState === 4) {
      console.log(xhr.status);
      console.log(xhr.responseText);
   }};

var data = `{
  "username":"",
  "api_key" :"",
  "input_str":"我想過過過兒過過的日子"}`;

xhr.send(data);
