$(document).ready(function () {
  $(".addComponentButton").each((index, button) => {
        button.onclick = function() {
       //     console.log($(this).text());
        }.bind(button)
    });
});
