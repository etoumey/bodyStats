// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.
function toggleSidebar() {
    var sidebar = document.querySelector('.sidebar');
    if (sidebar.style.display === "none") {
    	sidebar.style.display = "block";
    } else {
    	sidebar.style.display = "none";
    }


    console.log('Working')
}

function callNodeFunction() {
  console.log('button-clicked');
}


document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('myButton');
  const hamburger = document.getElementById('ham');

  button.addEventListener('click', callNodeFunction);
  hamburger.addEventListener('click', toggleSidebar);

});