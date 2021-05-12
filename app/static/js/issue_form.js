

// Grab our association fields
const folder = document.getElementById("id_associated_folder");
const file = document.getElementById("id_associated_file");
const loc = document.getElementById("id_associated_loc");

console.log(folder);

// Set editablity of the file and loc fields based on the value
//  of the folder field
function check_folder() {
    // If an option is currently selected in the folder field
    if($(folder).val()) {
        // console.log("folder has value");
        // Enable the file field
        file.disabled = false;
    // otherwise if the the field is empty
    } else {
        // console.log("folder is empty")
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
        // console.log("file has value");
        // Enable the loc field
        loc.disabled = false;
    // otherwise if the the field is empty
    } else {
        // console.log("file is empty")
        // Disable the loc field and set it to empty
        loc.disabled = true;
        loc.selectedIndex = 0;
    };
};

// When the page loads, enable/disable the fields 
// accordingly based on value
window.onload = () => {
    // console.log("page is loaded");
    // Call our check_folder and check_file functions
    check_folder();
    check_file();
};

// Listen for a change in the folder association field
// and enable/disable the file and loc fields accordingly
folder.addEventListener("change", function(){
    // console.log("change occurred");
    // Call our check_folder function
    check_folder();
});

// Listen for a change in the file association field
// and enable/disable the loc field accordingly
file.addEventListener("change", function(){
    // Call our check_file function
    check_file();
});
