myfunc = new Object();
//********************************************************************************************* */
myfunc.removechecks = function(){
    if (document.getElementById("remchecks").dataset.removecheck == "0"){
        document.getElementById("remchecks").dataset.removecheck = "1"
        for (eachsemel of document.querySelectorAll("input[type =checkbox]")){
            if (eachsemel.checked == true){
                eachsemel.checked = false
            }
        }
        document.getElementById("remchecks").value = "בחירה"   
    }
    else{
        document.getElementById("remchecks").dataset.removecheck = "0"
        for (eachsemel of document.querySelectorAll("input[type =checkbox]")){
            if (eachsemel.checked == false){
                eachsemel.checked = true
            }
        }
        document.getElementById("remchecks").value = "הסרה"
    }
}
//********************************************************************************************* */
myfunc.displaytable = function(td){
    if (td.children[0].style.display == 'none'){
        td.children[0].style.display = 'table';
    }
    else{
        td.children[0].style.display = 'none';
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
//*********************************************************************************** */
myfunc.msg = function(title,msg_txt){
    document.getElementById("msg_title").innerHTML = title
    document.getElementById("msg_txt").innerHTML = msg_txt
    document.getElementById("msg_dg").showModal()
}
//********************************************************************************************* */
myfunc.response = function(txt1,txt2){
    tbody = document.getElementById("response_tbody")
    tr = document.createElement("tr")
    td1 = document.createElement("td")
    td1_content = document.createTextNode(txt1)
    td1.appendChild(td1_content)

    td2 = document.createElement("td")
    td2_content = document.createTextNode(txt2)
    td2.appendChild(td2_content)
  
    tbody.appendChild(tr)
    tr.appendChild(td1)
    td1.insertAdjacentElement('afterend',td2)

    document.getElementById("response_dg").showModal()
}
//********************************************************************************************* */
myfunc.resp_close = function(){
    document.getElementById("response_dg").close();
    tbody = document.getElementById("response_tbody")
    tbody.innerHTML = ""
}
//********************************************************************************************* */
myfunc.sendrequest = function(fdata){
    return new Promise((resolve) =>{    
        var xhr = new XMLHttpRequest();
        xhr.open('POST',"http://localhost:"+ui.port,true)
    
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {   
                console.log(this.responseText)
    
                resobj = JSON.parse(this.responseText);
                resolve(resobj)    
     
            }
            else if (this.readyState == 4 && this.status != 200){
                resolve(["Error",this.responseText])

            }
        }
    
        xhr.send(fdata);   
    })
}

//*********************************************************************************** */
myfunc.submit = async function(){ //request can be insert or update
    var fdata = new FormData();

    fdata.append("request","salarycheck");   

    document.getElementById("loader").style.display='block'; //display loader

    for (eachsemel of document.querySelectorAll("input[type =checkbox]")){
        if (eachsemel.checked == true){
            fdata.set("reqtest",eachsemel.value);
            fdata.set("reqlevel",document.getElementById(eachsemel.id + "_level").value);
               
            const resobj = await myfunc.sendrequest(fdata)
            if (resobj[0] == "Error"){
                myfunc.msg(resobj[0], resobj[1])
            }
            else{
                if (resobj[0] == "totalrep"){
                    myfunc.response("טבלת השוואה מוכנה","")   
                    myfunc.resulttable(resobj[1])
                }
                else{
                    myfunc.response(resobj[2],resobj[1])
                }
            } 
        }
    }

    fdata.set("request","testfile");
    const resobj = await myfunc.sendrequest(fdata)
    if (resobj[0] == "testfile"){
        myfunc.download(resobj[1],resobj[2])
    }

    document.getElementById("loader").style.display='none'; //close loader


}
//************************************************************************************************ */
myfunc.upload = async function(){
    var fdata = new FormData();

    fdata.append("request","fileupload");   

    fdata.append("hazuti",document.getElementById("hazuti").files[0]);
    fdata.append("hoursquery",document.getElementById("hoursquery").files[0]);

    document.getElementById("loader").style.display='block'; //display loader

    const resobj = await myfunc.sendrequest(fdata)
    if (resobj[0] == "Error"){
        myfunc.msg( resobj[0], resobj[1])
        document.getElementById("loader").style.display='none'; //close loader

    }
    else{
       if (resobj[0] == "uploadedrows"){
           myfunc.response("מספר רשימות שהועלו", resobj[1])
           document.getElementById("loader").style.display='none'; //close loader
           myfunc.submit()
       }
    }
}
//************************************************************************************************* */
myfunc.resulttable = function(resobj){ //request can be insert or update
 
    reptbody = document.getElementById("reptbody")

    tbobj = resobj

    for (eachid in tbobj){
        tbody += "<tr>"
        tbody += `<td>${eachid}</td>`
        currtbody = ""
        retrobody = ""

        subobj = tbobj[eachid]

        for (eachkey in subobj){
            if(eachkey == "Empname" || eachkey == "Order"){
                tbody += `<td>${subobj[eachkey]}</td>`
            } 
            else if (eachkey != "CurrDiff" && eachkey != "RetroDiff"){
                tbody += `<td>${parseInt(subobj[eachkey])}</td>`
            }
            else if (eachkey == "CurrDiff"){
                            
                if (Object.keys(subobj.CurrDiff).length != 0){ //check if it is not an empty object
                    currtbody += `<td class="displaytable" onclick="myfunc.displaytable(this)"><div style="display:none"><table><thead><tr><th>סמל</th><th>הפרש מהותי</th></tr></thead><tbody>`
                                    
                    for (subkey in subobj.CurrDiff){
                        currtbody += "<tr>"
                        currtbody += `<td>${subobj.CurrDiff[subkey].Elem_heb}</td>`
                        //currtbody += `<td>${subobj.CurrGrossData[subkey].Diff}</td>`
                        currtbody += `<td>${subobj.CurrDiff[subkey].Significant}</td>`
                        currtbody += "</tr>"
                    }
    
                        currtbody += `</tbody></table></div></td>`
                                
                    }
    
                else{
                    currtbody += `<td></td>`
                }
            }
                         
            else if (eachkey == "RetroDiff"){
                            
                if (Object.keys(subobj.RetroDiff).length != 0){ //check if it is not an empty object 
                    retrobody += `<td class="displaytable" onclick="myfunc.displaytable(this)"><div style="display:none"><table><thead><tr><th>סמל</th><th>הפרש</th><th>סכום</th></tr></thead><tbody>`
 
                    for (subkey in subobj.RetroDiff){
                        retrobody += "<tr>"
                        retrobody += `<td>${subobj.RetroDiff[subkey].Elem_heb}</td>`
                        //retrobody += `<td>${subobj.RetroGrossData[subkey].Diff}</td>`
                        retrobody += `<td>${subobj.RetroDiff[subkey].Significant}</td>`
                        retrobody += "</tr>"
                    }

                    retrobody += `</tbody></table></div></td>`
                }
                else{
                    retrobody += `<td></td>`
                }
            }
        }

        tbody += ((currtbody != "")?currtbody:"<td></td>") + ((retrobody != "")?retrobody:"<td></td>") + "</tr>"
    }
                
    reptbody.innerHTML = tbody;
                
    document.getElementById("repthead").children[0].children[2].click()

}