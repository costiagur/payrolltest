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
                //console.log(this.responseText)
    
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
                    myfunc.response(resobj[2],"")   
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
        myfunc.response("בדיקות הסתיימו","")
    }

    document.getElementById("loader").style.display='none'; //close loader


}
//************************************************************************************************ */
myfunc.upload = async function(reqfiletype="new"){
    var fdata = new FormData();

    fdata.append("request","fileupload");   

    fdata.append("prevhazuti",document.getElementById("prevhazuti").files[0]);
    fdata.append("currhazuti",document.getElementById("currhazuti").files[0]);
    fdata.append("hoursquery1313",document.getElementById("hoursquery1313").files[0]);
    fdata.append("hoursquery1307",document.getElementById("hoursquery1307").files[0]);
    fdata.append("timesheetfile",document.getElementById("timesheetfile").files[0]);

    fdata.append("reqfiletype",reqfiletype);
    
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
           if (document.getElementById("currhazuti").files[0] != undefined){
                myfunc.submit()
            }
       }
    }
}
//************************************************************************************************* */
myfunc.adhoctest = async function(){
    var fdata = new FormData();

    fdata.append("request","adhoctest");
    fdata.append("semel",document.getElementById("semel").value);
    fdata.append("reqtype",document.getElementById("reqtype").value);
    fdata.append("pensionin",(document.getElementById("pensionin").checked == true)?1:0);



    document.getElementById("loader").style.display='block'; //display loader

    const resobj = await myfunc.sendrequest(fdata)
    if (resobj[0] == "Error"){
        myfunc.msg( resobj[0], resobj[1])
        document.getElementById("loader").style.display='none'; //close loader

    }
    else{
       if (resobj[0] == "adhocfile"){
        myfunc.download(resobj[1], resobj[2])
        document.getElementById("loader").style.display='none'; //close loader
       }
    }
}
//************************************************************************************************ */
myfunc.hazuti13m = async function(){
    var fdata = new FormData();

    fdata.append("request","hazuti13m");   
    
    fdata.append("hazuti13m",document.getElementById("hazuti13m").files[0]);
    fdata.append("expectedplus",document.getElementById("expectedplus").value);
    
    document.getElementById("loader").style.display='block'; //display loader

    const resobj = await myfunc.sendrequest(fdata)
    if (resobj[0] == "Error"){
        myfunc.msg(resobj[0], resobj[1])
        document.getElementById("loader").style.display='none'; //close loader

    }
    else{
       if (resobj[0] == "resanalysis"){
           myfunc.download(resobj[1], resobj[2])
           document.getElementById("loader").style.display='none'; //close loader
       }
    }
}
//************************************************************************************************* */
myfunc.resulttable = function(resobj){ //request can be insert or update
 
    tbody = ""

    for (eachid in resobj){

        //console.log(resobj[eachid].Empname)

        tbody += "<tr>";
        tbody += `<td onclick="myfunc.onecompare(${eachid})">${eachid}</td>`;
        tbody += `<td>${resobj[eachid].Empname}</td>`;
        tbody += `<td>${resobj[eachid].Pensioneer}</td>`;       
        tbody += `<td>${Number(resobj[eachid].NetCur).toFixed(0)}</td>`;
        tbody += `<td>${resobj[eachid].GrossCur.toFixed(0)}</td>`;
        tbody += `<td>${resobj[eachid].GrossPrev.toFixed(0)}</td>`;
        tbody += `<td>${resobj[eachid].TaxesCur.toFixed(0)}</td>`;
        tbody += `<td>${resobj[eachid].DeductsCur.toFixed(0)}</td>`;
        tbody += `<td>${resobj[eachid].Annual.toFixed(0)}</td>`;
        tbody += `<td>${resobj[eachid].Vehicle.toFixed(0)}</td>`;
        tbody += `<td>${resobj[eachid].Severance.toFixed(0)}</td>`;
        tbody += `<td>${resobj[eachid].Unexplained.toFixed(0)}</td>`;
        tbody += `<td>${resobj[eachid].Order}</td>`;
        
        currtbody = "";
        retrobody = "";

        if (resobj[eachid].CurrDiff != ""){ //check if it is not an empty object
                currtbody += `<td class="displaytable" onclick="myfunc.displaytable(this)"><div style="display:none"><table><thead><tr><th>סמל</th><th>הפרש מהותי</th></tr></thead><tbody>`;

                for (i=0;i<resobj[eachid].CurrDiff.Elem_heb.length;i++){
                    currtbody += "<tr>";
                    currtbody += `<td>${resobj[eachid].CurrDiff.Elem_heb[i]}</td>`;
                    currtbody += `<td>${resobj[eachid].CurrDiff.Currentdiff[i]}</td>`;
                    currtbody += "</tr>";
                }
    
            tbody +=  currtbody + `</tbody></table></div></td>`;                    
        }
        else{
            tbody += `<td></td>`;
        }
    
        if (resobj[eachid].RetroDiff != ""){ //check if it is not an empty object 
                retrobody += `<td class="displaytable" onclick="myfunc.displaytable(this)"><div style="display:none"><table><thead><tr><th>סמל</th><th>הפרש</th></tr></thead><tbody>`;
 
                for (i=0;i<resobj[eachid].RetroDiff.Elem_heb.length;i++){ 
                    retrobody += "<tr>";
                    retrobody += `<td>${resobj[eachid].RetroDiff.Elem_heb[i]}</td>`;
                    retrobody += `<td>${resobj[eachid].RetroDiff.Retrodiff[i]}</td>`;
                    retrobody += "</tr>";
                }

            tbody += retrobody + `</tbody></table></div></td>`;
        }
        else{
            tbody += `<td></td>`;
        }
        
        tbody += `</tr>`
    }    

    document.getElementById("reptbody").innerHTML = tbody;
                
    document.getElementById("repthead").children[0].children[2].click()

}
//*********************************************************************************** */
myfunc.onecompare = async function(empid){ //request can be insert or update
    var fdata = new FormData();

    fdata.append("request","onecompare");
    fdata.append("empid",empid);   
   
    document.getElementById("loader").style.display='block'; //display loader


    const resobj = await myfunc.sendrequest(fdata)
    if (resobj[0] == "Error"){
        document.getElementById("loader").style.display='none'; //close loader
        myfunc.msg(resobj[0], resobj[1])

    }
    else{
        
        thead = "<thead><tr>";
        thead += "<th>אגף</th>";
        thead += "<th>מנ</th>";
        thead += "<th>סוג</th>";
        thead += "<th>סמל</th>";
        thead += "<th>תקופה</th>";
        thead += "<th>סכום נוכחי</th>";
        thead += "<th>סכום קודם</th>";
        thead += "<th>הפרש</th>";
        thead += "</tr></thead>";

        tbody = "<tbody>";

        console.log(resobj)

        for (eachelem in resobj[1]){

            tbody += "<tr>";
            tbody += `<td>${resobj[1][eachelem].Division}</td>`;
            tbody += `<td>${resobj[1][eachelem].mn}</td>`;       
            tbody += `<td>${resobj[1][eachelem].Elemtype_heb}</td>`;
            tbody += `<td>${resobj[1][eachelem].Elem_heb}</td>`;
            tbody += `<td>${resobj[1][eachelem].Period}</td>`;
            tbody += `<td>${resobj[1][eachelem].CurAmount.toFixed(0)}</td>`;
            tbody += `<td>${resobj[1][eachelem].PrevAmount.toFixed(0)}</td>`;
            tbody += `<td>${resobj[1][eachelem].Diff.toFixed(0)}</td>`;
            tbody += `</tr>`
        }
        
        tbody += "</tbody>"

        restab = `<table id="onepersontab" class="w3-table w3-bordered w3-striped w3-border w3-hoverable">${thead}${tbody}</table>`
        document.getElementById("loader").style.display='none'; //close loader

        myfunc.msg(`נתוני עובד ${empid}`,restab)  
        
    }
}

//********************************************************************************************* */
myfunc.makellm = async function(reqtype){
    var fdata = new FormData();

    fdata.append("request","llmquery");
    fdata.append("reqtype",reqtype);
    fdata.append("myrequest",(reqtype=='timesheet')?document.getElementById("timesheetrequest").value:document.getElementById("hazutirequest").value);
   
    document.getElementById("loader").style.display='block'; //display loader

    const resobj = await myfunc.sendrequest(fdata)
    if (resobj[0] == "Error"){
        document.getElementById("loader").style.display='none'; //close loader
        myfunc.msg(resobj[0], resobj[1])
    }
    else{
        document.getElementById("loader").style.display='none'; //close loader
        if (resobj[0] == "timesheet"){
            document.getElementById("timesheetsql").value = resobj[1];
        }
        else if (resobj[0] == "hazutirequest"){
            document.getElementById("hazutisql").value = resobj[1];
        }
    }
}
//********************************************************************************************* */
myfunc.runsql = async function(reqtype,how){ //request can be insert or update
    var fdata = new FormData();

    fdata.append("request","sqlquery");
    fdata.append("reqtype",reqtype);   
    fdata.append("myrequest",(reqtype=='timesheet')?document.getElementById("timesheetsql").value:document.getElementById("hazutisql").value);
    fdata.append("how",how);

    document.getElementById("loader").style.display='block'; //display loader

    document.getElementById("timesheetresult").innerHTML = ''


    const resobj = await myfunc.sendrequest(fdata)
    if (resobj[0] == "Error"){
        document.getElementById("loader").style.display='none'; //close loader
        myfunc.msg(resobj[0], resobj[1])

    }
    else{
        document.getElementById("loader").style.display='none'; //close loader

        if (how == 'show'){

            table = '<table class="w3-table-all w3-card-4 w3-bordered"><thead><tr>';

            //console.log(resobj[0])

            for (eachkey of Object.keys(resobj[1][0])){
                table += `<th>${eachkey}</th>`
            }

            table += '</tr></thead><tbody>';
            
            for (var eachobj of Object.values(resobj[1])){
                //console.log(eachobj)

                table += "<tr>";
                for (var val of Object.values(eachobj)){
                    table += `<td>${val}</td>`;
                }
                table += "</tr>";
            }
            
            table += "</tbody></table>"

            document.getElementById("timesheetresult").innerHTML = table
        }
        else if(how == 'xls'){
            myfunc.download(resobj[1][0], resobj[1][1])
        }       
        
    }
}