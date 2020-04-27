javascript:(function() {
	if(window.getSelection){
	  var bookmarklet_text = window.getSelection();
	  console.log("Selected Text: " + bookmarklet_text);
	  window.location.href = "http://127.0.0.1:8000/guesthome/" + "#" + bookmarklet_text;
	}
})();



