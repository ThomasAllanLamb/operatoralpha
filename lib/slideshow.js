var $ = require("jquery");

var Slideshow = function (elements) {
  //build dom
  var $dOMElement = $("<div>");
  var $ul = $("<ul>");
  $dOMElement.append($ul);
  for (element of elements)
  {
    $ul.append(
      $("<li>").append(element)
    );
  }

  //initialize visibility
  function enforceTargetIndex () {
    $ul.children()
      .hide()
      .eq(targetIndex).show()
    ;
  }
  var targetIndex = 0;
  enforceTargetIndex();

  //change visibility on click        
  $dOMElement.on("click", function (event) {
    targetIndex = (targetIndex+1)%elements.length;
    enforceTargetIndex();

    event.preventDefault();
  })

  return $dOMElement.get(0)
}

module.exports = Slideshow