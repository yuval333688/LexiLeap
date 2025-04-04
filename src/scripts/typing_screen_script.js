

let user_typing 

  


window.onload = function () {
    user_typing = document.querySelector('.user_typing');
    onClicPlay();

   

}



function onClicPlay() {
  const randomChar = getRandomVisibleChar();
  user_typing.textContent += randomChar;
  console.log("Random char:", randomChar); // בדיקה

}


function onClicStop()
{

}
function onClicPause()
{

}
  



