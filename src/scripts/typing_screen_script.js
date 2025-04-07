let user_typing;
let timerInterval;
let seconds = 0;
let minutes = 0;
let isRunning = false;

window.onload = function () {
    user_typing = document.querySelector('.user_typing');
    timeDisplay = document.querySelector('.Performance_time_number');
    document.addEventListener('keydown', InputHandling);
}



function InputHandling( event)
{
    
    if (isRunning) {
        // Check if the key is a printable character (not a control key like Shift, Alt, etc.)
       
        if (event.key.length === 1) {
            // Add the typed character to the user_typing element
           
            user_typing.textContent += event.key;
        }  
        if (event.key === 'Enter') 
            user_typing.textContent += '↵';
        if (event.key === 'Backspace')//cut last letter
        user_typing.textContent = user_typing.textContent.slice(0, -1);

    }
}



function updateTimeDisplay() {
    // Format the time as MM:SS
    const formattedMinutes = minutes.toString().padStart(2, '0');
    const formattedSeconds = seconds.toString().padStart(2, '0');
    document.querySelector('.Performance_time_number').textContent = `${formattedMinutes}:${formattedSeconds}`;
}

function startTimer() {
    if (!isRunning) {
        isRunning = true;
        timerInterval = setInterval(function() {
            seconds++;
            if (seconds >= 60) {
                minutes++;
                seconds = 0;
            }
            updateTimeDisplay();
        }, 1000);
    }
}

function stopTimer() {
    clearInterval(timerInterval);
    isRunning = false;
    // Reset the timer
    seconds = 0;
    minutes = 0;
    updateTimeDisplay();
}

function pauseTimer() {
    clearInterval(timerInterval);
    isRunning = false;
}

function onClicPlay() {
    startTimer();
   
}

function onClicStop() {
    stopTimer();
    user_typing.textContent = '';  // Clear the typing area
}

function onClicPause() {
    pauseTimer();
}

function getRandomVisibleChar() {
    // This function needs to be defined to generate random characters
    // Here's a simple implementation that generates random letters
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    return chars.charAt(Math.floor(Math.random() * chars.length));
}