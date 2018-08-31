// This file contains some funcctions that are imported into the base html and can therefore
// be used in all sub html's'

function ticker(ul_id, subset_list, action) {
    var inputs = $('#' + ul_id + ' input');
    let i;
    for (i = 0; i < inputs.length; i++) {
        inputs[i].checked = false;
        if ($.inArray(inputs[i].value, subset_list) >= 0) {
            if (action = true) {
                inputs[i].checked = true;
            }
        }
    }
};

function defaultTab() {
    document.getElementById('control_panel').style.display = "block";
    document.getElementById('control_panel_tab').className += " active";
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}










