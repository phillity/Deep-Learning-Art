/*
    DeepLearningArtApp: used by index.html
*/

(function($) {
    "use strict";

    // Retrieve token from the image upload form
    $( document ).ready(function() {

        // Create global for csrf token
        var imageUploadform_csrf_token = $("#imageUploadform input[name=csrfmiddlewaretoken]").val();

        // Create jquery ui dialog for model selection
        $("#dialog").dialog({
            autoOpen: false,
            modal: true,
            dialogClass: "noTitleBar",
            resizable: false,
            open: function(event, ui) {
                $("#buttonOk").click(function() {
                    $("#dialog").dialog("close");
                });
            },
            close: function(event, ui) {
                $("#selectedModelImage").attr("src", $("#modelSelect").val());
            },
        });

        // When selection changes in choose model dialog
        $("#modelSelect").change(function() {
            $("#modelSampleImg").attr("src", $("#modelSelect").val())
        });

        // Load up model select dialog (on page load only)
        $.ajax({
                url: "/models/",
                type: "get",
                success: function(data) {
                    if (data["status"] === "true") {
                        let $select = $("#modelSelect");
                        $select.find("option").remove();  
                        $.each(data.models,function(index, value) 
                        {
                            let modelThumbnailImg = data.modelThumbnailDir + "/" + value + ".jpg";
                            $select.append("<option value='" + modelThumbnailImg + "'>" + value + "</option>");
                        });

                        // Set the sample image
                        $("#modelSampleImg").attr("src", $select.val());
                        $("#selectedModelImage").attr("src", $select.val());
                    }
                    else {
                    }
                },
                error: function (error) {
                    console.log(error);
                    alert('Sorry and unexpected error has occurred, please try again');
                },
            });

        // When user clicks on model gallery icon or model image, open up the choose model dialog
        $("#chooseModel,#selectedModelImage").click(function() {
            $("#dialog").dialog("open");
        });
        
        // When user clicks on upload image icon or uploaded image
        $("#chooseImage,#uploadedImage").click(function() {
            $("#id_file").trigger( "click" );
        });

        // When user chooses the upload image
        $("#id_file").on("change",function(e) {
            let data = new FormData($('form').get(0));
            $.ajax({
                url: $("#imageUploadform").attr("action"),
                type: $("#imageUploadform").attr("method"),
                data: data,
                cache: false,
                processData: false,
                contentType: false,
                success: function(data) {
                    if (data["status"] === "true") {
                        $("#uploadedImage").attr("src", data["filePath"]);
                    }
                    else {
                        let errMsg = "Sorry and unexpected error has occurred, please try again";
                        for (i=0; i<data.errors.length; i++)
                        {
                            console.log(data.errors[i]);
                            if (data.errors[i].length == 2)
                                errMsg = data.errors[i][1];  // extract the error msg
                        }
                        $("#uploadedImage").removeAttr("src");
                        alert(errMsg);
                    }
                },
                error: function (error) {
                    console.log(error);
                    alert('Sorry and unexpected error has occurred, please try again');
                },
            });
            
            // Clear file input so next time it triggers
            $("#id_file").val("");
        });
    
        // When user clicks on the merge icon
        $("#doMerge").click(function() {
            let image = $("#uploadedImage").attr("src");
            let model = $("#modelSelect :selected").text();

            // If no image yet, guide the user
            if (!image)
            {
                $("#chooseImage").click();
                return;
            }

            let data = { "image" : image, "model" : model, "csrfmiddlewaretoken" : imageUploadform_csrf_token };
            $.ajax({
                url: "/merge/",
                type: "post",
                data: data,
                success: function(data) {
                    if (data["status"] === "true") {
                        $("#mergedImage").attr("src", data["filePath"]);
                    }
                    else {
                        console.log(data.error);
                        $("#mergedImage").removeAttr("src");
                        alert('Sorry and unexpected error has occurred, please try again');
                    }
                },
                error: function (error) {
                    console.log(error);
                    alert('Sorry and unexpected error has occurred, please try again');
                },
            });                
        });

        // When user clicks on save result icon or merged image
        $("#downloadMerge,#mergedImage").click(function() {
            let imageFileName = $("#mergedImage").attr("src");
            
            // If no image yet, guide the user
            if (!imageFileName)
            {
                $("#doMerge").click();
                return;
            }

            let data = { "image" : imageFileName, "csrfmiddlewaretoken" : imageUploadform_csrf_token };
            $.ajax({
                url: "/download/image/",
                type: "post",
                data: data,
                xhrFields:{ responseType: 'blob' },
                success: function(data, textStatus, xhr) {
                    if (!xhr.status === 200) {
                        console.log(data.error);
                        alert("Sorry and unexpected error has occurred, please try again");
                        return;
                    }

                    // Write image to javascript blob object and then simulate download interaction
                    let blob = new Blob([data], { type: 'application/jpeg' });
                    let link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = imageFileName.substring(imageFileName.lastIndexOf('/')+1);;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    window.URL.revokeObjectURL(link.href);
                },
                error: function (error) {
                    console.log(error);
                    alert('Sorry and unexpected error has occurred, please try again');
                },
            });                
        });
    });
})(jQuery);