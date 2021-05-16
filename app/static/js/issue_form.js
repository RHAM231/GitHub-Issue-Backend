// Start our script if the loaded page is the issue form
if($('body').hasClass("issueForm")){
    // Grab our association fields
    var repo = document.getElementById("id_repository")
    var folder = document.getElementById("id_associated_folder");
    var file = document.getElementById("id_associated_file");
    var loc = document.getElementById("id_associated_loc");
    // When the page loads, enable/disable the fields 
    // accordingly based on value
    window.onload = () => {
        // Call our check_folder and check_file functions
        check_folder();
        check_file();
    };
    // Listen for a change in the folder association field
    // and enable/disable the file and loc fields accordingly
    folder.addEventListener("change", function(){
        // Call our check_folder function
        check_folder();
    });
    // Listen for a change in the file association field
    // and enable/disable the loc field accordingly
    file.addEventListener("change", function(){
        // Call our check_file function
        check_file();
    });
}


// Set editablity of the file and loc fields based on the value
//  of the folder field
function check_folder() {
    // If an option is currently selected in the folder field
    if($(folder).val()) {
        // Enable the file field
        file.disabled = false;
    // otherwise if the the field is empty
    } else {
        // Disable the file and loc fields and set them to empty
        file.disabled = true;
        loc.disabled = true;
        file.selectedIndex = 0;
        loc.selectedIndex = 0;
    };
};

// Set editablity of the loc field based on the value of the
// file field
function check_file() {
    // If an option is currently selected in the field
    if($(file).val()) {
        // Enable the loc field
        loc.disabled = false;
    // otherwise if the the field is empty
    } else {
        // Disable the loc field and set it to empty
        loc.disabled = true;
        loc.selectedIndex = 0;
    };
};
