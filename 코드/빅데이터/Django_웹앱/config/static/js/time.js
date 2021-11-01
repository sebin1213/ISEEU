$(function(){
    //prev 버튼 클릭하면 뒤로 이동
    $('#cal_month').on('click',function(){
        $('#cal_month span').css('color','#7456CA');
        $('#cal_week span').css('color','#DADADA');
        $('#cal_today span').css('color','#DADADA');
        $('#cal_month img').attr('src','/static/image/calendar.png');
        $('#cal_week img').attr('src','/static/image/calendar1.png');
        $('#cal_today img').attr('src','/static/image/calendar1.png');
    });
    $('#cal_week').on('click',function(){
        $('#cal_month span').css('color','#DADADA');
        $('#cal_week span').css('color','#7456CA');
        $('#cal_today span').css('color','#DADADA');
        $('#cal_month img').attr('src','/static/image/calendar1.png');
        $('#cal_week img').attr('src','/static/image/calendar.png');
        $('#cal_today img').attr('src','/static/image/calendar1.png');
    });
    $('#cal_today').on('click',function(){
        $('#cal_month span').css('color','#DADADA');
        $('#cal_week span').css('color','#DADADA');
        $('#cal_today span').css('color','#7456CA');
        $('#cal_month img').attr('src','/static/image/calendar1.png');
        $('#cal_week img').attr('src','/static/image/calendar1.png');
        $('#cal_today img').attr('src','/static/image/calendar.png');
    });
})


