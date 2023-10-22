ui = new Object();

ui.port = 50000
ui.reccount = 10

//********************************************************************************** */
window.addEventListener('beforeunload',function(event){ //when closing browser, close python  
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    event.preventDefault()

    fdata.append("request",'close'); //prepare files

    xhr.open('POST',"http://localhost:"+ui.port, true);

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(xhr.responseText);
            window.close()
        }
        else if (this.readyState == 4 && this.status != 200){
            alert(this.responseText)
        }
    };
    
    xhr.send(fdata);
    
})
//********************************************************************************** */
window.addEventListener('load',function(event){
    ui.onloadfunc()
})
//******************************************************************************************** */

ui.onloadfunc = function(){

    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    codeword = document.getElementsByTagName("body")[0].dataset.codeword

    fdata.append("request","uiportcodeword=" + codeword); //parol

    xhr.open('POST',"http://localhost:"+ui.port, true);

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(xhr.responseText);

            res = JSON.parse(xhr.responseText);
            
            if (res.port > 50000 ){
                ui.port = res.port;
            }
            else if (res.port == -1){
                if (ui.reccount >= 0){
                    ui.reccount = ui.reccount -1
                    ui.onloadfunc()
                    console.log("trying again")
                }                
            }

            if(res.args != null){

                for(key of Object.keys(res.args)){

                    if (document.getElementById(key)){ //if such id doesn't exists, than object will return null which is false
            
                        document.getElementById(key).value = res.args[key];
                    }
                }           
            }
        }
        else if (this.readyState == 4 && this.status != 200){
            alert(this.responseText)
            if (ui.reccount >= 0){
                ui.reccount = ui.reccount -1
                ui.onloadfunc()
                console.log("trying again")
            }  
        }
    };
    
    xhr.send(fdata);
}

