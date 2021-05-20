if($('body').hasClass("issueForm")){
    var repo = document.getElementById("id_repository")
    var folder = document.getElementById("id_associated_folder");
    var file = document.getElementById("id_associated_file");
    var loc = document.getElementById("id_associated_loc");
    window.onload = () => {
        check_repo();
        check_folder();
        check_file();
    };
    repo.addEventListener("change", function(){
        check_repo();
    });
    folder.addEventListener("change", function(){
        check_folder();
    });
    file.addEventListener("change", function(){
        check_file();
    });
}

function check_repo() {
    if($(repo).val()) {
        folder.disabled = false;
    } else {
        folder.disabled = true;
        file.disabled = true;
        loc.disabled = true;
        folder.selectedIndex = 0;
        file.selectedIndex = 0;
        loc.selectedIndex = 0;
    };
};

function check_folder() {
    if($(folder).val()) {
        file.disabled = false;
    } else {
        file.disabled = true;
        loc.disabled = true;
        file.selectedIndex = 0;
        loc.selectedIndex = 0;
    };
};

function check_file() {
    if($(file).val()) {
        loc.disabled = false;
    } else {
        loc.disabled = true;
        loc.selectedIndex = 0;
    };
};
