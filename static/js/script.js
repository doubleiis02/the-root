function changePrimColor() {
    var input = document.getElementById('pri-class-color-input');
    var element = document.getElementById('prim-color');
    element.style["background-color"] = input.value;
}

function changeSecColor() {
    var input = document.getElementById('sec-class-color-input');
    var element = document.getElementById('sec-color');
    element.style.fill = input.value;
}

function changeClassName() {
    var input = document.getElementById('class-name-input');
    var element = document.getElementById('new-class-name');
    element.innerHTML = input.value;
}