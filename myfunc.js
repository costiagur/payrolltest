myfunc = new Object();

//*********************************************************************************** */
myfunc.submit = function(){ //request can be insert or update
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    fdata.append("hazuti",document.getElementById("hazuti").files[0]);

    requestlist = []
    reqlevel = {}
    i = 0

    for (eachsemel of document.querySelectorAll("input[type =checkbox]")){
        if (eachsemel.checked == true){
            requestlist[i] = eachsemel.value
            reqlevel[eachsemel.id + "_level"] = document.getElementById(eachsemel.id + "_level").value
            i++
        }
    }

    console.log (requestlist)

    fdata.append("requestlist",JSON.stringify(requestlist));
    fdata.append("reqlevel",JSON.stringify(reqlevel));

    xhr.open('POST',"http://localhost:"+ui.port,true)

    document.getElementById("loader").style.display='block'; //display loader

    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {   
            console.log(this.responseText)

            document.getElementById("loader").style.display='none'; //close loader

            resobj = JSON.parse(this.responseText);

            if (resobj[0] == "Error"){
                alert(resobj[1])
            }
            else{
                myfunc.download(resobj[0],resobj[1])
            }
        }
        else if (this.readyState == 4 && this.status != 200){
            alert(this.responseText)
        }
    }

    xhr.send(fdata);     
}


//********************************************************************************************* */
myfunc.download = function(filename, filetext){

    var a = document.createElement("a");

    document.body.appendChild(a);

    a.style = "display: none";

    a.href = 'data:application/octet-stream;base64,' + filetext;

    a.download = filename;

    a.click();

    document.body.removeChild(a);

}
