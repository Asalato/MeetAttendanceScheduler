window.onload = function(){
    document.getElementById('use_date').checked = true;
    document.getElementById('logout_or').setAttribute('disabled', true);
    document.getElementById('logout_and').setAttribute('disabled', true);

    document.getElementById('stop_button').setAttribute("disabled", true);
    document.getElementById('mute_checkbox').setAttribute("disabled", true);
    document.getElementById('mute_checkbox').checked = true;
    let dt = new Date();
    let y = dt.getFullYear();
    let M = ("00" + (dt.getMonth() + 1)).slice(-2);
    let d = ("00" + (dt.getDate())).slice(-2);
    let h = ("00" + (dt.getHours())).slice(-2);
    let m = ("00" + (dt.getMinutes())).slice(-2);
    document.getElementById('login_date').value = y + "-" + M + "-" + d;
    document.getElementById('login_time').value = h + ":" + m;
    document.getElementById('logout_date').value = y + "-" + M + "-" + d;
    document.getElementById('logout_time').value = h + ":" + m;
    load_file("./identifier.txt")
};

window.addEventListener('beforeunload', (event) => {
    stop_system();
});

function switch_mute_disabled(ele){
    if(ele.checked)
        document.getElementById('mute_checkbox').removeAttribute("disabled");
    else
        document.getElementById('mute_checkbox').setAttribute("disabled", true);
}

function save_file(){
    const login_id = document.getElementById('login_id').value;
    const login_pw = document.getElementById('login_pw').value;
    const meet_room = document.getElementById('meet_room').value;
    eel.save_data([login_id, login_pw, meet_room, login_time, logout_time]);
}

async function load_file(path = ""){
    let data = await eel.load_data(path)();
    data = data.split(",");
    if(data.length !== 3) {
        show_log_error('Invalid file format.');
        return;
    }
    show_log('Identifier load Success.');
    document.getElementById('login_id').value = data[0];
    document.getElementById('login_pw').value = data[1];
    document.getElementById('meet_room').value = data[2];
}

async function start_system() {
    const login_id = document.getElementById('login_id').value;
    const login_pw = document.getElementById('login_pw').value;
    const meet_room = document.getElementById('meet_room').value;
    const login_date = document.getElementById('login_date').value;
    const login_time = document.getElementById('login_time').value;
    const logout_date = document.getElementById('logout_date').value;
    const logout_time = document.getElementById('logout_time').value;
    const open_window = document.getElementById('open_checkbox').checked;
    const mute_window = document.getElementById('mute_checkbox').checked;
    const use_date = document.getElementById('use_date').checked;
    const use_number = document.getElementById('use_number').checked;
    const logout_rate = document.getElementById('logout_rate').value;
    const type_or = is_or || !(use_date && use_number);
    let status = await eel.set_value([login_id, login_pw, meet_room, login_date, login_time, logout_date, logout_time, open_window, mute_window, use_date, use_number, logout_rate, type_or])();
    if(status){
        eel.start_system();
        document.getElementById('submit_button').setAttribute("disabled", true);
        document.getElementById('save_identifier').setAttribute("disabled", true);
        document.getElementById('load_identifier').setAttribute("disabled", true);
        document.getElementById('stop_button').removeAttribute("disabled");
    }
}

let is_or = true;
function use_number() {
    if(document.getElementById('use_number').checked && document.getElementById('use_date').checked){
        if(!is_or){
            document.getElementById('logout_or').removeAttribute('disabled');
            document.getElementById('logout_and').setAttribute('disabled', true);
        }else{
            document.getElementById('logout_or').setAttribute('disabled', true);
            document.getElementById('logout_and').removeAttribute('disabled');
        }
    }else{
        document.getElementById('logout_or').setAttribute('disabled', true);
        document.getElementById('logout_and').setAttribute('disabled', true);
    }
}

function toggle_or(){
    if(is_or){
        document.getElementById('logout_or').removeAttribute('disabled');
        document.getElementById('logout_and').setAttribute('disabled', true);
    }
    else{
        document.getElementById('logout_or').setAttribute('disabled', true);
        document.getElementById('logout_and').removeAttribute('disabled');
    }
    is_or = !is_or;
}

function stop_system(){
    show_log('Cancel requested.');
    document.getElementById('stop_button').setAttribute("disabled", true);
    eel.reset_system();
}

eel.expose(show_log)
function show_log(message){
    document.getElementById("log").innerHTML = message;
}

eel.expose(show_log_error)
function show_log_error(message){
    document.getElementById("log").innerHTML = '<span style="color: red; ">' + message + "</span>";
}

eel.expose(on_complete)
function on_complete(){
    document.getElementById('submit_button').removeAttribute("disabled");
    document.getElementById('save_identifier').removeAttribute("disabled");
    document.getElementById('load_identifier').removeAttribute("disabled");
    document.getElementById('stop_button').setAttribute("disabled", true);
}