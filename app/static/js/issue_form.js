

// Grab our association fields
const folder = document.getElementById("id_associated_folder");
const file = document.getElementById("id_associated_file");
const loc = document.getElementById("id_associated_loc");

console.log(folder);

// Listen for a change in the folder association field
folder.addEventListener("change", function(){
    console.log("change occurred");
    // If an option is currently selected in the field
    if($(folder).val()) {
        console.log("value was selected");
        file.disabled = false;
    // otherwise if the the field is empty
    } else {
        console.log("value is empty")
        file.disabled = true;
        loc.disabled = true;
        file.selectedIndex = 0;
        loc.selectedIndex = 0;
    }
});

// Listen for a change in the folder association field
file.addEventListener("change", function(){
    // If an option is currently selected in the field
    if($(file).val()) {
        console.log("value was selected");
        loc.disabled = false;
    // otherwise if the the field is empty
    } else {
        console.log("value is empty")
        loc.disabled = true;
        loc.selectedIndex = 0;
    }
});
