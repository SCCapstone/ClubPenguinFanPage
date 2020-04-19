function selection(){
if (window.getSelection)
       return window.getSelection();
}

function setText(text){
  document.getElementById("firstdocinput").value = text;
}

function newTab(){
  window.open('http://textpenguin.herokuapp.com/guesthome/', '_blank');
  window.addEventListener('load', function () {
    setText();
})
}

(function() {
  var text = selection();
  console.log("Selected Text:" + text);
  newTab();
})();
