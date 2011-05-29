// jscalendar glue -- Leonard Norrgård <vinsci@*>
// This function gets called when the user clicks on some date.
function onJsCalendarInGridDateUpdate(cal) {
    // cal.params.inputField.value = cal.date.print('%Y/%m/%d %H:%M'); // doesn't work in Opera, don't use time now
    //cal.params.inputField.value = cal.date.print('%Y/%m/%d'); // doesn't work in Opera
    var daystr = '' + cal.date.getDate();
    if (daystr.length == 1)
        daystr = '0' + daystr;
    var monthstr = '' + (cal.date.getMonth()+1);
    if (monthstr.length == 1)
    monthstr = '0' + monthstr;
    valStr = '' + cal.date.getFullYear() + '/' + monthstr + '/' + daystr;
    cal.params.inputField.value = valStr;
    fireEvent(cal.params.inputField, 'change');
}

function fireEvent(element,event){
    if (document.createEventObject){
        // dispatch for IE
        var evt = document.createEventObject();
        return element.fireEvent('on'+event,evt)
    }
    else{
        // dispatch for firefox + others
        var evt = document.createEvent("HTMLEvents");
        evt.initEvent(event, true, true ); // event type,bubbling,cancelable
        return !element.dispatchEvent(evt);
    }
}

function showJsCalendarInGrid(input_id, yearStart, yearEnd) {
    // do what jscalendar-x.y.z/calendar-setup.js:Calendar.setup would do
    var el = input_id + "_selectDateButton";
    var input_id = document.getElementById(input_id);
    var input_id_anchor = input_id;
    var format = 'y/mm/dd';

    var dateEl = input_id;
    var mustCreate = false;
    var cal = window.calendar;

    var params = {
        'range' : [yearStart, yearEnd],
        inputField : input_id,
    };

    function param_default(pname, def) { if (typeof params[pname] == "undefined") { params[pname] = def; } };

    param_default("inputField",     null);
    param_default("displayArea",    null);
    param_default("button",         null);
    param_default("eventName",      "click");
    param_default("ifFormat",       "%Y/%m/%d");
    param_default("daFormat",       "%Y/%m/%d");
    param_default("singleClick",    true);
    param_default("disableFunc",    null);
    param_default("dateStatusFunc", params["disableFunc"]); // takes precedence if both are defined
    param_default("dateText",       null);
    param_default("firstDay",       1);
    param_default("align",          "Bl");
    param_default("range",          [1900, 2999]);
    param_default("weekNumbers",    true);
    param_default("flat",           null);
    param_default("flatCallback",   null);
    param_default("onSelect",       null);
    param_default("onClose",        null);
    param_default("onUpdate",       null);
    param_default("date",           null);
    param_default("showsTime",      false);
    param_default("timeFormat",     "24");
    param_default("electric",       true);
    param_default("step",           2);
    param_default("position",       null);
    param_default("cache",          false);
    param_default("showOthers",     false);
    param_default("multiple",       null);

    if (!(cal && params.cache)) {
    window.calendar = cal = new Calendar(params.firstDay,
        null,
        onJsCalendarInGridDateUpdate,
        function(cal) { cal.hide(); });
        cal.time24 = true;
        cal.weekNumbers = true;
        mustCreate = true;
    } else {
        cal.hide();
    }
    cal.showsOtherMonths = false;
    cal.yearStep = 2;
    //cal.setRange(yearStart,yearEnd);
    cal.params = params;
    cal.setDateStatusHandler(null);
    cal.getDateText = null;
    cal.setDateFormat(format);
    if (mustCreate)
    cal.create();
    cal.refresh();
    if (!params.position)
        cal.showAtElement(input_id_anchor, null);
    else
        cal.showAt(params.position[0], params.position[1]);
    return false;
}


// This function updates a hidden date field with the current values of the widgets
function update_date_field(field, year, month, day, hour, minute, ampm)
{
    var field  = document.getElementById(field)
    var date   = document.getElementById(date)
    var year   = document.getElementById(year)
    var month  = document.getElementById(month)
    var day    = document.getElementById(day)
    var hour   = document.getElementById(hour)
    var minute = document.getElementById(minute)
    var ampm   = document.getElementById(ampm)

    if (0 < year.value)
    {
        // Return ISO date string
        // Note: This relies heavily on what date_components_support.py puts into the form.
        field.value = year.value + "-" + month.value + "-" + day.value + " " + hour.value + ":" + minute.value
        // Handle optional AM/PM
        if (ampm && ampm.value)
            field.value = field.value + " " + ampm.value
    } 
    else 
    {
        // Return empty string
        field.value = ''
        // Reset widgets
        month.options[0].selected = 1
        day.options[0].selected = 1
        hour.options[0].selected = 1
        minute.options[0].selected = 1
        if (ampm && ampm.options)
            ampm.options[0].selected = 1
    }
}


