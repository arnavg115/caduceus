function view(){
            var input = document.getElementById("password1");
            var input2 = document.getElementById("password2");
            if (input.type === "password"){
                input.type = "text"
                input2.type = "text"
            }
            else{
                input.type = "password"
                input2.type = "password"
            }
}