

function catControl()
{
    this.style.display = 'none';
    var kittyGif = document.querySelector("#kitty");
    kittyGif.style.display = 'inline';


}

var catBtn = document.querySelector("#funBtn");
catBtn.addEventListener('click', catControl);