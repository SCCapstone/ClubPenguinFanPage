function selection(){
if (window.getSelection)
       return window.getSelection();
}

(function() {
  var text = selection();
  console.log("Selected Text:" + text);
  console.log("Opening new tab!");
  var newP = window.open('http://textpenguin.herokuapp.com/guesthome/', '_blank').focus();
  console.log("New tab opened!");
  //Doesn't actually focus on the new tab and therefore says it can't update value of null for "firstdocinput"
  document.querySelector("firstdocinput").value = text;
})();
