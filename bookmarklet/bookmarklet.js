function selection(){
if (window.getSelection)
       return window.getSelection();
}

function setText(text){
  let text = document.querySelector("firstdocinput");
  return text;
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
  console.log("Opening new tab!");
  newTab();
  console.log("New tab opened!");
  window.onload = function(){
    console.log("loaded!");
};
})();
