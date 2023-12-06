myfunc = new Object();

//*********************************************************************************** */
myfunc.submit = function(){ //request can be insert or update
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    fdata.append("request","salarycheck");   
    
    fdata.append("hazuti",document.getElementById("hazuti").files[0]);
    fdata.append("f1313",document.getElementById("f1313").files[0]);

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
            //console.log(this.responseText)

            document.getElementById("loader").style.display='none'; //close loader

            resobj = JSON.parse(this.responseText);

            if (resobj[0] == "Error"){
                alert(resobj[1])
            }
            else{
                myfunc.download(resobj[0],resobj[1])
                reptb = document.getElementById("reptb")

                thead = "<thead id='repthead'><tr><th>מספר עובד</th><th>שם עובד</th><th onclick='myfunc.sort(this)'>נטו</th><th onclick='myfunc.sort(this)'>ברוטו שוטף</th><th onclick='myfunc.sort(this)'>ברוטו הפרשים</th><th onclick='myfunc.sort(this)'>ניכויי חובה</th>";
                thead += "<th onclick='myfunc.sort(this)'>ניכויי זכות</th><th onclick='myfunc.sort(this)'>ב.שוטף חודש קודם</th><th onclick='myfunc.sort(this)'>הפרש ברוטו</th><th onclick='myfunc.sort(this)'>הפ. חד שנתיים</th><th onclick='myfunc.sort(this)'>הפרש רכב</th><th onclick='myfunc.sort(this)'>הפרש לא מוסבר</th>"
                thead += "<th style='width:16.6%'>פרוט הפ. ברוטו שוטף</th><th style='width:16.6%'>פרוט הפ. ברוטו רטרו</th></tr></thead>"

                tbody = "<tbody id='reptbody'>"
                tbobj = JSON.parse(resobj[2])

                for (eachid in tbobj){
                    tbody += "<tr>"
                    tbody += `<td>${eachid}</td>`
                    currtbody = ""
                    retrobody = ""

                    subobj = tbobj[eachid]
                    console.log(subobj)

                    for (eachkey in subobj){
                        if(eachkey == "Empname"){
                            tbody += `<td>${subobj[eachkey]}</td>`
                        } 
                        else if (eachkey != "CurrGrossData" && eachkey != "RetroGrossData"){
                            tbody += `<td>${parseInt(subobj[eachkey])}</td>`
                        }
                        else if (eachkey == "CurrGrossData"){
                            
                            if (Object.keys(subobj.CurrGrossData).length != 0){ //check if it is not an empty object
                                currtbody += `<td><table><thead><tr><th>סמל</th><th>הפרש</th><th>סכום</th></tr></thead><tbody>`
                                    
                                for (subkey in subobj.CurrGrossData){
                                    currtbody += "<tr>"
                                    currtbody += `<td>${subobj.CurrGrossData[subkey].Elem}</td>`
                                    currtbody += `<td>${subobj.CurrGrossData[subkey].Diff}</td>`
                                    currtbody += `<td>${subobj.CurrGrossData[subkey].Amount}</td>`
                                    currtbody += "</tr>"
                                }
    
                                currtbody += `</tbody></table></td>`
                                
                            }
    
                            else{
                                currtbody += `<td></td>`
                            }
                        }
                         
                        else if (eachkey == "RetroGrossData"){
                            
                            if (Object.keys(subobj.RetroGrossData).length != 0){ //check if it is not an empty object 
                                retrobody += `<td><table><thead><tr><th>סמל</th><th>הפרש</th><th>סכום</th></tr></thead><tbody>`
 
                                for (subkey in subobj.RetroGrossData){
                                    retrobody += "<tr>"
                                    retrobody += `<td>${subobj.RetroGrossData[subkey].Elem}</td>`
                                    retrobody += `<td>${subobj.RetroGrossData[subkey].Diff}</td>`
                                    retrobody += `<td>${subobj.RetroGrossData[subkey].Amount}</td>`
                                    retrobody += "</tr>"
                                }

                                retrobody += `</tbody></table></td>`
                            }
                            else{
                                retrobody += `<td></td>`
                            }
                        }
                    }

                    tbody += ((currtbody != "")?currtbody:"<td></td>") + ((retrobody != "")?retrobody:"<td></td>") + "</tr>"
                }
                tbody += "</tbody>"
                
                reptb.innerHTML = thead + tbody;
                
                document.getElementById("repthead").children[0].children[2].click()
                //myfunc.sort()
            }
        }
        else if (this.readyState == 4 && this.status != 200){
            alert(this.responseText)
        }
    }

    xhr.send(fdata);     
}
//********************************************************************************************* */
myfunc.removechecks = function(){
    if (document.getElementById("remchecks").dataset.removecheck == "0"){
        document.getElementById("remchecks").dataset.removecheck = "1"
        for (eachsemel of document.querySelectorAll("input[type =checkbox]")){
            if (eachsemel.checked == true){
                eachsemel.checked = false
            }
        }   
    }
    else{
        document.getElementById("remchecks").dataset.removecheck = "0"
        for (eachsemel of document.querySelectorAll("input[type =checkbox]")){
            if (eachsemel.checked == false){
                eachsemel.checked = true
            }
        }           
    }


}
//********************************************************************************************* */
myfunc.sort = function(ev){
    ths = Array.from(document.getElementById("repthead").children[0].children)

    caller = ths.indexOf(ev)

    tbody = document.getElementById("reptbody")
    trs = Array.from(tbody.children)
    initrs = Array.from(tbody.children)
    newtbody = document.createElement("tbody")

    for (eachtr of initrs){
        vallist = []

        for (tr of trs){
            td  = tr.children[caller]
            vallist.push(parseInt(td.innerHTML))
        }
    
        maxval = vallist.reduce((a, b) => Math.max(a, b), -Infinity)
        j=0;
        for (tr of trs){
            td  = tr.children[caller]
            if (parseInt(td.innerHTML) == maxval){
                newtbody.appendChild(tr)
                trs.splice(j,1)
            }
            j++
        }
    }

    table = document.getElementById("reptb")
    table.children[1].remove()
    newtbody.setAttribute('id',"reptbody")
    table.appendChild(newtbody)
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

//********************************************************************************************** */
myfunc.switchtabs = function(divid){

    switchers = document.getElementsByClassName("switcher")
    
    bars = document.getElementsByClassName("w3-bar-item")

    for (eachswitch of switchers){
        if (eachswitch.id == divid){
            eachswitch.classList.remove("nondisplayed");
        }
        else{
            eachswitch.classList.add("nondisplayed");
        }
    }

    for (eachbar of bars){
        if (eachbar.id == "bar"+divid){
            eachbar.classList.add("w3-text-teal")
        }
        else{
            eachbar.classList.remove("w3-text-teal")
        }
    }
}

//*********************************************************************************** */
myfunc.submitfunds = function(){ //request can be insert or update
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    fdata.append("request","fundscheck");

    fdata.append("fundsfile",document.getElementById("fundsfile").files[0]);

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
                console.log(resobj[2])
            }
        }
        else if (this.readyState == 4 && this.status != 200){
            alert(this.responseText)
        }
    }

    xhr.send(fdata);     
}