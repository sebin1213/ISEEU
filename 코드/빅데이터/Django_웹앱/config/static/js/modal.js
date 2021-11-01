$(function(){
    $('.unknown_post').each(function(index){
        $('.unknown_post_area').on('click', function () {
                var index = $(this).index(".unknown_post_area");
                $(".modal").eq(index).show();
        }),
        $('.cls_button').on('click', function () {
                var index = $(this).index(".cls_button");
                $('.modal').eq(index).hide();
        });
    });
})

$(function(){
    $('.modal').each(function(index){
        $('.modal_btn').on('click', function () {
                $(".modal_sub").show();
        }),
        $('.cls_button_sub').on('click', function () {
                $('.modal_sub').hide();
        });
    });
})

$(function(){
    $('.unknown_post_area').on('click', function () {
        var index = $(this).index(".unknown_post_area");
        $('.modal_graph>div:nth-child(1)').eq(index).attr('id','container'+index);

    });
})
$(function(){
    $('.unknown_post_area').on('click', function () {
        var index = $(this).index(".unknown_post_area");
        $('.modal_graph>div:nth-child(2)').eq(index).attr('id','time_container'+index);
        var time_con_id = $('.modal_graph > div:nth-child(2)').eq(index).attr('id');
    });
})