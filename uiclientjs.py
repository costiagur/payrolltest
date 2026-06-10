## create 
def uiclientjs(port,currentfolder):
    uiclientstr = f"""
ui = new Object();

ui.port = {port}

//********************************************************************************** */
window.addEventListener('beforeunload',function(event){{ //when closing browser, close python  
    var xhr = new XMLHttpRequest();
    var fdata = new FormData();

    //event.preventDefault()

    fdata.append("request",'close'); //prepare files

    xhr.open('POST',"http://127.0.0.1:"+ui.port, true);

    xhr.onreadystatechange = function() {{
        if (this.readyState == 4 && this.status == 200) {{
            console.log(xhr.responseText);
            window.close()
        }}
        else if (this.readyState == 4 && this.status != 200){{
            alert(this.responseText)
        }}
    }};
    
    xhr.send(fdata);
    
}})
"""
    with open(f'{currentfolder}/uiclient.js',"w") as jsfile:
        jsfile.write(uiclientstr)
    #
#
