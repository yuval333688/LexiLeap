{
    
let template ;
let levelDiv ;
let CheckMarkIcon;
let starsIcon;
let axeIcon;

function main() {
        find_views();
        init_views();

    }


function find_views (){
    template = document.getElementsByTagName('template')[0];
    levelDiv = template.content.querySelector(".level").cloneNode(true);
    CheckMarkIcon = template.content.querySelector(".CheckMarkIcon").cloneNode(true);
    starsIcon = template.content.querySelector(".starsIcon").cloneNode(true);
    axeIcon = template.content.querySelector(".axeIcon").cloneNode(true);

}



function init_views (){
    

    setEqualHeightWidth(levelDiv);
    levels = api.load_levelsScore().then((levels)=> {
    console.log(levels);
    for(let level of levels)
    {
        let newlevel = levelDiv.cloneNode(true);
        newlevel.getElementsByClassName('score')[0].textContent = "score: " + level.score;
        newlevel.getElementsByClassName('id')[0].textContent = "" + levels.indexOf(level);
        document.body.appendChild(newlevel);
        if (!level.locked) {
            newlevel.getElementsByClassName('icon')[0].appendChild(CheckMarkIcon.cloneNode(true));
            newlevel.classList.add('open');


        }
        else {
            newlevel.getElementsByClassName('icon')[0].appendChild(axeIcon.cloneNode(true));
            newlevel.classList.add('locked');

        }
        if (level.score > 900) { starsNumer = 5; }
        else if (level.score > 750) { starsNumer = 4; }
        else if (level.score > 600) { starsNumer = 3; }
        else {
            starsNumer = 0;
        }

        for (let i = 0; i < starsNumer; i++) {
            let newStar = starsIcon.cloneNode(true);
            newlevel.getElementsByClassName('stars')[0].appendChild(newStar);

        }
        setEqualHeightWidth(newlevel);

        console.log(newlevel);

    }
    });
    
}





function handleClick(element) {
    // Toggle the clicked class for visual feedback
    element.classList.toggle('clicked');

    // Only proceed with navigation if the level is open (not locked)
    if (element.classList.contains('open')) {
        // Get level information to pass to the typing screen
        const levelId = element.querySelector('.id').textContent;
        //const levelScore = element.querySelector('.score').textContent;
        utility.saveNumber("levelNumber", levelId);

        //sessionStorage.setItem('level_number', levelId);

        
        // Add a small delay so the user can see the clicked state before navigation
        setTimeout(() => {
            // Navigate to the typing screen
            window.location.href = '../screen2/screen2.html';
        }, 300);
    }
     else {
        // If level is locked, show a message (optional)
        alert('This level is locked. Complete previous levels to unlock.');
    }
}

function setEqualHeightWidth(element) {
        const width = element.offsetWidth;
        element.style.height = width + 'px';
    }

main();



}














    