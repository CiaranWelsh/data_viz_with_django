// function for controlling control_panel tabs
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

// function for setting default tab
function defaultTab() {
    document.getElementById('control_panel').style.display = "block";
    document.getElementById('control_panel_tab').className += " active";
}

defaultTab();

// function for ticking/unticking checkboxes under <ul> tag that are in subset_list.
// action is boolean
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

//set size of genes box
var option_height = $('#genes-box option:first').height();
var table_height = $('#ctrl-panel-tbl').height();
size = Math.floor(table_height / option_height);
$('#genes-box>select').attr('size', size);

$(window).resize(function () {

    $('#genes-box>select').attr('size', size);
    // console.log(table_height);
});

$('#ctrl-panel-tbl').height = $('#genes-box').height;


