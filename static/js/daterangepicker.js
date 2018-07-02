function myFunction() {
    var x = document.getElementById("mySelect").value;
    if (x==="CustomRange"){
    var start = moment().subtract(1, 'days');
    var end = moment().subtract(1, 'days');
    $(function() {
    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }
    $('#reportrange').daterangepicker({
        "minDate": "1/1/2016",
        maxDate:moment().subtract(1, 'days'),
        startDate: start,
        endDate: end,
        "opens": "left",
        "alwaysShowCalendars": true,
    }, cb);
    cb(start, end);
    });
    $(".demo").html('<input name="dates" id="reportrange" readonly/>');
    }
    if (x==="7"){
    $(function() {
    var start = moment().subtract(1, 'days').subtract(6,'days');
    var end = moment().subtract(1, 'days');
    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }
    $('#reportrange').daterangepicker({
        "minDate": "1/1/2016",
        maxDate:moment().subtract(1, 'days'),
        startDate: start,
        endDate: end,
        "opens": "left",
        "alwaysShowCalendars": true,
    }, cb);
    cb(start, end);
    });
    $(".demo").html('<input name="dates" id="reportrange" readonly/>');
    }
    if (x==="30"){
    $(function() {
    var start = moment().subtract(29, 'days').subtract(1, 'days');
    var end = moment().subtract(1, 'days');
    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }
    $('#reportrange').daterangepicker({
        "minDate": "1/1/2016",
        maxDate:moment().subtract(1, 'days'),
        startDate: start,
        endDate: end,
        "opens": "left",
        "alwaysShowCalendars": true,
    }, cb);
    cb(start, end);
    });
    $(".demo").html('<input name="dates" id="reportrange" readonly/>');
    }
    if (x==="LastMonth"){
        $(function() {
        var start = moment().subtract(1, 'month').startOf('month');
        var end = moment().subtract(1, 'month').endOf('month');
        function cb(start, end) {
            $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        }
        $('#reportrange').daterangepicker({
            "minDate": "1/1/2016",
            maxDate:moment().subtract(1, 'days'),
            startDate: start,
            endDate: end,
            "opens": "left",
            "alwaysShowCalendars": true,
        }, cb);
        cb(start, end);
        });
    $(".demo").html('<input name="dates" id="reportrange" readonly/>');
    }
    if (x==="12"){
        $(function() {
        var start = moment().subtract(1,'month').endOf('months').startOf('months').subtract(1,'years');
        var end = moment().subtract(1,'month').endOf('months');
        function cb(start, end) {
            $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        }
        $('#reportrange').daterangepicker({
            "minDate": "1/1/2016",
            maxDate:moment().subtract(1, 'days'),
            startDate: start,
            endDate: end,
            "opens": "left",
            "alwaysShowCalendars": true,
        }, cb);
        cb(start, end);
        });
    $(".demo").html('<input name="dates" id="reportrange" readonly/>');
    }
    if (x==="LastYear"){
        $(function() {
        var start = moment().startOf('years').subtract(1, 'days').startOf('years');
        var end = moment().startOf('years').subtract(1, 'days');
        function cb(start, end) {
            $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        }
        $('#reportrange').daterangepicker({
            "minDate": "1/1/2016",
            maxDate:moment().subtract(1, 'days'),
            startDate: start,
            endDate: end,
            "opens": "left",
            "alwaysShowCalendars": true,
        }, cb);
        cb(start, end);
        });
    $(".demo").html('<input name="dates" id="reportrange" readonly/>');
    }
    if (x==="LastMonthPrevYear"){
        $(function() {
        var start = moment().subtract(1, 'month').startOf('month').subtract(1, 'years');
        var end = moment().subtract(1, 'month').endOf('month').subtract(1, 'years');
        function cb(start, end) {
            $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        }
        $('#reportrange').daterangepicker({
            "minDate": "1/1/2016",
            maxDate:moment().subtract(1, 'days'),
            startDate: start,
            endDate: end,
            "opens": "left",
            "alwaysShowCalendars": true,
        }, cb);
        cb(start, end);
        });
    $(".demo").html('<input name="dates" id="reportrange" readonly/>');
    }
};

