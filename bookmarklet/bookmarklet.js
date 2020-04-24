function selection(){
if (window.getSelection)
       return window.getSelection();
}

(function() {
  var text = selection();
  console.log("Selected Text:" + text);
  window.location.href = "http://textpenguin.herokuapp.com/guesthome/";
  document.getElementById("firstdocinput").value = text;
})();

