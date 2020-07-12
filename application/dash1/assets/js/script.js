$(function() {
    var showPass = 0;
    $(".btn-show-pass").on("click", function(){
        if(showPass == 0) {
            $(this).next("input").attr("type", "text");
            $(this).find("i").text("visibility_off");
            showPass = 1;
        }
        else {
            $(this).next("input").attr("type", "password");
            $(this).find("i").text("visibility");
            showPass = 0;
        }
    });

    $(".dropdown-trigger").dropdown({
        inDuration: 300,
        outDuration: 225,
        constrainWidth: false,
        belowOrigin: true // Displays dropdown below the button
    })
});
