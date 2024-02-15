function handleTab(tabButtonInstance) {
    const requestUrl = tabButtonInstance.getAttribute("value")
    fetch(requestUrl)
    .then(response => response.text())
    .then(text => {
        target = tabButtonInstance.getAttribute("data-bs-target").substring(1)
        element = document.getElementById(target);
        element.innerHTML = text;
    })

    return false;
}

const tabs = document.getElementsByClassName("nav-link");

for(i = 0; i < tabs.length; i++) {
    if (tabs[i].classList.contains("active")) {
        handleTab(tabs[i]); // get content of the default tab when page loads
    }
    tabs[i].addEventListener('click', e => {handleTab(e.currentTarget);});
}