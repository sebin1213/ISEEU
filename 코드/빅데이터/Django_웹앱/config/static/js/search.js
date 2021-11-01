$(function(){
   $(".modal_rename_text").addClass('blur');

    $(".modal_rename_text").focus(function(){
        $('.modal_rename_text').css({
        'box-shadow':'0px 3px 8px 0px rgb(0 0 0 / 40%)',
        'transition':'all ease 400ms',
        'background-color':'white',
        'border':'1px solid #dedede',
        });
        $(this).attr('placeholder','');
        $(this).addClass('focus');
        $(this).removeClass('blur');

    });
    $(".modal_rename_text").blur(function(){
        $('.modal_rename_text').css({
        'box-shadow':'0 0px 5px 0 rgb(0 0 0 / 10%)',
        'transition':'all ease 400ms',
        'background-color':'rgb(180 180 180 / 12%)',
        'border':'0px'
        });
        $(this).attr('placeholder','이름을 입력하세요');
        $(this).addClass('blur');
        $(this).removeClass('focus');
    });


});