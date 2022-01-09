// Basic Editor Settings
var editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.getSession().setMode("ace/mode/c_cpp");
editor.setOptions({
    fontSize: "18px",
    cursorStyle: 'smooth',
    enableBasicAutocompletion: true,
    enableLiveAutocompletion: true,
    enableSnippets: true,
});

// set text wrap
editor.session.setUseWrapMode(true);

// If user changes from one language to other
$("#p_language").change(function () {
        let l =($(this).val());
        if (l === "python"){
            editor.getSession().setMode("ace/mode/python");
        }
        else if (l === "cpp"){
        	editor.getSession().setMode("ace/mode/c_cpp");
        }
        else if (l === "c"){
        	editor.getSession().setMode("ace/mode/c_cpp");
        }
    });

// Helper function for setting codes
function setC_Code(code, language) {
    editor.setValue(code);
    if (language === 'c' || language === 'cpp') {
        editor.session.setMode("ace/mode/c_cpp");
    } else if (language === 'python') {
        editor.session.setMode("ace/mode/python");
    }
    document.getElementById('p_language').value = language;
}

// if no code is available save pre defined C code in Session Storage, else saves available code
$(document).ready(function() {
    let c_Code = sessionStorage.getItem('c');
    let cpp_Code = sessionStorage.getItem('cpp');
    let python_Code = sessionStorage.getItem('python');

    // Check if there's any code available in the session storage
    if (c_Code != null) {
        setC_Code(c_Code, 'c');
    } else if (cpp_Code != null) {
        setC_Code(cpp_Code, 'cpp');
    } else if (python_Code != null) {
        setC_Code(python_Code, 'python');
    } else {
        // If not code available set it to C language
        editor.setValue("#include <stdio.h> \nint main(){\n\n    return 0;\n}\n");
        editor.session.setMode("ace/mode/c_cpp");
        document.getElementById('p_language').value = 'c';
        editor.gotoLine(4);
    }
});

// Self Calling Function to detect previous & current programming language, save code to the session storage
(function() {
    let previous;

    $("select[name=language]").focus(function() {
        // Store the current value on focus, before it changes
        previous = this.value;
        let current_code = editor.getValue();
        sessionStorage.setItem(previous, current_code);
    }).change(function() {
        // Save code with previous value, and code
        let p_language = this.value;
        let codeAvailable = sessionStorage.getItem(p_language);
        if (codeAvailable != null) {
            setC_Code(codeAvailable, p_language);
        } else {
            editor.setValue('');
        }
        previous = this.value;
    });
})();

// If Editor Goes Out of focus, then save code to Session Storage
$("#editor").focusout(function () {
    let code = editor.getValue();
    let language = document.getElementById('p_language').value;
    sessionStorage.setItem(language, code);
})

// Change Font size of editor
function changeFontSize() {
    let font_size = document.getElementById('select-font-size').value;
    editor.setOptions({
        fontSize: font_size,
    });
}

// For showing share options
function showShareOptions() {
    $('#share-btn').prop('disabled', true);
    // Add HTML for share options
    $('#compilier').append('<div class="sharePop"> <div> <input type="text" id="shareURL" readonly> </div> <div> <select name="dropdownShareOptions" id="dropdownShareOptions" title="Select Permissions"> <option value="globally-viewer" class="options">Globally Viewer</option> <option value="globally-editor" class="options">Globally Editor</option> </select> </div> <div> <span class="material-icons-round" title="Copy Link" onclick="copyLink()">content_copy</span> </div> </div>');
    let result = '';
    if (location.pathname === '/') {
        // Generate 8 digit random string for unique url if it's not shared URL
        let characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let charactersLength = characters.length;
        for (let i = 0; i < 8; i++) {
            result += characters.charAt(Math.floor(Math.random() * charactersLength));
        }
        result = '/' + result;
    }
    else {
        // If shared url then share the same url
        result = location.pathname;
    }
    // let result = Math.random().toString(36).substring(2, 10);
    document.getElementById('shareURL').value = 'http://codeit.pythonanywhere.com' + result;
}

// Click on the content_copy button/icon
function copyLink() {
    let uniqueShareUrl = document.getElementById('shareURL').value;
    let permission = document.querySelector('#dropdownShareOptions').value;
    let language = document.getElementById('p_language').value;
    $.ajax({
       url: 'saveShareCode',
       type: 'POST',
       data: {
           code: editor.getValue(),
           permission: permission,
           language: language,
           uniqueShareUrl: uniqueShareUrl
       },
        success: function (json) {
            if (json.saved === true) {
                alert('Permission Updated! '+ permission +' and Copied to Clipboard');
            }
            else {
                alert('Something went wrong, please contact admin via report bug!');
            }
        },
        error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
             }
    });
    navigator.clipboard.writeText(uniqueShareUrl);
    $('#share-btn').prop('disabled', false);
    $('.sharePop').remove();
}

// Save code with specific name & use ajax for post request
function saveCode() {
    let filename = prompt("Please enter filename without extension:");
    let language = document.getElementById('p_language').value;
    if (language === 'python')
        language = 'py'
    if (filename != null && filename !== "") {
        filename = filename + '.' + language;
        $.ajax ({
            type: 'POST',
            url: 'save_code',
            data: {
                name: filename, 
                code: editor.getValue(), 
                language: language
            },
            success: function (json){
                if (json.is_saved === false)
                    alert(filename + " Saved!");
                else
                    alert('Something went wrong!')
            },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
        });
    }
}


// Compile Code and use ajax for post request
function compileCode() {
    $('.loader').show();
    let compile_btn = $('#compile-btn');
    compile_btn.prop('disabled', true);

    // Code
    // console.log(editor.getValue());
    // custom Input
    let custom_input = document.getElementById('custom_input').value;

    // Language
    let language = document.getElementById('p_language').value;
    if (language === 'c')
        language = 'C'
    else if (language === 'cpp')
        language = 'CPP'
    else if (language === 'python')
        language = 'PYTHON'

    $.ajax({
        url: 'https://flask-compiler-api.herokuapp.com/execute/v2/',
        type: 'POST',
        headers: {  'Access-Control-Allow-Origin': 'https://flask-compiler-api.herokuapp.com/execute/v2/'},
        data: {
           source: editor.getValue(),
           language: language,
           testcases: custom_input,
           timeout: 10
       },
        success: function (json){
           $('.loader').hide();
           let output = json.Output;
           // console.log(json);
           if (output.timeoutError){
               document.getElementById('compile-message').innerText = 'Message: Time Out Error, Code took more than 10s';
           }
           else {
               document.getElementById('compile-message').innerText = 'Output: ' + output.stdout;
           }
        },
        error : function(xhr,errmsg,err) {
           $('.loader').hide();
           console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
       }
    });
    compile_btn.prop('disabled', false);
    // $('.loader').hide();
}

// This will get code from the database and add it to editor
function getCode(slug){
    $.ajax(
        {
            url: 'getCode',
            type: 'POST',
            data: {
                slug: slug
            },
            success: function (json) {
                if (window.confirm('Current Code will be overwritten. Do you want to continue?')){
                    json = json[0];
                    // editor.setValue(json.code);
                    // document.getElementById('p_language').value = String(json.language);
                    setC_Code(json.code, String(json.language));
                    // $('#saved-code').hide();
                }
            },
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        }
    );
}


// Add trunc method to String Class
String.prototype.trunc =
      function(n){
          return this.substr(0,n-1)+(this.length>n?'&hellip;':'');
      };


// Delete saved code
function deleteSavedCode(slug){
    if (confirm('Are you sure, you want to delete the code ?')) {
        $.ajax({
        type: 'POST',
        url: 'deleteSavedCode',
        data: {
            unique_url: slug
        },
        success: function (json) {
            if (json.success) {
                alert('Code Deletion Successful!!!');
                window.location.assign('/');
            }
            else alert('Something went wrong or this file might be already deleted.');
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    })
    }
}


// Get all saved code for that user
function savedCode(){
    let loader = $('.loader');
    loader.show();
    // Send request if we don't have saved code data
    if ($('#saveTable tbody tr').length-1 === 0){
        $.ajax({
        type: 'POST',
        url: 'returnAllSavedCode',
        data: {},
        success: function (json){
            if (json.length === 0) {
                alert('No Saved Codes!');
            }
            else {
                if (json.length !== $('#saveTable tbody tr').length-1){
                    json.forEach(code => {
                    let slug = String(code.slug);
                    $('#saved-code').show();
                    $('#saveTable tr:last').after(`<tr><td> ${String(code.datetime).replace('T', '  ').replace('+05:30', ' ').substr(0, 20)} </td> <td> <a  href=javascript:getCode('${slug}'); >  ${code.name} </a></td> <td> ${String(code.code).trunc(30)} </td> <td> <a href="javascript:deleteSavedCode('${slug}')"> <i class="fa fa-trash-o" style="font-size: larger"></i> </a> </td> </tr>`);
                    });
                }
            }
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    }
    loader.hide();
}


// Show all shared codes
function sharedCode(){
    let loader = $('.loader');
    loader.show();
    // Send request if we don't have saved code data
    if ($('#shareTable tbody tr').length-1 === 0){
        $.ajax({
        type: 'POST',
        url: 'returnAllSharedCode',
        data: {},
        success: function (json){
            if (json.length === 0) {
                alert('No Saved Codes!');
            }
            else {
                if (json.length !== $('#shareTable tbody tr').length-1){
                    json.forEach(code => {
                    let slug = String(code.uniqueShareUrl);
                    $('#shared-code').show();
                    $('#shareTable tr:last').after(`<tr><td> ${String(code.code).trunc(50)} </td> <td> ${code.language} </td> <td> ${String(code.permission)} </td> <td> <a href="javascript:deleteSavedCode('${slug}')"> <i class="fa fa-trash-o" style="font-size: larger"></i> </a> </td> </tr>`);
                    });
                }
            }
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    }
    loader.hide();
}


// Once html share page is loaded call this function and get code
function getShareCodeHere() {
            $.ajax({
                url: 'getSingleShareCode',
                type: 'POST',
                data: {
                    uniqueShareUrl: window.location.href.slice(-8)
                },
                success: function (json) {
                    json = json[0];
                    if (json.exist === false){
                        alert("Code doesn't exist");
                    }
                    else {
                        editor.setValue(json.code);
                        if (json.permission === 'globally-editor'){
                            editor.setReadOnly(false);
                        }
                        else {
                            // setReadOnly if permission is viewer, so that user can't edit code
                            editor.setReadOnly(true);
                        }
                        document.getElementById('p_language').value = json.language;
                        if (json.language === 'python'){
                            editor.getSession().setMode("ace/mode/python");
                        }
                        else {
                            editor.getSession().setMode("ace/mode/c_cpp");
                        }
                    }
                },
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            })
        }

// If user not Logged IN
function userNotLogged() {
    alert("Please Login to use this feature!");
}

// If user refresh or close tab
// window.addEventListener('beforeunload', function(e) {
//     let p_language = document.getElementById('p_language').value;
//     let code = editor.getValue();
//     sessionStorage.setItem(p_language, code);
//     e.preventDefault();
//     e.returnValue = '';
// });